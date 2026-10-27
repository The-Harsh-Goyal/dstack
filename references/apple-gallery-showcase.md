# Apple Gallery Showcase · Gallery Wall Animation Style

> Inspiration: the Claude Design website hero video + the "wall of work" display style of Apple product pages
> Field source: huashu-design launch hero v5
> When to use: **product launch hero animations, skill capability demos, portfolio showcases**, any scenario where "many high-quality outputs" need to be exhibited at once while guiding the viewer's attention

---

## Trigger judgment: when to use this style

**Good fit**:
- There are 10+ real outputs to show on one screen (PPTs, apps, web pages, infographics)
- The audience is professional (developers, designers, product managers) and sensitive to "texture"
- The feel you want to convey is "restrained, exhibition-like, premium, spacious"
- You need focus and the whole picture at the same time (see details without losing the whole)

**Poor fit**:
- Focus on a single product (use the product hero template from frontend-design)
- Emotional/strongly story-driven animation (use the timeline narrative template)
- Small screens / portrait (the tilted perspective gets muddy in a small frame)

---

## Core visual tokens

```css
:root {
  /* Light gallery palette */
  --bg:         #F5F5F7;   /* Main canvas background: Apple website gray */
  --bg-warm:    #FAF9F5;   /* Warm off-white variant */
  --ink:        #1D1D1F;   /* Main text color */
  --ink-80:     #3A3A3D;
  --ink-60:     #545458;
  --muted:      #86868B;   /* Secondary text */
  --dim:        #C7C7CC;
  --hairline:   #E5E5EA;   /* 1px card border */
  --accent:     #D97757;   /* Terracotta orange: Claude brand */
  --accent-deep:#B85D3D;

  --serif-cn: "Noto Serif SC", "Songti SC", Georgia, serif;
  --serif-en: "Source Serif 4", "Tiempos Headline", Georgia, serif;
  --sans:     "Inter", -apple-system, "PingFang SC", system-ui;
  --mono:     "JetBrains Mono", "SF Mono", ui-monospace;
}
```

> This palette is the brand choice for huashu-design's own promo film (close to the Claude ecosystem), **not a default**. When you use this gallery technique for another subject, re-derive the colors from the subject: warm off-white + terracotta is exactly item one of the 2026 AI default look.

**Key principles**:
1. **Never use a pure black background**. A black background makes the work look like a movie, not like "work output that can be adopted"
2. **Terracotta orange is the only hue accent**; everything else is grayscale + white
3. **Triple font stack** (English serif + Chinese serif + sans + mono) creates the feel of a "publication" rather than an "internet product"

---

## Core layout patterns

### 1. Floating cards (the basic unit of the whole style)

```css
.gallery-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 6px;                          /* The padding is the "mat board" */
  border: 1px solid var(--hairline);
  box-shadow:
    0 20px 60px -20px rgba(29, 29, 31, 0.12),   /* Main shadow, soft and long */
    0 6px 18px -6px rgba(29, 29, 31, 0.06);     /* Second close-light layer, creates the floating feel */
  aspect-ratio: 16 / 9;                  /* Uniform slide ratio */
  overflow: hidden;
}
.gallery-card img {
  width: 100%; height: 100%;
  object-fit: cover;
  border-radius: 9px;                    /* Slightly smaller than the card's radius, for visual nesting */
}
```

**Anti-example**: don't use edge-to-edge tiles (no padding, no border, no shadow); that's infographic-density expression, not an exhibition.

### 2. 3D tilted wall of work

```css
.gallery-viewport {
  position: absolute; inset: 0;
  overflow: hidden;
  perspective: 2400px;                   /* A deeper perspective, so the tilt isn't exaggerated */
  perspective-origin: 50% 45%;
}
.gallery-canvas {
  width: 4320px;                         /* Canvas = 2.25× viewport */
  height: 2520px;                        /* Leaves room to pan */
  transform-origin: center center;
  transform: perspective(2400px)
             rotateX(14deg)              /* Tilt backward */
             rotateY(-10deg)             /* Turn left */
             rotateZ(-2deg);             /* Slight tilt, removes excessive regularity */
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 40px;
  padding: 60px;
}
```

