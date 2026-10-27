# Video Export: exporting HTML animations to MP4/GIF

> **dstack note (audio):** dstack ships **no music or sound effects**. The upstream `assets/bgm-*.mp3` (generated with Suno) and `assets/sfx/**` (generated with ElevenLabs) were removed because their licences couldn't be verified. File names below are kept only as a naming scheme: put your own licensed files in `~/.dstack/audio/` (`bgm-<mood>.mp3`) and `~/.dstack/audio/sfx/<category>/<name>.mp3` (override with `DSTACK_AUDIO_DIR` / `DSTACK_SFX_DIR`). If a file is missing, `add-music.sh`, `mix-voiceover.sh` and `sfx-cues.sh` warn and carry on without it.


Once an animation HTML is done, users often want to know "can I export this as a video?" This guide gives the complete workflow.

## When to export

**When to export**:
- The animation runs all the way through and has been visually verified (Playwright screenshots confirm the state at each time point is correct)
- The user has watched it in the browser at least once and said it looks OK
- **Don't** export while animation bugs are still unfixed; changes cost more once it's a video

**Trigger phrases the user might say**:
- "Can you export it as a video?"
- "Convert it to MP4"
- "Make it a GIF"
- "60fps"

## Output specs

By default, deliver three formats at once and let the user choose:

| Format | Spec | Good for | Typical size (30s) |
|---|---|---|---|
| MP4 25fps | 1920×1080 · H.264 · CRF 18 | Embedding in WeChat Official Accounts, WeChat Channels, YouTube | 1-2 MB |
| MP4 60fps | 1920×1080 · frame duplication by default (stable compatibility) · H.264 · CRF 18; high-quality interpolation requires an explicit `--minterpolate`; animations on the Stage clock use render-video-seek.js to record true 60fps directly | High-frame-rate showcases, Bilibili, portfolios | 1.5-3 MB |
| GIF | 960×540 · 15fps · palette optimized | Twitter/X, README, Slack previews | 2-4 MB |

## Toolchain

Two scripts in `scripts/`:

### 1. `render-video.js`: HTML → MP4

Records a basic 25fps MP4. Uses playwright from dstack's local node_modules (no global install).

```bash
node $HD/scripts/render-video.js <html file>
```

Optional arguments:
- `--duration=30` animation duration (seconds)
- `--width=1920 --height=1080` resolution
- `--trim=2.2` seconds to cut from the start of the video (removes reload + font loading time)
- `--fontwait=1.5` font loading wait time (seconds); raise it when there are many fonts

Output: same directory as the HTML, a `.mp4` with the same name.

### 2. `add-music.sh`: MP4 + BGM → MP4

Mixes background music into a silent MP4, picking from the built-in BGM library by scenario (mood), or you can bring your own audio. Duration is matched automatically, with fade-in and fade-out added.

```bash
bash add-music.sh <input.mp4> [--mood=<name>] [--music=<path>] [--out=<path>]
```

**Built-in BGM library** (in `assets/bgm-<mood>.mp3`):

| `--mood=` | Style | Fits |
|-----------|------|---------|
| `tech` (default) | Apple Silicon / Apple keynote, minimal synth + piano | Product launches, AI tools, Skill promos |
| `ad` | upbeat modern electronic, with build + drop | Social media ads, product teasers, promo clips |
| `educational` | Warm and bright, light guitar/electric piano, inviting | Popular science, tutorial intros, course teasers |
| `educational-alt` | Alternative of the same kind, try a different track | Same as above |
| `tutorial` | lo-fi ambient, barely noticeable | Software demos, coding tutorials, long demos |
| `tutorial-alt` | Alternative of the same kind | Same as above |

**Behavior**:
- Music is trimmed to the video duration
- 0.3s fade-in + 1s fade-out (avoids hard cuts)
- Video stream `-c:v copy`, no re-encoding; audio AAC 192k
- `--music=<path>` takes priority over `--mood`, so you can point to any external audio directly
- A wrong mood name lists all available options instead of failing silently

**Typical pipeline** (animation export trio + soundtrack):
```bash
node render-video.js animation.html                        # record
bash convert-formats.sh animation.mp4                      # derive 60fps + GIF
bash add-music.sh animation-60fps.mp4                      # add the default tech BGM
# or for different scenarios:
bash add-music.sh tutorial-demo.mp4 --mood=tutorial
bash add-music.sh product-promo.mp4 --mood=ad --out=promo-final.mp4
```

### 3. `convert-formats.sh`: MP4 → 60fps MP4 + GIF

Generates a 60fps version and a GIF from an existing MP4.

