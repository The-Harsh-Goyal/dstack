# HyperFrames render backend · selection boundaries and operating manual

> Introduced after hands-on validation on 2026-07-17 (toolchain / Chinese fonts / proxy environment / migration / 3D, all five passed; key data is embedded in this document).
> HyperFrames is HeyGen's open-source HTML→video framework (Apache 2.0): plain HTML + a paused GSAP timeline, with a headless browser seeking frame by frame for deterministic rendering.

## Selection boundaries (read this table before you start)

| Scenario | Which render route to use |
|---|---|
| New animation project (default) | **HyperFrames**. The audit suite comes free, and 3D/GSAP/Lottie/shader are all unlocked |
| Needs 3D / particles / physical inertia / shader transitions | HyperFrames (the in-house Stage can't do these) |
| Reusing / revising an old Stage demo | Migrate it while you're at it (adapter recipe below, 20-30 minutes each); if you're only re-rendering without changes, keep using render-video-seek.js |
| Weak runtime (no npm / can't install dependencies / single-file delivery the user opens by double-clicking) | In-house Stage (assets/animations.jsx), old workflow unchanged |
| Interactive demo (the user plays with it in the browser, no video export) | In-house Stage or plain HTML; HyperFrames is a render pipeline, not an interaction framework |
| Long narrated video (driven by narration_stage) | **In-house narration pipeline** (voiceover-pipeline.md + render-narration.sh); don't use HyperFrames for now, because the dual time source / subtitles / TTS timeline are deeply coupled to the in-house Stage. When both this row and "animation defaults to HyperFrames" match, this row decides |
| Batch parameterized video (personalized at scale / template text swaps) | Remotion (see planned direction 5, separate from this skill's main workflow) |

**The design language is always the client**: narrative structure, the easing system, and the SFX/BGM dual-track system all still apply as before (animation-best-practices.md / audio-design-rules.md); HyperFrames is just the implementation and rendering tool. GSAP implementation recipes are in `references/gsap-recipes.md`.

## Project scaffolding

> ⚠️ dstack: don't run `hyperframes init` without the user's OK: it installs into a global skills folder and fetches from the network. The default video path is `scripts/render-video.js` (local Playwright).
>
> ⚠️ Install warning: besides generating project files, `hyperframes init` also installs **19 hyperframes skills into
> `~/.claude/skills/`** (composition contract docs for the render backend, docs only, no executable hooks). If you mind, first run
> `npx hyperframes docs` to see the local doc list, then decide whether to init.

```bash
npx -y hyperframes init project-name --example blank   # non-interactive mode requires --example
cd project-name && npm install
```

This generates index.html / hyperframes.json / meta.json / package.json (with the CLI version pinned) + a project-level CLAUDE.md. init installs 19 hyperframes skills into `~/.claude/skills/` (already installed on this machine). For the composition authoring contract, read the SKILL.md of the hyperframes-core skill (init installs it into each runtime's skill directory, `~/.claude/skills/` by default for Claude Code; runtimes without a skill mechanism read the local docs from `npx hyperframes docs` instead). Local docs: `npx hyperframes docs <topic>` (data-attributes / gsap / rendering / troubleshooting).

**Version policy**: the project's package.json pins an exact version (the one currently tested hands-on is 0.7.61). It iterates extremely fast (300+ releases); before upgrading, run `npx hyperframes@latest upgrade --project . --check` to see the delta, and run a regression demo before changing anything.

## Composition contract quick reference (read hyperframes-core for the full version)

- Root container: `data-composition-id` + `data-start` + `data-duration` + `data-width/height`
- Every timed element: `class="clip"` + `data-start` + `data-duration` + `data-track-index`
- The timeline must be paused and registered: `window.__timelines["composition id"] = gsap.timeline({paused:true})`
- Video assets use `muted`; audio tracks are separate `<audio>` elements
- **Deterministic logic only**: no `Date.now()` / `Math.random()` / runtime network fetch; use a seeded function for randomness
- Fonts: Google Fonts are fetched automatically by the compiler and injected as deterministic @font-face (cached in `~/.cache/hyperframes/fonts/`); for pure system fonts (PingFang SC etc.) add one line `@font-face { font-family:"PingFang SC"; src: local("PingFang SC"); }` to pass lint
- Three.js goes through the `hf-seek` event adapter (`~/.claude/skills/hyperframes-animation/adapters/three.md`), and the root container must set `data-duration` explicitly

## Migrating old demos · adapter recipe (tested at 20-30 minutes each)

In-house Stage / pure render(t) animations don't need rewriting. Four steps:

1. **Wrap the container**: wrap it in an outer `#root` with the composition data attributes; using the whole `.stage` as the only clip is the least effort (`class="stage clip"` + data-start/duration/track-index); change `.stage` from fixed-centered to absolute inset:0, and fix html/body at 1920×1080
2. **Delete self-driving code**: delete the rAF tick loop, fitStage/resize listeners, replay button, and the `__ready/__setTime/__seek` protocol entirely (the renderer doesn't need them)
3. **Attach a proxy tween** (the core 12 lines):
   ```js
   const proxy = { t: 0 };
   const tl = gsap.timeline({ paused: true });
   tl.to(proxy, { t: DURATION, duration: DURATION, ease: "none",
     onUpdate: () => render(proxy.t) }, 0);
   window.__timelines = window.__timelines || {};
   window.__timelines["main"] = tl;
   render(0);   // required: onUpdate doesn't fire while the timeline sits at t=0; without this line the first frame may not be initialized
   ```
4. **Sweep for transitions**: search the whole file for `transition:` declarations. CSS transition + class toggling runs on wall-clock time and is nondeterministic under frame-by-frame seeking; it must be changed into a pure function of t (lerp) inside render(t)

## Checks and rendering

```bash
npm run check                        # five-gate audit: lint+runtime+layout+motion+contrast
npx hyperframes check --no-contrast  # for the dark cinematic style only (see below)
npx -y hyperframes@<pinned version> render --fps 60   # final render; default is 30fps
```

- **check must have 0 errors before rendering** (except the contrast gate). lint catches a whole class of "silent visual bugs" such as letterSpacing jitter, missing fonts, and nondeterminism
- **The contrast gate trade-off**: it checks against WCAG 4.5:1, which fundamentally conflicts with the low-contrast watermarks / decorative text (16-40% opacity) of the dark cinematic style, and it has no per-element exemption. Dark cinematic output uniformly uses `--no-contrast`; the other four gates must still have 0 errors. Don't skip it for light-background informational output; a contrast error there is usually a real problem
- **Two-level rendering**: first render quickly at the default 30fps; after it passes eyeball + frame-grab checks, do the final render with `--fps 60`. 60fps, 600 frames, 1080p tested at about 20 seconds
- For output-side checks (audio stream / black frames / loudness / duration), use `scripts/verify-video.sh` (see verification.md)

## Alpha channel (overlay text effects / stickers straight onto the edit track)

`npx hyperframes render --format mov` outputs ProRes 4444 (yuva444p12le, with alpha; tested on 2026-07-17 over a colored background, even soft shadows were correctly semi-transparent); `--format webm` is also transparent and smaller; `--format png-sequence` outputs an RGBA frame sequence for AE/DaVinci Resolve. Composition-side essentials: set the html/body background to `transparent` and don't lay down a background color. Overlay assets such as text effects / corner badges / lower-thirds can now go straight onto the edit track without keying. Note that MOV files are large (ProRes is near-lossless, around 15MB for 4 seconds); use them for editing deliveries, and webm for network transfer.

## Audio

In a HyperFrames composition, `<audio>` elements can go straight onto the timeline (BGM/narration render with the film). The current audio workflow is unchanged: the SFX/BGM dual-track system follows audio-design-rules.md, and post-mixing with add-music.sh / mix-voiceover.sh also works. Which route is better will be settled in real projects; neither is mandatory yet. For SFX hit points use `scripts/sfx-cues.sh <video> <cue sheet.tsv> <output>` (cue sheet = three columns: seconds / sfx path / volume dB; distilled from the B00 project; edit the sheet and rerun to get a film in 10 seconds).

## pitfalls delta (relative to the in-house pipeline)

The in-house pipeline's pitfalls (animation-pitfalls.md §7/10/12/13 recording-protocol items, §6 font timing, §15/17 network items) **do not apply** on the HyperFrames backend: the framework handles the recording protocol internally, fonts are fetched at compile time, and the CDN was tested to work through a proxy. There are four new pitfalls, already recorded in animation-pitfalls.md §18-21: CSS transition nondeterminism, the proxy tween first frame, the contrast gate conflict, and the fromTo immediateRender ghost.
