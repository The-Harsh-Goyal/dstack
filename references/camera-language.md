# Camera Language · Camera Direction System

> **When to read this file**: before any "camera-level" motion appears on screen (zoom / pan / orbit / parallax /
> transitions / establishing shots and final bows). Whenever what moves is the "camera" rather than an "element", read this before writing the timeline.
> How elements move (entrances/stagger/physicality) belongs to `animation-best-practices.md`;
> this file answers **when the camera moves, how much, for how long, and how shots connect to each other**.
> For runnable GSAP implementations (the rig container, PageCam translation, the logarithmic duration helper), see
> the "Camera Rig recipes" section of `gsap-recipes.md`; this file only gives design judgment and formulas.
>
> Source-labeling convention for parameters: **(HuaRec)** = parameters measured in the HuaRec Studio camera direction system;
> **(shotcraft)** = the video-shotcraft 106-card shot system; **(measured)** = hands-on project work in this skill;
> **(inferred)** = borrowed from general film vocabulary, parameters still to be calibrated by measurement.

---

## §0 · Thesis · Camera motion runs on a budget, not on effects

Camera motion in most AI-generated animation follows an "effects" mindset: add a zoom wherever a zoom fits, and the more the camera moves, the more "premium" it looks.
This is the common source of both dizziness and cheapness. The correct mental model comes from two axioms (HuaRec):

- **A1 Visibility invariant**: at any moment, what the viewer should be looking at must be inside the visible area (including an 8% safe margin).
  A shot that violates this should drop its magnification, be merged, or not be shot at all.
- **A2 Comfort budget**: every camera change is a spend of attention and must be managed as a budget.
  Once the budget is spent, even a great shot doesn't get shot.

| Budget item | Typical value | Tuning feel |
|---|---|---|
| Interval between adjacent camera changes | ≥2.6-3.0s (restrained tier 5.0s) | Below 2.6s viewers start getting dizzy; MTV-style fast cutting doesn't suit product demos (HuaRec) |
| Camera changes in any 15s window | ≤4-5 (restrained tier 3) | If over, cut the shot with the weakest motivation; don't compress the intervals (HuaRec) |
| Push-in magnification floor | 1.25x | Below 1.25x the visual change of a zoom isn't perceptible enough and reads as mere wobble, so don't shoot it (the 1.06x establishing shot is the only exception) (HuaRec) |
| Push-in magnification ceiling | 2.3x (restrained tier 1.8x) | Higher than this and pixel density can't hold up; change the source material before talking about magnification (HuaRec) |
| Shots per minute | Restrained ≤4 shots/min, standard ≤6 shots/min | "Leave room to breathe, it's not MTV" (HuaRec) |

Stack two more style axioms on top (shotcraft):

1. **Cinematic feel = camera motion × light and shadow × rhythm × sound, not flashy animation**. Passing on all four dimensions beats maxing out one.
2. **The rhythm preference runs one way: slower rather than faster**. All historical user feedback points to "slow down/linger"; not a single piece points to "speed up".
   When unsure about a duration, choose the longer one; when unsure whether to move the camera, choose not to.

These two share a root with "courtesy to the viewer" in best-practices §0.2: the camera makes decisions on behalf of the viewer's eyes,
and the fewer and more precise those decisions, the more the viewer trusts you.

---

## §1 · Camera vocabulary · Camera motivation decision table

For every camera move, ask about motivation first: **what question does this shot answer for the viewer?** If you can't answer, don't move.