**Parameter sweet spot**:
- rotateX: 10-15deg (any more and it looks like a VIP backdrop at a cocktail party)
- rotateY: ±8-12deg (left-right symmetry)
- rotateZ: ±2-3deg (the human touch of "a machine didn't place this")
- perspective: 2000-2800px (below 2000 gets fisheye, above 3000 approaches orthographic projection)

### 3. 2×2 four-corner convergence (selection scenes)

```css
.grid22 {
  display: grid;
  grid-template-columns: repeat(2, 800px);
  gap: 56px 64px;
  align-items: start;
}
```

Each card slides in toward the center from its corresponding corner (tl/tr/bl/br) + fades in. The corresponding `cornerEntry` vectors:

```js
const cornerEntry = {
  tl: { dx: -700, dy: -500 },
  tr: { dx:  700, dy: -500 },
  bl: { dx: -700, dy:  500 },
  br: { dx:  700, dy:  500 },
};
```

---

## Five core animation patterns

### Pattern A · Four-corner convergence (0.8-1.2s)

4 elements slide in from the four corners of the viewport while scaling 0.85→1.0, with a matching ease-out. Suits an opening that "shows choices in several directions".

```js
const inP = easeOut(clampLerp(t, start, end));
card.style.transform = `translate3d(${(1-inP)*ce.dx}px, ${(1-inP)*ce.dy}px, 0) scale(${0.85 + 0.15*inP})`;
card.style.opacity = inP;
```

### Pattern B · Selected card enlarges + others slide out (0.8s)

The selected card scales up 1.0→1.28, while the other cards fade out + blur + drift back toward the corners:

```js
// Selected
card.style.transform = `translate3d(${cellDx*outP}px, ${cellDy*outP}px, 0) scale(${1 + 0.28*easeOut(zoomP)})`;
// Not selected
card.style.opacity = 1 - outP;
card.style.filter = `blur(${outP * 1.5}px)`;
```

**Key**: unselected cards should blur, not just fade. Blur simulates depth of field and visually "pushes out" the selected one.

### Pattern C · Ripple expansion (1.7s)

Outward from the center, delayed by distance, each card fades in in turn + scales from 1.25x down to 0.94x ("camera pulls out"):

```js
const col = i % COLS, row = Math.floor(i / COLS);
const dc = col - (COLS-1)/2, dr = row - (ROWS-1)/2;
const dist = Math.sqrt(dc*dc + dr*dr);
const delay = (dist / maxDist) * 0.8;
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
card.style.opacity = easeOut(Math.min(1, localT));

// At the same time, overall scale 1.25→0.94
const galleryScale = 1.25 - 0.31 * easeOut(rippleProgress);
```

### Pattern D · Sinusoidal Pan (continuous drift)

Combine a sine wave + linear drift to avoid the looping feel of a marquee that "has a start and an end":

```js
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;    // Horizontal drift to the left
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;    // Vertical drift upward
const clampedX = Math.max(-900, Math.min(900, panX));   // Prevent exposed edges
```

