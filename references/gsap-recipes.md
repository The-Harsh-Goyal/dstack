# GSAP Recipes · the translation layer from design language to GSAP Timeline

> This file does only one thing: it translates the animation design language huashu-design has already settled
> (the five-segment narrative, easing system, 8 rules of motion language and scene recipes in `animation-best-practices.md`,
> and the 22-second 5-scene template in `cinematic-patterns.md`) into ready-to-paste
> GSAP timeline implementation recipes, running on the HyperFrames rendering backend.
>
> **Design judgment follows this skill's own references; GSAP is only the implementation tool.**
> When to pause, which narrative arc to use, what counts as beautiful: read §0 of `animation-best-practices.md`;
> this file only answers "how do you write this rule in GSAP".
> For the HyperFrames composition contract (composition root attributes, `.clip` markers, render commands, check audit),
> see `references/hyperframes-backend.md`; this document only cites it and doesn't repeat it.

---

## 0 · Base boilerplate (every composition starts here)

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  const tl = gsap.timeline({
    paused: true,                                   // required. HyperFrames handles seeking
    defaults: { ease: "expo.out", duration: 0.6 },  // this skill's main easing (see §1)
  });

  // ... every tween hangs on this timeline ...

  window.__timelines["main"] = tl;  // the key must equal the composition root's data-composition-id
</script>
```

Hard constraints (violate any one and the render result is nondeterministic):

- The timeline must be `paused: true`; **never call `tl.play()`** for render-critical animation
- The timeline must be built in synchronous code, not inside async / timers / event callbacks
- Render duration comes from the composition root's `data-duration`, not the timeline length. Don't pad the length with empty tweens
- `repeat: -1` is forbidden. For looping motion, compute a finite repeat count from the visible duration
- Note: `defaults: { ease: "expo.out" }` differs from the `power3.out` house default in the hyperframes-animation docs.
  That's its taste; this skill's existing rule is
  "expoOut is the default main easing", and the translation layer follows our own design language

---

## 1 · Easing mapping table · in-house Easing → GSAP

The in-house Easing functions in `assets/animations.jsx`, each mapped to its GSAP form.
The first three are mathematically **exactly the same curve**, not approximations.

| In-house Easing | Mathematical definition | GSAP form | Relation | Use (existing rules) |
|---|---|---|---|---|
| `expoOut` | `1 - 2^(-10t)` | `"expo.out"` | Identical | **Default main easing**. Card rise-in, panel entrance, Terminal fade, focus overlay |
| `overshoot` | easeOutBack, c1=1.70158 | `"back.out"` (default 1.70158) or `"back.out(1.7)"` | Identical | Toggle switches, button pop-ups, emphasized interactions |
| `spring` | easeOutElastic, period 2π/3 | `"elastic.out(1, 0.3)"` (i.e. the default `"elastic.out"`) | Identical | Geometry settling into place, physical landing, UI wobble |
| `easeIn` | `t²` | `"power1.in"` | Identical | Exits, the Anticipation wind-up |
| `easeOut` | `1-(1-t)²` | `"power1.out"` | Identical | Light motion on secondary elements (caption fades, etc.) |
| `easeInOut` | quad inOut | `"power1.inOut"` | Identical | Sustained motion (symmetric motion like mouse path interpolation) |
| `linear` | `t` | `"none"` | Identical | Only for proxy driving / constant-speed camera motion. **Forbidden on element animation** |
| `anticipation` | Piecewise curve, dips to -0.3 first and then rises | No built-in equivalent; use a function ease (see below) |  | Entrances with a wind-up |

### 1.1 anticipation · function ease

GSAP accepts any `(p) => number` as an ease, so you can carry the in-house definition over as is:

```js
// matches Easing.anticipation in animations.jsx point for point
const anticipation = (t) => {
  if (t < 0.2) return -0.3 * (t / 0.2) * (t / 0.2);   // first 20%: reverse dip
  const a = (t - 0.2) / 0.8;
  return -0.012 + 1.012 * a * a * (3 - 2 * a);         // last 80%: smoothstep rise
};

tl.fromTo("#card", { y: 40 }, { y: 0, duration: 0.7, ease: anticipation }, "s2");
```

Note: this curve goes below 0 (the negative range), so **only use it on transforms** (y / scale / rotation),
not on opacity or colors (it would push them out of the valid range).

### 1.2 Another option for spring · baked springs (seek-safe real physics)

`"elastic.out(1, 0.3)"` is the exact equivalent of the in-house spring, and using it directly is fine.
When you want the feel of a real spring with **adjustable damping** (for example "barely any overshoot on landing, just a long tail"),
use the `springEase` closed-form solution provided by hyperframes-animation (`adapters/gsap-easing-and-stagger.md`
has the complete 40-line implementation; the closed-form solution is a pure function of time, so it's seek-safe):

```js
// dampingFraction 1.0 = steady landing with no overshoot; 0.6-0.7 ≈ the bounce of the in-house spring
const settle = springEase({ response: 0.4, dampingFraction: 0.65 });
tl.fromTo("#hero", { scale: 0 }, { scale: 1,
  duration: settle.duration, ease: settle.ease }, "s4");   // duration must be used with it; it's part of the physics
