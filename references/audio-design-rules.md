# Audio Design Rules · dstack

> **dstack note (audio):** dstack ships **no music or sound effects**. The upstream `assets/bgm-*.mp3` (generated with Suno) and `assets/sfx/**` (generated with ElevenLabs) were removed because their licences couldn't be verified. File names below are kept as a naming scheme: put your own licensed files in `~/.dstack/audio/` (`bgm-<mood>.mp3`) and `~/.dstack/audio/sfx/<category>/<name>.mp3` (override with `DSTACK_AUDIO_DIR` / `DSTACK_SFX_DIR`), or, only when a task asks for it, generate them with ElevenLabs (the one approved outside audio service, off by default): `DSTACK_AUDIO_PROVIDER=elevenlabs node scripts/gen-audio.mjs sfx ui/click` / `... bgm tech`. Free-plan ElevenLabs output is non-commercial and needs attribution; see "Licensing" in `references/audio-design-rules.md`. If a file is missing, `add-music.sh`, `mix-voiceover.sh` and `sfx-cues.sh` warn and carry on without it.


> Audio application recipes for all animation demos. Use together with `sfx-library.md` (the asset list).
> Battle-tested through: the upstream launch hero v1-v9 iterations · Gemini deep breakdowns of Anthropic's three official films · 8000+ A/B comparisons

---

## Core principle · Dual-track audio (iron rule)

Animation audio **must be designed as two independent layers**; never just one:

| Layer | Role | Time scale | Relationship to visuals | Frequency band |
|---|---|---|---|---|
| **SFX (beat layer)** | Marks each visual beat | Short, 0.2-2 seconds | **Tightly synced** (frame-level alignment) | **High frequencies 800Hz+** |
| **BGM (ambient bed)** | Emotional bed, sound field | Continuous, 20-60 seconds | Loosely synced (section-level) | **Low-mid frequencies <4kHz** |

**Animation with only BGM is crippled**: viewers subconsciously sense that "the picture moves but nothing in the sound responds", and that's exactly where the cheap feel comes from.

---

## Gold standard · The golden ratios

These values are **hard engineering parameters** from measuring Anthropic's three official films + comparing against our own finalized v9; apply them directly:

### Volume
- **BGM volume**: `0.40-0.50` (relative to full scale 1.0)
- **SFX volume**: `1.00`
- **Loudness difference**: BGM **-6 to -8 dB below** the SFX peak (SFX stand out through the loudness difference, not through absolute loudness)
- **amix parameter**: `normalize=0` (never use normalize=1; it flattens the dynamic range)

### Frequency band separation (P1 hard optimization)
Anthropic's secret isn't "loud SFX"; it's **frequency band layering**:

```bash
[bgm_raw]lowpass=f=4000[bgm]      # Limit BGM to low-mid frequencies <4kHz
[sfx_raw]highpass=f=800[sfx]      # Push SFX up to mid-high frequencies 800Hz+
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]
```

Why: the human ear is most sensitive to the 2-5kHz range (the "presence band"). If the SFX all sit in this range and the BGM covers the full spectrum, **the SFX get masked by the BGM's high-frequency content**. Pushing the SFX up with highpass + pressing the BGM down with lowpass gives each its own part of the spectrum, and SFX clarity jumps up a notch.

### Fade
- BGM in: `afade=in:st=0:d=0.3` (0.3s, avoids a hard cut)
- BGM out: `afade=out:st=N-1.5:d=1.5` (1.5s long tail, a sense of closure)
- SFX carry their own envelope; no extra fade needed

---

## SFX cue design rules

### Density (how many SFX per 10 seconds)
Measured SFX density in Anthropic's three films falls into three tiers:

| Film | SFX per 10s | Product personality | Scenario |
|---|---|---|---|
| Artifacts (ref-1) | **~9 per 10s** | Feature-dense, lots of information | Complex tool demo |
| Code Desktop (ref-2) | **0** | Pure atmosphere, meditative | Developer tool focus state |
| Word (ref-3) | **~4 per 10s** | Balanced, office rhythm | Productivity tool |

**Heuristics**:
- Calm/focused product personality → low SFX density (0-3 per 10s), BGM-led
- Lively/information-heavy product personality → high SFX density (6-9 per 10s), SFX drive the rhythm
- **Don't fill every visual beat**: leaving space is more premium than density. **Deleting 30-50% of the cues makes the remaining ones more dramatic**.

### Cue selection priority
Not every visual beat needs an SFX. Choose by this priority:

**P0 must have** (leaving them out feels off):
- Typing (terminal/input)
- Click/select (moments of user decision)
- Focus switch (the visual protagonist shifts)
- Logo reveal (brand closure)

**P1 recommended**:
- Element entrance/exit (modal / card)
- Completion/success feedback
- AI generation start/end
- Major transitions (scene changes)

**P2 optional** (too many gets messy):
- hover / focus-in
- Progress ticks
- Decorative ambient

### Timestamp alignment precision
- **Same-frame alignment** (0ms error): clicks/focus switches/logo landing
- **1-2 frames early** (-33ms): fast whooshes (sets up the viewer's expectation)
- **1-2 frames late** (+33ms): objects landing/impacts (matches real physics)

---

## BGM selection decision tree

The upstream skill shipped 6 BGM tracks; dstack ships none. Use your own `bgm-<mood>.mp3`, a track from your local library (see "Local music library"), or generate one when a task asks for it (`DSTACK_AUDIO_PROVIDER=elevenlabs node scripts/gen-audio.mjs bgm tech`). Mood names:

```
What is the animation's personality?
├─ Product launch / tech demo → bgm-tech.mp3 (minimal synth + piano)
├─ Tutorial walkthrough / tool usage → bgm-tutorial.mp3 (warm, instructional)
├─ Educational learning / explaining principles → bgm-educational.mp3 (curious, thoughtful)
├─ Marketing ads / brand promotion → bgm-ad.mp3 (upbeat, promotional)
└─ Need a variant of the same style → bgm-*-alt.mp3 (their respective alternates)
```

### Scenarios without BGM (worth considering)
See Anthropic Code Desktop (ref-2): **0 SFX + pure lo-fi BGM** can also be very premium.

**When to choose no BGM**:
- Animation is <10s long (BGM can't establish itself)
- The product personality is "focus/meditation"
- The scene itself has ambient sound/narration
- When SFX density is very high (avoids auditory overload)

---

## Scene recipes (ready to use)

### Recipe A · Product launch hero (same as the upstream v9 hero)
```
Duration: 25 seconds
BGM: bgm-tech.mp3 · 45% · band <4kHz
SFX density: ~6 per 10s

cues:
  Terminal typing → type × 4 (0.6s apart)
  Enter          → enter
  Cards converge → card × 4 (staggered 0.2s)
  Select         → click
  Ripple         → whoosh
  4 focuses      → focus × 4
  Logo           → thud (1.5s)

Volume: BGM 0.45 / SFX 1.0 · amix normalize=0
```

### Recipe B · Tool feature demo (see Anthropic Code Desktop)
```
Duration: 30-45 seconds
BGM: bgm-tutorial.mp3 · 50%
SFX density: 0-2 per 10s (very few)

Strategy: let BGM + narration voiceover drive it, with SFX only at **decisive moments** (file saved/command finished)
```

### Recipe C · AI generation demo
```
Duration: 15-20 seconds
BGM: bgm-tech.mp3 or no BGM
SFX density: ~8 per 10s (high density)

cues:
  User input       → type + enter
  AI starts working → magic/ai-process (1.2s loop)
  Generation done  → feedback/complete-done
  Result shown     → magic/sparkle
  
Highlight: ai-process can loop 2-3 times across the whole generation process
```

### Recipe D · Pure-atmosphere long take (see Artifacts)
```
Duration: 10-15 seconds
BGM: none
SFX: 3-5 carefully designed cues used on their own

Strategy: every SFX is the star, with no problem of BGM "smearing everything together".
Suits: slow-motion single product shots, close-up showcases
```

---

## ffmpeg mixing templates

### Template 1 · Overlay a single SFX onto a video
```bash
ffmpeg -y -i video.mp4 -itsoffset 2.5 -i sfx.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### Template 2 · Multi-SFX timeline mix (aligned to cue times)
```bash
ffmpeg -y \
  -i sfx-type.mp3 -i sfx-enter.mp3 -i sfx-click.mp3 -i sfx-thud.mp3 \
  -filter_complex "\
[0:a]adelay=1100|1100[a0];\
[1:a]adelay=3200|3200[a1];\
[2:a]adelay=7000|7000[a2];\
[3:a]adelay=21800|21800[a3];\
[a0][a1][a2][a3]amix=inputs=4:duration=longest:normalize=0[mixed]" \
  -map "[mixed]" -t 25 sfx-track.mp3
```
**Key parameters**:
- `adelay=N|N`: the first value is the left-channel delay (ms), the second the right channel; write it twice to keep the stereo aligned
- `normalize=0`: preserves the dynamic range. Key!
- `-t 25`: truncates to the specified duration

### Template 3 · Video + SFX track + BGM (with frequency band separation)
```bash
ffmpeg -y -i video.mp4 -i sfx-track.mp3 -i bgm.mp3 \
  -filter_complex "\
[2:a]atrim=0:25,afade=in:st=0:d=0.3,afade=out:st=23.5:d=1.5,\
     lowpass=f=4000,volume=0.45[bgm];\
[1:a]highpass=f=800,volume=1.0[sfx];\
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k final.mp4
```

---

## Failure mode quick reference

| Symptom | Root cause | Fix |
|---|---|---|
| SFX can't be heard | Masked by the BGM's high frequencies | Add `lowpass=f=4000` to the BGM + `highpass=f=800` to the SFX |
| Sound effects too loud and harsh | SFX absolute volume too high | Lower SFX volume to 0.7 and BGM to 0.3 at the same time, keeping the gap |
| BGM and SFX rhythms clash | Wrong BGM (music with a strong beat) | Switch to ambient / minimal synth BGM |
| BGM cuts off suddenly when the animation ends | No fade out | `afade=out:st=N-1.5:d=1.5` |
| SFX overlap into mush | Cues too dense + each SFX too long | Keep SFX under 0.5s, with cues ≥ 0.2s apart |
| WeChat Official Account mp4 has no sound | WeChat Official Accounts sometimes mute auto-play | Don't worry, there's sound when the user opens it; GIFs never had sound anyway |

---

## Linking with visuals (advanced)

### SFX timbre should match the visual style
- Warm off-white/paper-like visuals → SFX with **wooden/soft** timbres (Morse, paper snap, soft click)
- Cold black tech visuals → SFX with **metallic/digital** timbres (beep, pulse, glitch)
- Hand-drawn/playful visuals → SFX with **cartoony/exaggerated** timbres (boing, pop, zap)

Our current warm off-white background in `apple-gallery-showcase.md` → pairs with `keyboard/type.mp3` (mechanical) + `container/card-snap.mp3` (soft) + `impact/logo-reveal-v2.mp3` (cinematic bass)

### SFX can guide the visual rhythm
Advanced technique: **design the SFX timeline first, then adjust the visual animation to align with the SFX** (not the other way around).
Because every SFX cue is a "clock tick", visual animation that adapts to the SFX rhythm is very stable; when SFX chase the visuals instead, being off by ±1 frame often feels wrong.

---

## Quality checklist (self-check before release)

- [ ] Loudness difference: SFX peak - BGM peak = -6 to -8 dB?
- [ ] Bands: BGM lowpass 4kHz + SFX highpass 800Hz?
- [ ] amix normalize=0 (preserves dynamic range)?
- [ ] BGM fade-in 0.3s + fade-out 1.5s?
- [ ] Is the number of SFX appropriate (density chosen by the scene's personality)?
- [ ] Is every SFX aligned to the same frame as its visual beat (within ±1 frame)?
- [ ] Is the logo reveal sound effect long enough (1.5s recommended)?
- [ ] Listen once with the BGM off: do the SFX alone have enough sense of rhythm?
- [ ] Listen once with the SFX off: does the BGM alone have emotional rise and fall?

Each of the two layers should hold together when heard alone. If it only sounds good with both layers stacked, it isn't done well.

## Local music library

Free background music that stays on this machine. `DSTACK_AUDIO_PROVIDER=local node scripts/gen-audio.mjs bgm <mood>` (or `DSTACK_AUDIO_PROVIDER=local bash scripts/add-music.sh anim.mp4 --mood=<mood>`) picks a track tagged `<mood>` from `$DSTACK_MUSIC_DIR` (default `~/.dstack/music`), copies it to `bgm-<mood>.mp3` with a `.provenance.json`, and prints the credit line. With `DSTACK_AUDIO_PROVIDER=elevenlabs`, bgm falls back to the library when there is no key, the plan is free (the Music API is paid-only) or the request fails; with no usable track the video stays silent. Selection is deterministic (same library + mood + `--seed`/`DSTACK_MUSIC_SEED` → same track) and makes no network calls. `bash tools/doctor.sh` validates the manifest.

Rules: a track is used only if it has a complete `manifest.json` entry; tracks with `"commercial": false` are refused unless `DSTACK_MUSIC_ALLOW_NONCOMMERCIAL=1` (then only for non-commercial work). `add-music.sh` prints the credit and writes `<output>.credits.txt`; put any "Attribution required" line in the delivery note. The library must be outside the repo, and `.gitignore` blocks all audio files.

### Adding tracks

1. Download a track from a source whose licence you have read, without logging in or getting past a captcha or bot check. No China-based hosts or mirrors.
2. Save it in `~/.dstack/music/` (mp3, wav, ogg, flac, m4a…; non-mp3 is converted locally).
3. Add an entry to `~/.dstack/music/manifest.json`:

```json
{ "version": 1, "tracks": [ {
  "file": "komiku-13-the-wind.ogg",
  "moods": ["calm", "ambient"],
  "duration": 114.0,
  "title": "The Wind", "artist": "Komiku",
  "source_url": "https://commons.wikimedia.org/wiki/File:Komiku_-_13_-_The_Wind.ogg",
  "licence": { "name": "CC0", "url": "https://creativecommons.org/publicdomain/zero/1.0/" },
  "attribution": "",
  "commercial": true,
  "fetched": "2026-10-28"
} ] }
```

Required fields are `file` (relative to the folder), `moods` (tags such as `tech`, `tutorial`, `educational`, `ad`, `calm`), `duration` (seconds), `source_url`, `licence.name` and `licence.url`, `attribution` (the exact credit text the licence asks for, `""` if none), `commercial` (true only if the licence allows commercial use) and `fetched` (YYYY-MM-DD). Extra fields (title, artist, sha1, the licence terms) are kept in the provenance. For CC BY music the attribution needs the title, the creator, the licence with a link, and the source. Then run `bash tools/doctor.sh` or `node scripts/audio/music-library.mjs list`.

## Licensing (dstack: ElevenLabs output)

dstack generates audio only through ElevenLabs, and only when a task asks for it (`DSTACK_TTS_PROVIDER=elevenlabs` for narration, `DSTACK_AUDIO_PROVIDER=elevenlabs` for `scripts/gen-audio.mjs`). What you may do with the output depends on the ElevenLabs plan **at the time it was generated**. What the official pages say (checked 28 Oct 2026):

- Help center, "Can I publish the content I generate on the platform?" (https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform, same text at https://help.elevenlabs.io/hc/en-us/articles/13313564601361): "The free plan does not include a commercial license and cannot be used for any commercial purpose. If you publish content generated using our Services on a free plan or without being signed-in to your account, you must attribute it to ElevenLabs by including "elevenlabs.io" or "11.ai" in the title (except in the case where your content is generated using Eleven Music on a free plan or without being signed-in to your account, you must attribute it to ElevenLabs by referencing "Eleven Music" when distributing such content)." and "All paid plans include a commercial license, provided you're not using Beta Services." It also says "Content created outside of a paid subscription (before or after) cannot be used commercially and always requires attribution when shared non-commercially." and "Attribution requirement is subject to the agreement you have with ElevenLabs."
- Terms of Service (https://elevenlabs.io/terms-of-use): "if you access or use our Services free of charge (such a user, a "Free User"), you may only use the Services for non-commercial purposes; (ii) if you access or use our Services through a paid subscription plan (such a user, a "Paid User"), you may use the Services for commercial purposes".
- Pricing (https://elevenlabs.io/pricing): Starter, the lowest paid plan, lists "Commercial License" and "Music commercial use" ("Everything in free, plus"). The pages say "all paid plans", i.e. Starter or above; the attribution rule is "elevenlabs.io" **or** "11.ai" in the title (music: "Eleven Music").
- Music: "The Music API is only available to paid users." (https://elevenlabs.io/docs/eleven-api/guides/cookbooks/music). Music rights also follow the Music Terms' "Music Commercial Rights Table" (https://elevenlabs.io/music-terms, last updated 09 October 2026), which varies by plan; check it before distributing music (e.g. to streaming platforms).

Practical rule: on the free plan, treat output as drafts (non-commercial, title must carry "elevenlabs.io" or "11.ai"; music: "Eleven Music"). For client or commercial work, generate on a paid plan. `gen-audio.mjs` writes a `<file>.provenance.json` next to each generated file so you can tell later where it came from.

Credits (pricing FAQ): text to speech about 1 credit per character, Sound Effects 200 credits per generation, Eleven Music 900 credits per minute. Generate only what the task needs; repeats come from the local cache for free.

---

## References

- SFX asset list: `sfx-library.md`
- Visual style reference: `apple-gallery-showcase.md`
- In-depth audio analysis of Anthropic's three films: AUDIO-BEST-PRACTICES.md (the author's local material, not distributed with the repo)
- Upstream v9 field case: hero-animation-v9-final.mp4 (not distributed with the repo)
