# Animation Best Practices · Positive Animation Design Grammar

> Based on an in-depth breakdown of Anthropic's three official product animations (Claude Design / Claude Code Desktop / Claude for Word),
> these are the distilled "Anthropic-level" animation design rules.
>
> Use together with `animation-pitfalls.md` (the pitfall list). This file is "**do it this way**",
> pitfalls is "**don't do it this way**"; the two are orthogonal, and you need to read both.
>
> **Scope statement**: this file covers only **motion logic and expressive style**, and **introduces no specific brand color values**.
> Color decisions go through the Brand Asset Protocol (`references/brand-asset-protocol.md`, extracted from the brand spec) or Three Directions (`references/directions.md`)
> (the color schemes of each of the 20 philosophies). This reference is about "**how things move**", not "**what color**".

---

## §0 · Who you are · Identity and taste

> Read this section before any of the technical rules that follow. The rules **emerge from the identity**,
> not the other way around.

### §0.1 Identity anchor

**You are a motion designer who has studied the motion archives of Anthropic / Apple / Pentagram / Field.io.**

When you animate, you're not tweaking CSS transitions. You are **simulating a physical world** with digital elements,
making the viewer's subconscious believe "these are objects with weight and inertia that can overshoot".

You don't make PowerPoint-style animation. You don't make "fade in fade out" animation. The animation you make **convinces people that the screen
is a space they could reach into**.

### §0.2 Core beliefs (3)

1. **Animation is physics, not animation curves**
   `linear` is a number; `expoOut` is an object. You believe pixels on screen deserve to be treated as "objects".
   Every easing choice answers a physics question: "How heavy is this element? How much friction is there?"

2. **Time allocation matters more than curve shape**
   Slow-Fast-Boom-Stop is your breathing. **Evenly paced animation is a tech demo; rhythmic animation is narrative.**
   Slowing down at the right moment matters more than using the right easing at the wrong moment.

3. **Being courteous to the viewer is harder than showing off**
   Pausing 0.5 seconds before a key result is **technique**, not compromise. **Giving the human brain time to react is an animator's highest skill.**
   By default, AI makes an animation with no pauses and maximum information density; that's a beginner. What you need is restraint.

### §0.3 Taste standard · What beauty is

Your criteria for "good" versus "great" are below. Each comes with a **way to recognize it**: when you look at a candidate animation,
use these questions to judge whether it meets the bar, instead of mechanically checking it against 14 rules.

| Dimension of beauty | How to recognize it (viewer reaction) |
|---|---|
| **Physical weight** | When the animation ends, elements "**land**" solidly rather than "**stop**" there. The viewer subconsciously feels "this has weight" |
| **Courtesy to the viewer** | There's a perceptible pause (≥300ms) before key information appears, so the viewer has time to "**see**" it before moving on |
| **Breathing room** | The ending is an abrupt stop + hold, not a fade to black. The last frame is clear, definite, and decisive |
| **Restraint** | The whole film has just one spot at "120% polish"; the other 80% is just right. **Showing off everywhere is a signal of cheapness** |
| **Hand feel** | Arcs (not straight lines), irregularity (not the mechanical rhythm of setInterval), a sense of breathing |
| **Respect** | Show the tweaking process, show bugs being fixed. **Don't hide the work, don't hand over "magic"**. AI is a collaborator, not a magician |

### §0.4 Self-check · The viewer's first reaction method

When you finish an animation, **what is the viewer's first reaction after watching it?** That is the only metric you need to optimize.

| Viewer reaction | Rating | Diagnosis |
|---|---|---|
| "Looks pretty smooth" | good | Acceptable but characterless; you're making PowerPoint |
| "This animation is really smooth" | good+ | The technique is right, but it doesn't wow |
| "This thing really looks like it's **floating up off the desk**" | great | You've reached physical weight |
| "This doesn't look like AI made it" | great+ | You've reached Anthropic's threshold |
| "I want to **screenshot** this and share it with friends" | great++ | You've gotten viewers to spread it on their own |

**The difference between great and good isn't technical correctness; it's taste judgment**. Technically correct + right taste = great.
Technically correct + no taste = good. Technically wrong = not even started.

### §0.5 The relationship between identity and rules