```bash
bash $HD/scripts/convert-formats.sh <input.mp4> [gif_width] [--minterpolate]
```

Output (same directory as the input):
- `<name>-60fps.mp4`: uses `fps=60` frame duplication by default (broad compatibility); add `--minterpolate` to enable high-quality interpolation
- `<name>.gif`: palette-optimized GIF (960 wide by default, adjustable)

**Choosing a 60fps mode**:

| Mode | Command | Compatibility | Use case |
|---|---|---|---|
| Frame duplication (default) | `convert-formats.sh in.mp4` | Works in QuickTime/Safari/Chrome/VLC | General delivery, uploading to platforms, social media |
| minterpolate interpolation | `convert-formats.sh in.mp4 --minterpolate` | macOS QuickTime/Safari may refuse to open it | Showcases that need true interpolation, such as Bilibili; **you must test locally** in the target player before delivery |

Why switch the default to frame duplication? The H.264 elementary stream minterpolate outputs has a known compat bug; when minterpolate was the default, we hit "macOS QuickTime can't open it" several times. See `animation-pitfalls.md` §14.

The `gif_width` argument:
- 960 (default): general use on social platforms
- 1280: sharper but larger file
- 600: loads first on Twitter/X

### 4. `render-video-seek.js`: true 60fps / deterministic rendering (recommended for high-quality delivery)

The recordVideo path in `render-video.js` has three inherent limits: the frame rate is locked at 25fps by the Chromium compositor, there are loading black frames at the start that need trimming, and 60fps can only come from minterpolate interpolation after the fact (with ghosting + a macOS QuickTime compatibility bug, see `animation-pitfalls.md §14`). When you need **true 60fps, deterministic output, or delivery for Bilibili / a portfolio**, use seek rendering instead.

It seeks frame by frame to each timestamp and takes a screenshot, then uses ffmpeg to encode the PNG sequence into an MP4. The technical core borrows the "frozen clock + seek screenshot" idea from HeyGen HyperFrames (Apache 2.0), but doesn't bring in any third-party packages: it uses only the playwright + ffmpeg this skill already has, so it's runtime neutral.

```bash
node $HD/scripts/render-video-seek.js <html file> --fps=60
```

Arguments: `--duration` · `--fps` (default 60) · `--width` · `--height` · `--concurrency` (default 4 workers in parallel) · `--settle` (how many rAFs to wait after a seek before the screenshot, default 2; raise it for layout-heavy animations) · `--keep-chrome`. Output goes to the same directory as the HTML, a `.mp4` with the same name.

It directly solves recordVideo's three dead ends:
- **True native arbitrary frame rate**: `--fps=60` produces true 60fps (every frame is a real seeked image), no longer going through `convert-formats.sh` minterpolate interpolation, which sidesteps ghosting + the macOS compatibility bug
- **No black frames at the start**: there's no screen recording, so there's no loading-period black frame at all, and no need for `--trim` / `--fontwait`
- **Deterministic**: screenshots are taken at seeked timestamps, so the same input gives the same output, unaffected by machine load / dropped frames

**Scope (important)**: only animations on the Stage clock are supported: `<Stage>` from `assets/animations.jsx` or `<NarrationStage>` from `narration_stage.jsx`, which respond to `window.__seekRender` by freezing their self-driven clock and exposing `window.__seek(t)`. Pure CSS `@keyframes` / Lottie / hand-written non-Stage animations don't take `__seek`; keep using `render-video.js` for those (if the script can't detect `__seek` it reports an error with a hint).

**Cost**: frame-by-frame screenshots mean long videos may take longer in total than real-time recordVideo recording (mitigated by multiple workers via `--concurrency`); lots of temporary PNGs take disk space, so we recommend closing other memory-heavy apps before rendering.

**Pick-one strategy**: keep `render-video.js` as the default (zero risk, covers every type of animation); when you need true 60fps / determinism / high-quality delivery and the animation runs on the Stage clock, use `render-video-seek.js`. For long narrated animations, `render-narration.sh --seek` does seek rendering + mixing in one step.

## Complete workflow (standard recommendation)

After the user says "export the video":

```bash
cd <project directory>

# $HD is this skill's root directory

# 1. record the basic 25fps MP4
node "$HD/scripts/render-video.js" my-animation.html

# 2. derive the 60fps MP4 and GIF
bash "$HD/scripts/convert-formats.sh" my-animation.mp4

# output list:
# my-animation.mp4         (25fps · 1-2 MB)
# my-animation-60fps.mp4   (60fps · 1.5-3 MB)
# my-animation.gif         (15fps · 2-4 MB)
```

