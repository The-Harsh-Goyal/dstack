# SFX Library · dstack

> **dstack note (audio):** dstack ships **no music or sound effects**. The upstream `assets/bgm-*.mp3` (generated with Suno) and `assets/sfx/**` (generated with ElevenLabs) were removed because their licences couldn't be verified. File names below are kept as a naming scheme: put your own licensed files in `~/.dstack/audio/` (`bgm-<mood>.mp3`) and `~/.dstack/audio/sfx/<category>/<name>.mp3` (override with `DSTACK_AUDIO_DIR` / `DSTACK_SFX_DIR`), or, only when a task asks for it, generate them with ElevenLabs (the one approved outside audio service, off by default): `DSTACK_AUDIO_PROVIDER=elevenlabs node scripts/gen-audio.mjs sfx ui/click` / `... bgm tech`. Free-plan ElevenLabs output is non-commercial and needs attribution; see "Licensing" in `references/audio-design-rules.md`. If a file is missing, `add-music.sh`, `mix-voiceover.sh` and `sfx-cues.sh` warn and carry on without it.

> **Generating a slot (dstack):** every row below can be generated from its own prompt and length: `DSTACK_AUDIO_PROVIDER=elevenlabs node scripts/gen-audio.mjs sfx <category>/<name>` writes `$DSTACK_SFX_DIR/<category>/<name>.mp3` (default `~/.dstack/audio/sfx/`). Pass `--prompt "..."` / `--seconds N` / `--loop` to override, `--force` to replace an existing file. Uses `/v1/sound-generation` (model `eleven_text_to_sound_v2`, 200 credits per generation); identical requests come from the cache in `~/.dstack/cache/elevenlabs/`. Generate only the cues the film uses. Licensing: see `audio-design-rules.md`.

> All generated with the ElevenLabs Sound Generation API, at Apple-keynote-grade audio quality.
> A product-grade SFX asset library covering animations, presentations and product demos.

**Asset location**: `assets/sfx/<category>/<name>.mp3` (dstack: `$DSTACK_SFX_DIR/<category>/<name>.mp3`, default `~/.dstack/audio/sfx/`)
**Total**: 37 SFX (30 batch-generated + 7 kept from v7b)
**Generation model**: ElevenLabs Sound Generation API (prompt_influence 0.4)
**Audio quality**: 44.1kHz MP3, Apple-keynote-grade clarity, no added reverb

---

## Directory structure

```
assets/sfx/
├── keyboard/      type, type-fast, delete-key, space-tap, enter
├── ui/            click, click-soft, focus, hover-subtle, tap-finger, toggle-on
├── transition/    whoosh, whoosh-fast, swipe-horizontal, slide-in, dissolve
├── container/     card-snap, card-flip, stack-collapse, modal-open
├── feedback/      success-chime, error-tone, notification-pop, achievement
├── progress/      loading-tick, complete-done, generate-start
├── impact/        logo-reveal, logo-reveal-v2, brand-stamp, drop-thud
├── magic/         sparkle, ai-process, transform
└── terminal/      command-execute, output-appear, cursor-blink
```

---

## Quick index

### ⌨️ Keyboard (keyboard input)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/keyboard/type.mp3` | 0.5s | Single key press (mechanical keyboard single key) | mechanical keyboard single key press |
| `sfx/keyboard/type-fast.mp3` | 1.5s | Fast continuous typing (demoing prompt input) | fast continuous typing rhythm, apple magic keyboard |
| `sfx/keyboard/delete-key.mp3` | 0.5s | backspace delete | single backspace key, low pitched thud |
| `sfx/keyboard/space-tap.mp3` | 0.5s | Light spacebar tap | soft spacebar tap, wide flat |
| `sfx/keyboard/enter.mp3` | 0.5s | Enter confirm (kept from v7b) | enter key press, crisp tactile |