```

**Don't** bring in any real-time spring library (integrators like react-spring): state accumulates frame by frame and can't be seeked deterministically.

---

## 2 · Five-segment narrative skeleton · Slow-Fast-Boom-Stop (15/15/40/20/10%)

Why: animation with an even pace is a tech demo; only animation with rhythm is narrative (best-practices §1).

A labeled timeline skeleton template; change `D` to fit any total duration:

```js
const D = 15;   // total duration (seconds), kept consistent with the composition root's data-duration
const at = (p) => D * p;

const tl = gsap.timeline({
  paused: true,
  defaults: { ease: "expo.out", duration: 0.6 },
});

// ── five-segment labels, ratio 15 / 15 / 40 / 20 / 10 ──────────────────
tl.addLabel("s1_trigger",  at(0));     // slow · trigger: give humans time to react, establish realism
tl.addLabel("s2_generate", at(0.15));  // medium · generate: the visual wow moment appears
tl.addLabel("s3_process",  at(0.30));  // fast · process: show controllability/density/detail
tl.addLabel("s4_boom",     at(0.70));  // Boom · burst: pull back/3D pop-out/multi-panel emergence
tl.addLabel("s5_hold",     at(0.90));  // still · landing: Logo morph + abrupt stop

// ── S1 trigger (slow pace: a single action + plenty of white space) ─────────────────────
tl.fromTo("#terminal", { y: 48, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.8 }, "s1_trigger+=0.1");

// ── S2 generate (one clear wow moment, don't pile on actions) ─────────────────────
tl.fromTo("#result-panel", { scale: 0.92, autoAlpha: 0 },
  { scale: 1, autoAlpha: 1, duration: 0.7 }, "s2_generate");

// ── S3 process (highest density: stagger, typewriter and focus switches all go here) ──
tl.fromTo(".row", { y: 10, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.4, stagger: 0.03 }, "s3_process");

// ── S4 burst (camera-level action: pull back / rotationX / multi-element emergence) ───────
tl.to("#stage", { scale: 0.82, rotationX: 8, duration: 1.2,
  ease: "expo.inOut" }, "s4_boom");

// ── S5 landing (Logo morph to close, see §3.6; nothing happens after that) ────────
// the last ~0.5s is an intentional still hold: add no tweens, and never fade to black

window.__timelines["main"] = tl;
```

Key points:

- **White space after S5**: `data-duration` covers through to the end, but there are no tweens on the timeline,
  so the frame holds on the final frame. That's how the "abrupt stop" is implemented (fade-out endings are forbidden)
- The 22-second 5-scene template (cinematic-patterns Pattern B) has the same structure: swap the ratios for
  Invoke 3-4s / Process 5-6s / Insight 4-5s / Output 3-4s / Hero 4-5s, with labels done the same way
- Full-screen transitions between scenes use overlapping autoAlpha + displacement, not display switching
  (`display` / bare `visibility` are off-limits for the renderer; show/hide always uses `autoAlpha`)

---

## 3 · The 8 rules of motion language · translated one by one

### 3.1 No pure black or pure white backgrounds

Not a timeline rule: the background is static CSS, a neutral with color temperature, with specific values from the brand spec.
The only GSAP connection: when the background color changes between scenes, tween `backgroundColor` (it's on the allowed list),
and the two scenes' background colors should be in the same color family (the color consistency constraint in cinematic-patterns §2):

```js
tl.to("#stage", { backgroundColor: "#F4EFE6", duration: 0.8, ease: "sine.inOut" }, "s4_boom");
```

### 3.2 Easing is never linear

Why: `linear` makes digital elements feel like machines, while `expoOut` gives a sense of physical weight (best-practices §2).

Implementation: write `ease: "expo.out"` in the timeline `defaults` (see the §0 boilerplate),
and override individual tweens according to the §1 mapping table. `ease: "none"` may appear in only two places:
proxy-driven tweens (§7) and deliberately mechanical motion (constant-speed camera pans).

### 3.3 Slow-Fast-Boom-Stop

See the §2 skeleton; not repeated here.

### 3.4 Show the "process", not the "magic result"

Why: the product is a collaborator, not a magician; showing tweaks / error fixes / redlines counters the "one-click magic"
AI slop (best-practices §3.4).

The two most common "sense of process" recipes:

**Chunk Reveal (simulating streamed token output)**. The original recipe uses `setTimeout + Math.random`,
both of which are illegal under seek rendering. Translated into "precomputed timetable + proxy driving", it's safe for seeking in both directions:

```js
// why not tl.call(): callbacks aren't reversible, so dragging backwards in preview leaves leftover state
const rand = mulberry32(42);                              // seeded random, see §7.4
const text = "为你生成了三个候选方案，第一个最激进。";
const chunks = text.split(/(?=[，。、；])|(?<=[，。、；])/); // split Chinese into chunks at punctuation
const times = []; let acc = 0;
chunks.forEach(() => { acc += 0.04 + rand() * 0.08; times.push(acc); }); // irregular 40-120ms

