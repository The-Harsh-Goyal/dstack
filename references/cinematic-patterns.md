# Cinematic Patterns · Best Practices for Workflow Demos

> 5 key patterns for upgrading from "PPT animation" to "launch-event-grade cinematic".
> Distilled from the two cinematic demos (Nuwa workflow + Darwin workflow) in the 2026-04 "Let's talk about skills" deck; measured and reproducible.

---

## 0 · What problem this document solves

When you need to make "a demo animation showing a workflow" (typical scenarios: skill workflows, product onboarding, API call flows, agent task execution), there are two common approaches:

| Paradigm | What it looks like | Consequence |
|---|---|---|
| **PPT animation** (bad) | step 1 fade in → step 2 fade in → step 3 fade in, 4 boxes arranged on the same screen | Viewers feel "it's just a PPT with a fade effect"; no wow moment |
| **Cinematic** (good) | Scene-based, focusing on only one thing at a time, with dissolve / focus pull / morph between scenes | Viewers feel "this is a clip from a product launch event" and want to screenshot and share it |

The root of the difference **isn't animation technique**; it's the **narrative paradigm**. This document explains how to upgrade from the former to the latter.

---

## 1 · Five core patterns

### Pattern A · Dashboard + Cinematic Overlay two-layer structure

**Problem**: a pure cinematic defaults to a black screen + a ▶ button; if the user flips to this page and doesn't click, they see nothing.

**Solution**:
```
DEFAULT state (always shown): the full static workflow dashboard
  └── Viewers see at a glance how this skill / workflow runs

POINT ▶ trigger (overlay floats up): 22-second cinematic
  └── Automatically fades back to DEFAULT when finished

```

**Implementation notes**:
- `.dash` is visible by default; `.cinema` defaults to `opacity: 0; pointer-events: none`
- `.play-cta` is a small gold button in the bottom-right corner (not a large central overlay)
- Click → `cinema.classList.add('show')` + `dash.classList.add('hide')`
- Run once with `requestAnimationFrame` (not a loop); when it ends, `endCinematic()` reverses the state

**Anti-pattern**: default = a large central ▶ overlay covering everything, so the page is blank until clicked.

---

### Pattern B · Scene-based, NOT Step-based

**Problem**: splitting the animation into "show step 1 → show step 2 → ..." is PPT thinking.

**Solution**: split it into 5 scenes; each scene is an **independent shot**, and the full screen focuses on only one thing:

| Scene type | Responsibility | Duration |
|---|---|---|
| 1 · Invoke | User input triggers it (terminal typewriter) | 3-4s |
| 2 · Process | Visualization of the core workflow (a unique visual language) | 5-6s |
| 3 · Result/Insight | The key distilled output (visualized) | 4-5s |
| 4 · Output | Showcase of the actual output (files / diff / numbers) | 3-4s |
| 5 · Hero Reveal | Closing hero moment (large type + value proposition) | 4-5s |

**Total duration ≈ 22 seconds**: this is the tested golden length:
- Shorter than 18 seconds: it's over before the PM gets into it
- Longer than 25 seconds: they lose patience
- 22 seconds is just enough for "hook → unfold → close → leave an impression"

**Implementation notes**:
- `T = { DURATION: 22.0, s1_in: [0, 0.7], s2_in: [3.8, 4.6], ... }` global timeline
- A single `requestAnimationFrame(render)` runs the opacity / transform calculations for every scene
- Don't use setTimeout chains (they break easily and are hard to debug)
- Easing must use `expoOut` / `easeOut` / cubic-bezier; **linear is forbidden**

---

### Pattern C · Each demo's visual language must be independent

**Problem**: after making the first cinematic, you get lazy on the second and reuse the same template (the same orbit + pentagon + typewriter + large hero type), changing only the copy.

**Consequence**: viewers notice the two skills "look exactly the same", which amounts to saying "there's no difference between these two skills".

**Solution**: each workflow has a different core metaphor, so its visual language must be different.

**Side-by-side case**:

| Dimension | Nuwa (distills people) | Darwin (optimizes skills) |
|---|---|---|
| Core metaphor | Collect → distill → write | Loop → evaluate → ratchet |
| Visual motion | Floating / radiating / pentagon | Looping / rising / contrasting |
| Scene 2 | 3D Orbit · 8 dossiers floating on a perspective ellipse | Spin Loop · a token runs 5 laps around a 6-node ring |
| Scene 3 | Pentagon · 5 tokens radiating from the center | v1 vs v5 · side-by-side diff (red version vs gold version) |
| Scene 4 | SKILL.md typewriter | Hill-Climb · full-screen curve drawing |
| Scene 5 hero | "21 minutes" in large serif italic | Rotating gear ⚙ + "KEPT +1.1" gold tag |

**Criterion**: cover the copy and look only at the visuals. Can you tell which demo this is? If you can't, that's laziness.

---

### Pattern D · Use real AI-generated assets, not emoji or hand-drawn SVG

**Problem**: a 3D orbit / gallery needs asset fragments floating around; emoji (📚🎤) are ugly and unbranded, and hand-drawn SVG book spines never look like real books.

**Solution**: use an image-generation tool to run one large 4×2 grid image (8 subject-related objects · white background · 60px breathing space · unified style), then cut it into 8 separate transparent PNGs with `extract_grid.py --mode bbox`.

**Prompt essentials** :
- IP anchoring ("1960s Caltech archive aesthetic" / "Hearthstone-style consistent treatment")
- White background (easy to cut out; a gray background has nice atmosphere but is hard to cut out to transparent)
- 4×2, not 5×5 (avoids the last-row compression bug)
- Persona finishing ("You are a Wired magazine curator preparing an exhibition photo")

**Anti-pattern**: using emoji as icons, using CSS silhouettes in place of product images.

---

### Pattern E · BGM + SFX dual-track system

**Problem**: with only animation and no sound, viewers subconsciously feel "this thing looks like a shabby demo".

**Solution**: a sustained BGM + 11 SFX cues.

**General SFX cue recipe** (for workflow demos):

