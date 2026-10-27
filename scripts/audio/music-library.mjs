#!/usr/bin/env node
// dstack local background-music library: free, licensed tracks you keep on this machine.
// Fully offline: this module never opens a network connection (tests run it under
// tools/egress/egress.cjs with a throwing fetch to prove it).
//
// Location: $DSTACK_MUSIC_DIR (default ~/.dstack/music, i.e. $DSTACK_HOME/music). It must be outside
// the dstack folder; .gitignore also blocks every audio file type so tracks can never be committed.
//
// manifest.json in that folder:
//   { "version": 1, "tracks": [ {
//       "file": "calm-piano.mp3",                 // relative to the library folder
//       "moods": ["calm", "ambient"],             // tags matched by `gen-audio.mjs bgm <mood>`
//       "duration": 94.2,                         // seconds
//       "title": "…", "artist": "…",               // optional
//       "source_url": "https://…",                // page the track came from
//       "licence": { "name": "CC0 1.0", "url": "https://creativecommons.org/publicdomain/zero/1.0/" },
//       "attribution": "",                        // text that must be shown with the work; "" if none
//       "commercial": true,                       // licence allows commercial use
//       "fetched": "2026-10-28"                   // date downloaded (YYYY-MM-DD)
//   } ] }
//
// Tracks with an invalid entry are never used. Tracks with "commercial": false are refused unless
// DSTACK_MUSIC_ALLOW_NONCOMMERCIAL=1. Audio files without a manifest entry are refused.
//
// CLI: node scripts/audio/music-library.mjs validate | list | pick <mood> [--seed S]

import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { insideRepo } from './keyfile.mjs';

export const AUDIO_EXT = /\.(mp3|wav|ogg|oga|flac|m4a|aac|opus)$/i;

export function musicDir(env = process.env) {
  const home = env.DSTACK_HOME || env.HUASHU_DESIGN_HOME || path.join(os.homedir(), '.dstack');
  return path.resolve((env.DSTACK_MUSIC_DIR || path.join(home, 'music')).replace(/^~(?=\/|$)/, os.homedir()));
}

const DATE = /^\d{4}-\d{2}-\d{2}$/;
const URL_RE = /^https?:\/\/\S+$/;

/** Validate one manifest entry. Returns a list of problems ([] when valid). */
export function entryProblems(t, dir) {
  const p = [];
  if (!t || typeof t !== 'object') return ['entry is not an object'];
  if (typeof t.file !== 'string' || !t.file) p.push('file missing');
  else {
    const abs = path.resolve(dir, t.file);
    if (path.relative(dir, abs).startsWith('..') || path.isAbsolute(t.file)) p.push('file must be inside the library folder');
    else if (!AUDIO_EXT.test(t.file)) p.push('file is not an audio file');
    else if (!fs.existsSync(abs)) p.push('file not found');
  }
  if (!Array.isArray(t.moods) || !t.moods.length || !t.moods.every((m) => typeof m === 'string' && m.trim())) p.push('moods must be a non-empty list of tags');
  if (!(typeof t.duration === 'number' && t.duration > 0)) p.push('duration must be seconds > 0');
  if (typeof t.source_url !== 'string' || !URL_RE.test(t.source_url)) p.push('source_url missing');
  if (!t.licence || typeof t.licence.name !== 'string' || !t.licence.name.trim()) p.push('licence.name missing');
  if (!t.licence || typeof t.licence.url !== 'string' || !URL_RE.test(t.licence.url)) p.push('licence.url missing');
  if (typeof t.attribution !== 'string') p.push('attribution must be a string ("" if none is required)');
  if (typeof t.commercial !== 'boolean') p.push('commercial must be true or false');
  if (typeof t.fetched !== 'string' || !DATE.test(t.fetched)) p.push('fetched must be YYYY-MM-DD');
  return p;
}

/**
 * Read and validate the library. Never throws.
 * Returns { dir, exists, manifest: bool, tracks: [valid entries + abs], errors: [string], unlisted: [file] }.
 */
