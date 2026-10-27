# Product UI Showcase Animation Playbook

> **This is the single entry point for when "the product being promoted has a UI".** Commercial commissions, launch animations, feature demos: whenever the star of the frame is an interface, read this file before you start.
>
> The core claim in one sentence: **the biggest source of quality in a product animation is "real UI + cinematic camera work", not effects.** A tech feel comes from the viewer recognizing "this is that product" and from how the camera looks at it, not from particles, glow or cyber gradients. One real screenshot with one restrained push-in beats ten layers of hand-built fake interface.
>
> Convention for citing parameter sources: (shotcraft·card name) = measured values from the video-shotcraft shot cards; (huarec) = the HuaRec Studio camera-direction system; (best-practices §x) (gsap-recipes §x) = existing references in this skill. 30fps context, 1f ≈ 33ms.
>
> Division of labor: this file covers "how the UI, as the star, performs"; for camera vocabulary and camera-move motivation see `camera-language.md`; for element-level motion grammar (easing, stagger, FLIP, Chunk Reveal) see `animation-best-practices.md`. This file only cites them and doesn't rewrite them.

---

## §0 Two axioms (overriding every parameter of the Eight Moves)

| Axiom | Content | Source |
|---|---|---|
| **Visibility invariant** | At every moment, the cursor and the UI operation in progress must be inside the visible area (including an 8% safe margin). For a shot that violates this, lower the magnification, merge shots, or don't shoot it | huarec A1 |
| **Visual language grows from the product** | First extract the product's own design tokens (fonts/corner radii/palette/grid); the whole film may only reuse them or extend them with restraint. Shot cards only pass down motion grammar and rhythm; the skin is re-wrapped to match the target product | shotcraft axiom 1 |

---

## §1 Decision tree: camera moves on real UI screenshots vs rebuilding the UI in HTML

This is **the decision in this file that affects workload most**; the two paths differ by an order of magnitude. By default, start judging from the cheapest path:

```
The product UI needs to appear
 │
 ├─ Does the interface only need to "be looked at" (push-in/tour/float/compare)?
 │   └─ Yes → [Path 1] Screenshot in a frame + 2.5D camera moves. Stop there, don't rebuild
 │
 ├─ Do only a few elements need to move on their own (one card lifts, one row of data scrolls)?
 │   └─ Yes → [Path 3] Hybrid: screenshot as the base + key elements sliced and rebuilt
 │
 └─ Is the interface itself the subject of the narrative, with elements entering one by one/responding to actions/changing state?
     └─ Yes → [Path 2] Rebuild in HTML. Use Eight Moves ② build-up
```

| Path | Method | Workload | Criteria |
|---|---|---|---|
| 1 · Screenshot camera moves | Put the real screenshot into a `browser_window.jsx` / `macos_window.jsx` device frame and do zoom/rotate/pan on the container | Hours | The interface is "an object being viewed"; the viewer doesn't need to see changes happening inside it |
| 2 · HTML rebuild | Rebuild an animatable DOM structure pixel by pixel from the screenshot | Days | Elements need independent timelines: step-by-step generation, typing, state switches, hover responses |
| 3 · Hybrid | A full-page screenshot as the base texture; the elements that need to move are cut out as transparent-background slices laid over their original coordinates and animated | Half a day | 90% of the frame is static and 10% of the elements need to come alive. **The right answer for most commercial commissions** |

**The key to the hybrid strategy**: once a sliced element finishes moving, it must return to its real slot on the screenshot. If the target card hovers above the grid and never drops back into the layout, the viewer immediately reads it as "fake" (shotcraft·type-and-filter; the Q9 precedent nearly required rewriting the whole file because of this).

The five steps of the hybrid path:

1. Lay a full-page 2x screenshot as the base and put it into a device frame (`browser_window.jsx` for web products, `macos_window.jsx` for desktop apps)
2. Cut the elements that need to move into transparent-background slices using the layout.json coordinates
3. On the screenshot's base layer, lay a "page background color patch" at each slice's original position to cover the baked-in original element (the in-place patch technique from spotlight-hero-card: after the card takes off, lay a background color patch in its original spot + an accent-color breathing outline, which brightens and disappears the instant it lands)
4. Animate the slices on top of the patches, ending back in their layout.json slots
5. In the close-up push-in, cross-fade in 4x high-res slices over 6f to cover the low-magnification texture (a companion technique to shotcraft·PageCam)