const tw = { t: 0 };
tl.to(tw, {
  t: acc, duration: acc, ease: "none",
  onUpdate: () => {   // recompute the full visible text from t every frame: a pure function, correct even when dragged back
    let n = 0;
    while (n < times.length && times[n] <= tw.t) n++;
    document.querySelector("#stream").textContent = chunks.slice(0, n).join("");
  },
}, "s2_generate+=0.3");
```

**Number counter (showing real data going up)**:

```js
// snap guarantees integers; innerText is the counter form HyperFrames accepts
tl.fromTo("#metric", { innerText: 0 },
  { innerText: 237, snap: { innerText: 1 }, duration: 1.2, ease: "expo.out" }, "s3_process");
```

For thousands separators / suffix formatting, switch to a proxy + onUpdate (derive `toLocaleString` from `tw.v`); same pattern as above.

### 3.5 Mouse paths · arcs + hand tremor

Why: a mouse moving by straight-line interpolation feels subconsciously robotic; real people "accelerate, arc, decelerate and correct"
(best-practices §3.5).

A Bézier arc can't be expressed with an ordinary property tween, so use proxy driving. For hand tremor, don't use Perlin
(the original implementation relies on runtime noise); layer two sine waves with incommensurable frequencies instead, a deterministic equivalent:

```js
const mouse = { p: 0 };
const P0 = [100, 100];                       // start point
const P2 = [tx, ty];                          // end point (click target)
const P1 = [tx - 200, ty + 80];               // control point: off the midpoint, to create the arc

tl.to(mouse, {
  p: 1, duration: 1.1, ease: "power1.inOut",  // symmetric easing: accelerate on start + decelerate on arrival
  onUpdate: () => {
    const t = mouse.p;
    let x = (1-t)*(1-t)*P0[0] + 2*(1-t)*t*P1[0] + t*t*P2[0];
    let y = (1-t)*(1-t)*P0[1] + 2*(1-t)*t*P1[1] + t*t*P2[1];
    x += Math.sin(t * 47.13) * 2 * (1 - t);   // ±2px hand tremor, converging near the target
    y += Math.sin(t * 33.7 + 1.3) * 2 * (1 - t);
    gsap.set("#cursor", { x, y });            // everything derived from p, seek-safe
  },
}, "s1_trigger+=0.5");

// click feedback: Anticipation shrink, then bounce back
tl.to("#cursor", { scale: 0.85, duration: 0.08, ease: "power1.in" }, ">");
tl.to("#cursor", { scale: 1, duration: 0.25, ease: "back.out" }, ">");
```

### 3.6 Logo morph to close (Morph)

Why: a Logo fade-in has no sense of narrative closure; make the previous visual element "collapse" and then "expand" into the Logo,
so the narrative collapses onto the brand point (best-practices §3.6).

Blur goes through a CSS variable (`filter` is paint-only and seek-safe, the approach endorsed by the official depth-of-field-blur
rule):

```css
#lastVisual, #logo { --blur: 0px; filter: blur(var(--blur)); will-change: filter; }
```

```js
tl.addLabel("morph", "s5_hold-=0.3");

// collapse: the previous visual element shrinks into a color block, motion blur rises
tl.to("#lastVisual", { scale: 0.1, "--blur": "6px",
  duration: 0.5, ease: "expo.out" }, "morph");

// expand: the Logo pops out of the center of the color block, blur converges to sharp
tl.fromTo("#logo",
  { scale: 0.1, "--blur": "6px", autoAlpha: 0 },
  { scale: 1, "--blur": "0px", autoAlpha: 1, duration: 0.6, ease: "back.out" },
  "morph+=0.35");                              // overlap on the order of 150ms = quick cut

tl.to("#lastVisual", { autoAlpha: 0, duration: 0.15 }, "morph+=0.5");
// after that: hold, no tweens, abrupt stop
```

### 3.7 Serif + sans-serif dual fonts

Not a timeline rule: static CSS, with font choices from the brand spec.
The HyperFrames compiler automatically fetches Google Fonts and injects deterministic @font-face
(measured in Phase 0; the font timing pitfall of the in-house pipeline doesn't exist in the new backend), so just reference Google Fonts in CSS as usual.

### 3.8 Focus switch = background dims + foreground sharpens + Flash guide

Why: when you only lower opacity, unfocused elements are still sharp; you must add blur for them to truly recede into the background
(best-practices §3.8).

All three filters go through a CSS variable, and GSAP tweens the variable itself:

```css
.tile {
  --f: 0;   /* focusIntensity 0→1 */
  filter: brightness(calc(1 - 0.5 * var(--f)))
          saturate(calc(1 - 0.3 * var(--f)))
          blur(calc(var(--f) * 4px));          /* ← key: blur makes unfocused elements truly recede */
  will-change: filter;
}
```

```js
tl.addLabel("focus", "s3_process+=1.5");

// unfocused elements: three filters + dim done in one tween
tl.to(".tile:not(.focus-target)", {
  "--f": 1, opacity: 0.4, duration: 0.5, ease: "expo.out",
}, "focus");

