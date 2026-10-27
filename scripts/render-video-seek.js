#!/usr/bin/env node
/**
 * HTML animation → MP4 via deterministic frame-by-frame SEEK (Playwright + ffmpeg).
 *
 * This is a frame-by-frame alternative renderer to render-video.js (Playwright recordVideo). The technical core borrows
 * the "freeze the clock + seek to a timestamp and screenshot" approach from HeyGen HyperFrames (Apache 2.0), but pulls in
 * no third-party packages: it only uses the playwright + ffmpeg this skill already has, and is runtime-neutral.
 *
 * Three deadlocks of render-video.js that it solves (see references/video-export.md §"seek rendering"):
 *   1. The frame rate is no longer locked to 25fps by the Chromium headless compositor; --fps gives any native frame rate
 *   2. No more need for convert-formats.sh's after-the-fact minterpolate frame interpolation (which has ghosting + a macOS
 *      QuickTime compatibility bug, see animation-pitfalls §14); every frame is a real seeked frame
 *   3. No screen recording → no black frames at the start → no need for the --trim / --fontwait / __ready offset logic
 *   Bonus: seeking to a timestamp and screenshotting is deterministic, same input same output (recordVideo is live recording, non-deterministic)
 *
 * Prerequisite: the animation must run on the Stage clock (<Stage> from assets/animations.jsx or <NarrationStage> from
 * narration_stage.jsx), which respond to window.__seekRender by freezing their self-driven clock, and expose
 * window.__seek(t). Pure CSS @keyframes / Lottie / animations not driven by Stage don't respond to __seek;
 * keep using render-video.js for those.
 *
 * Requires: global playwright (`npm install -g playwright`), ffmpeg on PATH.
 *
 * Usage:
 *   NODE_PATH=$(npm root -g) node render-video-seek.js <html-file> \
 *     [--duration=30] [--fps=60] [--width=1920] [--height=1080] \
 *     [--concurrency=4] [--settle=2] [--keep-chrome]
 *
 * Output: next to the HTML file, same basename with .mp4 suffix.
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

function arg(name, def) {
  const p = process.argv.find(a => a.startsWith('--' + name + '='));
  return p ? p.slice(name.length + 3) : def;
}
function hasFlag(name) {
  return process.argv.includes('--' + name);
}

const HTML_FILE = process.argv[2];
if (!HTML_FILE || HTML_FILE.startsWith('--')) {
  console.error('Usage: node render-video-seek.js <html-file>');
  console.error('Example: NODE_PATH=$(npm root -g) node render-video-seek.js my-animation.html --fps=60');
  process.exit(1);
}

const DURATION    = parseFloat(arg('duration', '30'));
const FPS         = parseFloat(arg('fps', '60'));      // any native frame rate, default true 60fps
const WIDTH       = parseInt(arg('width', '1920'));
const HEIGHT      = parseInt(arg('height', '1080'));
const CONCURRENCY = Math.max(1, parseInt(arg('concurrency', '4')));  // number of parallel workers (one page each)
const SETTLE      = Math.max(1, parseInt(arg('settle', '2')));        // how many rAFs to wait after a seek before screenshotting
const READY_TIMEOUT = parseFloat(arg('readytimeout', '8'));
const KEEP_CHROME = hasFlag('keep-chrome');

const HTML_ABS = path.resolve(HTML_FILE);
const BASENAME = path.basename(HTML_FILE, path.extname(HTML_FILE));
const DIR      = path.dirname(HTML_ABS);
const TMP_DIR  = path.join(DIR, '.seek-tmp-' + Date.now() + '-' + process.pid);
const MP4_OUT  = path.join(DIR, BASENAME + '.mp4');

// Chrome-hiding rules identical to render-video.js (so the output of both pipelines looks the same)
const HIDE_CHROME_CSS = `
  .no-record,
  .progress, .progress-bar,
  .counter, .tCur,
  .phases, .phase-label, .phase,
  .replay, button.replay,
  .masthead, .kicker, .title,
  .footer,
  [data-role="chrome"], [data-record="hidden"] {
    display: none !important;
  }
`;

const TOTAL_FRAMES = Math.round(FPS * DURATION);

console.log(`▸ Seek-rendering: ${HTML_FILE}`);
console.log(`  size: ${WIDTH}x${HEIGHT} · ${FPS}fps · duration: ${DURATION}s · frames: ${TOTAL_FRAMES} · workers: ${CONCURRENCY}`);
console.log(`  output: ${MP4_OUT}`);

// Runs in the page context: wait SETTLE rAFs (let React/Babel commit + layout settle before screenshotting)
async function waitRaf(page, n) {
  await page.evaluate((count) => new Promise(resolve => {
    let i = 0;
    const step = () => { i++; (i >= count) ? resolve() : requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }), n);
}

// One worker: open a page, goto, wait for __seek to be ready, render the frames assigned to it
async function renderFrames(context, url, frames) {
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });

  // Stage / NarrationStage expose window.__seek and freeze the self-driven clock in __seekRender mode
  await page.waitForFunction(
    () => window.__ready === true && typeof window.__seek === 'function',
    { timeout: READY_TIMEOUT * 1000 },
  );

  for (const f of frames) {
    const t = f / FPS;
    await page.evaluate((tt) => window.__seek(tt), t);
    await waitRaf(page, SETTLE);
    await page.screenshot({
      path: path.join(TMP_DIR, 'frame-' + String(f).padStart(6, '0') + '.png'),
      clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT },
    });
  }
  await page.close();
}

(async () => {
  fs.mkdirSync(TMP_DIR, { recursive: true });

  const browser = await chromium.launch();
  const url = 'file://' + HTML_ABS;

  const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1,
  });

  // Key signal: __seekRender makes Stage / NarrationStage freeze the wall-clock rAF and let the external __seek drive frames instead
  // __recording is kept, so Stage forces loop=false (reusing the existing convention)
  await context.addInitScript(() => {
    window.__recording = true;
    window.__seekRender = true;
  });

  if (!KEEP_CHROME) {
    // Same chrome hiding as render-video.js (CSS + fixed-bar heuristics)
    await context.addInitScript(css => {
      const HIDE_MARK = 'data-video-hidden';
      function injectStyle() {
        const style = document.createElement('style');
        style.setAttribute('data-inject', 'render-video-chrome-hide');
        style.textContent = css;
        (document.head || document.documentElement).appendChild(style);
      }
      function hideChromeBars() {
        const vh = window.innerHeight;
        document.querySelectorAll('div, nav, header, footer, section, aside')
          .forEach(el => {
            if (el.hasAttribute(HIDE_MARK)) return;
            if (el.dataset.recordKeep === 'true') return;
            const s = getComputedStyle(el);
            if (s.position !== 'fixed' && s.position !== 'sticky') return;
            const r = el.getBoundingClientRect();
            if (r.height > vh * 0.25) return;
            const atBottom = r.bottom >= vh - 30;
            const atTop = r.top <= 30 && r.height < 80;
            if (!atBottom && !atTop) return;
            const txt = el.textContent || '';
            const hasBtn = !!el.querySelector('button, [role="button"]');
            const hasCtrls = /[⏸▶⏮⏭↻↺↩↪]|\d+\.\d+\s*s/.test(txt);
            if (hasBtn || hasCtrls) {
              el.style.setProperty('display', 'none', 'important');
              el.setAttribute(HIDE_MARK, '1');
            }
          });
      }
      const start = () => {
        injectStyle();
        hideChromeBars();
        const obs = new MutationObserver(hideChromeBars);
        obs.observe(document.body, { childList: true, subtree: true });
        setTimeout(() => obs.disconnect(), 6000);
      };
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start, { once: true });
      } else {
        start();
      }
    }, HIDE_CHROME_CSS);
  }

  // Distribute the frames round-robin across CONCURRENCY workers (each page has its own window, so seeks don't interfere)
  const buckets = Array.from({ length: CONCURRENCY }, () => []);
  for (let f = 0; f < TOTAL_FRAMES; f++) buckets[f % CONCURRENCY].push(f);

  console.log(`▸ Capturing ${TOTAL_FRAMES} frames across ${CONCURRENCY} workers…`);
  try {
    await Promise.all(buckets.map(b => b.length ? renderFrames(context, url, b) : Promise.resolve()));
  } catch (e) {
    const msg = String(e && e.message || e);
    if (/__seek|__ready/.test(msg)) {
      console.error('');
      console.error('✗ The animation doesn\'t expose window.__seek (or it isn\'t ready).');
      console.error('  Seek rendering only supports animations on the Stage clock (<Stage> from assets/animations.jsx');
      console.error('  or <NarrationStage> from narration_stage.jsx). For pure CSS @keyframes / Lottie /');
      console.error('  hand-written non-Stage animations, use render-video.js instead.');
      console.error('');
    }
    await browser.close();
    fs.rmSync(TMP_DIR, { recursive: true, force: true });
    console.error(msg.slice(0, 500));
    process.exit(1);
  }

  await browser.close();

  const pngCount = fs.readdirSync(TMP_DIR).filter(f => f.endsWith('.png')).length;
  if (pngCount === 0) {
    console.error('✗ No frames were captured');
    process.exit(1);
  }
  console.log(`▸ Captured ${pngCount}/${TOTAL_FRAMES} frames. Encoding H.264…`);

  // PNG sequence → MP4. No trim (there were no black frames to begin with); input and output frame rates are both set to FPS.
  const ffmpeg = spawnSync('ffmpeg', [
    '-y',
    '-framerate', String(FPS),
    '-i', path.join(TMP_DIR, 'frame-%06d.png'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-crf', '18',
    '-preset', 'medium',
    '-r', String(FPS),
    '-movflags', '+faststart',
    MP4_OUT,
  ], { stdio: ['ignore', 'ignore', 'pipe'] });

  if (ffmpeg.status !== 0) {
    console.error('✗ ffmpeg failed:\n' + ffmpeg.stderr.toString().slice(-2000));
    process.exit(1);
  }

  fs.rmSync(TMP_DIR, { recursive: true, force: true });

  const mp4Size = (fs.statSync(MP4_OUT).size / 1024 / 1024).toFixed(1);
  console.log(`✓ Done: ${MP4_OUT} (${mp4Size} MB · ${FPS}fps native)`);
})();