**Choosing the device frame**: the frame is a context signal that says "this is real software"; a bare screenshot hanging on the canvas looks like a pasted image. But the frame also eats frame area, and when a close-up push-in goes past zoom 2x the frame has already left the frame, so at that point you can use frameless slices directly.

### The asset trio (collect all of it before taking Path 1/3)

The standard collected assets from stage 1 of the shotcraft pipeline (shotcraft·six-stage pipeline):

| Asset | Spec | Use |
|---|---|---|
| Full-page 2x screenshot | Device pixel ratio of 2 or more; capture long pages in full | Base texture; the floor for not getting blurry after a push-in |
| Transparent-background element slices | Cut out each element that needs to move on its own, 4x preferred | The "actors" of the hybrid path; cross-faded in over 6f during the close-up push-in to cover the low-magnification texture |
| layout.json coordinate table | Each slice's `{x,y,w,h}` in the full-page coordinate system | The basis for the "real slot" elements return to after moving; the positioning anchor for annotations/highlight boxes |

Screenshot sourcing follows the UI screenshot collection protocol in `brand-asset-protocol.md` (App Store screenshots, official website screenshots, frames from demo videos, real captures from a user account), and the "5-10-2-8" quality bar applies equally. For the root fix for blurry text in push-in close-ups (CSS `zoom` layout-level scaling instead of transform scale), see `camera-language.md`.

---

## §2 The Eight Moves of UI showcasing · overview

| # | Move | In one sentence | Path | Source card |
|---|---|---|---|---|
| ① | 3D display stand / hero close-up | One card stands up as the star of the whole film: spotlight→push-in→hover→return to place | 1/3 | spotlight-hero-card |
| ② | Interface build-up | The interface goes from nothing to something: skeleton→content→data, the entrance is the narrative | 2 | skeleton-reveal / row-embed / document-typewriter-reveal |
| ③ | User typing simulation | Typing at real human speed, the cursor steady-on, then blinking | 2/3 | type-and-filter |
| ④ | Cursor-action narrative | The cursor as an actor: arc movement, click ripple, hover linkage | All | type-and-filter / collab-cursor-moves |
| ⑤ | Timeline-driven UI state transitions | Tab/modal/route switches written as a scene on the timeline | 2 | command-palette-summon |
| ⑥ | 3D interface tour | A long interface glides past at a steep angle, or the camera tours it up close | 1 | steep-tilt-glide / graze-face-tour |
| ⑦ | Long-page scroll narrative | A long page scrolls fast and brakes hard, stopping on the target row | 1/3 | scroll-brake-moves |
| ⑧ | Feature callout annotations | Growing annotation lines, highlight boxes, caption cards, before/after comparisons | All | before-after-slider-scrub, etc. |

Selection discipline: **one shot features only one move, and one move is the star only once in the whole film** (shotcraft axiom 5). Several of the Eight Moves can appear in one film, but each gets its own shot.

---

## §3 The Eight Moves in detail

### ① 3D display stand / hero close-up