// Flash highlight guides the eye back.
// note: the original recipe uses element.animate() (WAAPI), which runs on the wall clock and is nondeterministic under seeking, so it must be translated into a tween
tl.fromTo("#focusFlash",
  { backgroundColor: "rgba(255,255,255,0.3)" },
  { backgroundColor: "rgba(255,255,255,0)", duration: 0.15, ease: "power1.out" },
  "focus+=0.5");

// focus release: settle sharp. Before handing off to the next scene, blur must be brought back to 0;
// stopping in a half-blurred state reads to viewers as "the render has a bug"
tl.to(".tile", { "--f": 0, opacity: 1, duration: 0.5, ease: "power2.inOut" }, "focus+=2.5");
```

Performance constraints (from the official DoF rule): blur radius ≤24px on large elements; prefer "dim + moderate blur"
rather than maxing out the blur; add `will-change: filter` only to elements whose blur actually animates.

---

## 4 · Specific motion techniques · GSAP versions of the §4 code snippets

### 4.1 FLIP / Shared Element (a button expanding into an input box)

Why: it's the same element transitioning between two states, not two elements cross-fading (best-practices §4.1).

The original recipe uses Framer Motion's layoutId. On the GSAP side we don't bring in the Flip plugin (unverified under HyperFrames)
and compute it by hand instead: the composition's viewport is fixed (data-width/height), and the geometry of both states are design constants,
so just hard-code them with fromTo. All displacement and scaling go through transform, and the element stays in its final layout position:

```css
/* the element is laid out in its "end state"; the start state is expressed by transform */
#search-box { width: 560px; height: 56px; }   /* static end state, size is not tweened */
```

```js
// start-state geometry: button 120x44 at (400, 300), end-state input box 560x56 at (200, 300)
tl.fromTo("#search-box",
  { x: 200, y: 0, scaleX: 120/560, scaleY: 44/56, transformOrigin: "left top" },
  { x: 0,   y: 0, scaleX: 1, scaleY: 1, duration: 0.6, ease: "expo.out" },
  "s2_generate");
// inner text is counter-compensated or enters later, to avoid being stretched by scaleX (same handling as §4.2)
tl.fromTo("#search-box .placeholder", { autoAlpha: 0 },
  { autoAlpha: 1, duration: 0.3 }, "s2_generate+=0.4");
```

### 4.2 Breathing expansion (expand first, then fill)

Why: a panel shouldn't stretch width and height at the same time; expanding horizontally first and then vertically is what feels like the physical world
(best-practices §4.2).

The original recipe tweens width/height directly, which is off-limits in HyperFrames because of reflow (integer pixel snapping,
visible jitter in slow segments, §7.2). Translated into scaleX/scaleY, the time offset stays the same:

```js
// L = total expansion duration; the first 40% stretches horizontally, vertical starts at 30%, the two overlap
const L = 0.9;
tl.fromTo("#panel",
  { scaleX: 0, scaleY: 0.12, transformOrigin: "left top" },
  { scaleX: 1, duration: 0.4 * L, ease: "expo.out" }, "open");
tl.to("#panel", { scaleY: 1, duration: 0.7 * L, ease: "expo.out" }, "open+=" + 0.3 * L);

// content only surfaces after the shell has finished expanding: it fits the "expand first, then fill" image,
// and also hides the content's stretching and distortion during the scale
tl.fromTo("#panel .content", { autoAlpha: 0, y: 8 },
  { autoAlpha: 1, y: 0, duration: 0.35 }, "open+=" + 0.75 * L);
```

Note that the scale version isn't pixel-faithful (rounded corners and borders distort with the ratio). When the expanding shell is a solid-color / large-radius panel,
it's imperceptible; if the panel's border details matter, switch to a "fixed shell + content revealed with clip-path" approach and check captured frames.

### 4.3 Staggered Fade-up (30ms stagger)

Why: list items entering one by one feel more "physical" than the whole block appearing at once; 30ms is the established interval (best-practices §4.3).

```js
tl.fromTo(".row",
  { y: 10, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.4, ease: "expo.out", stagger: 0.03 },
  "s3_process");

// variant: emerging from the center outwards (common for the multi-panel emergence of the S4 burst)
tl.fromTo(".panel",
  { y: 24, autoAlpha: 0, scale: 0.96 },
  { y: 0, autoAlpha: 1, scale: 1, duration: 0.5, ease: "expo.out",
    stagger: { each: 0.03, from: "center" } },
  "s4_boom");
```

Use `fromTo`, not `from`: sub-compositions get re-seeked repeatedly, and `from` snapshots the start state at registration time,
which may be misaligned after dragging back; `fromTo` declares both ends explicitly and is always consistent.

### 4.4 Pause 0.5s before the key result

Why: machines execute fast and seamlessly, but the human brain needs reaction time; pausing 0.5 seconds before the key result is courtesy to the viewer
(best-practices §4.4, core belief no. 3 in §0.2).

In GSAP a "pause" is just a gap in the position parameter; use labels to write the pause as an explicit design decision:

```js
// the moment generation completes
tl.addLabel("generated", "s2_generate+=1.2");
// hold the loading state for 0.5s: no tweens during this 0.5s, while the viewer watches the loading state
tl.addLabel("reveal", "generated+=0.5");

