# Gallery Ripple + Multi-Focus · a philosophy of scene choreography

> **A reusable visual choreography structure** distilled from the upstream hero animation v9 (25 seconds, 8 scenes).
> Not an animation production pipeline, but **in which situations this choreography is "right"**.
> Real-world reference: the upstream v9 render (`hero-animation-v9.mp4`, not distributed with dstack); the current source is [demos/hero-animation-v10.html](../demos/hero-animation-v10.html).

## The one-line version

> **When you have 20+ homogeneous visual assets and the scene needs to "convey scale and depth", reach for the Gallery Ripple + Multi-Focus choreography first, instead of piling up layouts.**

Generic SaaS feature animations, product launches, skill promos, series portfolio showcases: as long as there are enough assets and the style is consistent, this structure almost always works.

---

## What this technique is actually saying

It isn't "showing off assets"; it tells a story through **two rhythm changes**:

**Beat one · Ripple unfold (~1.5s)**: 48 cards spread out from the center, and the viewer is stunned by the "quantity": "oh, this thing produces this much".

**Beat two · Multi-Focus (~8s, 4 cycles)**: while the camera pans slowly, it dims + desaturates the background 4 times and enlarges one card on its own to the center of the screen. The viewer switches from "the impact of quantity" to "gazing at quality", at a steady 1.7s each time.

**Core narrative structure**: **scale (Ripple) → gaze (Focus × 4) → fade out (Walloff)**. Together these three beats express "Breadth × Depth": not only can it make a lot, but each one is also worth stopping to look at.

Compare the counterexamples:

| Approach | What the viewer perceives |
|------|---------|
| 48 cards arranged statically (no Ripple) | Nice-looking but no narrative, like a grid screenshot |
| Fast cuts one by one (no Gallery context) | Like a slideshow, losing the "sense of scale" |
| Ripple only, no Focus | Stunning, but nobody remembers any specific card |
| **Ripple + Focus × 4 (this recipe)** | **First awed by quantity, then gazing at quality, finally a calm fade out: a complete emotional arc** |

---

## Preconditions (all must be met)

This choreography **is not a cure-all**; all 4 of the following are required:

1. **Asset count ≥ 20, ideally 30+**
   With fewer than 20, the Ripple looks "empty"; it only feels dense when every one of the 48 cells is moving. v9 used 48 cells × 32 images (filled cyclically).

2. **Assets share a consistent visual style**
   All 16:9 slide previews / all app screenshots / all cover designs: aspect ratio, tone and layout have to look like "a set". A mix makes the Gallery look like a clipboard.

3. **Assets still carry readable information when enlarged individually**
   Focus enlarges a card to 960px wide; if the original gets blurry or is thin on information when enlarged, the Focus beat is wasted. Reverse check: can you pick 4 of the 48 as the "most representative"? If you can't, the asset quality is uneven.

4. **The scene itself is landscape or square, not vertical**
   The Gallery's 3D tilt (`rotateX(14deg) rotateY(-10deg)`) needs horizontal extension; in vertical format the tilt looks narrow and awkward.

**Fallback paths when a condition is missing**:

| What's missing | Fall back to |
|-------|-----------|
| Assets < 20 | Switch to "3-5 shown side by side statically + focus one at a time" |
| Inconsistent style | Switch to a keynote style of "cover + 3 large chapter images" |
| Thin information | Switch to a "data-driven dashboard" or "key quote + big type" |
| Vertical scene | Switch to "vertical scroll + sticky cards" |

---

## Technical recipe (v9 production parameters)

### 4-Layer structure

```
viewport (1920×1080, perspective: 2400px)
  └─ canvas (4320×2520, oversized overflow) → 3D tilt + pan
      └─ 8×6 grid = 48 cards (gap 40px, padding 60px)
          └─ img (16:9, border-radius 9px)
      └─ focus-overlay (absolute center, z-index 40)
          └─ img (matches selected slide)
```

**Key point**: the canvas is 2.25 times larger than the viewport, so the pan feels like "peeking into a larger world".

### Ripple unfold (distance-delay algorithm)

