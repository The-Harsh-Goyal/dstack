# Launch Film workflow: write 10,000 characters of director's notes first, then animate

> The standard workflow for high-spec visual work (≥ 20 seconds, with brand narrative, with a slogan reveal, possibly promoted on X / WeChat Official Account / Bilibili).
>
> Trigger condition: the task is "product upgrade promo film / brand launch film / launch trailer / superbowl-tier ad / brand campaign / hero animation video", and **the user has explicit quality expectations** (such as "Super Bowl quality", "10x detail", "Apple level").
>
> Anti-trigger: don't use this workflow for "quickly make an animation demo", "a simple motion graphic" or "a single icon animation". It would be over-engineering.

---

## 1. Why write director's notes first

Lesson from real work (the md-html v2.0 project, 2026-05-11):

The first round went straight to writing HTML, and the output was "a programmer's-eye animation": equal effort on every capability, a constant pace, slogans colliding with each other, and no narrative arc.
In the second round, after the user's instruction "stop, first write a 10,000-character storyboard script from an Apple director's point of view", v5-director-notes.md was written (11,500 characters, a 13-shot shot-by-shot spec), and then implemented according to the script. It passed in one go, every paused frame held up, and the pacing rose and fell with a climax.

**The core difference**: writing the script is think; writing the HTML is execute. Think it through first, and execution is mechanical translation. Execute first, and every shot is an on-the-spot decision, which is bound to be a mess.

Writing director's notes isn't "putting on airs"; it's settling every visual decision into a document **before you start**: every shot has already been visualized in your head, reasoned through, and traced against its context. During HTML implementation you don't need to make creative decisions any more, only translate faithfully.

---

## 2. Trigger judgment (ask yourself 3 questions first)

Before starting the launch film workflow, ask:

1. **Does this film carry brand narrative?** (has a thesis / slogan reveal / a sense of upgrade ceremony) → if yes, follow the director's notes workflow
2. **Will viewers pause to look?** (may screenshot, make X posters, make covers, review in slow motion) → if yes, every frame has to hold up
3. **Does the client/user have a reference like "I want it to be like XXX"?** (Apple / Anthropic / Nike / Penguin / a particular director) → if yes, the visual context must be made explicit

If any is "yes", follow the workflow. If all three are "no", skip it and use the standard workflow in [animations.md](animations.md) directly.

> 🔴 **Prerequisite gate (before this workflow)**: a launch film must also first pass SKILL.md's three-directions hard gate: one "direction board" per direction (a real still of the hero keyframe + palette + mood sentence + references). Only after the user picks a direction do the 10,000-character director's notes unfold around the chosen direction. Specifying a style word like "Apple level" doesn't grant an exemption (confirmed on HuaStudio, 2026-07-18).

---

## 3. The 5-part structure of Director's Notes

10,000-character (10,000-12,000 Chinese characters / an equivalent amount of English) director's notes must contain these 5 parts. **If any part is missing, it's incomplete, and quality will suffer**.

### Part I · Director's Statement (creative thesis, about 1,500-2,000 characters)

Answer 5 questions:

1. **What is this film not?** (explicit exclusions, such as "this isn't a feature walkthrough", "it isn't a demo")
2. **The core thesis in one line**: if viewers remember only one sentence afterwards, which one is it?
3. **Whose context is it in dialogue with?** List 5-8 visual references (director / designer / brand / photographer / work title + year), explaining what was learned from each
4. **Three audience profiles + a promise to each**: primary audience / secondary audience / outside audience, one paragraph each
5. **Pacing philosophy**: an explanation of the curve of slow beats / acceleration / peak / gentle close + which second the emotional climax falls on (**not necessarily the last second**)

Finally, add an anti-slop checklist: **things this film doesn't do** (listed specifically, not vaguely).

### Part II · Visual System (the full visual spectrum, about 1,500-2,500 characters)

This is the engineered visual spec. Once complete, any executor who gets it can produce consistent visuals.

Required subsections:

- **Complete palette**: at least 8-10 colors, each with HEX + functional definition + an upper limit on its share of the frame
- **Type system**: at least 6 font size levels, each with font name + weight + size + letter-spacing + use
- **Grid system**: canvas size + outer margins + column grid + baseline grid + key safe areas + golden-ratio anchor points
- **Animation system**: easing library (4 curves at most) + duration dictionary + stagger rules + scene transition rules
- **Chrome elements**: small details running through the whole film (counter / chip / ticker / watermark / texture), each with position + entry and exit timing
- **Audio system**: a 30-second BGM trajectory curve (layered) + SFX dictionary (10+ cues with timecode + volume + frequency band isolation)
- **Anti-AI-slop checklist**: a per-shot self-check table (10-15 items)

Iron rule: **every visual decision is derived from the Visual System; don't invent new values on the fly in the shot list**.

### Part III · Story Arc (about 500-800 characters)

Three-act structure + emotional curve:

- **Act I · SETUP** (0 → the first 1/5 of the duration, e.g. 0-6s for 30s): the audience comes in, the question is posed
- **Act II · ESCALATION** (the middle 2/3): the answer unfolds, the theme is laid out
- **Act III · PAYOFF** (the last 1/4): elevation, slogan reveal, brand stamp

Include an ASCII emotional curve chart + a marker for the emotional climax moment.

**Key decision**: the climax isn't necessarily at the end. For a 30s film the climax is usually at 22-25s (not 29s); the last few seconds are resolution / decay, not the peak. Violating this rule is bound to make the work "start strong and fizzle out".

### Part IV · Shot-by-Shot Storyboard (about 5,000-7,000 characters · 60% of the length)

Each shot has 11 fields (none can be missing):

```
SHOT NN · NAME
[TIMECODE]    start and end time + duration
[FUNCTION]    this shot's function in the story arc (one sentence)
[VISUAL]      frame composition + element positions + direction of motion
[CAMERA]      shot size (extreme long/long/medium/close/extreme close, mapped to zoom levels) + camera move + one-line motivation; "static" also needs a reason it's static; push-in must name a concrete anchor (vocabulary and budget in camera-language.md, shot size system in storyboard-basics.md §3)
[TYPE]        typesetting spec (font / size / tracking / line height / color / alignment)
[ANIM]        each element's in/out timing + easing + duration + stagger + delay
[AUDIO]       music beat + SFX cue (each shot's matching BGM rhythm + required SFX timetable)
[CHROME]      state of the four-corner elements (which chrome is present / which fade in/out / which pulse)
[ANTI-SLOP]   which self-check items this shot passed + what 120% detail signature it has
[WHY]         the logic carrying over from the previous shot + the hook pushing into the next shot
```

**Fields average 30-80 characters → 400-700 characters per shot → 12-15 shots → 5,000-7,000 characters**.

From real experience: after writing the storyboard, **read it through yourself**. If you delete any single shot, does the whole film still stand? If it can be deleted, that shot is redundant; delete it.

### Part V · Production Manifest (about 800-1,200 characters)

Engineering delivery checklist:

- Font loading URLs (with preconnect)
- CSS variables (ready to paste)
- BGM source selection criteria + Suno/Udio prompt keywords + backup libraries
- SFX dictionary (file path + volume for each cue, by timecode)
- **Keyframe verification plan**: 12-15 pause-and-check keyframe timecodes, with the verification items for each frame listed (fonts / positions / chrome state)
- Recording parameters (fps / codec / bitrate / preset)
- ffmpeg audio mixing command (with audio stream verification)
- Deliverables list (mp4 / mp4-60fps / gif / poster.png / silent.mp4 / shot-list.csv)
- End-to-end time estimate (to the hour)

---

## 4. 5 suggestions for writing director's notes

**4.1 Use a director's voice, not a PM's voice**

❌ "This shot displays the product features."
✅ "This is the hero shot: if the audience pauses anywhere, I want it to be here."

Director's notes are written for the executor to read, but also for your future self. First person + expressions of judgment leave more decision clues than descriptive statements.

**4.2 Cite specific works (with years), not just genre names**

