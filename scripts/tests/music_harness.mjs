// Test harness for the local music library. Runs one gen-audio / library call with the env it is
// given and prints a JSON result on the last stdout line. fetch is replaced: HARNESS_FETCH=throw
// (default) throws on any call, HARNESS_FETCH=402 answers like an ElevenLabs free plan. Run under
// `node --require tools/egress/egress.cjs` so any DNS lookup or socket is logged too.
import { run } from '../gen-audio.mjs';
import * as lib from '../audio/music-library.mjs';

let fetchCalls = 0;
globalThis.fetch = async () => {
  fetchCalls++;
  if (process.env.HARNESS_FETCH === '402') {
    return new Response(JSON.stringify({ detail: { status: 'payment_required', message: 'Music API needs a paid plan' } }), { status: 402, headers: { 'content-type': 'application/json' } });
  }
  throw new Error('real network fetch attempted in a test');
};

const [mode, ...args] = process.argv.slice(2);
const logs = [];
let out;
if (mode === 'gen') {
  const r = await run(args, { env: process.env, log: (m) => logs.push(m) });
  out = { ...r };
} else if (mode === 'pick') {
  const [mood, seed] = args;
  const r = lib.pick(mood, { seed: seed || '' });
  out = { file: r.track ? r.track.file : null, credit: r.credit || null, reason: r.reason || null };
} else if (mode === 'load') {
  const L = lib.loadLibrary();
  out = { tracks: L.tracks.map((t) => t.file), errors: L.errors, unlisted: L.unlisted, exists: L.exists };
}
console.log(JSON.stringify({ ...out, logs, fetchCalls }));
