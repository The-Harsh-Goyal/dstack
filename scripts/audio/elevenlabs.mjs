// dstack ElevenLabs client: the ONLY outside audio service dstack talks to (approved by Harsh, US host).
// Off by default. Used only when DSTACK_TTS_PROVIDER=elevenlabs (narration) or
// DSTACK_AUDIO_PROVIDER=elevenlabs (scripts/gen-audio.mjs: SFX + background music).
//
// Host: https://api.elevenlabs.io only (ElevenLabs' global default production server). The host
// is a constant on purpose: no env var can point dstack at another server, residency host or proxy API.
//
// Key: ELEVENLABS_API_KEY from the environment, or the first line of the file named by
// DSTACK_ELEVENLABS_KEY_FILE (must live outside the dstack folder; the bare key on line 1, or a dotenv
// line `ELEVENLABS_API_KEY=...`, see keyfile.mjs). The key is sent only in the
// xi-api-key header and is never written, logged or echoed; every message passes through mask().
//
// Endpoints (https://elevenlabs.io/docs/api-reference):
//   POST /v1/text-to-speech/{voice_id}/with-timestamps  -> { audio_base64, alignment }
//   POST /v1/sound-generation                           -> audio bytes
//   POST /v1/music                                      -> audio bytes (Music API: paid plans only)
//
// Cache: every successful generation is stored under $DSTACK_HOME/cache/elevenlabs/<sha256>.mp3
// (+ .json with the request parameters, never the key), so the same request is never paid for twice.

import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseKeyFile, readKeyFile } from './keyfile.mjs';

export { parseKeyFile };

export const HOST = 'api.elevenlabs.io';
export const BASE_URL = `https://${HOST}`;
export const DEFAULT_VOICE = 'JBFqnCBsd6RMkjVDRZzb';        // "George", an ElevenLabs default voice
export const DEFAULT_MODEL = 'eleven_multilingual_v2';       // the endpoint's own default; stable on long-form
export const DEFAULT_SFX_MODEL = 'eleven_text_to_sound_v2';
export const DEFAULT_MUSIC_MODEL = 'music_v1';               // the Music API's current default
export const OUTPUT_FORMAT = 'mp3_44100_128';                // available on every plan
const PACK_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

let warned = new Set();
export function warnOnce(id, msg) {
  if (warned.has(id)) return;
  warned.add(id);
  console.error(mask(msg));
}
export function _resetWarnings() { warned = new Set(); }

// ---------- key ----------
function keyFromFile(file) {
  const abs = path.resolve(file.replace(/^~(?=\/|$)/, os.homedir()));
  const rel = path.relative(PACK_ROOT, abs);
  if (!rel.startsWith('..') && !path.isAbsolute(rel)) {
    warnOnce('keyfile-in-repo', `[elevenlabs] DSTACK_ELEVENLABS_KEY_FILE points inside the dstack folder (${abs}); ignored. Keep the key file outside the repo.`);
    return null;
  }
  try {
    return readKeyFile(abs, 'ELEVENLABS_API_KEY');
  } catch {
    warnOnce('keyfile-unreadable', `[elevenlabs] DSTACK_ELEVENLABS_KEY_FILE is set but ${abs} can't be read.`);
    return null;
  }
}

/** Returns { key, source } where source is 'env' | 'file' | null. Never print `key`. */
export function loadKey(env = process.env) {
  const k = (env.ELEVENLABS_API_KEY || '').trim();
  if (k) return { key: k, source: 'env' };
  if (env.DSTACK_ELEVENLABS_KEY_FILE) {
    const f = keyFromFile(env.DSTACK_ELEVENLABS_KEY_FILE);
    if (f) return { key: f, source: 'file' };
  }
  return { key: null, source: null };
}

export function hasKey(env = process.env) { return !!loadKey(env).key; }

/** Replace any occurrence of the key (and anything that looks like an xi-api-key value) with ****. */
export function mask(text, env = process.env) {
  let s = String(text);
  const candidates = [(env.ELEVENLABS_API_KEY || '').trim()];
  if (env.DSTACK_ELEVENLABS_KEY_FILE) {
    try { candidates.push(readKeyFile(env.DSTACK_ELEVENLABS_KEY_FILE, 'ELEVENLABS_API_KEY') || ''); } catch { /* none */ }
  }
  for (const k of candidates) if (k && k.length >= 4) s = s.split(k).join('****');
  return s.replace(/(xi-api-key["']?\s*[:=]\s*["']?)[^\s"',}]+/gi, '$1****').replace(/\bsk_[A-Za-z0-9]{8,}\b/g, 'sk_****');
}