The technical rules in §1-§8 below are **the means of executing** this identity in specific scenarios, not a standalone rule list.

- When you hit a scenario the rules don't cover → go back to §0 and judge by **identity**; don't guess blindly
- When rules conflict with each other → go back to §0 and use the **taste standard** to judge which matters more
- When you want to break a rule → first answer: "Which kind of beauty in §0.3 does this serve?" If you can answer, break it; if not, don't

Good. Keep reading.

---

## Overview · Animation as physics, unfolded in three layers

The root of the cheap feel in most AI-generated animation is that **it behaves like "numbers", not "objects"**.
Real-world objects have mass, inertia, elasticity, and they overshoot. The root of the "premium feel" in Anthropic's three films
lies in giving digital elements a set of **physical-world motion rules**.

These rules have 3 layers:

1. **Narrative rhythm layer**: the Slow-Fast-Boom-Stop time allocation
2. **Motion curve layer**: Expo Out / Overshoot / Spring, rejecting linear
3. **Expressive language layer**: showing the process, cursor arcs, logo morph convergence

---

## 1. Narrative rhythm · The 5-part Slow-Fast-Boom-Stop structure

All three Anthropic films follow this structure without exception:

| Part | Share | Pace | Role |
|---|---|---|---|
| **S1 Trigger** | ~15% | Slow | Gives humans time to react, establishes realism |
| **S2 Generate** | ~15% | Medium | The visual wow moment appears |
| **S3 Process** | ~40% | Fast | Shows controllability/density/detail |
| **S4 Burst** | ~20% | Boom | Camera pulls out/3D pop-out/multiple panels surge in |
| **S5 Landing** | ~10% | Still | Brand logo + abrupt stop |

**Concrete duration mapping** (using a 15-second animation as the example):
S1 Trigger 2s · S2 Generate 2s · S3 Process 6s · S4 Burst 3s · S5 Landing 2s

**Don'ts**:
- ❌ Even pacing (the same information density every second): viewer fatigue
- ❌ Sustained high density: no peaks, nothing memorable
- ❌ Fading ending (fade out to transparent): it should **stop abruptly**

**Self-check**: sketch 5 thumbnails with pen and paper, each showing the climax frame of one part. If the 5 images don't differ much,
the rhythm hasn't come through.

---

## 2. Easing philosophy · Reject linear, embrace physics

All the motion in Anthropic's three films uses Bézier curves with a "damped" feel. The default cubic easeOut
(`1-(1-t)³`) **isn't sharp enough**: the start isn't fast enough and the stop isn't steady enough.

### Three core easings (already built into animations.jsx)

```js
// 1. Expo Out · fast start, slow braking (most used, the default main easing)
// CSS equivalent: cubic-bezier(0.16, 1, 0.3, 1)
Easing.expoOut(t) // = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)

// 2. Overshoot · springy toggle/button pop
// CSS equivalent: cubic-bezier(0.34, 1.56, 0.64, 1)
Easing.overshoot(t)

// 3. Spring physics · geometry settling into place, natural landing
Easing.spring(t)
```

### Usage mapping

| Scenario | Which easing |
|---|---|
| Card rise-in / panel entrance / Terminal fade / focus overlay | **`expoOut`** (main easing, most used) |
| Toggle switch / button pop / emphasized interaction | `overshoot` |
| Preview geometry settling / physical landing / UI element wobble | `spring` |
| Continuous motion (such as cursor path interpolation) | `easeInOut` (keeps symmetry) |

### Counterintuitive insight

The animation in most product promo films is **too fast and too stiff**. `linear` makes digital elements feel like machines, `easeOut` is the baseline,
and `expoOut` is the technical root of the "premium feel": it gives digital elements a **physical-world sense of weight**.

---

## 3. Motion language · 8 shared principles

### 3.1 Don't use pure black or pure white backgrounds

None of Anthropic's three films uses `#FFFFFF` or `#000000` as the main background. **Neutrals with a color temperature**
(warm or cool) have the material feel of "paper / canvas / desktop" and weaken the machine feel.

**Specific color value decisions** go through the Brand Asset Protocol (extracted from the brand spec) or Three Directions (`references/directions.md`)
(the background schemes of each of the 20 philosophies). This reference gives no specific color values; that's a **brand decision**, not a motion rule.