## Technical details (for troubleshooting)

### Playwright recordVideo pitfalls

- Frame rate is fixed at 25fps and can't record 60fps directly (the ceiling of the Chromium headless compositor)
- Recording starts as soon as the context is created, so `trim` must be used to cut the loading time at the front
- Default format is webm; ffmpeg has to convert it to H.264 MP4 for universal playback

`render-video.js` already handles all of the above.

### ffmpeg minterpolate parameters

Current configuration: `minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`

- `mi_mode=mci`: motion compensation interpolation
- `mc_mode=aobmc`: adaptive overlapped block motion compensation
- `me_mode=bidir`: bidirectional motion estimation
- `vsbmc=1`: variable size block motion compensation

Works well for CSS **transform animations** (translate/scale/rotate).
For **pure fades** it may produce slight ghosting; if the user dislikes it, fall back to simple frame duplication:

```bash
ffmpeg -i input.mp4 -r 60 -c:v libx264 ... output.mp4
```

### Why GIF palettes need two passes

GIF is limited to 256 colors. A single-pass GIF squeezes the whole animation's colors into a generic 256-color palette, which turns subtle palettes like beige background + orange muddy.

Two passes:
1. `palettegen=stats_mode=diff`: first scans the whole clip and generates an **optimal palette for this animation**
2. `paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle`: encodes with that palette; rectangle diff updates only the changed regions, greatly reducing file size

For fade transitions, `dither=bayer` is smoother than `none`, but the file is a bit larger.

## Pre-flight check (before export)

A 30-second self-check before exporting:

- [ ] The HTML has run all the way through in the browser with no console errors
- [ ] Frame 0 of the animation is the complete initial state (not a blank loading state)
- [ ] The last frame of the animation is a stable closing state (not cut off halfway)
- [ ] Fonts/images/emoji all render correctly (see `animation-pitfalls.md`)
- [ ] The duration argument matches the actual animation duration in the HTML
- [ ] The Stage in the HTML detects `window.__recording` and forces loop=false (must check for hand-written Stages; `assets/animations.jsx` has it built in)
- [ ] The final Sprite has `fadeOut={0}` (the last video frame doesn't fade out)
- [ ] Includes the "Created by Huashu-Design" watermark (required only for animations; for works featuring third-party brands, add the prefix "Unofficial · ". See SKILL.md §"Skill promo watermark")

## Notes to include with the delivery

Standard format for the notes given to the user after export:

```
**Complete delivery**

| File | Format | Spec | Size |
|---|---|---|---|
| foo.mp4 | MP4 | 1920×1080 · 25fps · H.264 | X MB |
| foo-60fps.mp4 | MP4 | 1920×1080 · 60fps (frame duplication by default; the interpolated version will be marked) · H.264 | X MB |
| foo.gif | GIF | 960×540 · 15fps · palette optimized | X MB |

**Notes**
- 60fps uses frame duplication by default (good compatibility); minterpolate interpolation is used only when explicitly requested (works well for transform animations, prone to artifacts on complex frames); true 60fps uses render-video-seek.js to record directly by seeking frame by frame
- The GIF is palette optimized; a 30s animation can be compressed to about 3MB

Let me know if you want a different size or frame rate.
```

## Common follow-up requests from users

| User says | Response |
|---|---|
| "It's too big" | MP4: raise CRF to 23-28; GIF: lower the resolution to 600 or the fps to 10 |
| "The GIF is too blurry" | Raise `gif_width` to 1280; or suggest MP4 instead (WeChat Moments supports it too) |
| "I need vertical 9:16" | Change the HTML source to `--width=1080 --height=1920` and re-record |
| "Add a watermark" | ffmpeg with `-vf "drawtext=..."` or `overlay=` a PNG |
| "I need a transparent background" | MP4 doesn't support alpha; use WebM VP9 + alpha or APNG |
| "I need lossless" | Set CRF to 0 + preset veryslow (the file will be 10x larger) |

## Skill promo watermark template (for animation export only)

SKILL.md specifies that animation MP4s/GIFs carry a watermark by default. The template is below (on dark backgrounds use `rgba(255,255,255,0.35)` instead; for animations featuring third-party brands, prefix "Unofficial · "):

```jsx
<div style={{
  position: 'absolute', bottom: 24, right: 32,
  fontSize: 11, color: 'rgba(0,0,0,0.4)',
  letterSpacing: '0.15em', fontFamily: 'monospace',
  pointerEvents: 'none', zIndex: 100,
}}>
  Created by Huashu-Design
</div>
```
