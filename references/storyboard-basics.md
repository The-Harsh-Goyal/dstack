# Storyboard Basics · lightweight storyboards and frame composition

> The storyboarding method before starting any animation, whether 5 seconds or 50. The core in one sentence: **every shot is first a cover that moves**.
>
> Sources of the methodology: the freeze-frame rules (S1-S11) distilled from 300+ covers tested in Huashu's illustration library, the energy-skeleton precedents from video-shotcraft's 106 shot cards, and the camera-budget axioms of the HuaRec Studio camera-direction system.

---

## 0 · Positioning: the division of labor with the launch-film director's script

This file is the **everyday lightweight version** of `launch-film-director-notes.md`. The 10,000-character launch film director's script is the heavyweight process, and everyday animation doesn't need all that, but **the storyboarding step itself can't be skipped**: skip it and you end up with timetable thinking (which element appears at which second), not frame thinking (what this frame looks like).

| Length / type | Storyboard requirement | Basis |
|---|---|---|
| < 20s animation, motion graphic, demo | This file's **lightweight storyboard card** (§5, one line per shot) | Under 20s isn't worth 10,000 characters, but each shot's frame composition must be thought through first |
| ≥ 20s animation | The `导演稿.md` (director's script) required by the Gate file protocol, **minimum requirement = this file's storyboard card format** (none of the eight fields in §5 can be missing), freely thickened on top of that | SKILL.md "Gate file protocol" |
| launch film / brand promo film / "Apple-level" expectations | Upgrade from the storyboard card baseline to 10,000-character director's notes | `launch-film-director-notes.md`, whose Part IV 10 fields per shot are the heavyweight version of this file's eight fields |

Trigger boundary: when the user says "quickly make an animation" or "a simple demo", don't throw the 10,000-character process at them, but **still draw the storyboard card**. The storyboard card costs a dozen or so minutes; skipping it costs reworking the whole film (measured on B00, 2026-07-17: skipping frame design and going straight to code, the motion was all green, but the visuals were rejected outright).

Relationship with existing files:

- `animation-best-practices.md` handles "how things move" (pacing, easing, motion language); this file handles "what each frame looks like and how shots are arranged". The two are orthogonal
- The scene-based narrative in `cinematic-patterns.md` is a prerequisite for this file: you need the scene breakdown before you can talk about each scene's freeze frame
- Implementation parameters for camera moves (camera rig, the difference between zoom and dolly, camera easing) → `camera-language.md`; this file only borrows its vocabulary at the design level

---

## 1 · Core thesis: every shot is first a cover that moves

After making 300+ covers, the illustration library settled on one judgment: **a good cover = 1 concrete star + ≤3 active elements + 1 clear line of sight**. For every shot of an animation, first design it as a static cover to this standard, then make it move.

**Cover = storyboard freeze frame**. The test is extremely concrete: pause any frame of the finished film at random, and that frame should work as a cover directly. A frame that fails the cover test shows that the shot's composition wasn't designed; it's just the sum of elements moving independently along the timeline.

Why animation is actually more likely to break this rule: animation defends itself with "the elements appear at different times", the next one enters before the previous one has left, and the result is that every frame is crowded. A static cover has no such excuse, so the cover's discipline happens to be exactly the discipline animation lacks most (core insight #1 from the illustration library's testing).

The order is therefore fixed: **set the freeze frame first, then choreograph the motion**. The thumbnail pass in §6 is the executable version of this order.

---

## 2 · The eleven laws of the freeze frame

The illustration library's S1-S11 rules rewritten for the animation context. This is the heart of this file; run every shot's composition design through them one by one.

### Law one · the cover test (S1)

Every scene's freeze frame must have: **1 concrete star + ≤3 active elements + 1 clear visual focus**.

"≤3" is **an invariant for every frame**, not a total for each scene. When a new element enters, an old one must exit (fading out, retreating to the background, blur+dim all count as exiting), so the budget of on-screen active elements stays constant. When writing the timeline, count the on-screen elements at every time point; if it's over, cut an entrance or exit something earlier.