### 🎯 UI (interface interaction)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/ui/click.mp3` | 0.5s | Standard UI click (kept from v7b) | crisp modern interface click |
| `sfx/ui/click-soft.mp3` | 0.5s | Soft UI click (secondary buttons/links) | soft gentle button click, mid pitched |
| `sfx/ui/focus.mp3` | 0.5s | Element focus/select (kept from v7b) | subtle focus tone, element highlight |
| `sfx/ui/hover-subtle.mp3` | 0.5s | Hover hint (microsecond-level feedback) | barely audible tick, air whisper |
| `sfx/ui/tap-finger.mp3` | 0.5s | Mobile tap (iOS interface) | finger tap on touchscreen, muted thud |
| `sfx/ui/toggle-on.mp3` | 0.5s | Toggle switched on | ios toggle switch flip, satisfying click |

### 🌊 Transition (transitions)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/transition/whoosh.mp3` | 0.5s | Standard whoosh (kept from v7b) | air whoosh transition |
| `sfx/transition/whoosh-fast.mp3` | 0.6s | Fast whoosh (title flash-in, tab switch) | quick fast air whoosh, cinematic |
| `sfx/transition/swipe-horizontal.mp3` | 0.7s | Horizontal swipe (carousel, tab switch) | smooth left-to-right air movement |
| `sfx/transition/slide-in.mp3` | 0.6s | Element slide-in (side panel, drawer) | smooth soft whoosh with arrival |
| `sfx/transition/dissolve.mp3` | 0.8s | Soft dissolve (image fade out/in) | soft dissolve, airy shimmer |

### 🃏 Container (cards/containers)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/container/card-snap.mp3` | 0.5s | Card snap/position (kept from v7b) | card snap into place |
| `sfx/container/card-flip.mp3` | 0.7s | Card flip (switching front and back) | playing card flip, crisp snap |
| `sfx/container/stack-collapse.mp3` | 0.8s | Stack collapse (list aggregation) | cards stacking, paper taps collapsing |
| `sfx/container/modal-open.mp3` | 0.6s | Modal opens | modal popping open, whoosh + thud |

### 🔔 Feedback (notifications/feedback)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/feedback/success-chime.mp3` | 1.0s | Success cue (payment succeeded, task complete) | two ascending bell tones, ios-style |
| `sfx/feedback/error-tone.mp3` | 0.7s | Error cue (warning, failure) | descending two-note warning, soft |
| `sfx/feedback/notification-pop.mp3` | 0.6s | Message pop-up (toast, notification) | notification bloop, ios message alert |
| `sfx/feedback/achievement.mp3` | 1.5s | Achievement unlocked (milestone, badge) | triumphant rising arpeggio, game-style |

### ⏳ Progress (progress/status)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/progress/loading-tick.mp3` | 0.5s | Loading tick (progress bar beat) | soft short pulse, minimal ambient |
| `sfx/progress/complete-done.mp3` | 0.8s | Completion confirm (step complete) | two ascending satisfying tones |
| `sfx/progress/generate-start.mp3` | 0.8s | AI starts generating | soft rising shimmer, magical whoosh |

### 💥 Impact (brand/impact)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/impact/logo-reveal.mp3` | 0.7s | Logo impact (kept from v7b) | logo reveal thud |
| `sfx/impact/logo-reveal-v2.mp3` | 1.5s | Longer Logo impact (cinematic) | cinematic bass hit with shimmer tail |
| `sfx/impact/brand-stamp.mp3` | 1.0s | Heavy stamp hit (certification, stamping) | rubber stamp thud, paper contact |
| `sfx/impact/drop-thud.mp3` | 0.7s | Object lands (insert, place) | heavy thud, wood surface contact |

### ✨ Magic (AI transformation)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/magic/sparkle.mp3` | 0.8s | Magic sparkle (AI highlight, surprise) | bright twinkling stars, fairy dust |
| `sfx/magic/ai-process.mp3` | 1.2s | AI processing sound (thinking state) | modulating digital hum with shimmer |
| `sfx/magic/transform.mp3` | 1.0s | Transform transition (morph effect) | rising shimmer whoosh with sparkle tail |

### 💻 Terminal (command line)

| File | Duration | Use | Prompt key points |
|---|---|---|---|
| `sfx/terminal/command-execute.mp3` | 0.5s | Command execution | crisp digital beep with tick, hacker ui |
| `sfx/terminal/output-appear.mp3` | 0.6s | Output appears | rapid digital ticks, retro printout |
| `sfx/terminal/cursor-blink.mp3` | 0.5s | Cursor blink | subtle soft digital pulse, rhythmic |