❌ "Apple-inspired"
✅ "Apple 'Designed by Apple in California' (2013, dir. Mark Romanek): what we're learning is the slow beats + serif + big white background"

Benefits of citing specific works: (a) any viewer can look it up online for comparison (b) it forces you to think clearly about which specific technique you're learning (c) it prevents "fuzzy inspiration".

**4.3 Trace every decision back to the first principle**

The whole film has one first principle (such as "Markdown is the new typewriter."). Every specific decision (color / type / pacing / chrome) must be traceable back to that sentence.

A decision that can't be traced back is decoration; delete it.

**4.4 Writing anti-slop matters more than writing do-this**

The "things this film doesn't do" list (purple gradients / emoji / Lorem ipsum / Inter display / SVG-drawn people / rounded cards + left border accent) protects quality better than the "things this film does" list.

Positive decisions are infinite, while a negative checklist is finite; but once a negative checklist is violated, it's slop.

**4.5 Don't implement right after writing: read it again 30 minutes later**

While writing, your brain is in "production mode" and can't see inconsistencies. Reading your own storyboard 30 minutes later, you'll find:
- Two shots with duplicate functions (delete one)
- A shot with too big a narrative jump (add a transition)
- The emotional climax in the wrong place (move it)
- Chrome elements that don't match the number of shots (realign them)

Those 30 minutes save 2 hours of rework later.

---

## 5. Director's Notes → HTML implementation workflow

After the director's notes are written, the HTML implementation steps:

1. **Reuse the starter components** (Stage/Sprite/Easing/interpolate in `assets/animations.jsx`): don't reinvent them
2. **Paste the CSS variables straight from the Visual System in Part II**: don't change colors on the fly in the HTML
3. **Match Sprite start/end timelines against the Part IV timecodes**: don't add shots on your own
4. **Extract chrome elements into standalone components** (ChromeA/B/C/D), with useTime() driving state changes
5. **The content of destination cards must be real and readable** (not fake bar lines): this was the most frequently mentioned 120% detail signature in the v5 project
6. **Capture a verification keyframe right after finishing each shot** (with the `?t=NN` URL parameter + Playwright); don't write the whole film and then verify it all at once

---

## 6. Keyframe verification workflow

URL parameter implementation (must be added to the Stage component):

```js
const urlMatch = window.location.search.match(/[?&]t=([\d.]+)/);
const frozenTime = urlMatch ? parseFloat(urlMatch[1]) : null;
const [time, setTime] = useState(frozenTime != null ? frozenTime : 0);
const [playing, setPlaying] = useState(frozenTime == null);
```

→ That way `file:///path/animation.html?t=14.5` freezes directly at 14.5 seconds.

Batch screenshots:

```bash
for t in 0.5 2.5 4.9 7.0 10.5 13.5 16.5 19.0 21.5 23.4 25.5 28.0 29.9; do
  npx -y playwright screenshot \
    "file://$PWD/animation.html?t=$t" \
    "keyframes/t-$t.png" \
    --viewport-size=1920,1136 \
    --wait-for-timeout=2500
done
```

Each screenshot must verify:
- [ ] No elements overflow the 1920×1080 canvas
- [ ] Tracking and line height are visually correct (not cramped, not loose)
- [ ] Key typography details (period color / em-dash / italic / small caps) are recognizable
- [ ] Chrome element positions + states are correct
- [ ] The anti-AI-slop checklist passes
- [ ] The 120% detail that's "worth looking at when paused" is present

---

## 7. Multi-perspective parallel strategy (advanced)

