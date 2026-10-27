#!/usr/bin/env node
/**
 * gen-audio.mjs · fill the audio library slots (background music + SFX) that dstack no longer ships.
 *
 * Provider (DSTACK_AUDIO_PROVIDER):
 *   none        (default) generate nothing; tells you where to put your own licensed file
 *   elevenlabs  ElevenLabs Sound Effects (/v1/sound-generation) and Music (/v1/music, paid plans only)
 *               over https://api.elevenlabs.io, key from ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE.
 *               No key: one warning, then behaves like `none` (exit 0).
 *
 * Usage:
 *   node scripts/gen-audio.mjs bgm <mood> [--prompt "..."] [--seconds 60] [--force]
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

/** Returns { status: 'kept'|'skipped'|'generated'|'cached'|'error', target, message } and never throws. */
export async function run(argv, { env = process.env, fetchImpl, log = (m) => console.error(el.mask(m, env)) } = {}) {
  const a = parse(argv);
  const [kind, slot] = a._;
  const d = dirs(env);
  if (kind === 'status') {
    const k = el.loadKey(env);
    log(`audio provider: ${provider(env)} · ElevenLabs key: ${k.key ? `present (${k.source})` : 'absent'} · bgm dir: ${d.audio} · sfx dir: ${d.sfx} · cache: ${el.cacheDir(env)}`);
    return { status: 'status' };
  }
  let target, req;
  if (kind === 'bgm' && slot && /^[\w-]+$/.test(slot)) {
    target = path.join(d.audio, `bgm-${slot}.mp3`);
    const prompt = a.prompt || BGM_PROMPTS[slot.replace(/-alt$/, '')];
    if (!prompt) return { status: 'error', message: `no built-in prompt for mood "${slot}"; pass --prompt "..."` };
    req = { kind: 'music', prompt, seconds: a.seconds ? Number(a.seconds) : 60 };
  } else if (kind === 'sfx' && slot && /^[\w-]+\/[\w-]+$/.test(slot)) {
    target = path.join(d.sfx, `${slot}.mp3`);
    const lib = libraryEntry(slot);
    const prompt = a.prompt || (lib && lib.prompt);
    if (!prompt) return { status: 'error', message: `"${slot}" isn't in references/sfx-library.md; pass --prompt "..."` };
    req = { kind: 'sfx', prompt, seconds: a.seconds ? Number(a.seconds) : lib && lib.seconds, loop: !!a.loop };
  } else {
    return { status: 'error', message: 'usage: gen-audio.mjs bgm <mood> | sfx <category>/<name> | status  [--prompt ..] [--seconds N] [--loop] [--force]' };
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
  if (prov !== 'elevenlabs') return { status: 'error', target, message: `unknown DSTACK_AUDIO_PROVIDER "${prov}" (none | elevenlabs)` };
  if (!el.hasKey(env)) {
    log(`WARNING: DSTACK_AUDIO_PROVIDER=elevenlabs but no ElevenLabs key (ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE); generating nothing. ${supply}`);
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
    log(`WARNING: ${msg.replace(/\.$/, '')}. Nothing written. ${supply}`);
    return { status: 'error', target, message: msg };
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  run(process.argv.slice(2)).then((r) => {
    if (r.status === 'error' && r.message) console.error(el.mask(r.message));
    process.exit(r.status === 'error' ? 1 : 0);
  });
}