**Parameters**:
- Sine period `0.09-0.15 rad/s` (slow, about one swing every 30-50 seconds)
- Linear drift `5-8 px/s` (slower than a viewer's blink)
- Amplitude `120-220 px` (big enough to feel, small enough not to cause dizziness)

### Pattern E · Focus Overlay (focus switch)

**Key design**: the focus overlay is a **flat element** (not tilted) floating above the tilted canvas. The selected slide scales from its tile position (about 400×225) to the center of the screen (960×540); the background canvas's tilt doesn't change, but it **dims to 45%**:

```js
// Focus overlay (flat, centered)
focusOverlay.style.width = (startW + (endW - startW) * focusIntensity) + 'px';
focusOverlay.style.height = (startH + (endH - startH) * focusIntensity) + 'px';
focusOverlay.style.opacity = focusIntensity;

// Background cards dim but stay visible (key! don't mask 100%)
card.style.opacity = entryOp * (1 - 0.55 * focusIntensity);   // 1 → 0.45
card.style.filter = `brightness(${1 - 0.3 * focusIntensity})`;
```

**Iron rules of sharpness**:
- The focus overlay's `<img>` must have `src` pointing directly at the original image; **don't reuse the compressed thumbnails from the gallery**
- Preload all original images in advance into a `new Image()[]` array
- The overlay's own `width/height` is computed per frame, and the browser resamples the original image every frame

---

## Timeline architecture (reusable skeleton)

```js
const T = {
  DURATION: 25.0,
  s1_in: [0.0, 0.8],    s1_type: [1.0, 3.2],  s1_out: [3.5, 4.0],
  s2_in: [3.9, 5.1],    s2_hold: [5.1, 7.0],  s2_out: [7.0, 7.8],
  s3_hold: [7.8, 8.3],  s3_ripple: [8.3, 10.0],
  panStart: 8.6,
  focuses: [
    { start: 11.0, end: 12.7, idx: 2  },
    { start: 13.3, end: 15.0, idx: 3  },
    { start: 15.6, end: 17.3, idx: 10 },
    { start: 17.9, end: 19.6, idx: 16 },
  ],
  s4_walloff: [21.1, 21.8], s4_in: [21.8, 22.7], s4_hold: [23.7, 25.0],
};

// Core easing (the v9 historical implementation uses cubic; for new projects the main easing defaults to expoOut, see the correction in best-practices §2 / hero-case-study pattern 1)
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeInOut = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2;
function lerp(time, start, end, fromV, toV, easing) {
  if (time <= start) return fromV;
  if (time >= end) return toV;
  let p = (time - start) / (end - start);
  if (easing) p = easing(p);
  return fromV + (toV - fromV) * p;
}

// A single render(t) function reads the timestamp and writes every element
function render(t) { /* ... */ }
requestAnimationFrame(function tick(now) {
  const t = ((now - startMs) / 1000) % T.DURATION;
  render(t);
  requestAnimationFrame(tick);
});
```

**The essence of the architecture**: **all state is derived from the timestamp t**, with no state machine and no setTimeout. This means:
- `window.__setTime(12.3)` jumps instantly to any moment (handy for Playwright frame-by-frame capture)
- Looping is naturally seamless (t mod DURATION)
- You can freeze any frame while debugging

---

## Texture details (easy to overlook but fatal)

### 1. SVG noise texture

The biggest fear with a light background is "too flat". Overlay a very faint fractalNoise layer:

```html
<style>
.stage::before {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.078  0 0 0 0 0.078  0 0 0 0 0.074  0 0 0 0.035 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity: 0.5;
  pointer-events: none;
  z-index: 30;
}
</style>
```

It looks like it makes no difference; remove it and you'll see that it does.

### 2. Corner brand mark

```html
<div class="corner-brand">
  <div class="mark"></div>
  <div>HUASHU · DESIGN</div>
</div>
```

```css
.corner-brand {
  position: absolute; top: 48px; left: 72px;
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
}
```

Shown only in the wall-of-work scene, fading in and out. Like a museum wall label.

### 3. Brand closing wordmark

```css
.brand-wordmark {
  font-family: var(--sans);
  font-size: 148px;
  font-weight: 700;
  letter-spacing: -0.045em;   /* Negative tracking is key; it tightens the letters into a mark */
}
.brand-wordmark .accent {
  color: var(--accent);
  font-weight: 500;           /* The accent characters are actually a bit lighter, for visual contrast */
}
```

`letter-spacing: -0.045em` is the standard practice for large type on Apple product pages.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Looks like a PPT template | Cards have no shadow / hairline | Add two layers of box-shadow + a 1px border |
| The tilt feels cheap | Only rotateY, no rotateZ | Add ±2-3deg rotateZ to break the neatness |
| The pan feels "choppy" | Used setTimeout or a CSS keyframes loop | Use rAF + continuous sin/cos functions |
| Text is unreadable during focus | Reused the gallery tile's low-res image | Separate overlay + `src` pointing directly at the original |
| Background feels too empty | Solid `#F5F5F7` | Overlay SVG fractalNoise at 0.5 opacity |
| Type feels too "internet" | Only Inter | Add a serif (one Chinese, one English) + mono for three stacks |

---

## References

- Full implementation sample: hero-animation-v5.html (the author's local sample, not distributed with the repo)
- Original inspiration: the claude.ai/design hero video
- Reference aesthetics: Apple product pages, Dribbble shot collection pages

When you get an animation request where "many high-quality outputs need to be displayed", copy the skeleton straight from this file, then swap the content + tune the timing.