| Time | SFX | Triggering moment |
|---|---|---|
| 0.10s | whoosh | Terminal rises from below |
| 3.0s | enter | Typewriter finishes, enter is pressed |
| 4.0s | slide-in | Scene 2 elements enter |
| 5-9s × 5 times | sparkle | Key process nodes (each generation / each token / each data point) |
| 14s | click | Switch to the output scene |
| 17.8s | logo-reveal | The hero reveal moment |
| typewriter | type | Triggered once every 2 characters (don't make it too dense) |

**Frequency band separation**: BGM volume 0.32 (low-frequency bed), SFX volume 0.55 (mid-high frequency punch), sparkle 0.7 (needs to stand out), logo-reveal 0.85 (the strongest hero moment).

**User control**:
- There must be a ▶ start overlay (browser autoplay restrictions)
- A small mute button in the top-right corner (the user can mute at any time)
- Don't make it "forced to play sound as soon as you flip to this page"

---

## 2 · Static dashboard design essentials

The dashboard is Layer 1 of the two-layer structure: the PM can understand the skill without clicking ▶.

**Layout**: a 3-column grid (or 1 large + 2 small), with each panel answering one question:

| Panel type | Question it answers | Example |
|---|---|---|
| **Pipeline / Flow Diagram** | "What is this skill's workflow?" | Nuwa 4-stage pipeline · Darwin autoresearch loop |
| **Snapshot / State** | "What does the real data it produces look like?" | Darwin 8-dimension rubric snapshot |
| **Trajectory / Evolution** | "How does it change over multiple runs?" | Darwin 5-generation hill-climb curve |
| **Examples / Gallery** | "What has it already produced?" | Nuwa 21 personas gallery |
| **Strip · Example I/O** | "What goes in → what comes out" | Nuwa example strip: `› nuwa distill Feynman → feynman.skill (21 min)` |

**Key constraints**:
- Information density must be high enough (every panel must carry differentiated information)
- But don't stuff in data slop (every number must mean something)
- Colors consistent with the cinematic (same color family, so switching isn't jarring)

---

## 3 · Debugging and development tools

Any long animation must come with three dev tools, or debugging will explode.

### Tool 1 · `?seek=N` freezes at second N

```js
const seek = parseFloat(params.get('seek'));
if (!isNaN(seek)) {
  started = true; muted = true;
  frozenT = seek;  // render() uses this t instead of elapsed
  cinema.classList.add('show'); dash.classList.add('hide');
}

// Inside render():
let t = frozenT !== null ? frozenT : (elapsed % T.DURATION);
```

Usage: `http://.../slide.html?seek=12` shows the frame at second 12 directly, without waiting for playback.

### Tool 2 · `?autoplay=1` skips the ▶ overlay

Handy for automated Playwright screenshot tests, and for force-starting when embedded in an iframe.

### Tool 3 · Manual REPLAY button

A small button in the top-right corner, so users/debugging can replay any number of times. CSS:

```css
.replay{position:absolute;top:18px;right:18px;background:rgba(212,165,116,0.1);
  border:1px solid rgba(212,165,116,0.3);color:#D4A574;
  font-family:monospace;font-size:10px;letter-spacing:.28em;text-transform:uppercase;
  padding:6px 12px;border-radius:1px;cursor:pointer;backdrop-filter:blur(6px);z-index:6}
```

---

## 4 · iframe embedding pitfalls (if the cinematic is embedded in a deck)

### Pitfall 1 · The parent window's click zones intercept buttons inside the iframe

If the deck's index.html adds "transparent 22vw click zones on the left and right for page turning", they **cover the ▶ play button inside the iframe**: the user's click on the button gets swallowed as "next page".

**Fix**: add `top: 12vh; bottom: 25vh` to the click zones so the top and bottom 25% aren't intercepted, letting both the central ▶ and the bottom-right ▶ inside the iframe be clickable.

### Pitfall 2 · Keyboard events are lost after the iframe grabs focus

After the user clicks the iframe, focus is inside the iframe and the parent window no longer receives ←/→ keyboard events.

**Fix**:
```js
iframe.addEventListener('load', () => {
  // Inject a keyboard forwarder
  const doc = iframe.contentDocument;
  doc.addEventListener('keydown', (e) => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: e.key, ... }));
  });
  // After a click, pull focus back to the parent window
  doc.addEventListener('click', () => setTimeout(() => window.focus(), 0));
});
```

### Pitfall 3 · Behavior differences between file:// and https://

A cinematic that tested fine locally over file:// may break after deployment, because:
- Under file://, the iframe's contentDocument is same-origin
- Under https:// it's also same-origin (if same host), but audio autoplay restrictions are stricter

**Fix**:
- Before deploying, start a local HTTP server with `python3 -m http.server` and test once
- BGM must wait until the user clicks ▶ before calling `bgm.play()`; don't play immediately on page load

---

## 5 · Anti-pattern quick reference

| ❌ Anti-pattern | ✅ Correct pattern |
|---|---|
| Default = black screen ▶ overlay | Default = static dashboard, ▶ is secondary |
| 4 steps side by side on one screen fading in | 5 full-screen scene switches, each focusing on only one thing |
| Reusing the template and swapping copy for different demos | Each demo has an independent visual language (distinguishable with the copy covered) |
| Emoji / hand-drawn SVG as assets | gpt-image-2 large image + extract_grid cutouts |
| No BGM, no SFX | BGM + 11 SFX cues dual-track system |
| Scheduling with setTimeout chains | requestAnimationFrame + global timeline T object |
| Linear animation | Expo / cubic-bezier easing |
| No dev tools | `?seek=N` + `?autoplay=1` + REPLAY button |
| Buttons inside the iframe swallowed by the parent's click zones | Add top/bottom margins to the click zones to make room for the buttons |

---

## 6 · Time budget

Following these patterns, a complete cinematic demo (including the dashboard):

| Task | Time |
|---|---|
| Design the 5-scene narrative + visual language | 30 minutes (be careful; this decides independence) |
| Dashboard static layout + content | 1 hour |
| Implement the 5 cinematic scenes | 1.5 hours |
| Tune audio cue timing + replay button | 30 minutes |
| Verify 5 key moments with Playwright screenshots | 15 minutes |
| **Total for a single demo** | **3-4 hours** |

The second demo reuses the framework, but **its visual language must be independent**; it takes about 2-3 hours.