### 3.2 Easing is never linear

See §2.

### 3.3 Slow-Fast-Boom-Stop narrative

See §1.

### 3.4 Show the "process", not the "magic result"

- Claude Design shows tweaking parameters and dragging sliders (not one-click generation of a perfect result)
- Claude Code shows a code error + AI fixing it (not success on the first try)
- Claude for Word shows the Redline editing process, with red deletions and green additions (not handing over the final draft directly)

**Shared subtext**: the product is a **collaborator, a pair-programming engineer, a senior editor**, not a one-click magician.
This hits professional users' pain points around "controllability" and "authenticity" precisely.

**Anti AI slop**: by default AI makes "magic one-click success" animations (one click → perfect result);
that's the lowest common denominator. **Doing the opposite** (showing the process, showing tweaks, showing bugs and fixes)
is the source of brand recognition.

### 3.5 Hand-drawn cursor paths (arc + Perlin noise)

Real human cursor movement isn't a straight line; it's "accelerate from rest → arc → decelerate and correct → click".
AI's direct straight-line interpolation of cursor paths **triggers a subconscious rejection**.

```js
// Quadratic Bézier interpolation (start → control point → end)
function bezierQuadratic(p0, p1, p2, t) {
  const x = (1-t)*(1-t)*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0];
  const y = (1-t)*(1-t)*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1];
  return [x, y];
}

// Path: start → offset midpoint → end (makes an arc)
const path = [[100, 100], [targetX - 200, targetY + 80], [targetX, targetY]];

// Then layer on a tiny bit of Perlin noise (±2px) to create "hand tremor"
const jitterX = (simpleNoise(t * 10) - 0.5) * 4;
const jitterY = (simpleNoise(t * 10 + 100) - 0.5) * 4;
```

### 3.6 Logo "morph convergence" (Morph)

The logo reveal in all three Anthropic films **is never a simple fade-in**; it **morphs out of the preceding visual element**.

**Shared pattern**: in the last 1-2 seconds, do a Morph / Rotate / Converge so the whole narrative "collapses" onto the brand point.

**Low-cost implementation** (no real morph needed):
make the preceding visual element "collapse" into a color block (scale → 0.1, translate toward the center),
then have the color block "expand" into the wordmark. Use a 150ms quick cut + motion blur for the transition
(`filter: blur(6px)` → `0`).

```js
<Sprite start={13} end={14}>
  {/* Collapse: previous element scale 0.1, opacity kept, filter blur increases */}
  const scale = interpolate(t, [0, 0.5], [1, 0.1], Easing.expoOut);
  const blur = interpolate(t, [0, 0.5], [0, 6]);
</Sprite>
<Sprite start={13.5} end={15}>
  {/* Expand: logo scales 0.1 → 1 from the center of the color block, blur 6 → 0 */}
  const scale = interpolate(t, [0, 0.6], [0.1, 1], Easing.overshoot);
  const blur = interpolate(t, [0, 0.6], [6, 0]);
</Sprite>
```

### 3.7 Serif + sans-serif type pairing

- **Brand / narration**: serif (carries an "academic / publication / refined taste" feel)
- **UI / code / data**: sans-serif + monospace

**A single typeface is always wrong**. Serif brings "taste", sans-serif brings "function".

Specific font choices go through the brand spec (the Display / Body / Mono stacks in brand-spec.md) or the 20 philosophies of the design direction
advisor. This reference gives no specific fonts; that's a **brand decision**.

### 3.8 Focus switch = dim the background + sharpen the foreground + flash guidance

A focus switch is **not just** lowering opacity. The full recipe is:

```js
// Filter combination for non-focused elements
tile.style.filter = `
  brightness(${1 - 0.5 * focusIntensity})
  saturate(${1 - 0.3 * focusIntensity})
  blur(${focusIntensity * 4}px)        // ← Key: adding blur is what actually makes it "recede"
`;
tile.style.opacity = 0.4 + 0.6 * (1 - focusIntensity);

// After the focus completes, do a 150ms flash highlight at the focus position to guide the eye back
focusOverlay.animate([
  { background: 'rgba(255,255,255,0.3)' },
  { background: 'rgba(255,255,255,0)' }
], { duration: 150, easing: 'ease-out' });
```