tl.fromTo("#result", { scale: 0.94, autoAlpha: 0 },
  { scale: 1, autoAlpha: 1, duration: 0.7, ease: "expo.out" }, "reveal");
```

### 4.5 Anticipation → Action → Follow-through

Why: animation with only the Action is PowerPoint animation; Disney's three stages give motion life
(best-practices §4.6).

Three sequential tweens, with easing mapped per §1 (wind-up power1.in, action expo.out, rebound elastic):

```js
tl.addLabel("pop", "s2_generate+=0.2");
tl.to("#card", { scale: 0.95, duration: 0.12, ease: "power1.in"  }, "pop");        // wind-up
tl.to("#card", { scale: 1.05, duration: 0.30, ease: "expo.out"   }, ">");          // action
tl.to("#card", { scale: 1.00, duration: 0.35, ease: "elastic.out(1, 0.3)" }, ">"); // rebound
```

Single-tween version: `ease: anticipation` (§1.1) does "wind-up + action" in one step, then add one more segment for the rebound.

### 4.6 3D Perspective + translateZ layering

Why: rotateX 8° / rotateY -4° simulates the natural angle of a camera looking down from the top-left corner of a desk
(best-practices §4.7).

Perspective and layering are static CSS (copied from the original recipe; perspective / translateZ don't need to move);
the moving parts (standing up on entrance, the S4 pull-back) use GSAP's 3D transform aliases:

```css
.stage-wrap { perspective: 2400px; perspective-origin: 50% 30%; }
.card-grid  { transform-style: preserve-3d; }
.card:nth-child(3n) { transform: translateZ(30px); }
.card:nth-child(5n) { transform: translateZ(-20px); }
.card:nth-child(7n) { transform: translateZ(60px); }
```

```js
// entrance: slowly stand up from a front view to the golden angle
tl.fromTo("#card-grid", { rotationX: 0, rotationY: 0 },
  { rotationX: 8, rotationY: -4, duration: 1.4, ease: "expo.out" }, "s2_generate");
```

### 4.7 Diagonal Pan · move X and Y together, at different frequencies

Why: using different frequencies for X and Y keeps the Lissajous loop from becoming regular, simulating the diagonal drift of a handheld camera
(best-practices §4.8).

The original recipe computes `Math.sin(flowT * ...)` frame by frame; the GSAP version layers two yoyo tweens with different durations
(GSAP tracks x / y independently, so the two tweens don't fight). repeat must be finite:

```js
// different periods (4.6s vs 2.9s) = different frequencies, so the path doesn't close
// the repeat count is computed from the visible duration: Math.ceil(D / dur) guarantees coverage of the whole film
tl.to("#stage", { x: 40, duration: 4.6, ease: "sine.inOut",
  yoyo: true, repeat: Math.ceil(D / 4.6) }, 0);
tl.to("#stage", { y: 30, duration: 2.9, ease: "sine.inOut",
  yoyo: true, repeat: Math.ceil(D / 2.9) }, 0);