// ---------- cache ----------
export function cacheDir(env = process.env) {
  const home = env.DSTACK_HOME || env.HUASHU_DESIGN_HOME || path.join(os.homedir(), '.dstack');
  return path.join(home, 'cache', 'elevenlabs');
}

export function cacheKey(kind, params) {
  const canon = JSON.stringify([kind, Object.keys(params).sort().map((k) => [k, params[k]])]);
  return crypto.createHash('sha256').update(canon).digest('hex').slice(0, 32);
}

export function cacheGet(kind, params, env = process.env) {
  const base = path.join(cacheDir(env), cacheKey(kind, params));
  if (!fs.existsSync(base + '.mp3')) return null;
  let meta = {};
  try { meta = JSON.parse(fs.readFileSync(base + '.json', 'utf8')); } catch { /* audio only */ }
  return { file: base + '.mp3', meta };
}

export function cachePut(kind, params, audio, extra = {}, env = process.env) {
  const dir = cacheDir(env);
  fs.mkdirSync(dir, { recursive: true });
  const base = path.join(dir, cacheKey(kind, params));
  fs.writeFileSync(base + '.mp3', audio);
  fs.writeFileSync(base + '.json', JSON.stringify({ kind, params, ...extra, created: new Date().toISOString() }, null, 2));
  return base + '.mp3';
}

// ---------- HTTP ----------
export class ElevenLabsError extends Error {
  constructor(message, status) { super(mask(message)); this.status = status; }
}

function explain(status, kind, detail) {
  if (status === 401) return 'the API key was rejected (401). Check ELEVENLABS_API_KEY.';
  if (status === 402 || (status === 403 && kind === 'music')) {
    return kind === 'music' ? `the Music API needs a paid ElevenLabs plan (${status}).` : `the plan has no credits or doesn't allow this (${status}).`;
  }
  if (status === 429) return 'rate limit or concurrency limit reached (429); try again later.';
  return `HTTP ${status}${detail ? `: ${detail}` : ''}`;
}

/**
 * POST to an ElevenLabs endpoint on the fixed host. Returns { json } or { audio: Buffer }.
 * `fetchImpl` defaults to globalThis.fetch (tests swap it for a mock; nothing else should).
 */
export async function post(endpoint, body, { query = {}, kind = 'tts', expect = 'audio', env = process.env, fetchImpl } = {}) {
  const { key } = loadKey(env);
  if (!key) throw new ElevenLabsError('no ElevenLabs API key (set ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE)', 0);
  if (!endpoint.startsWith('/v1/')) throw new ElevenLabsError(`refusing endpoint ${endpoint}`, 0);
  const url = new URL(endpoint, BASE_URL);
  for (const [k, v] of Object.entries(query)) if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
  if (url.host !== HOST || url.protocol !== 'https:') throw new ElevenLabsError(`refusing host ${url.host}`, 0);
  const f = fetchImpl || globalThis.fetch;
  let res;
  try {
    res = await f(url.toString(), {
      method: 'POST',
      headers: { 'xi-api-key': key, 'Content-Type': 'application/json', Accept: expect === 'json' ? 'application/json' : 'audio/mpeg' },
      body: JSON.stringify(body),
    });
  } catch (e) {
    throw new ElevenLabsError(`network error reaching ${HOST}: ${e && e.message ? e.message : e}`, 0);
  }
  if (!res.ok) {
    let detail = '';
    try { const t = await res.text(); const j = JSON.parse(t); detail = (j.detail && (j.detail.message || j.detail.status || JSON.stringify(j.detail))) || t; } catch { /* no body */ }
    throw new ElevenLabsError(`ElevenLabs ${kind}: ${explain(res.status, kind, String(detail).slice(0, 200))}`, res.status);
  }
  if (expect === 'json') return { json: await res.json() };
  return { audio: Buffer.from(await res.arrayBuffer()) };
}

