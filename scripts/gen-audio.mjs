#!/usr/bin/env node
/**
 * gen-audio.mjs · fill the audio library slots (background music + SFX) that dstack no longer ships.
 *
 * Provider (DSTACK_AUDIO_PROVIDER):
 *   none        (default) generate nothing; tells you where to put your own licensed file
 *   elevenlabs  ElevenLabs Sound Effects (/v1/sound-generation) and Music (/v1/music, paid plans only)
 *               over https://api.elevenlabs.io, key from ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE.
 *               No key: one warning, then behaves like `none` (exit 0).
 *               bgm only: no key, a free plan (the Music API is paid-only) or any error falls back to
 *               the local library below when it has a track for the mood; otherwise nothing is written.
 *   local       background music from your local library (scripts/audio/music-library.mjs):
 *               $DSTACK_MUSIC_DIR (default ~/.dstack/music) + manifest.json. Free, fully offline.
 *               Picks a track by mood tag, deterministically (--seed S for a different pick); prints
 *               the attribution the licence needs. No SFX from the local library.
 *
 * Usage:
 *   node scripts/gen-audio.mjs bgm <mood> [--prompt "..."] [--seconds 60] [--seed S] [--force]
 *        -> $DSTACK_AUDIO_DIR/bgm-<mood>.mp3          (default ~/.dstack/audio)
 *   node scripts/gen-audio.mjs sfx <category>/<name> [--prompt "..."] [--seconds 0.5] [--loop] [--force]
 *        -> $DSTACK_SFX_DIR/<category>/<name>.mp3     (default ~/.dstack/audio/sfx)
 *        Without --prompt, the prompt and length come from the table in references/sfx-library.md.
 *   node scripts/gen-audio.mjs status
 *
 * Existing files are never overwritten without --force (they may be your own licensed audio).
 * Every generation is cached in $DSTACK_HOME/cache/elevenlabs/, so the same request is free the second time.
 * A <file>.provenance.json is written next to each generated file (provider, model, prompt, date; never the key).
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as el from './audio/elevenlabs.mjs';
import * as lib from './audio/music-library.mjs';
import { execFileSync } from 'node:child_process';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

// Built-in prompts matching the mood table in references/video-export.md (add-music.sh --mood=).
export const BGM_PROMPTS = {
  tech: 'minimal modern synth pads and soft piano, clean keynote product-launch feel, steady pulse, instrumental',
  ad: 'upbeat modern electronic track with a build and a drop, confident and promotional, instrumental',
  educational: 'warm and bright light guitar and electric piano, inviting and curious, instrumental',
  tutorial: 'lo-fi ambient bed, soft and barely noticeable, steady and calm, instrumental',
};

export function dirs(env = process.env) {
  const home = env.DSTACK_HOME || env.HUASHU_DESIGN_HOME || path.join(os.homedir(), '.dstack');
  const audio = env.DSTACK_AUDIO_DIR || path.join(home, 'audio');
  return { audio, sfx: env.DSTACK_SFX_DIR || path.join(audio, 'sfx') };
}

export function libraryEntry(slot) {
  // rows like: | `sfx/ui/click.mp3` | 0.5s | Standard UI click | crisp modern interface click |
  const md = fs.readFileSync(path.join(ROOT, 'references', 'sfx-library.md'), 'utf8');
  for (const line of md.split('\n')) {
    const m = line.match(/^\|\s*`sfx\/([\w-]+\/[\w-]+)\.mp3`\s*\|\s*([\d.]+)s\s*\|[^|]*\|\s*([^|]+?)\s*\|/);
    if (m && m[1] === slot) return { seconds: parseFloat(m[2]), prompt: m[3] };
  }
  return null;
}

/**
 * Copy a library track for req.mood to `target` (+ provenance with licence and attribution).
 * Returns a result, or null when the library has nothing usable (the caller then stays silent).
 */
function fromLibrary(req, target, log, env, fallbackFrom = null) {
  const r = lib.pick(req.mood, { seed: req.seed, env });
  if (!r.track) { log(`local music: ${r.reason}.${fallbackFrom ? ' No music (silent).' : ''}`); return null; }
  const t = r.track;
  fs.mkdirSync(path.dirname(target), { recursive: true });
  if (/\.mp3$/i.test(t.file)) fs.copyFileSync(t.abs, target);
  else execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', t.abs, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', target], { stdio: ['ignore', 'pipe', 'pipe'] });
  const { abs, ...entry } = t;
  fs.writeFileSync(target + '.provenance.json', JSON.stringify({
    provider: 'local', library: lib.musicDir(env), mood: req.mood, seed: req.seed || '', ...entry,
    credit: r.credit, fallback_from: fallbackFrom || undefined, copied: new Date().toISOString(),
  }, null, 2));
  log(`✓ ${target} ← local library ${t.file}${fallbackFrom ? ` (fallback: ${fallbackFrom})` : ''}`);
  if (r.noncommercial) log('WARNING: this track is licensed for NON-COMMERCIAL use only (allowed by DSTACK_MUSIC_ALLOW_NONCOMMERCIAL=1).');
  log(r.credit);
  return { status: 'local', target, track: t.file, credit: r.credit, fallback: fallbackFrom || undefined };
}

