# Voiceover Pipeline · narration-driven animation

> Upgrades animation from "silent visuals + voiceover added in post" to a workflow of "**narration script first, then visuals driven by the measured audio durations**".
> Applies to: 5-20 minute concept explainer videos, tutorial videos, long-form science and knowledge content.
>
> Use it together with `references/animation-best-practices.md`: this file handles **how to sync narration and visuals**,
> while animation-best-practices handles **how each frame moves**.

---

## 🛑 Iron rules · must read before writing a single line of code

> **This can't be stressed enough: failure mode #1 for narrated animation is ending up with a PowerPoint with a voiceover.**

### Rule one · the whole film is one continuous motion narrative, not a set of independent scenes

PowerPoint is 7 slides. What we make is **one film lasting X minutes**.

**Identity switch**:
- ❌ You're not "making the content for 7 scenes"
- ✅ You're "having one or a few hero elements perform an X-minute play on screen"

**Visual skeleton = one or a few hero elements running through the whole film**:
- It appears at t=0 and leaves only at the end
- Each cue is a **state change** of it (position / size / color / perspective / form), not "swapping in a new element"
- Scene boundaries exist in the script, **but shouldn't exist on screen**: viewers can't tell "this is scene 3"; they only see one continuous motion

**Counterexample (a pitfall hit in real work on this skill's v1 · 2026-05-10)**:
- 7 `<Scene>`s each with their own independent layout, scene switch = whole page opacity 1→0 cutting to the next page
- Every cue = `opacity: p, transform: translateY((1-p)*30px)` (fade-up used monotonously)
- Result: viewers' first reaction after watching was "it's like a keynote, page after page", and the whole film's quality dropped to zero

**Correct pattern**:
- Pick 1-2 hero elements (for this article's demo, the two strings "md" and "html" should be chosen as the skeleton)
- These two strings stay on screen **from the opening to the end**
- Each "scene" is actually one state change of the hero element
  - opening: the two strings face off in the center of the screen
  - md-side: md grows larger and bolder and takes over the frame, html retreats to small type in a corner; data pours in around md
  - html-side: html flips to become the star; md retreats to a corner
  - the-real-question: the two strings return to the center, but a "≠" divider appears between them
  - the-split: the two strings push apart to either side, and the blank space in the middle opens up
  - activity-proof: the two strings flash alternately on a timeline
  - closing: the two strings land in their final answer positions
- That way the whole film is "md and html performing on screen for X minutes", not 7 independent PPT slides

**Minimal implementation skeleton** (copy and adapt directly):

```jsx
// ── Step 1: define the hero's target state (position/size/opacity) for each scene ──
const HERO_KEYS = {
  opening:    { md: { x: 50, y: 35, scale: 1.0, opacity: 1 }, html: { x: 50, y: 65, scale: 1.0, opacity: 1 } },
  'md-side':  { md: { x: 78, y: 50, scale: 1.6, opacity: 1 }, html: { x: 92, y: 8,  scale: 0.25, opacity: 0.4 } },
  'html-side':{ md: { x: 8,  y: 8,  scale: 0.25, opacity: 0.4 }, html: { x: 22, y: 50, scale: 1.6, opacity: 1 } },
  // ... one entry per segment; continuous motion runs from the previous segment's final → this segment's from
};

// ── Step 2: easing + lerp utilities ──
const expoOut = t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
const lerp = (a, b, t) => a + (b - a) * t;
const lerpPos = (from, to, t) => ({
  x: lerp(from.x, to.x, t), y: lerp(from.y, to.y, t),
  scale: lerp(from.scale, to.scale, t),
  opacity: lerp(from.opacity ?? 1, to.opacity ?? 1, t),
});

// ── Step 3: HeroAnchor component: mount it directly as a child of <NarrationStage>, not inside a <Scene> ──
const HeroAnchor = () => {
  const { time, scene, timeline } = useNarration();
  if (!scene) return null;
  const idx = timeline.scenes.findIndex(s => s.id === scene.id);
  const prevId = idx > 0 ? timeline.scenes[idx - 1].id : scene.id;
  const from = HERO_KEYS[prevId];
  const to   = HERO_KEYS[scene.id];

  // the first ~45% of the segment morphs from the prev state to this segment's state; the rest holds
  const transitionDur = Math.min(2.0, scene.duration * 0.45);
  const t = expoOut(Math.min(1, (time - scene.start) / transitionDur));
  const md   = lerpPos(from.md,   to.md,   t);
  const html = lerpPos(from.html, to.html, t);

  // add subtle breathing so every frame has motion (matches iron rule three)
  const breath = 1 + Math.sin(time * 0.6) * 0.012;

  const renderHero = (label, pos, color) => (
    <div style={{
      position: 'absolute', left: `${pos.x}%`, top: `${pos.y}%`,
      transform: `translate(-50%, -50%) scale(${pos.scale * breath})`,
      opacity: pos.opacity, color, fontSize: 360, fontWeight: 800,
      lineHeight: 1, willChange: 'transform, opacity', pointerEvents: 'none',
    }}>{label}</div>
  );
  return <>
    {renderHero('md',   md,   '#1B4965')}
    {renderHero('html', html, '#C04A1A')}
  </>;
};

// ── Step 4: main component: the hero is a child of NarrationStage; scene-level supporting elements are managed separately ──
const App = () => (
  <NarrationStage timeline={TIMELINE} audioSrc="_narration/voiceover.mp3" width={1920} height={1080}>
    <HeroAnchor />  {/* ← persists across scenes, the visual skeleton of the whole film */}
    {/* supporting elements inside scenes use useSceneFade for soft fade in/out; no hard cuts */}
    <MdSideAux />
    <HtmlSideAux />
    {/* ... */}
  </NarrationStage>
);
```

**Complete runnable reference**: `demos/md-html-narration/md-html-demo.html` (3 min 21 s, 7 segments, 21 cues, verified in real use)

### Rule two · no "hard cuts" between scenes

| Wrong pattern (PowerPoint slop) | Right pattern (cinematic) |
|---|---|
| Scene A as a whole goes `opacity 1→0` while scene B goes `opacity 0→1` | Scene A's core elements **morph into** B (smooth changes in position/size/color) |
| Each scene has its own layout, with elements appearing/disappearing | Elements **persist** on screen; only their position and form change |
| `keepMounted=false`, so components unmount the instant a scene switches | The hero uses `keepMounted=true`, sharing DOM nodes across scenes |
| Subtitle bars/data cards each fade in and fade out | The subtitle bar is the only "non-hero" entrance on screen; after holding, it **exits together with the hero's motion** |

At the implementation level:
- **Shared elements across scenes** → lift the hero to a direct child of `<NarrationStage>`, **not inside any `<Scene>`**
- Use the `useNarration()` hook in the hero to read `time`, `scene` and `isCueTriggered`, and decide its form yourself based on the current time
- Use `<Scene>` only to manage supporting elements that appear only in that segment (data cards, quotation blocks, etc.), and **don't hard-cut these supporting elements either**: enter with expoOut + stagger, exit with a fade overlap layered over the next segment

### Rule three · every frame must have motion

**Self-check method**: during recording, **grab any frame at random** (not the second a cue fires).
- If the frame looks "**completely still**" → wrong. Go back and add underlying motion (background drift / hero subtle scale / camera pan / parallax)
- There's always an **underlying motion** running (even when it's not the focus):
  - A 5-second breathing loop of `scale: 1 ↔ 1.02` on the hero element
  - A slow background drift of `translateX: 0 ↔ -20px`
  - Data cards keep a slight `translateY` jitter after entering (Perlin noise)
- A completely still frame = PowerPoint slop

### Rule four · Easing / Stagger / Hold are the baseline

| Item | Must | Forbidden |
|---|---|---|
| Easing | `expoOut` as the main axis (`cubic-bezier(0.16, 1, 0.3, 1)`), `overshoot` for emphasis, `spring` for settling | `linear`, `ease`, CSS defaults |
| Multi-element entrance | 30ms stagger (each one comes in 30ms later) | Everything appearing at once |
| Before key cues | Hold 0.3-0.5s so viewers "see" it (the previous segment's elements go still for 0.3s first, then the cue fires) | One segment ends and cuts seamlessly to the next |
| Ending | Stop abruptly, hold the last frame for 1s | Fade to black |

For detailed rules, see §1-§4 of `animation-best-practices.md`.

### Self-check · first viewer reaction

When it's done, show it to someone who hasn't seen it (or watch it yourself 24 hours later). What is **their first reaction**?

| Reaction | Rating | Action |
|---|---|---|
| "This is a PPT with a voiceover" | Fail | Go back and redo it |
| "The visuals switch along with the voice" | Below passing | Lacks continuous narrative; the hero element doesn't exist or doesn't run through |
| "This thing moves" | Passing | But nothing memorable |
| "I want to watch to the end" | Good | The pacing is right |
| "I want to screenshot this part" | Great | You've nailed it |

---

## Workflow (high level)

```
                ┌──────────────────────────┐
                │  script .md (## scene +  │
                │  [[cue:xx]] key lines)   │
                └──────────────┬───────────┘
                               │
                  narrate-pipeline.mjs
                               │
                               ▼
            ┌──────────────────────────────┐
            │ voiceover.mp3 (concatenated) │
            │ timeline.json (measured)     │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌─────────────────┐      ┌──────────────────┐
    │ HTML animation  │      │ record MP4 + mix │
    │ (NarrationStage)│      │ render-narration │
    │ live, audio sync│      │ → final MP4      │
    └─────────────────┘      └──────────────────┘
      Deliverable 1             Deliverable 2
```

## Narration script format

Put it anywhere in the project directory; the suggested file name is `script.md`:

```markdown
---
title: What Is an LLM
voice: S_JSdgdWk22   # optional, overrides the .env default voice
speed: 1.0           # optional, 0.5-2.0
gap: 0.4             # seconds of silence between segments, default 0.3
---

## intro
Hi everyone, today we'll explain what an LLM is in 5 minutes.

## what-is
LLM stands for Large Language Model, [[cue:bigmodel]]a neural network with hundreds of billions of parameters.
At its core it's a predictor playing a word-chain game.

## demo
For example, if you type "the weather today", [[cue:input]]the model predicts the most likely next word.
[[cue:predict]]Maybe "is great", maybe "is fine".
```

**Rules**:
- Segment headings `## scene-id` are English letters/digits + hyphens (such as `## what-is`, `## scene-1`)
- Put `[[cue:xx]]` **in the middle of the key line**: when the script runs, it splits the text at that position, and the moment right after the cue is the visual trigger point
- Listen for the cue id in the animation HTML with `<Cue id="xx">`
- When writing narration, **focus on rhythm + short sentences**; long sentences come out flat from TTS

## timeline.json schema

```ts
{
  title: string,
  voice: string | null,
  speed: number,
  gap: number,
  totalDuration: number,        // measured seconds of the whole voiceover.mp3
  voiceover: 'voiceover.mp3',   // path relative to timeline.json
  scenes: [
    {
      id: string,
      start: number,            // start time of this segment within the whole audio
      end: number,
      duration: number,
      audio: 'audio/<id>.mp3',  // this segment's own audio (sub-segments already concatenated before merging)
      text: string,             // full segment text with [[cue:xx]] markers stripped
      // chunks are the source for subtitle display: each chunk is a sub-segment split by cues, with its measured TTS time window
      chunks: [
        {
          text: string,            // sub-segment text
          start: number,           // time relative to the segment
          end: number,
          absoluteStart: number,   // absolute time on the whole track (aligned with voiceover.mp3)
          absoluteEnd: number,
          // words: per-character timestamps (returned as measured by TTS enable_subtitle, included by default; turn off with --no-timestamps)
          // note that text is post-TN text ("2025"→"二零二五"), with punctuation attached to the preceding character
          words: [
            { text: string, start: number, end: number, absoluteStart: number, absoluteEnd: number }
          ],
        }
      ],
      cues: [
        {
          id: string,
          offset: number,       // time relative to the segment
          absoluteTime: number, // absolute time on the whole timeline
        }
      ]
    }
  ]
}
```

`absoluteTime` and `absoluteStart/End` are all **actually measured**: the pipeline splits each segment's text at the cues into sub-segments and runs TTS on each separately, and time = the sum of the measured durations of the preceding sub-segments. **Not an approximation estimated linearly from character counts**.

## Subtitles

> **Subtitles are on by default**: long narrated videos without subtitles see retention drop significantly. NarrationStage provides `<Subtitles />` out of the box.

### Usage (one line)

```jsx
const { NarrationStage, Subtitles } = NarrationStageLib;
<NarrationStage timeline={TIMELINE} audioSrc="...">
  {/* your hero / scene content */}
  <Subtitles />  {/* ← automatically takes the active text from timeline.scenes[].chunks */}
</NarrationStage>
```

### Visual rules (Bilibili style · anti-PowerPoint)

| Item | Rule | Counterexample |
|---|---|---|
| Background | **No background** (no black bar, no backdrop-blur) | Semi-transparent black + blur = subtitle bar covering the frame = PPT feel |
| Text color | **On light backgrounds, dark ink `#1a1a1a` + white halo**; on dark backgrounds, white text + black halo | White text + black outline on a light background = muddy text |
| Font size | 32px (1080p video) | <24px is unreadable, >40px competes with the main visual |
| Font | `PingFang SC` / `Noto Sans SC` (sans-serif, the Bilibili standard) | Serif fonts = looks like film subtitles |
| Position | bottom: 90px (not hugging the edge) | Hugging the bottom edge looks cheap |
| Line length | **≤ 12-13 characters** (in mixed Chinese and English, English counts as 0.5 character) | >15 characters per line can't be read in time on phones |
| Line-splitting rule | **Never break across a full stop**: first split sentences at `。！？`, then merge each sentence at `，、；：` up to ≤maxLen | Hard-splitting by character count, turning "this is good" into "this is goo" + "d" |

`<Subtitles />` follows the rules above by default; no props needed. For dark-background scenes: `<Subtitles color="#fff" haloColor="rgba(0,0,0,0.85)" />`.

### Karaoke mode (per-character highlighting)

```jsx
<Subtitles karaoke />                          {/* whichever character is being read turns brand orange #e8590c */}
<Subtitles karaoke karaokeColor="#0a84ff" />   {/* custom highlight color */}
```

- Depends on the per-character `words` timestamps in the timeline chunks (output by narrate-pipeline.mjs; with the default silent provider they are even-spread estimates, `wordsEstimated: true`; a TTS command can return measured ones)
- Displays the whole line and changes color character by character; line splitting reuses the ≤maxLen + no-breaking-across-full-stops rule (lines are built from words, strictly aligned with pronunciation)
- When a chunk has no words, it automatically falls back to ordinary chunk mode; callers don't need to check

### Line-splitting algorithm (built into narration_stage.jsx)

```js
splitChunkToLines(text, maxLen = 13)
// 1. split sentences at strong punctuation (。！？\n)
// 2. sentences ≤ maxLen are kept as is
// 3. otherwise slice at weak punctuation (，、；：) and merge up to ≤ maxLen
// 4. hard split as a last resort (rare)
// mixed Chinese and English: English/digits count as 0.5 character of visual width
```

If, after a chunk is split, some line is obviously too long or too short, **change the cue position in the narration script** (cues split the segment more finely); don't adjust the splitting logic on the front end.

## NarrationStage API

```jsx
import 'assets/narration_stage.jsx';
const { NarrationStage, Scene, Cue, useNarration } = NarrationStageLib;

<NarrationStage
  timeline={TIMELINE}                  // contents of timeline.json
  audioSrc="_narration/voiceover.mp3"  // path relative to the current HTML
  width={1920} height={1080}
  background="#f5f1e8"
  controls={true}                      // show the bottom playback bar during live playback
>
  {/* hero element: persists across scenes; place it directly as a child of NarrationStage */}
  <HeroAnchor />

  {/* supporting elements inside a scene: appear only in that segment */}
  <Scene id="intro">
    <Cue id="bigmodel">{(triggered, progress) => (
      <SomeElement style={{ opacity: progress }} />
    )}</Cue>
  </Scene>
</NarrationStage>
```

**Hooks**:
- `useNarration()` returns `{ time, scene, sceneTime, isCueTriggered, cueProgress }`
- Read it directly in custom components; no props needed

**Scene component**:
- By default mounted only when `scene.id === id`
- Add `keepMounted` to keep it mounted (use when animation continues across scenes)

**Cue component**:
- children must be `(triggered, progress) => ReactNode`
- progress is a value ramping 0→1 after the cue fires (default 0.6s ramp)

## Time source (dual-track)

NarrationStage automatically detects `window.__recording`:
- **Live playback mode** (default): follows the audio element's currentTime, so user pauses/seek drags stay in sync
- **Video recording mode** (render-video.js sets `window.__recording = true`): rAF wall-clock self-drives from 0, and exposes `window.__seek(t)` for render-video.js to reset

## Three scripts

| Script | Input | Output |
|---|---|---|
| `scripts/tts/providers.mjs` | A single segment of text | A single mp3 + duration + word timings (silent estimate, your local TTS command, or ElevenLabs) |
| `scripts/audio/elevenlabs.mjs` | Text / prompt | ElevenLabs client: fixed host, key handling, cache (used by the elevenlabs provider and `gen-audio.mjs`) |
| `scripts/gen-audio.mjs` | Mood / SFX slot | `bgm-<mood>.mp3` or `sfx/<category>/<name>.mp3` in your audio library (`DSTACK_AUDIO_PROVIDER=elevenlabs`) |
| `scripts/narrate-pipeline.mjs` | Narration script .md | voiceover.mp3 + timeline.json |
| `scripts/mix-voiceover.sh` | Video + voiceover.mp3 [+ BGM] | MP4 with audio |
| `scripts/render-narration.sh` | Narration HTML + timeline.json | Final MP4 (recording + mixing in one go) |

## TTS providers (dstack)

> dstack note: the upstream Doubao (ByteDance) TTS client was removed. By default dstack sends narration text nowhere. The only cloud provider is ElevenLabs (approved, US host `api.elevenlabs.io`), and it runs only when you select it for a task.

- `--tts silent` (default, or `DSTACK_TTS_PROVIDER=silent`): no voice. Each chunk gets a silent track whose length is estimated from the text (English ~155 words/min, set `DSTACK_TTS_WPM`; CJK ~4.2 chars/s; small pauses for punctuation). timeline.json keeps the same schema, with estimated word timings, so subtitle-only films and karaoke layout still work. Record a real voice later and re-run with a provider.
- `--tts command` with `DSTACK_TTS_COMMAND`: runs a local command per chunk. Placeholders `{text_file}`, `{out}` (audio to write), `{voice}`, `{speed}`. If it prints `{"words":[{"text","start","end"}]}` on its last stdout line, those timings are used. This is also where a vetted provider adapter can be plugged in later.
- `--tts elevenlabs` (or `DSTACK_TTS_PROVIDER=elevenlabs`): real voice from ElevenLabs. Each chunk goes to `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128`; the character alignment it returns becomes measured word timings (`wordsEstimated: false`), and the audio is re-encoded to 24 kHz mono so it joins the silent gaps cleanly.
  - Voice: `DSTACK_ELEVENLABS_VOICE` (default `JBFqnCBsd6RMkjVDRZzb`, "George"). A script's `voice:` is used only if it looks like an ElevenLabs voice id (20 letters/digits). Find ids in the ElevenLabs voice library or with `GET /v1/voices`.
  - Model: `DSTACK_ELEVENLABS_MODEL` (default `eleven_multilingual_v2`, stable on long-form, 1 credit per character; `eleven_flash_v2_5` is cheaper and faster, `eleven_v3`/`eleven_v4` are more expressive).
  - `speed:` maps to `voice_settings.speed` (clamped to 0.7–1.2).
  - Key: `ELEVENLABS_API_KEY` in the environment, or `DSTACK_ELEVENLABS_KEY_FILE` pointing at a file outside the repo. Never in the script, the repo or `.env.example`.
  - No key: one warning, then the whole run uses `silent` (timeline.json records `ttsRequested`/`ttsFallback`). An API error (bad key, no credits, rate limit) does the same for the failing chunk and every later one; the run never crashes and the key is masked in every message.
  - Cache: each chunk is cached in `~/.dstack/cache/elevenlabs/` by voice + model + speed + text, so re-running after editing one scene only pays for the changed chunks.
  - Licensing: free-plan output is non-commercial and must carry "elevenlabs.io" or "11.ai" in the title when published; paid plans include a commercial licence. Quotes and links: "Licensing" in `audio-design-rules.md`.
- Anything else errors out with a clear message before any work starts.

## Standard workflow (10 steps)

1. **Write the narration script**: the narration script is the source code. First write the complete voiceover, mark segment headings `## scene-id`, and add `[[cue:xx]]` before key lines
2. **Run narrate-pipeline**: `node scripts/narrate-pipeline.mjs --script script.md --out-dir _narration` (add `--tts command` for a local TTS, or `--tts elevenlabs` when the task asks for a real voice)
3. **Listen to the whole voiceover.mp3**: if the pacing is off, go back and revise the script. **This step sets the ceiling on the whole film's quality**
4. **🛑 Answer the iron rules before designing**: what is the hero element? What state is it in for each segment? How does it morph across scenes? If you can't answer, don't write code
5. **Write the animation HTML**: use NarrationStage + one or a few hero elements performing across scenes
6. **Live preview**: open the HTML in a browser, click ▶ Play, and listen to the visuals + narration sync
7. **First-viewer self-check**: score it with the "Self-check · first viewer reaction" table above. If it fails, go back to Step 4 and redo it
8. **Record the video**: `bash scripts/render-narration.sh demo.html --timeline=_narration/timeline.json` (automatically records a silent MP4 + mixes in the voiceover)
9. **Optional BGM**: add `--bgm-mood=educational` (or tech / tutorial, etc.) to render-narration
10. **Deliver**: browser HTML (for live demos) + final MP4 (for publishing)

## Troubleshooting

| Problem | Fix |
|---|---|
| TTS error | `--tts command` needs `DSTACK_TTS_COMMAND`; run the command by hand on one line of text to check it writes `{out}` |
| elevenlabs fell back to silent | Read the one `[tts] WARNING` line (and `ttsFallback` in timeline.json): no key, 401 bad key, 402 no credits / plan, 429 rate limit. Fix it and re-run; finished chunks come from the cache |
| A segment's audio is noticeably longer/shorter than the script | That segment's text has odd punctuation or emoji and TTS parsed it abnormally → revise the script |
| cue absoluteTime is inaccurate | Something went wrong with ffmpeg when concatenating sub-segments within the segment → check mp3 encoding consistency |
| The recorded video has black screens | render-video.js didn't receive the `window.__ready` signal → check whether NarrationStage mounted properly |
| The recorded video stutters | The animation has heavy layout (lots of box-shadow / blur) → simplify or pre-composite |
| Audio and video out of sync during live playback | Audio element loading delay → add `preload="auto"` or preload locally |

## When not to use this pipeline

- **Short animations <60s**: just make a silent animation + add voiceover in post (add-music.sh + a single separate TTS segment); no timeline driving needed
- **BGM-only videos**: use `add-music.sh` with your own `bgm-<mood>.mp3` (or one made with `gen-audio.mjs bgm <mood>`)
- **Replacing TTS with a human recording**: replace `voiceover.mp3` with the human recording, and write the timeline by hand or measure segment durations with ffprobe + generate it with a utility script → the rest of the workflow is the same

---

**One last reminder**: go back to the iron rules before writing code. **Don't make a PowerPoint with a voiceover**.
