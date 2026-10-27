// Test harness for the ElevenLabs integration: runs one scenario with a mocked HTTP layer and
// prints a JSON result on the last stdout line. globalThis.fetch is replaced so nothing can
// reach the network. Driven by test_elevenlabs.py.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

globalThis.fetch = async () => { throw new Error('real network fetch attempted in a test'); };

const scenario = process.argv[2];
const work = fs.mkdtempSync(path.join(os.tmpdir(), 'dstack-el-test-'));
process.env.DSTACK_HOME = path.join(work, 'home');
delete process.env.DSTACK_AUDIO_DIR; delete process.env.DSTACK_SFX_DIR;

const prov = await import('../tts/providers.mjs');
const el = await import('../audio/elevenlabs.mjs');
const gen = await import('../gen-audio.mjs');

function mp3(seconds = 0.6) {
  const f = path.join(work, 'tone.mp3');
  execFileSync('ffmpeg', ['-y', '-f', 'lavfi', '-i', `sine=f=440:d=${seconds}`, '-acodec', 'libmp3lame', '-q:a', '9', f], { stdio: 'ignore' });
  return fs.readFileSync(f);
}

function mockFetch(handler) {
  const calls = [];
  const f = async (url, init) => {
    calls.push({ url, method: init.method, headers: init.headers, body: JSON.parse(init.body) });
    return handler(url, init);
  };
  return { f, calls };
}
const ok = (obj) => ({ ok: true, status: 200, json: async () => obj, text: async () => JSON.stringify(obj), arrayBuffer: async () => new ArrayBuffer(0) });
const okAudio = (buf) => ({ ok: true, status: 200, arrayBuffer: async () => buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength), text: async () => '', json: async () => ({}) });
const fail = (status, body) => ({ ok: false, status, text: async () => body, json: async () => JSON.parse(body) });

function alignmentFor(text, dur) {
  const chars = [...text];
  const step = dur / chars.length;
  return { characters: chars, character_start_times_seconds: chars.map((_, i) => +(i * step).toFixed(3)), character_end_times_seconds: chars.map((_, i) => +((i + 1) * step).toFixed(3)) };
}