function parse(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === '--force') a.force = true;
    else if (t === '--loop') a.loop = true;
    else if (t.startsWith('--')) { const [k, v] = t.slice(2).split('='); a[k] = v !== undefined ? v : argv[++i]; }
    else a._.push(t);
  }
  return a;
}

export function provider(env = process.env) { return (env.DSTACK_AUDIO_PROVIDER || 'none').toLowerCase(); }

/** Returns { status: 'kept'|'skipped'|'generated'|'cached'|'local'|'error', target, message } and never throws. */
export async function run(argv, { env = process.env, fetchImpl, log = (m) => console.error(el.mask(m, env)) } = {}) {
  const a = parse(argv);
  const [kind, slot] = a._;
  const d = dirs(env);
  if (kind === 'status') {
    const k = el.loadKey(env);
    const L = lib.loadLibrary(env);
    log(`audio provider: ${provider(env)} · ElevenLabs key: ${k.key ? `present (${k.source})` : 'absent'} · bgm dir: ${d.audio} · sfx dir: ${d.sfx} · cache: ${el.cacheDir(env)} · local music: ${L.exists ? `${L.tracks.length} track(s), ${L.errors.length} error(s)` : 'none'} (${L.dir})`);
    return { status: 'status' };
  }
  let target, req;
  if (kind === 'bgm' && slot && /^[\w-]+$/.test(slot)) {
    target = path.join(d.audio, `bgm-${slot}.mp3`);
    const prompt = a.prompt || BGM_PROMPTS[slot.replace(/-alt$/, '')];
    if (!prompt && provider(env) !== 'local') return { status: 'error', message: `no built-in prompt for mood "${slot}"; pass --prompt "..."` };
    req = { kind: 'music', mood: slot.replace(/-alt$/, ''), prompt, seconds: a.seconds ? Number(a.seconds) : 60, seed: a.seed || '' };
  } else if (kind === 'sfx' && slot && /^[\w-]+\/[\w-]+$/.test(slot)) {
    target = path.join(d.sfx, `${slot}.mp3`);
    const entry = libraryEntry(slot);
    const prompt = a.prompt || (entry && entry.prompt);
    if (!prompt) return { status: 'error', message: `"${slot}" isn't in references/sfx-library.md; pass --prompt "..."` };
    req = { kind: 'sfx', prompt, seconds: a.seconds ? Number(a.seconds) : entry && entry.seconds, loop: !!a.loop };
  } else {
    return { status: 'error', message: 'usage: gen-audio.mjs bgm <mood> | sfx <category>/<name> | status  [--prompt ..] [--seconds N] [--seed S] [--loop] [--force]' };
  }

  if (fs.existsSync(target) && !a.force) {
    log(`✓ ${target} already exists; kept (use --force to replace it).`);
    return { status: 'kept', target };
  }
  const prov = provider(env);
  const supply = `Put your own licensed file at ${target}.`;
  if (prov === 'none') {
    log(`DSTACK_AUDIO_PROVIDER=none: dstack generates no audio. ${supply}`);
    return { status: 'skipped', target };
  }
  if (prov === 'local') {
    if (req.kind !== 'music') { log(`DSTACK_AUDIO_PROVIDER=local: the local library holds music only, no SFX. ${supply}`); return { status: 'skipped', target }; }
    const r = fromLibrary(req, target, log, env);
    if (r) return r;
    return { status: 'skipped', target };
  }
  if (prov !== 'elevenlabs') return { status: 'error', target, message: `unknown DSTACK_AUDIO_PROVIDER "${prov}" (none | local | elevenlabs)` };
  if (!el.hasKey(env)) {
    log(`WARNING: DSTACK_AUDIO_PROVIDER=elevenlabs but no ElevenLabs key (ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE); generating nothing. ${supply}`);
    if (req.kind === 'music') { const r = fromLibrary(req, target, log, env, 'no ElevenLabs key'); if (r) return r; }
    return { status: 'skipped', target };
  }
  try {
    const r = req.kind === 'music' ? await el.music(req, { env, fetchImpl }) : await el.soundEffect(req, { env, fetchImpl });
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.copyFileSync(r.file, target);
    const params = req.kind === 'music' ? el.musicParams(req, env) : el.sfxParams(req, env);
    fs.writeFileSync(target + '.provenance.json', JSON.stringify({
      provider: 'elevenlabs', endpoint: req.kind === 'music' ? '/v1/music' : '/v1/sound-generation', ...params,
      generated: new Date().toISOString(), cached: r.cached,
      licence: 'ElevenLabs output: commercial use only if generated on a paid plan; free plan = non-commercial and needs attribution. See references/audio-design-rules.md.',
    }, null, 2));
    log(`✓ ${target} (${r.cached ? 'cache hit, no credits used' : 'generated by ElevenLabs'})`);
    return { status: r.cached ? 'cached' : 'generated', target };
  } catch (e) {
    const msg = el.mask(e && e.message ? e.message : String(e), env);
    log(`WARNING: ${msg.replace(/\.$/, '')}. Nothing written by ElevenLabs. ${supply}`);
    if (req.kind === 'music') { const r = fromLibrary(req, target, log, env, msg); if (r) return r; }
    return { status: 'error', target, message: msg };
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  run(process.argv.slice(2)).then((r) => {
    if (r.status === 'error' && r.message) console.error(el.mask(r.message));
    process.exit(r.status === 'error' ? 1 : 0);
  });
}