| Shot | Motivation (when to use it) | Parameter range | Don'ts |
|---|---|---|---|
| **push in** | "Look here next": focus on a specific UI element / data point / keyword; rising tension | Magnification tiers 1.3 / 1.45 / 1.8 / 2.3 (see §4); duration follows the logarithmic formula; enter 0.15s early (HuaRec) | Don't push below 1.25x; don't push during full-screen changes such as scrolling / page switches / video playback ("pushing in while scrolling causes dizziness"); don't move the camera mid-narration (see §6 move on pause) (HuaRec) |
| **pull out** | Reveal the whole picture and context: "so it belongs to a bigger system"; closing bow | Duration follows the same logarithmic formula; final bow pulls out over 0.55s + ≥0.8s wide-shot pause (HuaRec) | No "out-in-out" pumping: when the gap between shots is shorter than the transition time, go straight to the next shot without returning to 1x (see §5) (HuaRec) |
| **pan** | Move between two mid-distance focal points (normalized distance 0.22-0.45); sweep across several parallel elements in one shot | Only worth panning if the combined magnification is ≥1.25; diagonal pans use a dual-frequency sine (X/Y frequency ratio 0.22:0.35, amplitude 30-40px) (HuaRec / existing in this skill) | Don't pan if the focal distance is >0.45 (diagonal jumping); drop the shot; a pure single-axis pan feels mechanical, so prefer diagonal |
| **orbit** | Texture close-up of a single protagonist, the shot with the strongest "physical presence"; a hero element's showcase moment | rotY-led + persp 1100-1200px; measured camera positions rotX46/rotY−30/rotZ9 → rotX42/rotY26/rotZ−7 (shotcraft) | Any one technique gets to be the star only once per film (shotcraft); not for information-dense frames (camera position serves readability; with lots of text, face it head-on) |
| **dolly zoom** | The reveal moment of a "worldview reversal": the subject stays the same while the context changes drastically | See §8 for the fake recipe: subject pinned, background scale 1→2.0-2.5 + opacity ≤0.6 (shotcraft) | At most once per film; using it without a narrative drop = pure showing off |
| **Static** | Reading text, real-speed interaction demos, information-dense shots; the default answer when the budget runs short | Brand wordmark lands and holds ≥1s; 0.5s of stillness after batch motion ends; opening subject action arc ≥3s (shotcraft) | None. Staying still is always a legitimate choice; "no camera move" is itself a directing decision |

Two cross-cutting rules:

- **A sense of speed comes from acceleration, not from fast constant speed** (shotcraft). Constant-speed motion reads as cheap PPT;
  for a feeling of "fast", use a short burst of acceleration + a long ease-out, not halving the whole duration.
- **Camera position serves readability** (shotcraft): face information-dense shots head-on; for text close-ups use a side-on horizontal camera position
  (rotY-led, very small rotX); no one-size-fits-all global tilt; product promo films get no handheld shake by default.

---

## §2 · Choosing zoom vs dolly · Ruling on real vs fake 3D

"Push in" has two implementations that look completely different. Choose first, then write code:

| Dimension | zoom (scale) | dolly (perspective + translateZ forward) |
|---|---|---|
| Parallax | None. All layers scale up proportionally; the frame is "one image being enlarged" | Yes. Near layers move fast, far layers slow; the frame is "the camera moving forward through space" |
| Feel | Clean, informational, suits UI close-ups / data focus | Spatial, cinematic, suits hero showcases / atmospheric passages |
| Cost | Low: a single transform | High: needs a layered structure + preserve-3d, and has the rasterization blur problem (§3.4) |
| Selection rule | Content is flat information (interfaces, documents, charts) → zoom | Content has clear "foreground/subject/background" layers, and those layers are worth seeing → dolly |

**Ruling on real vs fake 3D** (the boundary line that resolves two contradictory older passages in this skill):

- **≤8** elements involved in 3D → use real translateZ layering (apply the golden-angle recipe from best-practices §4.7 as is)
- **≥20** elements → give up on real 3D and fake depth with shadow / blur / brightness differences (the stance of hero-case-study)
- Between 8 and 20 → ask one question: does this shot need parallax? Only use real 3D if it does; otherwise fake the depth.
  The cost of real 3D isn't in writing it, it's in tuning it: every extra layer adds another set of "perspective distortion + blurry text + layer interpenetration" to troubleshoot.

---

## §3 · Camera Rig implementation conventions