---

## Recommended combinations by scenario

### 💻 Terminal interaction demo
```
type (0.5s) → enter (0.5s) → command-execute (0.5s) → output-appear (0.6s)
```
Looping element: `cursor-blink` as ambient sound while idle.

### 🃏 Card selection flow
```
hover-subtle (0.5s, UI hover) → click-soft (0.5s, click) → card-snap (0.5s, position)
```
Or the advanced version: `card-flip` to switch front and back.

### 🤖 Full AI generation flow
```
generate-start (0.8s, start) → ai-process (1.2s, process) → sparkle (0.8s, flash) → complete-done (0.8s, done)
```
On error, use `error-tone` instead of `complete-done`.

### 🎬 Logo Reveal (brand moment)
```
whoosh-fast (0.6s, setup) → logo-reveal-v2 (1.5s, landing) → sparkle (0.8s, tail)
```
Short version: `whoosh → logo-reveal` (the v7b pair as is).

### 📱 UI interaction demo (mobile)
```
tap-finger (0.5s, tap) → slide-in (0.6s, panel slides in) → toggle-on (0.5s, toggle)
```
When done: `success-chime` or `notification-pop`.

### 📊 Data visualization / dashboard
```
loading-tick (0.5s, beat) × N → complete-done (0.8s, data in place) → achievement (1.5s, wow landing)
```

### 🎯 Form submission flow
```
click-soft (0.5s) → loading-tick ×2 (1.0s) → success-chime (1.0s)
```
Failure branch: `error-tone (0.7s)`.

### 🪄 Magic Transform scenario
```
whoosh-fast (0.6s) → transform (1.0s) → sparkle (0.8s)
```
Good for: element morphing, before/after effect comparisons, "AI rewrite" and similar demos.

---

## Usage guidelines

### Volume recommendations (from the audio dual-track system in apple-gallery-showcase.md)
- **SFX main track**: `1.0` (no attenuation)
- **BGM background track**: `0.4 ~ 0.5` (SFX clearly cut through)
- **Layering multiple SFX**: use `amix=inputs=N:duration=longest:normalize=0` to preserve dynamic range

### ffmpeg mixing template
```bash
# Single SFX aligned to a time point:
ffmpeg -i video.mp4 -itsoffset 2.5 -i sfx/ui/click.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4

# Multiple SFX + BGM:
ffmpeg -i video.mp4 \
  -itsoffset 1.0 -i sfx/transition/whoosh-fast.mp3 \
  -itsoffset 1.6 -i sfx/impact/logo-reveal-v2.mp3 \
  -i bgm.mp3 \
  -filter_complex "[3:a]volume=0.4[bgm];[0:a][1:a][2:a][bgm]amix=inputs=4:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### Selection decision tree
1. **Tactile action** (typing/clicking/swiping) → `keyboard/` or `ui/`
2. **Element entering/exiting** → `transition/`
3. **Container-level operations** (cards/modals) → `container/`
4. **Status feedback** (success/failure/notification) → `feedback/`
5. **Progress / passage of time** → `progress/`
6. **Brand landing / key moment** → `impact/`
7. **AI magic / transformation** → `magic/`
8. **Command line / code demo** → `terminal/`

### Avoid stacking sounds
- At most `max 2 SFX` playing concurrently at the same time point
- When BGM drops below 0.3, you can play 3
- Clear other SFX during a brand impact (leave 0.2s of silence before the landing)

---

## Prompt writing principles (for reuse)

Reference style: `apple keynote, tight, minimal, no reverb unless ambient, crisp, elegant`

**Three elements of a good prompt**:
1. **Physical description of the sound**: what object, what action ("mechanical keyboard single key press")
2. **Texture/style qualifiers**: apple-style / ios-style / cinematic / retro
3. **Exclusions**: no reverb / clean studio / minimal

❌ "click sound"
✅ "crisp ui button click, clean modern interface sound, apple-style, high pitched"

❌ "magic"
✅ "bright twinkling stars sound, high pitched glittery chime, fairy dust"

---

## See also
- Audio dual-track system and ffmpeg mixing: `apple-gallery-showcase.md`
- Original generation script: `/tmp/gen_sfx_batch.sh` (one-off batch generator)
