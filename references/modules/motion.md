# Module · Animation / Video / Promo Films

> **dstack note (audio):** dstack ships **no music or sound effects**. The upstream `assets/bgm-*.mp3` (generated with Suno) and `assets/sfx/**` (generated with ElevenLabs) were removed because their licences couldn't be verified. File names below are kept as a naming scheme: put your own licensed files in `~/.dstack/audio/` (`bgm-<mood>.mp3`) and `~/.dstack/audio/sfx/<category>/<name>.mp3` (override with `DSTACK_AUDIO_DIR` / `DSTACK_SFX_DIR`), or, only when a task asks for it, generate them with ElevenLabs (the one approved outside audio service, off by default): `DSTACK_AUDIO_PROVIDER=elevenlabs node scripts/gen-audio.mjs sfx ui/click` / `... bgm tech`. Free-plan ElevenLabs output is non-commercial and needs attribution; see "Licensing" in `references/audio-design-rules.md`. If a file is missing, `add-music.sh`, `mix-voiceover.sh` and `sfx-cues.sh` warn and carry on without it.


Everything timeline-driven goes through here: HTML animation, product feature demos, launch films, narrated concept videos, MP4/GIF export. This is the module with the most capabilities in the skill, so it has its own routing. First pass through the core rules in SKILL.md (the three-direction gate still applies, and the first-draft format is the direction board), then follow this manual.

## First decide what kind of film it is

| Film | Main line | Must read |
|---|---|---|
| Short animation / concept demo (<1 minute, no narration) | The "General flow" below | `storyboard-basics.md` → `animation-pitfalls.md` → backend files |
| Product UI is the protagonist (feature demos, commercial work, UI showcases) | General flow + UI showcase | `ui-demo-animation.md` (decision tree for screenshot camera moves vs HTML rebuild, the eight UI showcase moves) + `assets/cursor.jsx` |
| Launch film / brand promo film ("Apple-level" expectations) | Three-direction direction boards → after one is chosen, write a 10,000-word director's script | `launch-film-director-notes.md`, `cinematic-patterns.md` |
| Narrated long video (≥1 minute, explaining one concept clearly) | Narration-driven: write the narration script first, then make the visuals | `voiceover-pipeline.md` + `assets/narration_stage.jsx` |
| Lots of homogeneous material (20+ screenshots/works, conveying scale) | Gallery-style scenes | `hero-animation-case-study.md`, `apple-gallery-showcase.md` |
| Want to see multiple versions / distribute to multiple platforms | Multi-perspective in parallel | `multi-perspective-parallel-case-study.md` |

## General flow

