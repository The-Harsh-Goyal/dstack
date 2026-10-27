#!/usr/bin/env node
/**
 * gen_deck_thumbs.mjs: generate a thumbnail for every slide of a multi-file deck (for the "infinite gallery" overview in deck_index.html).
 *
 * Background: deck_index.html has two overviews:
 *   · grid (default 60%): renders the real sub-pages in iframes, sharp and WYSIWYG, no thumbnails needed.
 *   · infinite gallery (40%): tiles every slide seamlessly and infinitely + drifts slowly; dozens to hundreds of tiles would be very laggy if they all used iframes,
 *     so the gallery uses <img> thumbnails instead: the same image reused many times is decoded only once by the browser, so it's smooth.
 *   This script prepares those thumbnails for the gallery. Grid mode doesn't need it.
 *
 * Usage (copy into the deck project root, install the dependencies, then run):
 *   npm install playwright sharp
 *   node gen_deck_thumbs.mjs --slides slides --out thumbs [--width 1600] [--quality 86]
 *
 * Then in index.html's MANIFEST, add a thumb to each entry (a .jpg with the same name as file):
 *   { file: "slides/01-cover.html", thumb: "thumbs/01-cover.jpg", label: "Cover" }
 * deck_index.html only uses thumb in gallery mode; grid mode always uses file (iframe). Without a thumb, the gallery falls back to an iframe.
 *
 * Tip: don't make the thumbnail resolution too low (default 1600px), or cards in the gallery will look blurry when enlarged on hover.
 */
import { chromium } from 'playwright';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';

const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const slidesDir = arg('slides', 'slides');
const outDir = arg('out', 'thumbs');
const width = parseInt(arg('width', '1600'), 10);
const quality = parseInt(arg('quality', '86'), 10);
const W = parseInt(arg('canvas-w', '1920'), 10);
const H = parseInt(arg('canvas-h', '1080'), 10);

if (!fs.existsSync(slidesDir)) { console.error('slides directory not found: ' + slidesDir); process.exit(1); }
fs.mkdirSync(outDir, { recursive: true });
const files = fs.readdirSync(slidesDir).filter(f => f.endsWith('.html')).sort();
if (!files.length) { console.error('no .html in the slides directory'); process.exit(1); }

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
let ok = 0;
for (const f of files) {
  const base = f.replace(/\.html$/, '');
  const out = path.join(outDir, base + '.jpg');
  try {
    await page.goto('file://' + path.resolve(slidesDir, f), { waitUntil: 'load' });
    await page.waitForTimeout(2800);                 // wait for webfonts / images to paint
    const buf = await page.screenshot({ type: 'png', clip: { x: 0, y: 0, width: W, height: H } });
    await sharp(buf).resize(width).jpeg({ quality }).toFile(out);
    ok++; console.log('[ok] ' + out);
  } catch (e) { console.error('[FAIL] ' + f + ': ' + e.message); }
}
await browser.close();
console.log(`\n=== ${ok}/${files.length} thumbnails → ${outDir}/ ===`);
console.log('In index.html\'s MANIFEST, add thumb: "' + outDir + '/<same-name>.jpg" to each entry (used only in gallery mode)');