```

### 4.8 Abrupt-stop ending

Why: a fade-out has no sense of decision; the last frame should be clear and assertive (best-practices §0.3 white space).

In implementation it's "write no code": after the S5 Logo lands, there are no more tweens on the timeline,
`data-duration` is 0.5-1s longer than the end of the last tween, and the frame holds on the end state.
If there's BGM, fade the sound out at the tail with a volume tween (volume is on the allowed list):

```js
tl.to("#bgm", { volume: 0, duration: 0.4 }, "s5_hold+=0.8");  // the audio cuts off, the frame doesn't move
```

---

## 5 · Scene recipes A/B/C · timeline structure essentials

For design judgment (which one to choose, SFX density, BGM style), see best-practices §5; here we only give the differences on the timeline side.

### Recipe A · Apple Keynote dramatic style

- Skeleton: the §2 five-segment structure as is, with the S4 Boom done in full
- defaults: `ease: "expo.out"`, overridden with `"back.out"` on emphasized interactions
- S4 signature move: a sharp camera pull-back + drop. `tl.to("#stage", { scale: 0.78, y: -40, duration: 1.1, ease: "expo.inOut" }, "s4_boom")`
- S5: Logo Morph (§3.6) + an ethereal single tone + hold

### Recipe B · single-take tool style

- Skeleton: **don't** use the five-segment peak structure; one continuous flow. Place labels on BGM bars:
  `tl.addLabel("bar1", 0); tl.addLabel("bar2", 60/88*4);` (88 BPM, one bar ≈ 2.73s)
- Write the position parameters of key UI actions directly on the kick/snare moments, so the music's groove serves as the interaction sound effects
- easing: `springEase` (§1.2) + `"expo.out"`, more a sense of settling than of bursting
- No S4-style Boom; the ending is also an abrupt stop

### Recipe C · productivity narrative style

- Skeleton: hard cuts between multiple scenes. One label per scene, with quick autoAlpha cuts between scenes (0.15s)
  rather than long overlaps; paired with Dolly In/Out:
  `tl.fromTo("#scene2", { scale: 1.06 }, { scale: 1, duration: 1.2, ease: "expo.out" }, "sc2")`
- Toggle-type interactions always use `"back.out"`, panels always use `"expo.out"`
- The film must have one highlight: a 3D pop-out (the rotationX + translateZ element rising from §4.6),
  done only once; showing off everywhere is a cheap signal (§0.3 restraint)

---

## 6 · Seek safety rules (measured in Phase 0, every one of them hit)

HyperFrames rendering is frame-by-frame seek + screenshot. Any state that isn't "a pure function of time" will produce nondeterministic results
in the render, and **it often looks fine in preview**; only the rendered output exposes it.

### 6.1 No CSS transition + class switching · always express it with a tween

CSS transitions run on the browser's wall clock, not the timeline. When seeking frame by frame, every frame is a "sudden state change",
so the transition either doesn't fire or starts from the wrong point; this bit us in practice when migrating c3 in Phase 0.

```css
/* ✗ old way: classList.add('lit') in JS, relying on a transition */
.capsule { transition: transform 0.3s ease; }
.capsule.lit { transform: scale(1.06); }
```

```js
// ✓ new way: the state change itself is a tween on the timeline
tl.to("#capsule", { scale: 1.06, duration: 0.3, ease: "expo.out" }, "lit_at");
tl.to("#capsule", { scale: 1.0,  duration: 0.3, ease: "expo.out" }, "lit_at+=1.2");
```

Similar off-limits areas: `element.animate()` (WAAPI, also on the wall clock; the Flash in §3.8 already gives the translation),
and CSS `@keyframes` animation used for render-critical animation.
Scan before delivery: `grep -n "transition:\|animation:\|\.animate(" index.html`;
every hit must either be deleted or translated into a tween.

### 6.2 Don't animate properties that trigger reflow · use transform instead

Layout properties snap to integer device pixels in the browser's layout phase. You can't see it in fast tweens;
on the tail of a slow ease-out, where each frame moves less than 1px, it "holds for a few frames, then jumps 1px", a visible jitter.
The Phase 0 lint caught letterSpacing jittering frame by frame on the spot, exactly this kind of visual bug that raises no alarm.

| ✗ Don't tween | ✓ Faithful replacement |
|---|---|
| `width` / `height` | `scaleX` / `scaleY` + `transformOrigin` (see §4.2 for handling content) |
| `top` / `left` / `right` / `bottom` | The element stays at its CSS end position; tween the `x` / `y` offset |
| `fontSize` | `scale` (visually equivalent, sub-pixel smooth) |
| `letterSpacing` / `wordSpacing` | Split per character, then tween each character's `x` (uniform scale isn't the same effect; it scales glyphs, not spacing) |
| `margin*` / `padding*` | Hard-code the layout, animate `x` / `y` |

Fix principle: **reproduce the same visual, just without the jitter**. Passing lint isn't the standard; comparing frame by frame against the original animation is.

### 6.3 onUpdate doesn't fire at t=0 · proxy tweens must draw the first frame manually

When the timeline seeks to 0, a proxy tween's `onUpdate` may not fire, so the first frame is a blank screen / the initial DOM.
For every proxy-driven scene (§3.4 chunk reveal, §3.5 mouse, §7 old demo adapter),
call it once manually after registering the timeline:

```js
window.__timelines["main"] = tl;
render(0);   // first-frame insurance: draw the t=0 frame explicitly
```

### 6.4 No Math.random / Date.now · use a seeded function for randomness

Every seek to the same frame must produce the same image. Runtime randomness = different every render = frame-by-frame rendering is impossible.
When you need "a sense of randomness" (particles, jitter, irregular intervals), use mulberry32 and generate all random values **before building the timeline**,
in one go (the approach measured in the Phase 0 3D particle demo):

```js
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(20260717);   // seed hard-coded; changing the seed = a different version of randomness

// usage: pre-generate, don't draw on the spot in onUpdate
const offsets = Array.from({ length: 40 }, () => (rand() - 0.5) * 24);
```

Likewise forbidden: `Date.now()`, `performance.now()`, and any event-driven state (render mode has no input events).

---

## 7 · Old demo adapter recipe · hooking render(t) into GSAP

The animation core of all 21 old in-house-engine demos is a `render(t)` pure function. Migration doesn't rewrite the animation logic;
a proxy tween hooks render(t) onto the GSAP timeline (measured in Phase 0: 20-30 minutes per demo,
not one line of animation code changed, verified on the 1,134-line c3 cinematic demo).

### 7.1 Proxy tween template (12 lines, the original measured on c3)

```js
// =============== HyperFrames adapter ===============
// a proxy tween drives the original render(t). Every frame is a pure function of timeline time:
// no rAF, no clock, no input state.
window.__timelines = window.__timelines || {};
const proxy = { t: 0 };
const tl = gsap.timeline({ paused: true });
tl.to(proxy, {
  t: T.DURATION,            // the old demo's total duration constant
  duration: T.DURATION,
  ease: "none",             // time must map at a constant rate; easing lives inside render(t)
  onUpdate: () => render(proxy.t),
}, 0);
window.__timelines["main"] = tl;