**Why blur is required**: with only opacity + brightness, out-of-focus elements are still "sharp",
so visually there's no "receding into the background" effect. blur(4-8px) makes non-focused elements genuinely drop back one layer of depth.

---

## 4. Concrete motion techniques (code snippets you can copy directly)

### 4.1 FLIP / Shared Element Transition

A button "expands" into an input box; it is **not** the button disappearing + a new panel appearing. The core is **the same DOM element**
transitioning between two states, not two elements cross-fading.

```jsx
// Using Framer Motion layoutId
<motion.div layoutId="design-button">Design</motion.div>
// ↓ After the click, same layoutId
<motion.div layoutId="design-button">
  <input placeholder="Describe your design..." />
</motion.div>
```

For a native implementation, see https://aerotwist.com/blog/flip-your-animations/

### 4.2 "Breathing" expansion (width→height)

A panel expansion **doesn't stretch width and height at the same time**; instead:
- First 40% of the time: stretch only the width (keep the height small)
- Last 60% of the time: hold the width, grow the height

This mimics the physical-world feel of "unfold first, then fill with water".

```js
const widthT = interpolate(t, [0, 0.4], [0, 1], Easing.expoOut);
const heightT = interpolate(t, [0.3, 1], [0, 1], Easing.expoOut);
style.width = `${widthT * targetW}px`;
style.height = `${heightT * targetH}px`;
```

### 4.3 Staggered Fade-up (30ms stagger)

When table rows, card columns, or list items enter, **delay each element by 30ms**, with `translateY` going from 10px back to 0.

```js
rows.forEach((row, i) => {
  const localT = Math.max(0, t - i * 0.03);  // 30ms stagger
  row.style.opacity = interpolate(localT, [0, 0.3], [0, 1], Easing.expoOut);
  row.style.transform = `translateY(${
    interpolate(localT, [0, 0.3], [10, 0], Easing.expoOut)
  }px)`;
});
```

### 4.4 Nonlinear breathing · Hover 0.5s before a key result

The machine executes fast and continuously, but **hover for 0.5 seconds before a key result appears** so the viewer's brain has time to react.

```jsx
// Typical scenario: AI finishes generating → hover 0.5s → result emerges
<Sprite start={8} end={8.5}>
  {/* 0.5s pause: nothing moves, let the viewer watch the loading state */}
  <LoadingState />
</Sprite>
<Sprite start={8.5} end={10}>
  <ResultAppear />
</Sprite>
```

**Counterexample**: AI finishes generating and immediately cuts seamlessly to the result. The viewer has no time to react, and information is lost.

### 4.5 Chunk Reveal · Simulating token streaming

For AI-generated text, **don't use `setInterval` to pop out one character at a time** (like old movie subtitles); use **chunk reveal**:
2-5 characters appear at a time, at irregular intervals, simulating real token streaming output.

```js
// Split into chunks, not characters
const chunks = text.split(/(\s+|,\s*|\.\s*|;\s*)/);  // Split by word + punctuation
let i = 0;
function reveal() {
  if (i >= chunks.length) return;
  element.textContent += chunks[i++];
  const delay = 40 + Math.random() * 80;  // Irregular 40-120ms
  setTimeout(reveal, delay);
}
reveal();
```

### 4.6 Anticipation → Action → Follow-through

Three of Disney's 12 principles. Anthropic uses them very explicitly:

- **Anticipation**: a small reverse motion before the action starts (the button shrinks slightly before popping out)
- **Action**: the main motion itself
- **Follow-through**: an aftertaste after the action ends (a slight bounce after the card lands)

```js
// The full three phases of a card entrance
const anticip = interpolate(t, [0, 0.2], [1, 0.95], Easing.easeIn);     // Anticipation
const action  = interpolate(t, [0.2, 0.7], [0.95, 1.05], Easing.expoOut); // Main action
const settle  = interpolate(t, [0.7, 1], [1.05, 1], Easing.spring);       // Rebound
// Final scale = product of the three phases, or apply them in sequence
```

**Counterexample**: an animation with only Action and no Anticipation + Follow-through looks like a "PowerPoint animation".

### 4.7 3D Perspective + translateZ layering