export function loadLibrary(env = process.env) {
  const dir = musicDir(env);
  const out = { dir, exists: fs.existsSync(dir), manifest: false, tracks: [], errors: [], unlisted: [] };
  if (insideRepo(dir)) { out.errors.push(`DSTACK_MUSIC_DIR ${dir} is inside the dstack folder; keep the library outside the repo`); return out; }
  if (!out.exists) return out;
  const mf = path.join(dir, 'manifest.json');
  let listed = new Set();
  if (fs.existsSync(mf)) {
    out.manifest = true;
    let j;
    try { j = JSON.parse(fs.readFileSync(mf, 'utf8')); } catch (e) { out.errors.push(`manifest.json is not valid JSON (${e.message})`); j = null; }
    if (j && !Array.isArray(j.tracks)) out.errors.push('manifest.json needs a "tracks" list');
    for (const [i, t] of ((j && Array.isArray(j.tracks)) ? j.tracks : []).entries()) {
      if (t && typeof t.file === 'string') listed.add(path.normalize(t.file));
      const probs = entryProblems(t, dir);
      if (probs.length) out.errors.push(`track ${i + 1} (${(t && t.file) || '?'}): ${probs.join('; ')}`);
      else out.tracks.push({ ...t, moods: t.moods.map((m) => m.trim().toLowerCase()), abs: path.resolve(dir, t.file) });
    }
  }
  const walk = (d) => { for (const f of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, f.name); if (f.isDirectory()) walk(p); else if (AUDIO_EXT.test(f.name)) { const rel = path.relative(dir, p); if (!listed.has(path.normalize(rel))) out.unlisted.push(rel); } } };
  try { walk(dir); } catch { /* unreadable */ }
  return out;
}

export function allowNonCommercial(env = process.env) { return env.DSTACK_MUSIC_ALLOW_NONCOMMERCIAL === '1'; }

/** Attribution line to print with a delivery. */
export function creditLine(t) {
  const who = [t.title && `"${t.title}"`, t.artist && `by ${t.artist}`].filter(Boolean).join(' ');
  if (t.attribution && t.attribution.trim()) return `Attribution required: ${t.attribution.trim()}`;
  return `No attribution required (${t.licence.name}${who ? `; ${who}` : ''}; ${t.source_url})`;
}

/**
 * Pick a track for a mood. Deterministic: the same library, mood and seed always give the same track.
 * Returns { track, credit } or { track: null, reason }.
 */
export function pick(mood, { seed = '', env = process.env } = {}) {
  const lib = loadLibrary(env);
  const m = String(mood || '').trim().toLowerCase();
  if (!lib.exists) return { track: null, reason: `no local music library at ${lib.dir}` };
  const tagged = lib.tracks.filter((t) => t.moods.includes(m));
  const usable = tagged.filter((t) => t.commercial || allowNonCommercial(env)).sort((a, b) => a.file.localeCompare(b.file));
  if (!usable.length) {
    const why = tagged.length ? `only non-commercial tracks are tagged "${m}" (set DSTACK_MUSIC_ALLOW_NONCOMMERCIAL=1 to allow them)` : `no valid track tagged "${m}" in ${lib.dir}`;
    return { track: null, reason: why };
  }
  const h = crypto.createHash('sha256').update(`${m}\u0000${seed}`).digest();
  const track = usable[h.readUInt32BE(0) % usable.length];
  return { track, credit: creditLine(track), noncommercial: !track.commercial };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [cmd, mood, ...rest] = process.argv.slice(2);
  const si = rest.indexOf('--seed');
  const seed = si >= 0 ? rest[si + 1] : (rest.find((a) => a.startsWith('--seed=')) || '').slice(7);
  const lib = loadLibrary();
  if (cmd === 'validate' || cmd === 'list') {
    const moods = [...new Set(lib.tracks.flatMap((t) => t.moods))].sort();
    if (!lib.exists) console.log(`empty: no library at ${lib.dir}`);
    else console.log(`${lib.tracks.length} track(s), ${lib.tracks.filter((t) => t.commercial).length} commercial-ok, moods: ${moods.join(', ') || '-'}; ${lib.errors.length} error(s), ${lib.unlisted.length} unlisted file(s)${lib.manifest ? '' : ' (no manifest.json)'}`);
    for (const e of lib.errors) console.log(`  ✗ ${e}`);
    for (const u of lib.unlisted) console.log(`  ! ${u}: no manifest entry, never used`);
    if (cmd === 'list') for (const t of lib.tracks) console.log(`  ${t.file}  [${t.moods.join(',')}]  ${t.duration}s  ${t.licence.name}${t.commercial ? '' : ' (non-commercial)'}`);
    process.exit(lib.errors.length ? 1 : 0);
  } else if (cmd === 'pick' && mood) {
    const r = pick(mood, { seed });
    if (!r.track) { console.error(r.reason); process.exit(1); }
    console.log(JSON.stringify({ file: r.track.abs, credit: r.credit }));
  } else {
    console.error('usage: music-library.mjs validate | list | pick <mood> [--seed S]');
    process.exit(2);
  }
}