Camera motion and element animation **must not fight over the same transform**. All camera-level motion is funneled into one dedicated container.

### 3.1 Layered container structure

```html
<div id="viewport">          <!-- Fixed viewport, overflow: hidden, holds perspective -->
  <div id="camera">          <!-- Camera layer: carries only the camera transform, does nothing else -->
    <div id="world">         <!-- World layer: all frame content lives here; element animation only moves things inside world -->
      ...scene content...
    </div>
  </div>
  <div id="hud">             <!-- Captions / corner badges / chrome: sibling of #camera, naturally doesn't move with the camera -->
  </div>
</div>
```

Iron rules for division of labor:

- Only camera tweens (translate / scale / rotate / zoom properties) appear on `#camera`; element entrances, stagger,
  and hover states are always written on elements inside `#world`. The two layers don't know about each other, so the camera can be rearranged wholesale at any time without touching element animation
- Captions and chrome **go in `#hud` first**, staying still at zero cost; only labels that "must follow some element in world
  but keep a constant font size" (such as a following tooltip) get a counter-transform on that element:
  `scale(1/zoom)` cancels out the camera scaling, updated every frame in sync with the camera
- **transform-origin is the push-in target point**: for a flat zoom, set the origin to the center of the target element and then scale,
  which is equivalent to "pointing the camera at it and pushing in". In PageCam mode, cx/cy take on the same role

### 3.2 PageCam keyframe model (shotcraft, 2.5D camera math)

Define the camera state as a keyframe object; camera motion = interpolation between keyframes:

```
{ frame, cx, cy, zoom, rotX, rotY, rotZ, persp }
```

cx/cy is **the point in world coordinates the camera is aimed at**, and zoom is the magnification. Using a 1920×1080 canvas as the example
(for other sizes, replace 960/540 with W/2, H/2):

**Flat mode** (no rotation, pure zoom + pan):

```
transform: translate(960 − cx·zoom, 540 − cy·zoom) scale(zoom)
transform-origin: 0 0
```

**3D mode** (with rotX/rotY/rotZ):

```
Outer layer (#camera): perspective: persp·zoom;  perspective-origin: 960px 540px
Inner layer (#world):  zoom: {zoom};                        /* note: this is the CSS zoom property, see §3.4 */
                Tx = 960/zoom − cx;  Ty = 540/zoom − cy
                transform: translate(Tx, Ty) rotateY() rotateX() rotateZ()
                transform-origin: cx cy
                transform-style: preserve-3d
```

Typical camera position parameters (shotcraft, measured): full page zoom 0.78 → close-up 2.6;
side shot rotY34 / rotX8 / persp1200 (side shots beat top-down shots; rotY-led with just a little rotX);
for orbit start and end positions, see the §1 table.

### 3.3 Rig construction notes (camera-specific pitfalls)

- **Pan exposes the edges**: `#world` must be larger than the viewport (bleed on all sides ≥ the maximum pan amplitude + an 8% margin),
  or panning exposes blank space outside the canvas. This is the flip side of the A1 visibility axiom: what shouldn't be seen must not be visible either
- **perspective gets broken**: any intermediate layer between `#camera` and `#world` with
  `overflow: hidden`, `filter`, or `opacity <1` creates a new stacking context,
  which kills preserve-3d and instantly flattens the 3D layering. In 3D mode, apply filter effects only to the innermost elements
- **Per-frame out-of-bounds fallback** (HuaRec): when the camera focus follows a moving point, check every frame whether the target leaves the visible area;
  if it does, keep the magnification and make only the minimal correction along the overflowing axis to pull it back to the edge. Better for the camera to "give way" than to let the target leave the frame

### 3.4 CSS zoom rasterization technique · Curing blurry 3D text for good (the most expensive knowledge in the whole library, shotcraft)

**Problem**: in 3D mode, if you enlarge the page with `transform: scale()`, Chromium rasterizes at the element's layout size
and then enlarges the bitmap, so the text is guaranteed to blur. The higher the magnification, the worse the blur; above 2x it's undeliverable.