For a "tilted 3D + floating cards" feel, give the container perspective and give individual elements different translateZ values:

```css
.stage-wrap {
  perspective: 2400px;
  perspective-origin: 50% 30%;  /* Line of sight looks slightly down */
}
.card-grid {
  transform-style: preserve-3d;
  transform: rotateX(8deg) rotateY(-4deg);  /* Golden ratio */
}
.card:nth-child(3n) { transform: translateZ(30px); }
.card:nth-child(5n) { transform: translateZ(-20px); }
.card:nth-child(7n) { transform: translateZ(60px); }
```

**Why rotateX 8° / rotateY -4° is the golden ratio**:
- Above 10° → elements look too distorted, as if "falling over"
- Below 5° → looks like "skew" rather than "perspective"
- The asymmetric 8° × -4° ratio mimics the natural angle of "a camera looking down from the top-left corner of the desk"

### 4.8 Diagonal pan · Move X and Y together

Camera motion isn't purely up-down or purely left-right; **move X and Y at the same time** to simulate diagonal movement:

```js
const panX = Math.sin(flowT * 0.22) * 40;
const panY = Math.sin(flowT * 0.35) * 30;
stage.style.transform = `
  translate(-50%, -50%)
  rotateX(8deg) rotateY(-4deg)
  translate3d(${panX}px, ${panY}px, 0)
`;
```

**Key**: X and Y use different frequencies (0.22 vs 0.35) to avoid a regular Lissajous loop.

---

## 5. Scene recipes (three narrative templates)

The three videos in the reference material correspond to three product personalities. **Pick the one that best fits your product**; don't mix and match.

### Recipe A · Apple Keynote dramatic style (Claude Design type)

**Suits**: major version launches, hero animations, visual wow first
**Pace**: strong Slow-Fast-Boom-Stop arc
**Easing**: `expoOut` throughout + a little `overshoot`
**SFX density**: high (~0.4/s), SFX pitch tuned to the BGM scale
**BGM**: IDM / minimal tech electronica, calm + precise
**Ending**: camera pulls out sharply → drop → logo morph → ethereal single note → abrupt stop

### Recipe B · Single-take tool style (Claude Code type)

**Suits**: developer tools, productivity apps, flow-state scenarios
**Pace**: continuous steady flow, no obvious peaks
**Easing**: `spring` physics + `expoOut`
**SFX density**: **0** (editing rhythm driven purely by BGM)
**BGM**: Lo-fi Hip-hop / Boom-bap, 85-90 BPM
**Core technique**: key UI actions land on BGM kick/snare transients: "**the musical groove is the interaction sound effect**"

### Recipe C · Office productivity narrative style (Claude for Word type)

**Suits**: enterprise software, document/spreadsheet/calendar products, professionalism first
**Pace**: multi-scene hard cuts + Dolly In/Out
**Easing**: `overshoot` (toggles) + `expoOut` (panels)
**SFX density**: medium (~0.3/s), mostly UI clicks
**BGM**: Jazzy Instrumental, minor key, BPM 90-95
**Core highlight**: one scene must have the "highlight of the whole film": a 3D pop-out / lifting off the plane

---

## 6. Counterexamples · Doing this is AI slop

| Anti-pattern | Why it's wrong | The right way |
|---|---|---|
| `transition: all 0.3s ease` | `ease` is a relative of linear; every element moves at the same speed | Use `expoOut` + per-element stagger |
| Every entrance is `opacity 0→1` | No sense of motion direction | Pair with `translateY 10→0` + Anticipation |
| Logo fades in | No sense of narrative convergence | Morph / Converge / collapse-expand |
| Cursor moves in straight lines | Subconscious machine feel | Bézier arc + Perlin noise |
| Typing pops out one character at a time (setInterval) | Looks like old movie subtitles | Chunk Reveal, random intervals |
| No hover before key results | The viewer has no time to react | Hover 0.5s before the result |
| Focus switch only changes opacity | Non-focused elements are still sharp | opacity + brightness + **blur** |
| Pure black / pure white background | Cyber feel / glare fatigue | Neutrals with a color temperature (via the brand spec) |
| Every animation equally fast | No rhythm | Slow-Fast-Boom-Stop |
| Fade-out ending | No sense of decisiveness | Abrupt stop (hold the last frame) |