```js
// each card's entry time = distance from center × 0.8s delay
const col = i % 8, row = Math.floor(i / 8);
const dc = col - 3.5, dr = row - 2.5;       // offset to the center
const dist = Math.hypot(dc, dr);
const maxDist = Math.hypot(3.5, 2.5);
const delay = (dist / maxDist) * 0.8;       // 0 → 0.8s
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
const opacity = expoOut(Math.min(1, localT));
```

**Core parameters**:
- Total duration 1.7s (`T.s3_ripple: [8.3, 10.0]`)
- Maximum delay 0.8s (center appears first, corners last)
- Each card's entry takes 0.7s
- Easing: `expoOut` (explosive, not smooth)

**At the same time**: canvas scale goes from 1.25 → 0.94 (zoom out to reveal), a synchronized pulling-back feel that accompanies the appearance.

### Multi-Focus (4 beats)

```js
T.focuses = [
  { start: 11.0, end: 12.7, idx: 2  },  // 1.7s
  { start: 13.3, end: 15.0, idx: 3  },  // 1.7s
  { start: 15.6, end: 17.3, idx: 10 },  // 1.7s
  { start: 17.9, end: 19.6, idx: 16 },  // 1.7s
];
```

**Rhythm pattern**: each focus is 1.7s, with a 0.6s breather in between. 8s in total (11.0–19.6s).

**Inside each focus**:
- In ramp: 0.4s (`expoOut`)
- Hold: 0.9s in the middle (`focusIntensity = 1`)
- Out ramp: 0.4s (`easeOut`)

**Background change (this is the key)**:

```js
if (focusIntensity > 0) {
  const dimOp = entryOp * (1 - 0.6 * focusIntensity);  // dim to 40%
  const brt = 1 - 0.32 * focusIntensity;                // brightness 68%
  const sat = 1 - 0.35 * focusIntensity;                // saturate 65%
  card.style.filter = `brightness(${brt}) saturate(${sat})`;
}
```

**Not just opacity: desaturate + darken at the same time**. This makes the foreground overlay's colors "pop out" instead of just "getting a bit brighter".

**Focus overlay size animation**:
- From 400×225 (entry) → 960×540 (hold state)
- Surrounded by 3 layers of shadow + a 3px accent-colored outline ring, giving a "framed" feeling

### Pan (continuous motion keeps stillness from being boring)

```js
const panT = Math.max(0, t - 8.6);
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;
```

- Two layers of motion, sine wave + linear drift: not a pure loop, so the position is different at every moment
- Different X/Y frequencies (0.12 vs 0.09) keep the eye from spotting a "regular loop"
- Clamped at ±900/500px to keep it from drifting out

**Why not a pure linear pan**: with pure linear motion the viewer "predicts" where it'll be next second; sine + drift makes every second new, and under the 3D tilt it creates a "slight seasickness" (the good kind) that holds attention.

---

## 5 reusable patterns (distilled from the v6→v9 iterations)

### 1. **expoOut as the main easing, not cubicOut**

`easeOut = 1 - (1-t)³` (smooth) vs `expoOut = 1 - 2^(-10t)` (bursts, then converges quickly).

**Why**: expoOut reaches 90% within the first 30%, more like physical damping, matching the intuition of "something heavy landing". Especially good for:
- Card entry (weight)
- Ripple spread (shockwave)
- Brand rising (settling)

**When to still use cubicOut**: the focus out ramp, symmetric micro-motion.

### 2. **Paper-feel background + terracotta orange accent (Anthropic lineage)**

> This is the brand choice for this skill's own hero animation (a Claude-ecosystem subject); **don't carry it over to other subjects as a default**. What transfers is the method of "one accent tying together every visual anchor", not these two color values.

```css
--bg: #F7F4EE;        /* warm paper */
--ink: #1D1D1F;       /* almost black */
--accent: #D97757;    /* terracotta orange */
--hairline: #E4DED2;  /* warm hairlines */
```

**Why**: a warm background still "breathes" after GIF compression, unlike pure white, which feels "screen-like". Terracotta orange as the only accent runs through the terminal prompt, the selected dir-card, the cursor, the brand hyphen and the focus ring: every visual anchor is tied together by this one color.

**v5 lesson**: a noise overlay was added to simulate "paper grain", and GIF frame compression broke down completely (every frame was different). v6 switched to "background color + warm shadows only", keeping 90% of the paper feel and shrinking the GIF by 60%.