Stand one core object (a card/panel/module) up as the product's atomic unit. The shot with the highest polish and the slowest rhythm, suited to the "single-hero showcase" segment after the opening.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Camera position | rotY 34° dominant + rotX only 8°, perspective 1200px | A side angle beats a top-down one: "shoot from the left, not from below"; once rotX gets large it turns into looking at a desktop |
| Push-in | Hold still for one beat at full-page zoom 0.78, then push in over 16f to zoom 2.6 | The stillness before the push-in is "let the viewer see the whole first"; pushing in straight away gives no sense of space |
| Action arc | rise 10f (`cubic-bezier(0.2,1.25,0.3,1)` overshoot) → hover 54f (sin bob amplitude 4px period 40f, translateZ 110px) → reseat 18f, landing with press scale 0.997 | About 3.3s from lock to landing; a polish shot has to be this slow; first drafts are almost always too fast |
| Outline light beam | An SVG rounded-rect stroke runs two laps: the first lap 14f, fast and bright, the second 20f, slow and faint (opacity 0.62) | Only two laps at different speeds read as "continuous scanning"; one lap is a blink; the beam is given only to the star, once in the whole film |
| Double shadow | `0 8·lift px …, 0 46·lift px 90·lift px` grows with the hover height | If the shadow doesn't grow with height, the hover doesn't hold up |
| Spotlight guidance | A roving light passes 4 intermediate stops before locking onto the card's center, the light pool radius tightens 620→420→360, with a +6% pulse at the instant of lock; the outer vignette darkens 0.16→0.42 | The intermediate stops make "random illumination" believable; heading straight for the target reads as programmatic; the vignette is the other half of the spotlight |
| Floating annotation (optional) | Two lines of serif annotation appear beside the card, translateZ 92px + bob period 44f (close to the card's 40f but not in sync) | "Resonance" rather than mirrored sync; the annotation must live in the same 3D space under the same camera perspective; flat overlaid text breaks the unity of the space |

(All of the above are shotcraft·spotlight-hero-card measured values)

Known pitfalls: tail drift like "zoom 2.6→2.58" is forbidden at the close, the breath must be true stillness; a multi-card ensemble dance at the opening can't carry the first impression, so draft straight from a single hero + a complete action arc; per-card glint was vetoed twice in precedents, so light effects are strictly for the star only.

Camera pairing: dolly-in push + a static hold after the lock (see `camera-language.md`). When the magnification span is over 2x, scale the duration logarithmically and forbid spring overshoot (huarec).

### ② Interface build-up

The entrance narrative of an interface "going from nothing to something". **The build order has a grammar**: chrome (window frame/title bar) → skeleton (gray placeholder bars) → content block stagger → data (numbers/charts come alive last). Viewers have a free expectation from skeleton screens: as soon as the gray bars appear, they know content is coming.

The three source cards divide the work by object: use skeleton-reveal for **one interface** becoming real step by step; row-embed for **a group of rows/cards** embedding into a list; document-typewriter-reveal for **a document** being written out.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Three-stage reveal | Scribble ("boiling" with a new seed every 5f) → a swap-to-real beat of 8f, accelerating shrink-out + skeleton springs in → skeleton rows roll in staggered by 6f → revealed rows staggered by 13f, 12f within a row | The swap-to-real beat must be fast and decisive; drag it out into a crossfade and the "leap" is gone; the three stages must have strictly identical layouts, misalignment reads as a different page |
| Word-by-word entrance | 2.5f/word rising 14px; the last word of the last row +14f, half a beat late | The half-beat delay is the period on "loading complete"; everything landing together is flat |
| Row embedding | Row i cue = 12 + i·9, flight 12f; `perspective(900px) translateY(−120·air) rotateX(16°·air)` | **rotateX flattening out is the key to reading it as "embedding"**; pure translateY is just "dropping" |
| Embed accent seam | A 2px accent-color seam on the bottom edge expands from the center over 5f, fades out over 8f | Gives each embed a confirmation point, but it has to fade fast |
| Document block by block | Block g cue = 6 + g·3.5, each block wipes for 8f; the accent-color caret only follows the newest block | **"Check blocks × beat against the budget first" is the core arithmetic**; with too many blocks, cut blocks first rather than speeding up; "there's only ever one pen tip": two carets blinking at once means two authors |

(Measured values from the three cards skeleton-reveal / row-embed / document-typewriter-reveal)

Known pitfalls: when the real content layer is a product screenshot, measure the skeleton bars' row heights and slots from the screenshot, not from imagination; don't draw details at the scribble stage, or if it looks too much like UI the first and second stages become indistinguishable; mock copy must not show real names of clients/members.

Camera pairing: pair the reveal segment with a slow 1→1.34 push (giving the gaze a "lean in to see clearly" motivation); don't add a lateral camera move during the whole build; the camera has to stay steady while the interface changes (huarec: no push during full-screen-level changes).

### ③ User typing simulation

Simulates a real person typing into an input box/terminal. It is **a different thing from the existing Chunk Reveal (AI streaming output)**: AI output is irregular chunks surging out (best-practices §4.5, gsap-recipes §3.4; keep using that, it isn't rewritten here); user input is character by character, steady, with the hesitant rhythm of a human hand. Getting the scenario wrong is a frequent accident: turning user typing into chunks reads as "the input box is generating by itself".

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Typing speed | Body text 3f/character; terminal 2f/character; decorative small text 0.7f/character | "The final values after first drafts were judged too fast and reworked"; interactive demos follow real human operating speed, a precedent-level iron rule |
| Cursor state machine | **Steady-on** while typing, switching to an 8f-period blink when done | Blinking while typing reads as lag; the switch from steady-on to blinking is itself the "done typing" signal |
| Backspace correction | Once, occasionally: type 1-2 extra characters, pause 4-6f, backspace, type it right | "People make typos" is the cheapest realism; but it must be pre-written into the script (frame determinism), not random at runtime |
| Confirmation pause | Leave an 11f (0.37s) breath between finishing typing and the page responding | Responding immediately after typing reads as machine-automatic, and viewers can't follow the cause and effect |
| Code typing | Terminal 2f/character; syntax highlighting colors in progressively with the typing (the current token is colored as soon as it's typed), not the whole passage changing color at once after typing | Changing color all at once is "pasting", not "writing code"; a highlight delay within half a token goes unnoticed by viewers |
| Typing on a screenshot | A background color patch covers the placeholder baked into the screenshot (keep the icon), and the text layer is laid on top and typed | Overlaying text directly ghosts against the baked-in placeholder |

(shotcraft·type-and-filter measured values)

The deterministic way to write backspace corrections (a pre-written script, not a runtime draw):

```js
// Compile "typo→pause→backspace→fix" into a character event table; the timeline just plays it back
const script = typeScript("nano-lab", {
  perChar: 3 / 30,                       // 3f/character
  typo: { at: 5, wrong: "0", pauseF: 5 } // Mistype a "0" at the 5th character, pause 5f, then backspace
});
// script = [{t:0, text:"n"}, {t:0.1, text:"na"}, ... {t, text:"nano-0"},
//           {t+0.17, text:"nano-"}, {t+0.27, text:"nano-l"}, ...]
// The render layer looks up text by t, safe for seeking in both directions
```

Camera pairing: before typing, the camera first moves up/pushes in to the input box (give the shot first, then act: the visibility axiom); the camera is locked while typing.

### ④ Cursor-action narrative

The cursor is the only "person" in a UI demo. The component is `assets/cursor.jsx` (CursorSprite / ClickRipple / a hover linkage hook, driven by two kinds of clock; see the API in that file's header comment).

The path algorithm isn't rewritten here: for Bézier arcs + converging hand tremor see best-practices §3.5, and for the GSAP proxy approach see gsap-recipes §3.5. What this move fills in is **the parameters for clicks and linkage**:

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Double-ring ripple | Two concentric rings, **starting 3f apart**, radius 14→54 / 14→78px | A single ring is too light to see; 3f apart is "the ripple of one click"; more apart looks like two clicks |
| Decoupled spread/fade | Spread out-cubic 22f, fade linear 26f | The spread should surge and the fade should be even; one curve handling both "flashes and is gone". In compact scenes it can be compressed to 10f each (type-and-filter uses the compressed version) |
| Click anticipation | Cursor scale 0.85 (power1.in about 3f) → back.out rebound | Anticipation gives the click the weight of "pressing down" (same as gsap-recipes §3.5) |
| Hover linkage | When the cursor enters the target area, the target lights up on the same frame (brightness +6% or a hairline outline appears), and reverts as soon as the cursor leaves | If the target doesn't respond, the cursor is just a pasted image; the linkage window is declared by path progress, with no runtime hit detection |
| Cursor role split | Operating cursor (clicks carry a payload) vs performing cursor (movement is the plot: a duet of named collaboration cursors / an ensemble cast) | Use this move when the cursor needs to click things; purely narrative collaboration cursors are a different scene (shotcraft·collab-cursor-moves); both can coexist in one film but don't mix them |

Quick reference for the two performing-cursor moves (for collaboration/multiplayer themes, parameters from collab-cursor-moves):

| Move | Mechanism | Key parameters |
|---|---|---|
| dialogue-duet | Two named cursors, blue and green, approach each other in conversation, swap positions on upper and lower arcs (R≈270px), their name tags hand over the light by one brightening as the other dims, and the green cursor scales up tens of times with easeIn to become the transition mask | All moves on cubic Béziers, no linear; two cursors on the same arc in the same direction feel like a collision, and the upper/lower arcs are "giving way" |
| cast-ensemble | 5 colored cursors fly in on springs, staggered with delays 0/5/9/13/17f, and stay on screen with dual-frequency sine drift (0.055/0.021 rad/f, amplitude ±46/30px), with one doing a typing cameo | Name tags fading in 12f late is what reads as "people arriving and introducing themselves"; after gathering, drift decays and keeps 25%; a completely still cursor group reads as frozen |

Known pitfalls: cursor movement must obey the visibility axiom throughout; if the target is off-screen, move the camera first, then the cursor; the name tag color of a collaboration cursor = identity coding, consistent across the whole film, and changing color midway makes viewers think it's a different person; a drifting cursor must never cover the main content being read.

Camera pairing: after the click is confirmed, the camera pushes in over 16f (zoom≈2.2) through to the detail page, the standard handoff for "click→enter" (type-and-filter); for how to join transitions see `camera-language.md`.

### ⑤ Timeline-driven UI state transitions

Tab switches, modal pop-ups, page route pushes. **Timeline-driven playback and an interactive prototype are two different forms of code**; when turning a prototype into a render version, translate item by item:

| | Interactive prototype | Timeline playback (for rendering) |
|---|---|---|
| Trigger | `addEventListener('click')` | A label / position parameter on the timeline |
| State switch | `classList.add` + CSS transition | Explicit tween (gsap-recipes §6.1 no-go rules) |
| Open/close | Toggling `display: none` | `autoAlpha` tween |
| hover | The `:hover` pseudo-class | A linkage window declared by path progress (Eight Moves ④) |
| Randomness | `Math.random()` | Pre-generated with a mulberry32 seed (gsap-recipes §6.4) |

After the rewrite, clear every hit of `grep "addEventListener\|classList\|transition:"` one by one. State must be a pure function of time; every bug that looks fine in preview and only breaks in the render comes from this.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| modal / command palette | Background darkens over 10f to rgba(20,20,20,0.45) + blur 10px; panel −20px→overshoot +8px (9f)→settles back (6f); candidate rows staggered by i·4f | Without the background darkening, the panel doesn't "float on top"; an 8px overshoot is a "soft landing", any more becomes toy-like |
| tab switch | The indicator bar slides with FLIP (best-practices §4.1), old content fades out over 5f sinking 8px, new content fades in over 8f rising | The indicator bar and content being out of sync is where cheapness comes from: the bar moves first, the content follows half a beat later |
| Route push | The new page pushes in whole from the right over 12-16f, the old page retreats 30% of the distance in the same direction + darkens | The old page retreating a short distance (parallax) reads deeper than an equal-distance push; equal distance is a "conveyor belt" |

(The modal parameters are shotcraft·command-palette-summon measured values)

Known pitfalls: state transitions are the hardest-hit area for "one shot, one motion": in one transition the tab switches, a toast pops up and the data scrolls, and the viewer sees nothing clearly; one shot plays only one state change.

Camera pairing: the camera must be still at the instant of a state switch and only move after it's done (huarec shot-to-shot grammar: change consumes attention, don't stack it with camera motion).

### ⑥ 3D interface tour

A shot that shows the "sense of space" of a long interface/multi-screen interface. The two cards have a clear division of labor, and picking the wrong card is this move's main accident:

| Card | Mechanism | Use |
|---|---|---|
| steep-tilt-glide | **Camera still, page moving**: the page is tilted at rotateY −60° and glides across the frame at a constant speed by itself | Pages parade past as "exhibits"; the content doesn't need to be readable, what's on show is scale and texture |
| graze-face-tour | **Camera moving, page still**: a group of pages hovers in place, and the camera tours them up close | When local content needs to be readable during the tour; the camera has a "visitor" persona |

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Tilt angle | rotateY −60°, practical ruling range 55-65° | −45° was judged "not steep enough"; beyond −70° the content can't be read |
| Hover height | 120-180px (graze-face-tour) | Too low and it hugs the ground with no "display" feel; too high and the shadow disconnects |
| Group stagger | Stagger the start points but let the drops overlap in parallel | A fully sequential drop is "queuing to clock in"; overlap is "a batch arriving" |
| Joining segments | Cross-fade ≥8f | Hard cuts flash black; the tour is a continuous space, jump cuts are not allowed |

(shotcraft·steep-tilt-glide / graze-face-tour measured values)

A third variant for showing many pages on one screen (shotcraft·page-waterfall-wall): a 3-column waterfall wall of pages, rotateX 20° + perspective 1000px, adjacent columns with loop periods differing by ≥25% (e.g. 12/9/14s) and the middle column reversed. Suited to the "the product has lots of pages" statement of scale in the closing segment, where the content doesn't need to be readable. When the periods differ by less than 25%, the three columns periodically line up, and the "wall" instantly turns into a "table".

Known pitfalls: the mechanisms of the two cards can't be mixed; if the page and the camera move at the same time, the viewer loses the frame of reference (dizziness); the page textures used for the tour must be 2x or more, since they blur fastest after being tilted and magnified.

Camera pairing: this move is itself the star of the camera work, so the shots before and after should be still (alternating energy); for camera paths and orbit vocabulary see `camera-language.md`.

### ⑦ Long-page scroll narrative

The "fast scroll, hard brake" of a long landing page/document/timeline. The scrolling itself isn't the content; **the braking point is**.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Braking curve | One `Easing.out(Easing.exp)` curve covering the whole run in 50f | Segmented deceleration "pumps"; a single expo curve is naturally "hard scroll, gradual stop" |
| Motion blur | Blur driven by the frame-to-frame displacement difference: high speed is blurry, it's sharp as soon as it stops | Constant blur is "the lens is dirty"; blur only exists in the moving moments, and still frames are always sharp (the same conclusion as huarec) |
| Target row emphasis | After stopping, the target row goes to scale 1.03, and the rest dims to 0.38 | Don't dim to 0, the context needs to stay; 1.03 is a "breath", not a "pop" |

(shotcraft·scroll-brake-moves measured values)

Budget management for multiple braking points (the huarec comfort budget, taken as is): ≥2.6-3.0s between two adjacent "scroll + brake" actions; ≤4-5 times in any 15s window; stay on each braking point for ≥1.2s before scrolling again. A braking point consumes attention, and costs more than the scrolling itself.

Known pitfalls: no push-ins while scrolling, "pushing in while scrolling is dizzying" (huarec: don't push the camera during full-screen-level changes); when the braking point has no content emphasis (the target row doesn't lift, the rest doesn't dim), viewers don't know why it stopped there.

Camera pairing: after the hard brake you can follow with one light push-in (1.3x level) to the target row, but only after it has come completely to rest; for the level table see `camera-language.md`.

### ⑧ Feature callout annotations

"Pointing things out to the viewer" on a real screenshot. Four sub-recipes, with a shared principle: **the annotation is a tour guide, not part of the interface**, and stylistically it should sit one layer apart from the product UI (serif type/a handwritten feel/accent color).

| Sub-recipe | Parameters | Tuning feel |
|---|---|---|
| Growing annotation line | SVG path drawn with stroke-dashoffset, 12-18f, out-cubic; line first, then text, the text fading in 5f after the line arrives | Line and text appearing together reads as a sticker; the line is the time of "a finger swiping across" |
| Highlight box | A rounded-rect outline around the target area expands over 8f + the area outside the box darkens to 0.3 | Outlining without darkening doesn't focus the gaze; darkening beyond 0.5 becomes an interrogation lamp |
| Magnifier | A circular loupe embedding a 2-3x high-res slice (not CSS-magnifying the screenshot base), 2px outline + soft shadow, pops out with an 8f overshoot, follows the target with a 10-14f slow drift | The loupe must contain a high-res slice; magnifying a blurry texture is exposing your own poor assets; at most one loupe per shot |
| Connected caption card | The caption card floats in 3D space, translateZ on the order of 90px + a bob period close to but not in sync with the subject | Same 3D space, same camera; flat overlaid text was vetoed in precedents (the same constraint as spotlight-hero-card's floating annotation) |
| before/after slider | Quick flick 12f (out-cubic 8%→76% overshoot rebounding to 70%) → pause 18f → slow sweep 48f to 40% and freeze; speed ratio 5:1; the after layer's clip-path follows the bar; the handle's speed difference drives a slight scaleX stretch peaking at 1.18 | Below a 3:1 speed ratio the rhythm contrast isn't perceptible; the quick flick announces "it changed", the slow sweep proves "where it changed"; stopping the slow sweep at 40% keeps the after state in the freeze frame |

(The slider values are shotcraft·before-after-slider-scrub measured values)

Known pitfalls: the before and after versions must have the same layout and the same camera position, or they read as two pages; before uses the real old state (inject old data/turn the feature off), not a hand-built "deliberately ugly" fake before; put the corner badge in the content area, not over the sidebar avatar.

Camera pairing: before the annotation appears, the camera first pushes to the 1.3-1.45x level so the target area fills the screen (huarec: content takes up 80% of the visible area), and the camera is locked during the annotation.

---

## §3.9 Where the Eight Moves sit in the film's energy skeleton

A single move is just a shot; the finished film has to be arranged by the four promo-energy-arc stages (shotcraft·the director-layer trio; the storyboard discipline "carve out the hold/rest frame budget first, then arrange the motion" applies as well):

| Energy stage | Share of duration | Which moves go there | Reason |
|---|---|---|---|
| ① Brand opening | 8-12% | No UI moves | Wordmark hold ≥1s; the UI shouldn't steal the opening |
| ② Single-hero showcase | 12-15% | ① hero close-up or ② build-up | The shot with the highest polish and slowest rhythm; there's only one slot for it in the whole film |
| ③ Feature climb | 55-65% | ③④⑤⑦⑧ alternating, each shot tied to one distinct feature | Medium-high and low energy alternating; ⑧ callout is a good filler for the low-energy breathing slots |
| ④ Launch-event close | 13-16% | ⑥ 3D tour (group-shot variant) | The film's energy peak, sign-off after a multi-screen group display |

Quick reference for sound hooks (only done after the picture is locked; pin to frames with relative expressions, shotcraft stage 5):

| Move | Which sound to pin |
|---|---|
| ① hero close-up | A whoosh-big on the lift, a sparkle on the beam, a snap on the reseat: three actions, three dedicated sounds |
| ② build-up | A pop on the swap-to-real beat, an extremely soft tick for each row's reveal, a soft chime to close at the half-beat-late last word |
| ③ typing | The keyboard sound must be exactly as long as the typing segment (cut by character count); if it's short, cut the segment; if it's long, trim the sound |
| ④ click | The click is the loudest sound in the film (the top of the loudness hierarchy), the ripple is silent |
| ⑤ state transition | One soft pop for a modal pop-up, one whoosh-fast for a route push |
| ⑥⑦ tour/scroll | Silence or an extremely soft hum in constant-speed segments, one dull thud on the hard brake |
| ⑧ callout | An extremely soft draw friction sound for the growing annotation line; whoosh + rebound tick for the slider's quick flick, the slow sweep is silent |

---

## §4 Rhythm iron rules (inherited from shotcraft precedents, specific to UI demos)

1. **Interactive demos run at real human operating speed.** Typing at 3f/character, movement before a click, a breath before a response. The first version of an interactive shot is almost always too fast, so draft at human speed from the start (precedent R3; type-and-filter was reworked because of this).
2. **Batch motion closes out with 0.5s of stillness.** Once the grid has converged, the list has finished embedding, the panel has landed, hold the full board still for half a second before moving to the next shot.
3. **Exits must be staggered.** Non-target elements fade out staggered in reading order at 0.4f intervals; "disappearing at the same time reads as the page crashing", and even a 0.4f difference is enough (type-and-filter).
4. **One shot, one motion.** A shot features only one UI behavior; two motions on screen at once steal each other's scene, and the viewer sees neither.
5. **The close is truly still.** Breathing slots and hold frames forbid any tail drift (tiny zoom changes and opacity tweaks both count); "stillness" is a designed beat, not a gap where no action was scheduled.

---

## §5 Connecting to the three-directions gate / asset protocol

**How to produce the three direction boards**: the three directions for a product UI animation are not three visual skins, but **three camera-narrative interpretations of the same UI assets**. Collect the asset trio once and reuse it across all three directions. For example, with the same product screenshot: direction A uses Eight Moves ① (a single-hero hero close-up showcase), direction B uses Eight Moves ② (build-up from nothing, telling the story of generation capability), direction C uses Eight Moves ⑥+⑦ (tour + scroll narrative telling the story of scale). Each direction board comes with 2-3 keyframe thumbnails, so what Huashu chooses is "how to tell the story of this interface", not "which image looks nice". The three-directions gate is a 100% hard gate, and a specified style doesn't exempt it either (an existing SKILL.md rule).

**UI screenshot sourcing goes through `brand-asset-protocol.md`**: in that protocol, a digital product's UI screenshots are first-class assets (they contribute extremely highly to recognizability), and the collection channels, the 5-10-2-8 quality bar and locking into brand-spec.md all apply as is. This file adds only one thing: when collecting, follow the §1 asset trio spec (2x full page + transparent-background slices + layout.json), collecting everything in one go, which is enough for both the camera-move path and the rebuild path.

**Hand-built fake UI is forbidden**: when you can't find real screenshots, fall back as the protocol says (ask the user for real captures / take frames from official demo videos); don't patch something together with a mockup generator, and don't draw a "close enough" interface in CSS. What we're expressing is this product, not "a product".

**There's only one exception**: when you take Path 2, the HTML rebuild, the rebuild itself is "a replica based on the real screenshots", and must be checked against the screenshots block by block (fonts, corner radii, spacing and icons are all measured from the screenshots); once the rebuild is done, capture frames side by side with the screenshots to compare. Rebuilding a "roughly similar" interface hurts more than just using the screenshot, because viewers are extremely sensitive to errors in a product interface they use every day.

---

## §6 Pre-delivery self-check (UI demo specific, supplementing best-practices §7)

- [ ] Did you go through the §1 decision tree? Did you avoid rebuilding HTML in a scenario where "the screenshot is enough"?
- [ ] Do sliced elements return to their real slots in layout.json after moving?
- [ ] Are the cursor and operations inside the visible area throughout (including the 8% margin)?
- [ ] Is user typing at a character-by-character 3f rhythm, with only AI output using Chunk Reveal, and the two not mixed up?
- [ ] Is the cursor steady-on while typing and only blinking when done? Do clicks have a double-ring ripple?
- [ ] Are there no leftover addEventListener / classList / CSS transition in the state transitions?
- [ ] Are batch exits staggered ≥0.4f, with the full board still for 0.5s at the close?
- [ ] Does only one shot in the whole film use outline light/glint, and only for the star?
- [ ] Do before/after share the same layout and camera position, and is before the real old state?
- [ ] Are the three direction boards three camera interpretations of the same UI assets, not three skins?

---

## §7 Quick reference for common failure modes

| Symptom | Root cause | Which section to go back to |
|---|---|---|
| "Not tech enough", so particles/glow get added | The direction itself is wrong; the quality gap is in real UI and camera work | Opening claim + §1 |
| The interface looks like an image hanging on the canvas | No device frame, no shadow language | §1 device frame + Eight Moves ① double shadow |
| Text is blurry after pushing in | Insufficient screenshot magnification or a rasterization resolution issue | §1 asset trio + camera-language.md |
| Interactions "feel scripted, not human" | Typing/clicking/responses all run at machine speed | Eight Moves ③④ + §4 iron rule 1 |
| Fine in preview, breaks in the render | Event-driven state got mixed into the timeline | Eight Moves ⑤ comparison table + gsap-recipes §6 |
| Viewers say "it's a bit dizzying" | The camera and the page move at the same time, or braking points exceed the budget | Eight Moves ⑥⑦ + huarec budget |

---

## Appendix · Relationship with other files

| File | Relationship |
|---|---|
| `camera-language.md` | Camera vocabulary, camera-move motivation, camera rig implementation. This file says "which shot to pair", that one says "how to make the shot" |
| `animation-best-practices.md` | The master outline of element-level motion grammar. §3.5 mouse paths, §4.1 FLIP and §4.5 Chunk Reveal are cited by this file |
| `gsap-recipes.md` | The implementation-layer translation. The §3.4/§3.5 proxy recipes and the §6 seek-safety rules are prerequisites for executing every recipe in this file |
| `brand-asset-protocol.md` | The sourcing protocol for UI screenshots. This file's §1 asset trio is its spec-level extension |
| `assets/cursor.jsx` | The component implementation of Eight Moves ④, used together with `browser_window.jsx` / `macos_window.jsx` |
| `apple-gallery-showcase.md` | Multi-output same-screen displays go there; single-product UI narratives go in this file |