// ---------- endpoints ----------
export function ttsParams(text, opts = {}, env = process.env) {
  const speed = Math.min(1.2, Math.max(0.7, Number(opts.speed) || 1));
  return {
    // a script's `voice:` is used only if it looks like an ElevenLabs voice id (e.g. not espeak's 'en-us')
    voice_id: (opts.voice && /^[A-Za-z0-9]{20}$/.test(opts.voice) ? opts.voice : null) || env.DSTACK_ELEVENLABS_VOICE || DEFAULT_VOICE,
    model_id: env.DSTACK_ELEVENLABS_MODEL || DEFAULT_MODEL,
    text,
    speed,
    output_format: OUTPUT_FORMAT,
  };
}

/** Text -> { audio: Buffer, alignment, cached }. Uses the with-timestamps endpoint for measured word timings. */
export async function tts(text, opts = {}, { env = process.env, fetchImpl } = {}) {
  const p = ttsParams(text, opts, env);
  const hit = cacheGet('tts', p, env);
  if (hit) return { audio: fs.readFileSync(hit.file), alignment: hit.meta.alignment || null, cached: true };
  const { json } = await post(`/v1/text-to-speech/${encodeURIComponent(p.voice_id)}/with-timestamps`,
    { text: p.text, model_id: p.model_id, voice_settings: { speed: p.speed } },
    { query: { output_format: p.output_format }, kind: 'tts', expect: 'json', env, fetchImpl });
  if (!json || !json.audio_base64) throw new ElevenLabsError('ElevenLabs tts: response had no audio', 200);
  const audio = Buffer.from(json.audio_base64, 'base64');
  const alignment = json.alignment || null;
  cachePut('tts', p, audio, { alignment }, env);
  return { audio, alignment, cached: false };
}

export function sfxParams({ prompt, seconds, loop, influence } = {}, env = process.env) {
  return {
    text: prompt,
    duration_seconds: seconds ? Math.min(30, Math.max(0.5, Number(seconds))) : null,
    loop: !!loop,
    prompt_influence: influence !== undefined ? Number(influence) : 0.3,
    model_id: env.DSTACK_ELEVENLABS_SFX_MODEL || DEFAULT_SFX_MODEL,
    output_format: OUTPUT_FORMAT,
  };
}

export async function soundEffect(opts, { env = process.env, fetchImpl } = {}) {
  const p = sfxParams(opts, env);
  const hit = cacheGet('sfx', p, env);
  if (hit) return { file: hit.file, cached: true };
  const body = { text: p.text, loop: p.loop, prompt_influence: p.prompt_influence, model_id: p.model_id };
  if (p.duration_seconds) body.duration_seconds = p.duration_seconds;
  const { audio } = await post('/v1/sound-generation', body, { query: { output_format: p.output_format }, kind: 'sfx', env, fetchImpl });
  return { file: cachePut('sfx', p, audio, {}, env), cached: false };
}

export function musicParams({ prompt, seconds } = {}, env = process.env) {
  return {
    prompt,
    music_length_ms: Math.round(Math.min(600, Math.max(3, Number(seconds) || 60)) * 1000),
    force_instrumental: true,
    model_id: env.DSTACK_ELEVENLABS_MUSIC_MODEL || DEFAULT_MUSIC_MODEL,
    output_format: OUTPUT_FORMAT,
  };
}

export async function music(opts, { env = process.env, fetchImpl } = {}) {
  const p = musicParams(opts, env);
  const hit = cacheGet('music', p, env);
  if (hit) return { file: hit.file, cached: true };
  const { audio } = await post('/v1/music',
    { prompt: p.prompt, music_length_ms: p.music_length_ms, force_instrumental: p.force_instrumental, model_id: p.model_id },
    { query: { output_format: p.output_format }, kind: 'music', env, fetchImpl });
  return { file: cachePut('music', p, audio, {}, env), cached: false };
}

/** ElevenLabs character alignment -> [{ text, start, end }] words (split on whitespace). */
export function alignmentToWords(al) {
  if (!al || !Array.isArray(al.characters)) return null;
  const words = [];
  let cur = null;
  al.characters.forEach((ch, i) => {
    const s = al.character_start_times_seconds[i];
    const e = al.character_end_times_seconds[i];
    if (/\s/.test(ch)) { if (cur) { words.push(cur); cur = null; } return; }
    if (!cur) cur = { text: ch, start: s, end: e };
    else { cur.text += ch; cur.end = e; }
  });
  if (cur) words.push(cur);
  return words.map((w) => ({ text: w.text, start: +w.start.toFixed(3), end: +w.end.toFixed(3) }));
}