### 3. **Two shadow levels simulate depth, no real 3D**

```css
.gallery-card.depth-near { box-shadow: 0 32px 80px -22px rgba(60,40,20,0.22), ... }
.gallery-card.depth-far  { box-shadow: 0 14px 40px -16px rgba(60,40,20,0.10), ... }
```

A deterministic `sin(i × 1.7) + cos(i × 0.73)` algorithm assigns each card one of three shadow levels, near/mid/far. **Visually it feels like "3D stacking", but the transform doesn't change at all from frame to frame, so GPU cost is 0**.

**The cost of real 3D**: each card gets its own `translateZ`, and the GPU computes 48 transforms + shadow blurs every frame. v4 tried it, and Playwright struggled to record even 25fps. v6's two shadow levels look <5% different to the eye, but cost 10 times less.

### 4. **Weight changes (font-variation-settings) feel more cinematic than size changes**

```js
const wght = 100 + (700 - 100) * morphP;  // 100 → 700 over 0.9s
wordmark.style.fontVariationSettings = `"wght" ${wght.toFixed(0)}`;
```

The brand wordmark transitions from Thin → Bold over 0.9s, together with a slight letter-spacing adjustment (-0.045 → -0.048em).

**Why it's better than scaling up and down**:
- Viewers have seen too much scaling; their expectations are fixed
- A weight change is "filling out from within", like a balloon being blown up, rather than "being pushed closer"
- Variable fonts only became widespread in 2020+, so viewers subconsciously read them as "modern"

**Limitation**: you must use a font that supports variable fonts (Inter/Roboto Flex/Recursive etc.). Ordinary static fonts can only imitate it (switching between a few fixed weights causes jumps).

### 5. **Corner Brand: a low-intensity persistent signature**

During the Gallery phase there's a small `DSTACK` mark in the top-left corner, at 16% opacity, 12px font size, wide letter spacing.

**Why add it**:
- After the Ripple burst, viewers easily "lose focus" and forget what they're watching; a light mark in the top-left helps anchor them
- More refined than a big full-screen logo; people who do branding know a brand signature doesn't need to shout
- It still leaves an attribution signal when the GIF is screenshotted and shared

**Rule**: it appears only in the middle section (when the frame is busy); off at the opening (so it doesn't cover the terminal), off at the end (the brand reveal is the star).

---

## Counterexamples: when not to use this choreography

**❌ Product demos (that need to show features)**: the Gallery makes every card flash past, and viewers can't remember any single feature. Switch to "single-screen focus + tooltip annotations".

**❌ Data-driven content**: viewers need to read numbers, and the Gallery's fast rhythm gives them no time. Switch to "data charts + item-by-item reveal".

**❌ Storytelling**: the Gallery is a "parallel" structure, and stories need "cause and effect". Switch to keynote-style chapter transitions.

**❌ Only 3-5 assets**: the Ripple isn't dense enough and looks like "patches". Switch to "static arrangement + highlight one at a time".

**❌ Vertical (9:16)**: the 3D tilt needs horizontal extension; in vertical format the tilt feels "crooked" rather than "unfolding".

---

## How to tell whether your task suits this choreography

A quick three-step check:

**Step 1 · Asset count**: count how many visual assets of the same kind you have. < 15 → stop; 15-25 → make do; 25+ → use it directly.

**Step 2 · Consistency test**: put 4 random assets side by side; do they look like "a set"? If not → unify the style first, or change the plan.

**Step 3 · Narrative match**: are you expressing "Breadth × Depth" (quantity × quality)? Or a "process", "features", a "story"? If it's not the former, don't force it.

If all three are yes, fork the v6 HTML directly; change the `SLIDE_FILES` array and the timeline and you can reuse it. Change the palette via `--bg / --accent / --ink`: a new skin on the same skeleton.

---

## Related references

- Full technical workflow: [references/animations.md](animations.md) · [references/animation-best-practices.md](animation-best-practices.md)
- Animation export pipeline: [references/video-export.md](video-export.md)
- Audio setup (BGM + SFX dual track): [references/audio-design-rules.md](audio-design-rules.md)
- A parallel reference for the Apple gallery style: [references/apple-gallery-showcase.md](apple-gallery-showcase.md)