**Solution**: don't enlarge with `transform: scale`; use the **CSS `zoom` property**. `zoom` is layout-level scaling, so
Chromium re-lays out and rasterizes at the enlarged size, and text stays vector-sharp at any magnification.
That's exactly why the inner layer in the §3.2 3D-mode formula is written as `zoom: {zoom}` rather than `scale({zoom})`.

Supporting points:

| Point | How | Source |
|---|---|---|
| Coordinate compensation | `zoom` changes the layout coordinate system, so translate amounts must be divided by zoom: `Tx = 960/zoom − cx` (already in the §3.2 formula) | (shotcraft) |
| Relationship to the reflow ban | gsap-recipes §6.2 bans tweening layout properties because of integer snap jitter; `zoom` is page-level scaling, so the snapping is imperceptible, and the text-sharpness gain far outweighs it. **This technique is the only legitimate exception to §6.2, and it is used only on the `#world` camera layer** | (measured) |
| Render environment | Fully applicable under HyperFrames / Playwright offline frame-by-frame seek rendering: the cost of re-laying out every frame doesn't affect the output, only the render time. Real-time browser preview may drop frames; that's normal, and the rendered output is what counts | (shotcraft) |
| Bitmap asset enhancement | Take full-page screenshots at 2x sampling; prepare separate 4x screenshots of close-up elements and use a 6f crossfade during the push-in to cover the low-magnification texture | (shotcraft) |
| Depth-of-field atmosphere | DoF is atmosphere only: a gradient band of blur + mask at the top, no true per-layer depth of field | (shotcraft) |

---

## §4 · Camera easing and duration

### 4.1 Easing vocabulary

| Scenario | easing | Tuning feel |
|---|---|---|
| Active camera moves (push in/pull out, with clear start and end points) | `cubic-bezier(0.65,0,0.35,1)` = GSAP `power3.inOut` | Steady at both ends, the feel of "the director giving you a shot"; **never linear, never spring overshoot** (HuaRec) |
| Following camera moves (the camera chases an action that has already started) | `cubic-bezier(0.33,0,0.15,1)` | Brisk departure, very long braking; the camera seems to "catch up" rather than "cut over"; the shotcraft camera default |
| Continuous drift (idle drift, constant-speed tours) | `sine.inOut` yoyo or `none` | The only scenario where constant camera speed is allowed (an existing rule in gsap-recipes §1); banned for moves with start and end points |
| Cursor/focus follow smoothing | `quickTo` + ~0.15s smoothing; Catmull-Rom path interpolation | Zero-phase idea of forward + backward EMA: follows tightly without jitter (HuaRec) |

Ruling when the two sets of defaults conflict: for a single push or pull, trust HuaRec (power3.inOut); for compound movement
and multi-segment continuous shots, trust shotcraft (0.33,0,0.15,1).

### 4.2 Logarithmic zoom duration formula (fixed durations are a source of amateurishness)

All push and pull durations are determined by the change in magnification, so zooms of any size have the same "visual speed":

```
duration = 0.55 × |ln(zoom₂ / zoom₁)| / ln 2      clamped to [0.30, 0.94] seconds
```

A 1→2x push-in is exactly 0.55s; 1→1.3x is about 0.30s (hits the floor); 0.78→2.6x hits the ceiling at 0.94s. (HuaRec)
Big framing changes take longer and small ones shorter, preventing both "jumping into place" and "dragging".

### 4.3 Zoom tier table

| Tier | Magnification | Use | Tuning feel |
|---|---|---|---|
| Establishing micro-push | 1.06x | Only for the opening establishing shot (§6); viewers don't perceive a zoom, only that "the frame is alive" | The only tier allowed below 1.25x (HuaRec) |
| Light push | 1.3x | Hinting focus: doesn't interrupt overall reading, just "notice this area" | |
| Medium push | 1.45x | Standard UI close-up: a panel / a block of code | |
| Heavy push | 1.8x | Single-element close-up: a button / a number | The ceiling of the restrained tier (HuaRec) |
| Ceiling | 2.3x | Extreme close-up; the source material must hold up (2x screenshot / 4x slice, §3.4) | Beyond this, change the material; don't force the push (HuaRec) |