// first-frame insurance (onUpdate doesn't fire when the timeline is stopped at t=0, §6.3)
render(0);
```

### 7.2 Four migration steps

1. **Wrap root / clip**: add the composition root attributes to the outermost container
   (`data-composition-id="main"` + `data-duration` + dimensions),
   and add `.clip` and `data-start` / `data-duration` / `data-track-index` to stage elements.
   For the full contract, see `hyperframes-backend.md`
2. **Remove self-driving**: delete the rAF loop, `setInterval`, auto-play logic and
   the `performance.now()` start point. `render(t)` only takes the parameter t and no longer looks up the time itself
3. **Hook up the proxy**: paste the §7.1 template, match `T.DURATION` to `data-duration`, and end with `render(0)`
4. **Scan for transitions**: `grep -n "transition:\|animation:\|\.animate(\|Math.random\|Date.now\|performance.now"`
   and clear them one by one. Turn class-switching effects into pure functions of t per §6.1 (the most common leftover in old demos
   is the "classList.add + transition" combination)

After migrating, run `npx hyperframes check` once (use `--no-contrast` for dark cinematic pieces;
the other four gates must have 0 errors), then capture frames at 3-4 key moments and compare them with the old version.

### 7.3 When not to use the adapter

The adapter is a **migration for existing work**. Newly written animation should use the native timeline approach in §0-§5 of this file directly:
labels are readable, staggers are declarative, and the GSAP inspector can check tween by tween,
whereas animation inside the big proxy black box is opaque to audit tools.

---

## 8 · Pre-delivery self-check (GSAP side, supplementing the best-practices §7 checklist)

- [ ] Timeline is `paused: true`, and the registered key equals `data-composition-id`?
- [ ] defaults is `expo.out`, with no bare `linear` / `ease` appearing on element animation?
- [ ] All five segment labels are present, with a hold of white space after S5 (no fade out)?
- [ ] `grep "transition:\|\.animate(\|Math.random\|Date.now"` returns 0 results?
- [ ] No tweens on width / height / top / left / letterSpacing / fontSize?
- [ ] Every `repeat` is a finite number?
- [ ] Proxy scenes end with `render(0)`?
- [ ] All blur / filter go through CSS variables, and elements whose blur animates have `will-change: filter`?
- [ ] Entrances inside sub-compositions all use `fromTo`, not `from`?
- [ ] `npx hyperframes check` passes (`--no-contrast` for dark pieces, 0 errors otherwise)?

---

## 9 · Camera Rig recipe · the implementation layer for camera motion

Why: camera motion and element animation fighting over the same transform is the technical root of messy camera work
(camera-language.md §3). All camera-level tweens are funneled into a dedicated rig container,
camera state is carried by one proxy object, and every frame derives all camera DOM state from it, seek-safe.

### 9.1 Rig container structure (static skeleton)

```html
<div id="viewport">                <!-- fixed viewport -->
  <div id="camera">                <!-- camera layer: only camera transforms -->
    <div id="world">...</div>      <!-- world layer: element animation happens only in here -->
  </div>
  <div id="hud">...</div>          <!-- subtitles/corner labels: a sibling of #camera, naturally still -->
</div>
```

```css
#viewport { position: relative; width: 1920px; height: 1080px; overflow: hidden; }
#camera   { position: absolute; inset: 0; perspective-origin: 960px 540px; }
#world    { position: absolute; transform-origin: 0 0; will-change: transform; }
/* insurance against edges showing during pans: #world size ≥ viewport + maximum pan amplitude + 8% margin (camera-language §3.3) */
```

### 9.2 Camera proxy + PageCam keyframe translation

The camera is a plain object; GSAP tweens its fields, and `onUpdate` writes the state into the DOM.
Everything derives from cam, so it's correct even when dragged back (the same proxy idea as the §3.4 chunk reveal):

```js
const cam = { cx: 960, cy: 540, zoom: 1, rotX: 0, rotY: 0, rotZ: 0, persp: 1200 };
const camEl = document.querySelector("#camera");
const world = document.querySelector("#world");

// ── flat mode (pure zoom + pan, no rotation) ──────────────────────────
function applyCam() {
  world.style.transform =
    `translate(${960 - cam.cx * cam.zoom}px, ${540 - cam.cy * cam.zoom}px) scale(${cam.zoom})`;
  applyCounter();
}