1. **Three-direction direction boards**: 1 direction board per direction: 1–2 real HTML still-frame screenshots of the hero keyframe + a palette strip + a one-line positioning of its character + names of reference works. Not three finished films, but they must be rendered images (`references/directions.md`). The differences between the three directions lie in motion language and materials, not just color.
2. **Storyboard cards**: before starting any animation, produce lightweight storyboard cards first, with each shot starting as a moving cover (the format in `storyboard-basics.md` §5, including the [CAMERA] column and acceptance frame numbers). For films ≥20s, write the storyboard cards into `director-script.md` (director's script), along with **visual density clauses**. A director's script that covers only narrative and camera moves produces wireframes (`animation-best-practices.md` §6.5).
3. **Camera language**: for shot-level motion such as zoom / pan / transitions, read `camera-language.md` first (budget system, inter-shot grammar); for implementation see `gsap-recipes.md` §9.
4. **Choose the backend** (table below) and write the animation. Reading `animation-pitfalls.md` before starting is required.
5. **Look at frames**: capture frames at key moments and actually look at them: clipping, collisions, empty frames, rhythm that only works on paper. Also capture the first second after every scene change.
6. **Sound**: by default deliver an MP4 with SFX + BGM ("Sound" below).
7. **Export and verification** ("Export" below).

## Backends

| Backend | When to use it | Read |
|---|---|---|
| **HyperFrames** (default for new animations) | Need to render a finished film, need determinism, need 60fps | `hyperframes-backend.md` (selection boundaries, composition contract, migrating old demos) + `gsap-recipes.md` |
| **Stage + Sprite** (`assets/animations.jsx`) | Single-file delivery, purely interactive demos, weak runtimes | `animations.md` |
| Narration-driven (`assets/narration_stage.jsx`) | Long videos with voiceover | `voiceover-pipeline.md` |

When hand-writing Stage / Sprite (without `animations.jsx`), you must implement two things, or video recording is sure to break: synchronously set `window.__ready = true` on the first tick frame; force `loop = false` when `window.__recording === true` is detected.

## The two most common failures

- **PowerPoint with a voiceover**: each scene with its own independent layout + text fade-up + whole-page opacity switches. The whole film should be one continuous motion narrative: pick 1–2 hero elements that persist across scenes, each segment being a change in their state, morphing between scenes instead of cutting (the "Iron rules" in `voiceover-pipeline.md`).
- **Fake chrome drawn into the frame**: a bottom progress bar, timecode or copyright credit bar that clashes with Stage's built-in scrubber. Put only narrative content in the frame (`animation-pitfalls.md` §11).

## Sound (included by default)

A silent version is a half-finished product. Do BGM + SFX as two tracks together; doing only BGM is one-third complete.

- Design the SFX cue list according to `audio-design-rules.md`, using `assets/sfx/<category>/*.mp3` (37 prebuilt, `sfx-library.md`); about 6 per 10s for a launch hero, 0–2 per 10s for tool demos; mark cues with `scripts/sfx-cues.sh`
- BGM: `scripts/add-music.sh` (6 scene-specific music tracks)
- Before delivery, confirm there's an audio track with `ffprobe -select_streams a`
- Skip only when the user says "no audio", "visuals only" or "I'll do my own voiceover"

## Export

- HyperFrames: `npm run check` (five-gate audit; add `--no-contrast` for dark cinematic styles) → `npx hyperframes render --fps 60` → `scripts/verify-video.sh`
- In-house pipeline: `scripts/render-video.js` (25fps intermediate) or `scripts/render-video-seek.js --fps=60` (frame-by-frame seek, true 60fps, no black frames, used when running on the Stage clock) → `scripts/convert-formats.sh` derives a 60fps MP4 and a palette-optimized GIF
- Narrated: `bash "$HD/scripts/render-narration.sh" demo.html --timeline=_narration/timeline.json [--bgm-mood=educational]` (calls `scripts/mix-voiceover.sh` internally to mix the voice; you can also use it directly for standalone mixing)
- After the final render, a local video review: `python3 "$HD/scripts/review-video.py" --video <finished film> --context director-notes.md` (ffmpeg checks + contact sheets, nothing sent anywhere; `ai-video-review.md`)
- Full explanation: `video-export.md`

**Watermark**: none by default (dstack adds no promo watermark). Unofficial tribute animations for third-party brands carry a small "Unofficial" label; add any other watermark only when the user asks. Template in the last section of `video-export.md`.

**Gate**: before rendering a long film ≥45s, `scripts/design-gate-hook.sh` checks for `direction-approved.md` and blocks the render if the file is missing; when the user explicitly says to skip, let it through with `SKIP_DESIGN_GATE=1`.

## Starter components

| File | Use |
|---|---|
| `assets/animations.jsx` | Stage + Sprite + useTime + Easing + interpolate |
| `assets/narration_stage.jsx` | NarrationStage + Scene + Cue + Subtitles (narration-driven) |
| `assets/cursor.jsx` | Cursor for product demos: four shapes, arc trajectories, click ripples, frame-deterministic |
| `assets/ios_frame.jsx`, `android_frame.jsx`, `macos_window.jsx`, `browser_window.jsx` | Device and window shells |

## Engine layer (reserved)

This module's method (directorial judgment, motion language, rhythm, sound design) and its execution engine (rendering, audio output, verification) are two separate layers. What's listed above is the current engine; when a new engine is plugged in later, it goes into the "Backends" table and the "Sound" and "Export" sections, and the method-layer files don't need to change with it.
