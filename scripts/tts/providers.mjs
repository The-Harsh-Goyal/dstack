// dstack TTS providers. Off by default: the default "silent" provider makes no
// sound and sends nothing anywhere. The only cloud provider is ElevenLabs (approved, US host),
// and it runs only when you select it.
//
// Providers (choose with --tts <name> or DSTACK_TTS_PROVIDER):
//   silent   (default) silent track whose length is estimated from the text
//            (English ~DSTACK_TTS_WPM words/min, default 155; CJK ~4.2 chars/s).
//            Timeline words are evenly spread estimates (wordsEstimated: true),
//            so subtitle/karaoke layout still works without any voice.
//   command  run a LOCAL command you configure in DSTACK_TTS_COMMAND, e.g.
//              DSTACK_TTS_COMMAND='espeak-ng -v en-us -w {out} -f {text_file}'
//            Placeholders: {text_file} (UTF-8 text), {out} (audio file to write,
//            any format ffmpeg reads), {voice}, {speed}. If the command prints a
//            JSON object on stdout like {"words":[{"text","start","end"}]} those
//            timings are used. This is also the plug-in point for a vetted
//            provider adapter later (an adapter script you add yourself).
//            Whatever the command does with the text is its responsibility:
//            dstack prints the command before running it.
//   elevenlabs  ElevenLabs TTS over https://api.elevenlabs.io (scripts/audio/elevenlabs.mjs):
//            with-timestamps endpoint, so word timings are measured. Voice/model from
//            DSTACK_ELEVENLABS_VOICE / DSTACK_ELEVENLABS_MODEL (or the script's `voice:`).
//            Key: ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE. No key, or an API error:
//            one warning, then the chunk (and the rest of the run) falls back to silent.
//            Results are cached, so re-running the same text costs no credits.
//
// Contract: await synthesize(name, text, outMp3, opts) -> { duration, words: [...], wordsEstimated, provider }

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import * as el from '../audio/elevenlabs.mjs';

const CJK = /[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]/g;

export function estimateDuration(text, speed = 1) {
  const cjk = (text.match(CJK) || []).length;
  const latinWords = text.replace(CJK, ' ').split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
  const wpm = parseFloat(process.env.DSTACK_TTS_WPM || '155');
  const pauses = (text.match(/[.!?。！？]/g) || []).length * 0.25 + (text.match(/[,;:，、；：]/g) || []).length * 0.12;
  const secs = (latinWords / wpm) * 60 + cjk / 4.2 + pauses;
  return Math.max(0.4, secs / (speed || 1));
}

export function estimateWords(text, duration) {
  // tokens: each CJK char is a token, each latin word (with trailing punctuation) is a token
  const tokens = text.match(/[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af][。！？，、；：]*|[^\s\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]+/g) || [];
  const weight = (t) => Math.max(1, t.replace(/[^\p{L}\p{N}]/gu, '').length);
  const total = tokens.reduce((a, t) => a + weight(t), 0) || 1;
  let cur = 0;
  return tokens.map((t) => {
    const d = (weight(t) / total) * duration;
    const w = { text: t, start: +cur.toFixed(3), end: +(cur + d).toFixed(3) };
    cur += d;
    return w;
  });
}

function probeDuration(file) {
  const out = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
    '-of', 'default=noprint_wrappers=1:nokey=1', file], { encoding: 'utf8' });
  return parseFloat(out.trim());
}

function silentMp3(duration, outPath) {
  execFileSync('ffmpeg', ['-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', duration.toFixed(3),
    '-q:a', '9', '-acodec', 'libmp3lame', outPath], { stdio: ['ignore', 'pipe', 'pipe'] });
}