For complex projects (such as when the launch film's direction can't be decided / you want to see several aesthetic differences / the client hasn't settled on a style), you can **launch several subagents in parallel to make versions from different directors' perspectives**.

Real configuration (the md-html project, 2026-05-11, 6 versions in parallel):

```
v5  · baseline (Anthropic / Penguin Classics publisher taste)
v5a · Wes Anderson (symmetry + retro + chapter cards)
v5b · Saul Bass (paper cutouts + 60s big type + geometric cuts)
v5c · Wong Kar-wai (Chinese serif + slow motion + nostalgia)
v5d · Massimo Vignelli (modernist grid + red and black)
v5e · Kenya Hara (minimalist Japanese + white space)
v5f · Yayoi Kusama (polka dots + repetition + a single strong color)
```

Each subagent gets an independent brief:
- Project background (the same one)
- Required reading (the same v5-director-notes.md as the methodology template)
- **The assigned artist's DNA** (palette / type / visual language / pacing / signature elements / a strengthened anti-slop version, 30-50 characters each)
- A unified task list (director-notes.md + animation.html + keyframes/ + README.md)
- Unified constraints (30s / 1920×1080 / file:// / Google Fonts)

Launch in parallel + run in the background, and in about 30-60 minutes you get 6 complete versions.

After completion, review and compare:
1. A table of each version's core aesthetic decisions
2. Keyframes side by side (one frame from each version at the same moment)
3. Vote: which one best fits the user's real needs

**Key point**: don't let the subagents reference each other. They must produce independently, otherwise they'll converge on the "average". Each subagent's instructions should state clearly "don't repeat v5's aesthetics".

---

## 8. Typical trigger scenarios

| User scenario | Triggers? | Notes |
|---------|---------|------|
| "Make a SaaS upgrade promo film" | ✅ Triggers | Follow the full workflow by default |
| "An Apple-level / Super Bowl quality video" | ✅ Triggers + escalate | Multi-perspective parallel strongly recommended |
| "A 30-second brand launch film" | ✅ Triggers | |
| "For this project, a 10,000-character script first, then the animation" | ✅ Triggers | The user specified it explicitly |
| "A simple motion graphic, spin the logo a bit" | ❌ Doesn't trigger | Use the standard workflow in animations.md |
| "Make an onboarding animation demo" | ❌ Doesn't trigger | Use animations.md |
| "A tutorial video with voiceover" | ❌ Doesn't trigger | Follow voiceover-pipeline.md |
| "A single hero animation" | ⚠️ Depends on complexity | If it's a high-spec hero, it triggers; for an ordinary hero use hero-animation-case-study.md |

---

## 9. Reference samples

Complete director's notes reference sample (self-contained, inside this skill):

`assets/director-notes-samples/launch-film-30s-sample.md` (about 78KB · 11,500 characters · 13 shots · all 5 parts complete)

Original project location (with the corresponding implementation HTML + keyframes):

- v5-director-notes.md (director's notes, the author's local copy, not distributed with the repo)
- v5-six-forms.html (HTML implementation, the author's local copy, not distributed with the repo)
- v5-keyframes/ (keyframe verification screenshots, the author's local copy, not distributed with the repo)

When writing a new project, it's strongly recommended to **Read this sample first** to understand the workload and density of detail, then decide whether to follow the full workflow.

---

## 10. Anti-patterns (don't do these)

❌ **Writing a 1,000-character condensed version of the director's notes and starting**
→ A condensed version is bound to miss some subitem of the Visual System, so during HTML implementation you keep going back to fill in the spec. If you do it, do the 10,000-character version; if you want to save time, skip it entirely.

❌ **A storyboard with only 5-8 shots**
→ A 30-second film needs at least 12-15 shots (2-3 seconds each). Fewer shots = constant pace = no climax.

❌ **Delivering the director's notes as soon as they're written, without implementing**
→ The document isn't the deliverable; the animation is. Deliver the document + animation together, with the document as a "design rationale" appendix.

❌ **Letting subagents see other versions during multi-perspective parallel work**
→ Each subagent must be independent, otherwise they converge. Compare only in the review stage.

❌ **Skipping keyframe verification and recording the MP4 directly**
→ Rework is guaranteed. Keyframe verification is the cheapest quality gate.

❌ **Postponing animation detail decisions to "I'll think about it when I record"**
→ The recording stage is mechanical execution, and you can't make creative decisions there. Every decision must be fixed in the director's notes.

---

*Last revised: 2026-05-11*
*Real case: md-html v2.0 launch film (v5-director-notes.md)*