> Self-check: pause at three time points picked at random and count the on-screen active elements. Is there a frame with more than 3?

### Law two · the zoom endpoint must be a concrete anchor (S2)

The endpoint of a push-in / zoom can only be: a brand logo, a key number, that button in the UI, that line of code, a person's expression. **Background textures, atmospheric elements and decorative graphics don't deserve a zoom**. Pushing in on something with no information tells the viewer "there's actually nothing to see here".

A HuaRec precedent adds one more point: **a zoom of < 1.25x isn't worth doing** (the visual change isn't perceptible enough; it's just shaking. The only exception is the 1.06x establishing micro-push at the opening). When designing the storyboard, write down what the anchor is for every [CAMERA] push-in; if you can't name the anchor, delete that camera move.

> Self-check: can you name this shot's push-in endpoint with one noun (that button / that number / that logo)? If not, delete the camera move.

### Law three · line of sight and arrows = the camera motion script (S3)

The static cover rule "the person's gaze points toward the subject, and one image gets only one arrow" translates to animation as: **the guide line in the freeze frame is this shot's camera motion instruction**. The camera follows the gaze, pushes along the arrow, and pans in the UI's reading direction.

A scene has only 1 guide line. If you can't find a guide line in the freeze frame, the shot has no idea how it should move. Don't force a camera move in that case; go back and fix the composition (core insight #3 from the illustration library).

> Self-check: show someone the freeze frame for 3 seconds. Does their gaze path match the camera motion you planned?

### Law four · text and image divide the work, two tracks (S4 + the illustration library's C series)

The text track and the image track are two independent timelines, with non-overlapping roles:

| Rule | Content | Source |
|---|---|---|
| Text carries the hook | Hard limit of 2-6 characters of big text per shot, 2-4 ideal for the main copy; text states the hook, the image carries the atmosphere, and the image isn't forced to act out the text | Illustration library C1/C3 testing |
| Two-beat entrance | Big text always enters in two beats: **the action word slams in first, the modifier color block follows** ("Tested" slams down across the screen, then the "Claude 4.8" color block sticks on) | Illustration library C5 |
| Text lands in negative space | Text always lands in the negative space reserved by the composition, never over the star or the focus | Illustration library C2 |
| Solid strong color | Display text must be a solid strong color; **hollow white text + colored outline is absolutely forbidden** | Illustration library G no-go zone |

> Self-check: cover the image and keep only the text: is the hook still there? Cover the text and keep only the image: does the composition still hold? Only when both pass is the division of labor clean.

### Law five · percentage spatial language (S5)

Composition descriptions in the storyboard card must be written at percentage granularity: "product screenshot in the top right 60% with perspective, person in the bottom left 25%, big text pressing against the top edge of the screenshot, 10% safe area from all four edges".

This isn't ritual; it's an engineering interface: **percentage language maps directly to CSS/GSAP layout parameters**, so the implementing agent can translate it immediately without making composition decisions. Writing at the granularity of "product on the left, text on the right" is as good as writing nothing (gbro composition template comparison test: prompts at percentage granularity produced output a whole tier above vague descriptions).

> Self-check: does this shot's composition description contain at least 3 percentage numbers? If not, it's still a literary description, not a spec.

### Law six · foreground, midground, background = three parallax layers (S6)

When designing the freeze frame, write out explicitly what the foreground / midground / background each are and what covers what. This layering is natural parallax material: three layers at three speeds, and changes in what covers what are where the sense of depth comes from.

Copy the implementation parameters straight from the shotcraft precedent: parallax layer speed coefficients 0.35 / 0.7 / 1.4, **a speed ratio of ≥2x between layers to be distinguishable**, ≤4 layers.

> Self-check: can you say what the foreground, midground and background of this frame each are, and what covers what? If not, it isn't layered yet.

### Law seven · setup → payoff, the opening frame plants suspense (S7)

Every scene's opening freeze frame leaves a gap (an unfinished bridge, a number not yet revealed, half a screen of blank space), and the shot's motion is responsible for closing it. The "from A to B" structure is naturally a transition narrative: the previous shot's payoff can directly be the next shot's setup.

The opposite is "the opening frame already lays out all the information, and then the elements do effects in place": that's a poster that moves, not a shot.

> Self-check: put this shot's opening frame and ending frame side by side. Can the viewer say "what was delivered"?

### Law eight · materialize + choose imagery with a sense of process (S8)

Abstract concepts must be materialized into visible physical actions, and **actions with a sense of process are preferred**: "connection" = a bridge built section by section, "price cut" = a $89 price tag crossed out digit by digit to become $29, "too AI-flavored" = a manuscript page filling up with neat gray blocks in a stagger.

The action itself is the animation script: choose the right image, and the frame's focus and camera motion grow out of the image by themselves, with no need to invent separate effects. The method is to do a Feynman-style translation first (how does this concept "happen"?), and only after translating, talk about the visual style (core insight #4 from the illustration library).

> Self-check: can this image be summed up with one verb (build, cross out, grow, drop)? Imagery that can only be described with nouns has no sense of process; switch to another.

### Law nine · style × composition are orthogonal (S9)

The illustration library's most important architectural insight, carried over as is: **the style skin is set once for the whole film** (palette, fonts, materials, background logic), **the composition template changes scene by scene** (this shot a centered close-up, the next a three-column grid, the one after a diagonal two-zone layout).

Scene switch = composition switch, never a style switch. Changing styles throughout the film is a disaster; one composition for the whole film is hypnotic. The link to the three-directions gate: the direction board the user picks is that "set once" style skin.

> Self-check: compare any two shots. The style (palette / fonts / materials) should be indistinguishable, and the composition should be obviously different at a glance. If it's the other way round, the architecture is wrong.

### Law ten · inherited no-go zones (S10)

All of the illustration library's aesthetic no-go zones are inherited, and be especially wary of animation's occupational hazards: **glowing particles, data streams, holographic HUDs and cyber neon are motion graphics' handiest lazy materials, and they're exactly all in Huashu's no-go zones**. Your hands itch more when animating than when making static images; keep them in check.

The right answer for a tech feel = real UI screenshots (in a 3D floating card form) + clean big type + a light background. The combination of a dark blue background #0D1117 + neon glow remains forbidden (details as in SKILL.md §6.2).

> Self-check: is any element in the frame "glowing"? If so, first suspect that you're using an occupational hazard to be lazy, and justify keeping or cutting each one.

### Law eleven · the 3-meter test (S11)

Pause on any frame, and the largest word in the frame must be readable from 3 meters away. **Don't shrink the font size because "it's going to move anyway"**: viewers give each frame of an animation less attention than a still image, so font sizes can only be larger, never smaller. This and the visual density clause in §6.5 of `animation-best-practices.md` are each other's upper and lower bounds: the density clause guards against emptiness, and the 3-meter test guards against sacrificing readability when things get crowded.

> Self-check: shrink a keyframe screenshot to phone-screen size. Can the largest word still be read?

---

## 3 · The shot size system: a five-level zoom mapping

The five shot sizes of traditional film and TV (extreme long, long, medium, close, extreme close) correspond to five zoom levels in HTML animation (the level values match `camera-language.md` §4.3, which is authoritative for implementation details):

| Shot size | Zoom level | What it shows | Typical use | Source |
|---|---|---|---|---|
| Extreme long shot | 0.78x | The whole + environmental white space | Opening establishing, closing group shot | shotcraft full-page camera position 0.78 |
| Long shot | 1x (establishing micro-push 1.06x) | The complete interface / complete scene | The narrative baseline, home to most shots | HuaRec establishing 1.06x precedent |
| Medium shot | 1.3-1.45x | One functional block | The workhorse shot size for feature demos | HuaRec light push / medium push levels |
| Close shot | 1.8x | A single component / a single data item | Emphasizing a specific interaction | HuaRec heavy push level |
| Extreme close-up | 2.3x (upper limit) | Law two's concrete anchor | Key numbers, that button, the logo | HuaRec magnification upper limit 2.3x |

Two notes:

- The same level can be achieved with zoom (scale, no parallax) or with dolly (perspective + translateZ, with parallax), and the feel is completely different; the selection rules for the two and how to write the camera rig are in `camera-language.md`, and at the storyboard layer you only need to state the level and motivation clearly in the [CAMERA] column
- The levels are design vocabulary, not shackles: 1.5x and 2.0x are both legitimate; the levels' role is to give words like "medium shot" and "extreme close-up" a definite numerical meaning in the storyboard table

### Shot size rhythm between adjacent shots

| Rule | Content | Basis |
|---|---|---|
| Avoid consecutive cuts at the same shot size | Two adjacent shots at the same level give no sense of change when switching, reading as "the frame jumped" rather than "the shot changed"; differ by at least one level | HuaRec's "a zoom under 1.25x isn't worth shooting" extended to between shots |
| Avoid two-level jumps | Cutting straight from an extreme long shot to an extreme close-up (0.78x → 2.3x) is dizzying; if you must jump, it has to be a deliberate punch-in, cushioned by a transition (white flash / whip-pan) | HuaRec comfort budget |
| Close focuses: merge shots | When the focuses of two adjacent shots are very close, merge them into one shot and re-level using their combined bounding box | HuaRec shot-to-shot grammar |
| Mid-distance focuses: pan | Rather use a shot size one level wider and pan over in one shot than do "pull out, then push in" pumping | HuaRec "switch to a pan" precedent |
| Distant focuses: drop the shot | For two focuses jumping diagonally across the frame, never shoot two zooms in a row; cut one or insert a long-shot transition | HuaRec "drop the shot" precedent |
| Duration scales with magnitude | The transition duration of a shot size change isn't a constant: `duration = 0.55 × |ln(zoomTo/zoomFrom)| / ln2`, clamped to [0.30, 0.94]s; fixed durations are where the amateur feel comes from | HuaRec logarithmic scaling formula |
| Rhythm budget | Changes between adjacent shots ≥2.6s apart, ≤4-5 shot size changes in any 15s window | HuaRec comfort budget A2 |
| Final bow iron rule | The finished film always ends on a long shot / extreme long shot, with a ≥0.8s long-shot pause before the end; **never stop abruptly in a pushed-in state** | HuaRec final bow precedent |

---

## 4 · The energy skeleton: carve out the hold budget first, then arrange the motion

The shot arrangement of a multi-shot film (≥10s) isn't an even split; apply shotcraft's four-stage promo-energy-arc skeleton:

| Stage | Share of duration | Energy | Content | Hard metric |
|---|---|---|---|---|
| ① Opening | 8-12% | Low | Brand / theme reveal | Wordmark settles and holds ≥1s |
| ② Single-star showcase | 12-15% | Low to medium · slowest in the film | One complete action arc for the star (entrance → pause → landing) | Action arc ≥3s, the segment with the highest polish |
| ③ Feature climb | 55-65% | Medium-high ⇄ low, alternating | Each shot tied to one distinct feature, arranged with energy alternating high and low | After every 1-2 feature shots, insert a **breathing title card** (low energy, lots of white space, 2-6 characters) |
| ④ Close | 13-16% | Peak of the film | Group shot + sign-off | Closing hold, final bow back to the long shot (the §3 iron rule) |

**Scheduling discipline: carve out the hold / rest frame budget first, then arrange the motion** (shotcraft's fill-in-the-blanks process precedent). The specific order:

1. List the features and count the number of shots N
2. First carve the inviolable still time out of the total budget: wordmark hold ≥1s, 0.5s of stillness to close out batch motion, an opening action arc ≥3s, a ≥0.8s long-shot pause at the end, a 0.5s pause before key results (best-practices §4.4)
3. Only the remaining time goes to motion, arranged with energy alternating high and low; two high-energy shots in a row aren't allowed
4. Choose a transition for each seam (§7); transition frames are carved out of the adjacent shots' budgets, with no extra time added

The breathing title card's composition also has a fixed form: 2-6 characters of big text + full-screen negative space + zero decoration. It's itself a freeze frame that passes the cover test (active elements = 1), and its role is to lower the energy of the feature climb and give viewers time to digest. Don't turn the breathing title card into yet another information shot, or you might as well not have inserted it.

Relationship with the five-segment narrative in §1 of `animation-best-practices.md`: Slow-Fast-Boom-Stop is the rhythm curve for **single scenes / short pieces** (≤15s in one breath), while promo-energy-arc is the skeleton for **multi-shot films**; under 15s, pick one of the two; above 20s, arrange the shots with the energy skeleton, and use the feel of the five-segment narrative inside each shot.

---

## 5 · The lightweight storyboard card: this file's deliverable

One line per shot, and none of the eight fields can be missing. shotcraft's four-column table (#|time|shot|key motion) is the bare minimum; here it's expanded to eight columns, with [CAMERA] as its own column (the launch film director's script's 10 fields were later expanded to 11 to match, and the new one is this field):

```
| # | Time | Shot size | [CAMERA] move+motivation | Composition (percentage language) | Key motion | Transition to next shot | Check frames |
```

How to write each field:

- **Time**: start and end seconds + implied duration; transition time is included in this shot's budget, not listed separately (rule 4 of the §4 scheduling discipline)
- **Shot size**: one of the five levels in §3 + the zoom value
- **[CAMERA]**: camera move + a one-line motivation; "static" is also a legitimate camera move, but write why it's static; every push-in must name its anchor (law two)
- **Composition**: percentage language (law five), including foreground/midground/background layering (law six)
- **Key motion**: each shot features only one motion (shotcraft's "one shot, one motion" precedent)
- **Transition to next shot**: choose from the §7 decision table; it can't be left blank or say "straight cut" (a bare cut is only legitimate when written as a deliberate hidden-cut)
- **Check frames**: **pre-write 1-2 frame numbers per shot**, and after implementation capture exactly those frames for the self-check (shotcraft's "read each shot three times + pre-write check frames" precedent). The point of pre-writing: the acceptance criteria are fixed before you start, leaving no fuzzy room for "it looks okay" after implementation

### Example: a complete storyboard table for a 12s product animation

Hypothetical product: the screenshot organizer PicSort. 1920×1080 · 30fps · 360 frames.

| # | Time | Shot size | [CAMERA] move+motivation | Composition (percentage language) | Key motion | Transition to next shot | Check frames |
|---|---|---|---|---|---|---|---|
| 1 | 0-2.0s | Long shot 1x | Static, light push to 1.06x in the last 0.3s · establishing + planting suspense | A messy pile of screenshots on a desktop fills the middle 70%, big text "3000 screenshots" lands in the top 20% of negative space, 10% safe area from all four edges; 2 foreground screenshots slightly cover the midground pile | Screenshots drop onto the desk with a 30ms stagger; big text enters in two beats ("3000" slams down, the "screenshots" color block follows) | Defocus handoff (the messy pile blurs away) | f30 / f55 |
| 2 | 2.0-3.5s | Extreme close-up 2.3x | Push-in 1x→2.3x · anchor = the date badge in the bottom right corner of one screenshot | A single screenshot fills 80%, centered, with 2° perspective, date badge in the bottom right 15%; other screenshots recede to a blurred background | Background blur+dim in sync with the push-in (the focus-switch trio) | Shared-element homing (this screenshot shrinks and flies to beside the input box in the next shot) | f85 |
| 3 | 3.5-6.0s | Medium shot 1.4x | Horizontal pan following the cursor · guide line = the cursor's arc path | Product UI fills 85% with perspective, logo in the top left 10%, search box horizontally centered at 55%; the cursor enters on an arc from the bottom left 25% | Typing at 3f/character + result Chunk Reveal; a 0.4s breath after typing | mask-wipe (the edge of the result panel unfolds into the next shot's grid) | f130 / f165 |
| 4 | 6.0-8.5s | Long shot 1x | Pull-out 1.4x→1x · motivation = show the scale after organizing | A 3-column category grid fills 85%, a color tag at the top of each column; the top 15% of negative space is reserved for the next shot's number | Cards stagger into their columns column by column (30ms between columns), still for 0.5s once the board is full | Flash-wash | f210 / f250 |
| 5 | 8.5-10.5s | Close shot 1.8x | Static · key result hold, not upstaging the number | "3000 → 12 categories" fills the middle 60%, with the action word largest and the modifier as a color block; large negative space all around | digit-roll lands (tabular-nums), then holds 0.6s after settling | Shared-element homing (the number shrinks and moves up to make way for the logo) | f290 |
| 6 | 10.5-12s | Long shot 1x | Static · final bow, ending on the long shot | Logo centered at 12%, a one-line slogan 8% below it, everything else white space | Logo morph to close (previous element collapses → expands), last frame holds ≥1s | None (end of film) | f330 / f359 |

Checking against this table you can see the skeleton: shot 1 is the setup that plants suspense (law seven), shots 2-4 are the feature climb with alternating shot sizes (extreme close-up → medium → long, no consecutive same-level cuts, no two-level jumps), shot 5 is the energy peak + hold budget, and shot 6 is the long-shot final bow. Every shot has ≤3 active elements on screen.

---

## 6 · Thumbnail Pass: gray-box verification before writing the real code

The storyboard table is text; the thumbnail pass turns it into visible composition verification. It costs under half an hour and is insurance against the cost of rework.

**Step 1 · Build a gray-box HTML**: a temporary HTML with one 1920×1080 `<section>` per keyframe. Lay out the composition using only solid color blocks + text labels: the star is a dark gray block labeled "Product UI 85%", the text area is a color block labeled "Big text: 3000 screenshots", foreground elements are light gray blocks. Don't write any motion, don't choose fonts, don't adjust colors; just turn the storyboard card's percentage language into visible blocks.

Making it pretty is forbidden at the gray-box stage (choosing fonts, color schemes, adding shadows are all off-limits): beauty is something the direction board already settled, and the gray box only verifies composition and rhythm. Starting to make it pretty = starting to dodge composition problems.

**Step 2 · Make only 3-5 keyframes**: not one per shot; pick the key nodes of the energy skeleton: the opening setup frame, the hero frame of the showcase segment, one representative frame of the climb segment, the peak frame, and the final bow frame.

**Step 3 · Batch screenshots with Playwright**:

```bash
for i in 1 2 3 4 5; do
  npx -y playwright screenshot "file://$PWD/thumbnails.html#f$i" \
    "thumbs/f$i.png" --viewport-size=1920,1080
done
```

**Step 4 · Three acceptance questions** (ask while looking at the thumbnails side by side):

1. **With all text labels covered, can you still see the composition differences across the 5 images?** If not = the rhythm hasn't been achieved, and changing the composition template scene by scene wasn't carried out (law nine; same origin as the thumbnail self-check in best-practices §1)
2. **Does each one pass the cover test on its own?** (law one: 1 star + ≤3 elements + 1 focus)
3. **Can you point out each one's guide line?** For any shot where you can't, go back and fix the composition; don't move on (law three)

**Step 5 · Only write the real code once it passes**. Keep the gray-box HTML in the project directory as the composition baseline, and come back to compare against it when the implementation drifts.

**Relationship with the three-directions gate**: the "direction board" of the three-directions hard gate (a real still of the hero keyframe + palette + mood sentence) is in essence **the first thumbnail**. After the user picks a direction, the thumbnail pass expands that one direction board into the keyframe sequence for the whole film: the direction board sets the style skin, and the thumbnail pass sets the shot-by-shot composition, which is exactly the two orthogonal layers of law nine.

---

## 7 · Transition decision table: choose by narrative relationship

Transitions aren't decoration; they're the narrative logic at the seams. First judge the **narrative relationship** between two adjacent shots, then choose. For the implementation parameters of the transition vocabulary (duration, easing, how to write the masks), see the three-layer transition vocabulary in §7 of `camera-language.md`.

| Narrative relationship between adjacent shots | First-choice transition | Alternative | Precedent basis |
|---|---|---|---|
| Time jump ("three days later", "once organized") | Title card / flash-wash | whip-pan | shotcraft's six moves: cushion big drops with white / black |
| Spatial shift (different areas of the same interface) | **Pan in one shot, don't cut at all** | hidden-cut | HuaRec "mid-distance: switch to a pan": rather go one level wider and pan over in one shot than do out-in pumping |
| Conceptual contrast (before/after, A vs B) | mask-wipe | Split screen then hard cut + white flash | shotcraft mask-wipe precedent |
| Progression / cause and effect (the setup's answer is in the next shot) | Shared-element homing (the previous shot's element flies over to become the next shot's star) | morph | shotcraft's two travel moves; same origin as voiceover-pipeline's iron rule "the hero morphs across scenes, no cuts" |
| Large energy drop (breathing title card → high-energy shot) | Flash-wash / white flash FlashCut | whip-pan | shotcraft: choose seams by the size of the energy drop |
| Small energy drop (adjacent feature shots in the climb) | Defocus handoff / cross-fade ≥8f | hidden-cut | shotcraft graze-face-tour "cross-fade between segments to prevent black flashes" |

Three disciplines:

1. **One move per seam**, no stacking (white flash + whip-pan together is slop)
2. **Transition frames are carved out of the adjacent shots' budgets**, with no extra duration added out of thin air; the storyboard table's time column already includes transitions
3. **Zero bare cuts in the whole film**. The shotcraft precedent in its own words: widely acclaimed launch films don't have a single bare cut from start to finish. If you want the effect of a "cut", use a hidden-cut (hiding the cut point behind a full-screen element / white frame / motion peak), which is a designed cut, not an undesigned one

Narrated films get one more rule: **move on pause** (HuaRec precedent). Camera switches and transitions snap to gaps in the speech, only ever earlier, never later, with an upper limit of 0.8s, because the cognitive cost of moving the eyes is lowest during auditory gaps. When following voiceover-pipeline, set the cut points from the real gaps in timeline.json.

---

## 8 · Kickoff checklist (the definition of a finished storyboard)

Before writing code, confirm that all of the following exist:

- [ ] Storyboard table: one line per shot, all eight fields complete, saved in the project directory (for ≥20s it's the core section of `导演稿.md`, the director's script)
- [ ] Each shot's freeze frame has passed the applicable laws among the eleven, with at least law one (cover test), law three (guide line) and law five (percentage composition) checked explicitly
- [ ] The shot size column has no consecutive same-level cuts and no two-level jumps (§3)
- [ ] The hold / rest budget was carved out first, and breathing title cards were inserted (§4)
- [ ] The transition choice for each seam is written in the table, with zero bare cuts in the whole film (§7)
- [ ] The 3-5 gray-box screenshots from the thumbnail pass passed the three acceptance questions (§6)
- [ ] Check frames were pre-written for each shot, to compare frame by frame after implementation (§5)

When all seven pass, the storyboard stage is over and implementation begins. When the implementation is rejected, first locate the layer: is it a motion skeleton problem or a visual craft problem (the fix pattern in best-practices §6.5)? The storyboard table itself usually doesn't need to be rewritten.

---

*Written: 2026-07-23 · Sources: illustration library S1-S11 freeze-frame rules + video-shotcraft energy-skeleton precedents + HuaRec camera-budget axioms*
*Sister files: `camera-language.md` (camera implementation layer) · `launch-film-director-notes.md` (heavyweight version)*