// ── 3D mode (with rotX/rotY/rotZ) · magnification uses the CSS zoom property, not scale ──
// layout-level scaling makes Chromium rasterize at the magnified size, which cures blurry text in 3D
// (camera-language §3.4, the most expensive knowledge in the whole library). zoom changes the coordinate system, so translate must be divided by zoom.
function applyCam3d() {
  camEl.style.perspective = `${cam.persp * cam.zoom}px`;
  world.style.zoom = cam.zoom;
  world.style.transformOrigin = `${cam.cx}px ${cam.cy}px`;
  world.style.transform =
    `translate(${960 / cam.zoom - cam.cx}px, ${540 / cam.zoom - cam.cy}px)` +
    ` rotateY(${cam.rotY}deg) rotateX(${cam.rotX}deg) rotateZ(${cam.rotZ}deg)`;
  applyCounter();
}
```

Note: CSS `zoom` triggers re-layout every frame, and it's the **only legitimate exception** to the §6.2 reflow ban,
allowed only on the `#world` camera layer. Under HyperFrames / Playwright offline frame-by-frame rendering, per-frame cost doesn't affect the output;
dropped frames in real-time preview are normal, and the rendered output is what counts.

### 9.3 Logarithmic duration helper (fixed durations are where the amateur feel comes from)

```js
// camera-language §4.2: 1→2x is exactly 0.55s, so zooms of any magnitude have the same visual speed
function zoomDur(z1, z2) {
  return gsap.utils.clamp(0.30, 0.94,
    0.55 * Math.abs(Math.log(z2 / z1)) / Math.LN2);
}
```

### 9.4 Writing camera passages (push in → hold → pan → final-bow pull-out)

All camera tweens drive cam, with easing per camera-language §4.1:
active push/pull uses `power3.inOut`, follow-style uses `cubic-bezier(0.33,0,0.15,1)` (custom ease below).

```js
const followEase = gsap.parseEase("0.33,0,0.15,1");   // shotcraft camera default

// establishing micro-push: start at 1.06x, ease out back to the wide shot over 3s (only add it when the film is >14s and the first shot >7s)
tl.fromTo(cam, { zoom: 1.06 },
  { zoom: 1, duration: 3.0, ease: "power2.out", onUpdate: applyCam }, 0);

// push in to a close-up: target point (1240, 430), 1 → 1.8x, duration given by the formula
tl.to(cam, { cx: 1240, cy: 430, zoom: 1.8,
  duration: zoomDur(1, 1.8), ease: "power3.inOut", onUpdate: applyCam },
  "s2_generate");
// once the camera is in position, hold ≥1.2s before moving on (writing no tween is the hold)

// mid-distance focus shift: don't return to 1x, pan straight over (shot-to-shot grammar: 0.22-0.45 switch to a pan)
tl.to(cam, { cx: 880, cy: 620,
  duration: 0.7, ease: followEase, onUpdate: applyCam }, "s3_process+=1.5");

// final bow: 0.55s pull-out + ≥0.8s wide-shot pause, with data-duration covering through to the end of the pause
tl.to(cam, { cx: 960, cy: 540, zoom: 1,
  duration: 0.55, ease: "power3.inOut", onUpdate: applyCam }, "s5_hold");

window.__timelines["main"] = tl;
applyCam();   // first-frame insurance: onUpdate doesn't fire when the timeline is stopped at t=0 (§6.3)
```

The camera budget isn't written in the code; it's set when planning shots: tween start points of adjacent camera moves ≥2.6s apart,
≤4-5 per 15s window, and no zooms of <1.25x (camera-language §0/§4.4).

### 9.5 counter-transform · keeping the font size of follow-along subtitles/labels constant

Subtitles and chrome should preferably go in `#hud` (doesn't follow the camera, zero cost). For labels that must sit inside world,
follow an element, yet keep a constant font size, counteract the camera zoom in reverse:

```js
const counters = gsap.utils.toArray(".cam-counter");   // labels that need a constant font size
function applyCounter() {
  const inv = 1 / cam.zoom;
  counters.forEach((el) => { el.style.transform = `scale(${inv})`; });
}
```

Write `.cam-counter`'s own entrance animation on its **child elements**, to avoid fighting the counter scale over transform.

### 9.6 Multi-layer parallax · all derived from cam

Don't give each layer its own tween; multiply the same camera displacement by a speed coefficient (coefficient ratio between layers ≥2x, ≤4 layers,
camera-language §8.1), which is naturally synchronized and naturally seek-safe:

```js
const LAYERS = [
  { el: document.querySelector("#bg"),  k: 0.35 },
  { el: document.querySelector("#mid"), k: 0.7  },
  { el: document.querySelector("#fg"),  k: 1.4  },
];
function applyParallax() {
  const dx = 960 - cam.cx, dy = 540 - cam.cy;    // camera displacement
  LAYERS.forEach(({ el, k }) => {
    el.style.transform = `translate(${dx * k}px, ${dy * k}px)`;
  });
}
// just append applyParallax() to the end of applyCam()
```

### 9.7 Camera Rig self-check (append to the §8 checklist)

- [ ] Camera tweens only move the cam proxy, and no element inside `#world` has been touched by a camera tween?
- [ ] `applyCam()` was called for the first frame after registering the timeline?
- [ ] 3D text close-ups use CSS `zoom`, with no blurry `scale()` magnification?
- [ ] The `zoom` property appears only on `#world` (the reflow exception doesn't spread)?
- [ ] All push/pull durations come from `zoomDur()`, with no hand-written constants?
- [ ] After the final-bow pull-out there's a ≥0.8s wide-shot hold with no tweens?