Framing formula (HuaRec): `scale = 0.8 / max(target bounding box normalized width, height)`, then clamp it into the tier range.
Content takes up 80% of the visible area, leaving 20% to breathe; don't fill edge to edge.

### 4.4 Rhythm budget (linked to the §0 budget table)

- Interval between adjacent camera changes ≥2.6-3.0s; ≤4-5 per 15s window (HuaRec)
- Enter the shot 0.15s before the action (the camera arrives first, the action happens after), and stay 1.2s after the action ends before moving on (HuaRec)
- Isolated small actions shorter than 1.2s aren't worth their own shot; prevents "one click, one pump" (HuaRec)

---

## §5 · Shot-to-shot grammar · The core of preventing dizziness

**Dizziness isn't caused by individual shots; it's caused by how shots are joined.** "Out-in-out" pumping and consecutive jumps between distant focal points
account for the vast majority of the dizzy feeling (HuaRec). For two adjacent shots (interval <1.5s), split three ways by focal distance:

| Normalized focal distance | Join | Notes |
|---|---|---|
| <0.22 (near) | **Merge shots** | Combine into one shot: recompute the magnification from the union bounding box of both targets and see both in one shot |
| 0.22-0.45 (mid) | **Switch to a pan** | Rather a slightly wider magnification (combined magnification ≥1.25) and pan over in one shot than "out and back in" |
| >0.45 (far/diagonal) | **Drop the shot** | Cut the shot with the weaker motivation. **Never shoot two distant focal points back to back**; diagonal jumping is the dizziest join of all |

Two more timing rules (HuaRec):

- **If the gap is short, join directly**: when the gap between adjacent shots is shorter than the transition time, don't return to 1.0x; transition directly from the current magnification to
  the next shot's magnification and focus. Returning to 1x and pushing again is the direct source of the "pumping" feel
- **Only allow "pull out then push in" if the gap is ≥1.5s**: viewers have enough time to reorient in the wide shot, so out-in doesn't cause dizziness

---

## §6 · Cinematic openings and closings · Establishing shot, final bow, move on pause

Three grammar rules that cost very little and noticeably raise the sense of a finished work (HuaRec):

1. **Establishing shot**: when the film is >14s long and the first real shot comes after 7s,
   insert a **1.06x center micro-push** over [0, 3.0s] at the start: open already in a light push-in state and ease out back to the wide shot within 3 seconds.
   The viewer's first impression is "the camera is alive", not "the PPT has started playing"
2. **Iron rule of the wide-shot final bow**: wrap up the last shot early, leaving a 0.55s pull-out transition + a **≥0.8s wide-shot pause**.
   The finished film always ends on a still wide shot and **never stops abruptly in a pushed-in state**. This is fully compatible with the best-practices
   "abrupt stop + hold" ending: the frame that holds must be a wide shot
3. **Move on pause**: cut on action, move on pause. In narrated animation, if a camera move collides with
   the middle of speech, snap it earlier to the nearest speech silence (move it at most 0.8s earlier, **only earlier, never later**).
   Shifting the viewer's gaze during an audio gap has the lowest cognitive cost. When the narration pipeline (voiceover-pipeline.md) lays out shots,
   it uses the gaps between narration clauses directly as snap points

---

## §7 · Transition grammar table · Three layers of vocabulary

Transitions are an independent layer: choose the type for each seam by **energy drop**, use only one type per seam, and take the transition frames out of the adjacent shots' budget.
"The widely acclaimed launch films never have a single bare cut from start to finish" (shotcraft).

### 7.1 Six shot-transitions (transitions with presence, for seams with a big energy drop)