function shellQuote(s) { return `'${String(s).replace(/'/g, `'\\''`)}'`; }

const providers = {
  silent(text, outPath, opts) {
    const duration = estimateDuration(text, opts.speed);
    silentMp3(duration, outPath);
    return { duration: probeDuration(outPath), words: estimateWords(text, duration), wordsEstimated: true };
  },
  command(text, outPath, opts) {
    const tpl = process.env.DSTACK_TTS_COMMAND;
    if (!tpl) throw new Error('TTS provider "command" needs DSTACK_TTS_COMMAND, e.g. DSTACK_TTS_COMMAND=\'espeak-ng -w {out} -f {text_file}\'. Or use --tts silent.');
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'dstack-tts-'));
    const textFile = path.join(dir, 'text.txt');
    const raw = path.join(dir, 'out.wav');
    fs.writeFileSync(textFile, text, 'utf8');
    const cmd = tpl.replaceAll('{text_file}', shellQuote(textFile)).replaceAll('{out}', shellQuote(raw))
      .replaceAll('{voice}', shellQuote(opts.voice || '')).replaceAll('{speed}', shellQuote(opts.speed || 1));
    if (!opts.quiet) console.error(`[tts] running local command: ${cmd}`);
    const stdout = execFileSync('bash', ['-c', cmd], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'inherit'] });
    if (!fs.existsSync(raw)) throw new Error(`TTS command finished but wrote no audio to {out} (${raw})`);
    execFileSync('ffmpeg', ['-y', '-i', raw, '-ar', '24000', '-ac', '1', '-acodec', 'libmp3lame', '-q:a', '4', outPath], { stdio: ['ignore', 'pipe', 'pipe'] });
    fs.rmSync(dir, { recursive: true, force: true });
    const duration = probeDuration(outPath);
    let words = null;
    try { const j = JSON.parse(stdout.trim().split('\n').pop() || ''); if (Array.isArray(j.words)) words = j.words; } catch { /* no timings */ }
    return words ? { duration, words, wordsEstimated: false } : { duration, words: estimateWords(text, duration), wordsEstimated: true };
  },
  async elevenlabs(text, outPath, opts) {
    const r = await el.tts(text, opts, { fetchImpl: opts.fetchImpl });
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'dstack-el-'));
    const raw = path.join(dir, 'el.mp3');
    fs.writeFileSync(raw, r.audio);
    // same encoding as the silent gaps (24 kHz mono mp3) so the concat demuxer can join them
    execFileSync('ffmpeg', ['-y', '-i', raw, '-ar', '24000', '-ac', '1', '-acodec', 'libmp3lame', '-q:a', '4', outPath], { stdio: ['ignore', 'pipe', 'pipe'] });
    fs.rmSync(dir, { recursive: true, force: true });
    const duration = probeDuration(outPath);
    const words = el.alignmentToWords(r.alignment);
    if (!opts.quiet) console.error(`[tts] elevenlabs ${r.cached ? 'cache hit' : 'generated'} (${duration.toFixed(2)}s)`);
    return words && words.length ? { duration, words, wordsEstimated: false } : { duration, words: estimateWords(text, duration), wordsEstimated: true };
  },
};

let elevenDisabled = null;   // reason string once ElevenLabs failed in this run
export function _resetFallback() { elevenDisabled = null; el._resetWarnings(); }

export function providerName(cli) {
  return cli || process.env.DSTACK_TTS_PROVIDER || 'silent';
}

export function checkProvider(name) {
  if (!providers[name]) throw new Error(`Unknown TTS provider "${name}". Available: ${Object.keys(providers).join(', ')}. See references/voiceover-pipeline.md.`);
  if (name === 'command' && !process.env.DSTACK_TTS_COMMAND) throw new Error('TTS provider "command" needs DSTACK_TTS_COMMAND, e.g. DSTACK_TTS_COMMAND=\'espeak-ng -w {out} -f {text_file}\'. Or use --tts silent.');
  if (name === 'elevenlabs' && !el.hasKey()) {
    el.warnOnce('tts-nokey', '[tts] WARNING: DSTACK_TTS_PROVIDER=elevenlabs but no ElevenLabs key (ELEVENLABS_API_KEY or DSTACK_ELEVENLABS_KEY_FILE): using the silent provider instead.');
  }
}

export async function synthesize(name, text, outPath, opts = {}) {
  checkProvider(name);
  if (name === 'elevenlabs') {
    if (!el.hasKey()) elevenDisabled = elevenDisabled || 'no API key';
    if (!elevenDisabled) {
      try {
        return { ...(await providers.elevenlabs(text, outPath, opts)), provider: 'elevenlabs' };
      } catch (e) {
        elevenDisabled = el.mask(e && e.message ? e.message : String(e));
        el.warnOnce('tts-fail', `[tts] WARNING: ElevenLabs failed (${elevenDisabled}); this and the remaining chunks use the silent provider.`);
      }
    }
    return { ...providers.silent(text, outPath, opts), provider: 'silent', fallback: elevenDisabled };
  }
  return { ...(await providers[name](text, outPath, opts)), provider: name };
}