const out = {};
const KEY = 'sk_testSECRETkey0123456789abcdef';
try {
  if (scenario === 'selection') {
    delete process.env.DSTACK_TTS_PROVIDER;
    out.defaultTts = prov.providerName();
    process.env.DSTACK_TTS_PROVIDER = 'elevenlabs';
    out.envTts = prov.providerName();
    out.cliTts = prov.providerName('silent');
    try { prov.checkProvider('nope'); out.unknown = 'accepted'; } catch (e) { out.unknown = 'rejected'; }
    out.defaultAudio = gen.provider({});
    out.envAudio = gen.provider({ DSTACK_AUDIO_PROVIDER: 'elevenlabs' });
    out.host = el.BASE_URL;
    out.defaults = { voice: el.DEFAULT_VOICE, model: el.DEFAULT_MODEL, format: el.OUTPUT_FORMAT };
  } else if (scenario === 'missing-key') {
    delete process.env.ELEVENLABS_API_KEY; delete process.env.DSTACK_ELEVENLABS_KEY_FILE;
    const m = mockFetch(() => ok({}));
    const r1 = await prov.synthesize('elevenlabs', 'Hello there world.', path.join(work, 'a.mp3'), { fetchImpl: m.f, quiet: true });
    const r2 = await prov.synthesize('elevenlabs', 'Second chunk here.', path.join(work, 'b.mp3'), { fetchImpl: m.f, quiet: true });
    out.providers = [r1.provider, r2.provider];
    out.fallback = r1.fallback;
    out.duration = r1.duration > 0;
    out.calls = m.calls.length;
    const g = await gen.run(['sfx', 'ui/click'], { env: { ...process.env, DSTACK_AUDIO_PROVIDER: 'elevenlabs' }, fetchImpl: m.f });
    out.gen = g.status;
    out.genCalls = m.calls.length;
  } else if (scenario === 'request-shape') {
    process.env.ELEVENLABS_API_KEY = KEY;
    process.env.DSTACK_ELEVENLABS_VOICE = 'AbCdEfGhIjKlMnOpQrSt';
    process.env.DSTACK_ELEVENLABS_MODEL = 'eleven_flash_v2_5';
    const audio = mp3();
    const text = 'Rain on the fields.';
    const m = mockFetch((url) => url.includes('/text-to-speech/')
      ? ok({ audio_base64: audio.toString('base64'), alignment: alignmentFor(text, 0.6) })
      : okAudio(audio));
    const r = await prov.synthesize('elevenlabs', text, path.join(work, 't.mp3'), { speed: 1.1, quiet: true, fetchImpl: m.f });
    out.tts = { provider: r.provider, wordsEstimated: r.wordsEstimated, words: r.words.map((w) => w.text) };
    const env = { ...process.env, DSTACK_AUDIO_PROVIDER: 'elevenlabs' };
    await gen.run(['sfx', 'ui/click'], { env, fetchImpl: m.f, log: () => {} });
    await gen.run(['bgm', 'tech', '--seconds', '30'], { env, fetchImpl: m.f, log: () => {} });
    out.calls = m.calls.map((c) => ({ url: c.url, method: c.method, key: c.headers['xi-api-key'] === KEY, body: c.body }));
    out.sfxFile = fs.existsSync(path.join(gen.dirs(env).sfx, 'ui', 'click.mp3'));
    out.bgmFile = fs.existsSync(path.join(gen.dirs(env).audio, 'bgm-tech.mp3'));
  } else if (scenario === 'cache') {
    process.env.ELEVENLABS_API_KEY = KEY;
    const audio = mp3();
    const m = mockFetch((url) => url.includes('/text-to-speech/') ? ok({ audio_base64: audio.toString('base64'), alignment: alignmentFor('Same words.', 0.6) }) : okAudio(audio));
    const env = { ...process.env, DSTACK_AUDIO_PROVIDER: 'elevenlabs' };
    const a = await gen.run(['sfx', 'ui/click'], { env, fetchImpl: m.f, log: () => {} });
    const b = await gen.run(['sfx', 'ui/click', '--force'], { env, fetchImpl: m.f, log: () => {} });
    const c = await gen.run(['sfx', 'ui/click'], { env, fetchImpl: m.f, log: () => {} });
    const d = await gen.run(['sfx', 'ui/click', '--force', '--prompt', 'a different click'], { env, fetchImpl: m.f, log: () => {} });
    out.sfx = [a.status, b.status, c.status, d.status];
    await prov.synthesize('elevenlabs', 'Same words.', path.join(work, '1.mp3'), { quiet: true, fetchImpl: m.f });
    const t2 = await prov.synthesize('elevenlabs', 'Same words.', path.join(work, '2.mp3'), { quiet: true, fetchImpl: m.f });
    out.ttsSecondMeasured = !t2.wordsEstimated;
    out.calls = m.calls.length;
  } else if (scenario === 'key-hygiene') {
    process.env.ELEVENLABS_API_KEY = KEY;
    // a hostile error body that echoes the key back
    const m = mockFetch(() => fail(401, JSON.stringify({ detail: { status: 'invalid_api_key', message: `Invalid API key ${KEY}` } })));
    const r = await prov.synthesize('elevenlabs', 'Hello.', path.join(work, 'x.mp3'), { quiet: false, fetchImpl: m.f });
    out.provider = r.provider;
    out.fallbackMasked = !String(r.fallback).includes(KEY);
    const env = { ...process.env, DSTACK_AUDIO_PROVIDER: 'elevenlabs' };
    const logs = [];
    const m500 = mockFetch(() => fail(500, JSON.stringify({ detail: { message: `upstream saw xi-api-key: ${KEY} and ${KEY}` } })));
    const g = await gen.run(['bgm', 'tech'], { env, fetchImpl: m500.f, log: (s) => logs.push(el.mask(s, env)) });
    console.error(logs.join('\n'));
    console.error(g.message);
    out.gen = g.status;
    out.maskSample = el.mask(`key=${KEY} xi-api-key: ${KEY}`);
    // nothing on disk may contain the key
    const files = [];
    const walk = (d) => { for (const f of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, f.name); f.isDirectory() ? walk(p) : files.push(p); } };
    if (fs.existsSync(process.env.DSTACK_HOME)) walk(process.env.DSTACK_HOME);
    out.keyOnDisk = files.some((f) => fs.readFileSync(f).includes(KEY));
    // key file: inside the repo is refused, outside is used
    delete process.env.ELEVENLABS_API_KEY;
    const outside = path.join(work, 'el.key');
    fs.writeFileSync(outside, KEY + '\n');
    out.fileKey = el.loadKey({ DSTACK_ELEVENLABS_KEY_FILE: outside }).source;
    out.repoKey = el.loadKey({ DSTACK_ELEVENLABS_KEY_FILE: path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..', 'SKILL.md') }).source;
    try { await el.post('/../other', {}, { env: { ELEVENLABS_API_KEY: KEY }, fetchImpl: m.f }); out.badEndpoint = 'sent'; } catch { out.badEndpoint = 'refused'; }
    out.key = KEY; // the test checks stdout/stderr apart from this field
  } else {
    throw new Error(`unknown scenario ${scenario}`);
  }
} finally {
  fs.rmSync(work, { recursive: true, force: true });
}
console.log(JSON.stringify(out));