| Type | Energy drop it suits | Parameters | Pitfalls |
|---|---|---|---|
| flash-wash | High→high, strong section change | White frame peaks for 2-4f, with a 5f ramp on each side | The white flash only covers the cut point; don't reuse it as decoration |
| dip-to-dark | High→low, downshifting the mood | Darken to around rgba(20,20,20,0.9), total length ≤0.6s | Don't linger in the dark frame, or viewers think the film has ended |
| defocus-handoff | Mid→mid, switching between topics of equal weight | Outgoing blur 0→8px overlapping incoming blur 8px→0 for ≥8f | Large-area blur ≤24px (DoF performance constraint) |
| title-card (on black) | Chapter-level separation | Card holds ≥1s, with a 0.3s transition before and after | ≤2 per film; more than that looks like a slideshow |
| whip-pan | Low→high, a sharp rise in energy | Hold ≥20f at both ends → 8f whip across 1.5 screens; peak ≥300px/f to blur fully (shotcraft) | Too slow and it's just an ordinary pan; if it doesn't blur fully, it exposes the trick |
| mask-wipe | Spatial move, "passing through one interface into another" | Mask edge easing `(0.4,0,0.6,1)` (shotcraft) | The mask shape must come from an element already in the frame (window/card rounded corners); a shape from nowhere is slop |

### 7.2 Three hidden-cuts (transitions where viewers don't notice a cut happened)

| Type | How | Source |
|---|---|---|
| flash-cut | A white flash straddles the hard cut point, 5f on each side, covering only the cut point | (shotcraft, empirically validated parameters) |
| Foreground-occlusion cut | Switch scenes the moment a foreground element (card/panel/cursor hand) sweeps across the full screen | (inferred: general film vocabulary, parameters still to be measured) |
| Motion-blur cut | Hard cut on the peak frame of high-speed motion, with matching motion direction on both sides, so motion blur swallows the cut point | (inferred: general film vocabulary, parameters still to be measured) |

### 7.3 Two travel transitions (spatially continuous transitions: no energy drop, the scene is moving)

| Type | How | Pitfalls |
|---|---|---|
| Shared-element homing | An element from the previous shot (logo/card) moves continuously to its new position in the next shot; the camera version of the FLIP idea | The element must have the same identity in both shots; too much deformation breaks the perception of "the same thing" |
| Letter-counter fly-through | The camera pushes through the counter of a large letter (the hole in O/D/0) into the next scene | The counter must be big enough (≥1/3 of screen height); the zoom during the fly-through uses the logarithmic duration ceiling of 0.94s |

Quick selection: big energy drop → pick one of the six; don't want it noticed → hidden-cut; two scenes that are spatially continuous → travel.
Hard cuts aren't banned; they "must be wrapped by any one of the layers above".

---

## §8 · Multi-layer parallax recipe · Fake dolly zoom

### 8.1 Parallax layer speed coefficients (shotcraft)

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Layer speed coefficients | Background 0.35 / midground 0.7 / foreground 1.4 (multiples of camera displacement) | Adjacent layer speed ratios must be **≥2x** to be distinguishable; viewers can't read a 1.2x difference |
| Number of layers | ≤4 layers | Nobody can perceive parallax beyond 4 layers; it's pure budget waste |
| Implementation | Each layer translates by the same camera x/y multiplied by its own coefficient | Everything is derived from the camera state, so it's seek-safe; don't give each layer its own tween |

### 8.2 Fake dolly zoom (pure CSS, no real 3D needed)

```
Subject: pinned in place (or at most a ≤1.02x breathing motion)
Background: scale 1 → 2.0-2.5, while opacity drops to ≤0.6
```

The subject stays put while the background surges toward the viewer, creating the reversal feeling of "the world closing in while the protagonist freezes" (shotcraft).
Give it enough time (≥1.2s). For usage, see §1: at most once per film, saved for a true reveal moment.

---

## §9 · Motion-derived signals · Blur / follow / aftershock