---

## 6.5 · The visual density clause for director's scripts (lesson from the B00 project, 2026-07-17)

**A director's script that only covers narrative + camera motion will get you a wireframe.** B00 step-function b-roll, measured: the v1 director's script covered the narrative, timeline, and camera motion of all six acts thoroughly, and the implementing agent delivered animation and motion that all passed, with every check green. But the visuals were at the level of a schematic of "three plain dark blocks + big text", and the director rejected it outright ("too simple, too boring"). Without a density standard, an agent will always hand in the least geometry it can get away with.

**A director's script (or any animation brief) must explicitly include three things**:

1. **A visual density standard**: the expected level of detail elements per screen (skeleton UI content rows, legends, textures, secondary elements), plus one actionable acceptance statement, such as "pause on any frame and it holds up next to the reference benchmark"
2. **A reference benchmark**: point to a specific existing finished piece (an older animation in the same project/the A series/some demo), and carry over its component craftsmanship directly instead of letting the agent invent from scratch
3. **A global atmosphere layer checklist**: ground line anchoring, soft shadows on components, paper/background texture, hero sidekicks or similar personified small elements, idle micro-motion on static components (breathing/cursor/micro-push). This layer is the main antidote to "empty, boring", not the main elements themselves

**The fix path also has a set pattern**: motion skeleton (timeline/camera motion/morph paths/title-card timing) and visual craftsmanship (components/density/atmosphere) are two layers. When a review rejects the work, first pin down which layer the problem is in. If the motion passes, just re-skin; don't re-choreograph.

---

## 7. Self-check list (60 seconds before delivering an animation)

- [ ] Is the narrative structure Slow-Fast-Boom-Stop, not even pacing?
- [ ] Is the default easing `expoOut`, not `easeOut` or `linear`?
- [ ] Do toggles / button pops use `overshoot`?
- [ ] Do card / list entrances have a 30ms stagger?
- [ ] Is there a 0.5s hover before key results?
- [ ] Does typing use Chunk Reveal, not single characters via setInterval?
- [ ] Does the focus switch add blur (not just opacity)?
- [ ] Is the logo a morph convergence (Morph), not a fade-in?
- [ ] Is the background not pure black / pure white (does it have a color temperature)?
- [ ] Does the text have a serif + sans-serif hierarchy?
- [ ] Is the ending an abrupt stop, not a fade?
- [ ] (If there's a cursor) Is the cursor path an arc, not a straight line?
- [ ] Does the SFX density match the product personality (see Recipes A/B/C)?
- [ ] Is there a 6-8dB loudness difference between BGM and SFX? (see `audio-design-rules.md`)

---

## 8. Relationship to other references

| reference | Role | Relationship |
|---|---|---|
| `animation-pitfalls.md` | Technical pitfalls (16 items) | "**Don't do it this way**" · the flip side of this file |
| `animations.md` | Stage/Sprite engine usage | The basics of **how to write** animation |
| `audio-design-rules.md` | Dual-track audio rules | Rules for **adding audio** to animation |
| `sfx-library.md` | List of 37 SFX | Sound effect **asset library** |
| `apple-gallery-showcase.md` | Apple gallery showcase style | A deep dive into one specific motion style |
| **This file** | Positive motion design grammar | "**Do it this way**" |

**Reading order**:
1. First look at the five form-derivation questions in Step 3 of the SKILL.md workflow (they decide the narrative role and visual temperature)
2. Once the direction is chosen, read this file to settle the **motion language** (Recipe A/B/C)
3. When writing code, refer to `animations.md` and `animation-pitfalls.md`
4. When exporting video, follow `audio-design-rules.md` + `sfx-library.md`

---

## Appendix · Source material for this file

- Breakdown of Anthropic's official animations: `参考动画/BEST-PRACTICES.md` in Huashu's project directory
- Anthropic audio breakdown: `AUDIO-BEST-PRACTICES.md` in the same directory
- 3 reference videos: `ref-{1,2,3}.mp4` + the corresponding `gemini-ref-*.md` / `audio-ref-*.md`
- **Strict filtering**: this reference includes no specific brand color values, font names, or product names.
  Color/font decisions go through the Brand Asset Protocol or the direction cards of Three Directions.