The camera's "sense of speed" doesn't come from shorter durations; it comes from secondary signals **derived** from velocity (shotcraft / HuaRec):

| Signal | Formula | Parameters |
|---|---|---|
| Velocity-driven blur | `v = velocityAt(f)` (central difference: `(pos(f+1)−pos(f−1))/2`), blur strength ∝ v | Only triggers when zoom speed is >0.6/s, strength `min(10, v×5)`px. **Blur only during motion; still frames are always sharp** (HuaRec) |
| Lagged follow layer | Follow layer = the subject sampled at `f − delay` | Shadow lags 2f, afterimage lags 4f (shotcraft). Afterimage as a stand-in for motion blur: 5% path lag + blur(6px) + opacity 0.25·(1−t) |
| dampedSettle aftershock | `e^(−d·t) · sin(2π·f·t)`, f≈0.1, damping≈0.15 | 1-2 tiny residual swings after the camera stops abruptly, amplitude ≤3px; not added to active camera moves (the §4.1 inOut family), only to whip-pan / hard-braking types |

All three are pure functions of time (differences, delayed sampling, closed-form decay), so they are naturally seek-safe
and meet the determinism requirement of gsap-recipes §6.

---

## §10 · Camera self-check list (60 seconds after writing the timeline)

- [ ] Can every camera move answer "what question it answers for the viewer"? Did you delete the ones that can't?
- [ ] No zoom below 1.25x (except the 1.06x establishing shot)?
- [ ] Adjacent camera changes ≥2.6s apart, ≤4-5 per 15s window?
- [ ] All push and pull durations follow the logarithmic formula, with no gut-feel fixed durations?
- [ ] Push and pull easing is power3.inOut, with no linear / spring overshoot?
- [ ] Adjacent shots went through the three-way ruling by focal distance (merge/pan/drop)? No back-to-back jumps between distant focal points?
- [ ] Shots with short gaps join directly, with no pumping back to 1x?
- [ ] Film >14s and first shot later than 7s: added the 1.06x establishing micro-push?
- [ ] Ends on a still wide shot for ≥0.8s, not in a pushed-in state?
- [ ] With narration: camera moves snap to speech gaps (only earlier, ≤0.8s)?
- [ ] All camera motion funneled into the `#camera` layer, not fighting element animation for the transform?
- [ ] 3D text close-ups use CSS zoom rasterization, not blurry scale enlargement?
- [ ] Each transition seam uses only one type, with no bare cuts in the whole film?
- [ ] Parallax adjacent layer speed ratio ≥2x, ≤4 layers?
- [ ] Blur appears only during motion transients, with all still frames sharp?

---

## §11 · Relationship to other references

| reference | Division of labor | Boundary |
|---|---|---|
| `animation-best-practices.md` | How elements move, narrative rhythm, taste standards | It handles the "actors", this file handles the "camera"; the "camera pull-out" in the S4 burst segment takes its parameters from §4 of this file |
| `gsap-recipes.md` | Runnable GSAP implementations of every rule in this file | "Camera Rig recipes" section: rig container, PageCam translation, logarithmic duration helper, counter-transform |
| `animation-pitfalls.md` | List of pitfalls | Camera-specific pitfalls (scale blur / broken perspective / pan exposing edges): §3.3-3.4 covers the design side, pitfalls covers the technical reproduction |
| `hyperframes-backend.md` | Render backend contract | For the applicability of the CSS zoom technique under offline frame-by-frame rendering, see §3.4 |
| `voiceover-pipeline.md` | Narration-driven long videos | The silence-point data for move on pause (§6.3) comes from the gaps between narration clauses |
| `ai-video-review.md` | Finished-film review | The review checklist's transition categories are extended using the §7 three-layer vocabulary |

**Reading order**: in the director's script / storyboard stage, read §0-§2 to set the budget and vocabulary → before writing the timeline, read §3-§7 to set implementation conventions
and seams → before delivery, go through the §10 checklist.
