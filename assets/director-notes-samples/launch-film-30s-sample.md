# v5 · "Markdown is the new typewriter."

> **dstack note (audio):** dstack ships **no music or sound effects**. The upstream `assets/bgm-*.mp3` (generated with Suno) and `assets/sfx/**` (generated with ElevenLabs) were removed because their licences couldn't be verified. File names below are kept only as a naming scheme: put your own licensed files in `~/.dstack/audio/` (`bgm-<mood>.mp3`) and `~/.dstack/audio/sfx/<category>/<name>.mp3` (override with `DSTACK_AUDIO_DIR` / `DSTACK_SFX_DIR`). If a file is missing, `add-music.sh`, `mix-voiceover.sh` and `sfx-cues.sh` warn and carry on without it.


> Director's Notes for the **huashu-md-html v2.0** launch film
> 30 seconds · 1920×1080 · 25 fps · no voiceover
> Director: huashu-design (acting as Apple-tier launch film director)
> Composer: TBD (target: Max Richter / Ólafur Arnalds / Jóhann Jóhannsson minimal-cinematic register)
> Color base: ivory white #FAFAF6 · ink #1A1A1A · terracotta #C2410C
> Type: Newsreader (display + body) · JetBrains Mono (interface) · Noto Serif SC (Chinese)

---

## Contents

- [Part I · Director's Statement](#part-i--directors-statement)
- [Part II · Visual System](#part-ii--visual-system)
- [Part III · Story Arc](#part-iii--story-arc)
- [Part IV · Shot-by-Shot Storyboard](#part-iv--shot-by-shot-storyboard)
- [Part V · Production Manifest](#part-v--production-manifest)

---

# Part I · Director's Statement

## 1.1 This is not a "feature walkthrough film"

The vast majority of SaaS upgrade videos make the same mistake: they treat the camera like a PPT. Open → 6 features slide past → logo + slogan → end. Every second is spent "showing" and not a single second "telling". When viewers leave, what they remember is not the product but "yet another page that looks AI-made".

**This film does not do that**.

We are going to tell a story. The story is a single line:

> **"md is the source code; everything else is product."**

This is not a slogan; it's a worldview. Markdown is not "a lightweight document format". It is the source of writing. Every downstream form (html, docx, pdf, epub) is a product derived from this same source. huashu-md-html v2.0 extends this product chain from 4 to 6, but what it extends is not the "feature list"; it's **the radius of the source's influence**.

If viewers remember only one thing after watching this film, I want it to be: "so md is actually the source code". However much of the feature list they remember is a bonus.

## 1.2 A dialogue with the context of visual language

Every good promotional film is in dialogue with a set of earlier works. The context I want this film to be in dialogue with is:

**Apple — "Designed by Apple in California" (2013)**

To me, that film is the ceiling of tech-company promotional films. Director Mark Romanek got three things right:
1. **Pure white background + serif type**: it tells viewers this is "design about design", not a demo
2. **Slow beats**: every line of on-screen text lags half a beat behind the viewer's reading speed, forcing viewers to linger
3. **Jony Ive's narration is almost a whisper**: not selling, sharing

Our film **has no voiceover**, so the first two principles have to be amplified to 200% through typography and timing.

**Apple Silicon Launch Films (M1 / M2 / M3, 2020-2024)**

This series of short films taught me that **typography can dance too**. The three characters "M1" can go from vanishing, to appearing, to scaling up, to rotating, to exploding into dust, to reassembling. Viewers watch a logo become the lead of a dance drama in 30 seconds.

**The hero of this film is not the product UI; it's the two characters `md.` + an orange period**. It has to become the lead of a dance drama in 30 seconds.

**Anthropic brand language (2024-2026)**

Anthropic turned "terracotta orange + serif + geometric abstraction" into an anti-slop template for AI companies. It told the industry: you can be a tech company, and you can also look like a small philosophy book published by Penguin Classics.

We inherit this palette, but we make it **more restrained**. Anthropic sometimes uses pure terracotta as large color blocks; our terracotta is only ever an accent (< 8% of the total frame area), and the remaining 92% is left to ivory white and ink black.

**Penguin Classics (since 1947, after Romek Marber's 1961 grid)**

Penguin taught me **the courage of typography**. A book cover can be a large serif + one black horizontal rule + no illustration, and readers will actually stop.

The slogan reveal at seconds 25-29 borrows this language: **ONE SOURCE.** and **SIX FORMS.** are not "decorative text"; they are the frame itself.

**Pentagram (Paula Scher / Michael Bierut)**

Pentagram's signature is **information architecture**: the distance between words, the distance between words and edges, the size ratio between type levels, none of it is "by intuition"; it's math.

Our grid system (Part II.3) comes from this tradition.

**Kenya Hara, *White* (2008)**

Hara wrote: "White is not a color; it is a sensibility." (白は色彩ではなく、感受性なのだ)

The real lead of this film is not `md.`; it's **the field of ivory white** surrounding it. Every shot has to leave at least 60% negative space. Negative space is not "not filled yet"; it is the content itself.

**Massimo Vignelli — Modernism in design**

Vignelli's motto: "If you can design one thing, you can design everything."

Our design system doesn't allow "adding a font just for this shot" or "adding a corner radius just for this shot". All 12 shots share the same set of 5 color values, 3 typefaces, and 4 easing curves.

## 1.3 Audience profile

Three kinds of viewers, ranked by importance:

**Primary audience A · existing users of huashu-md-html v1 (about 60% of traffic)**

They open the film to find out "what got upgraded". Our promise to them: within 30 seconds, you must know clearly that:
- New capability 5: md → publication-grade PDF
- New capability 6: md → standard EPUB
- The visual quality of these two capabilities is higher than you'd expect (not the "I could hack that with wkhtmltopdf" level)

→ Shot 08 and Shot 09 get 3 seconds each, must carry a "★ NEW" tag, and the destination card must show **visible professional-grade details** like "printer's crop marks" and "Apple Books frame", so existing users instantly get that "this isn't a filler feature; it was built properly".

**Secondary audience B · AI-native creators who've heard of huashu-md-html but haven't used it (about 25%)**

What they care about is "what does this skill have to do with me". Our promise to them: within 30 seconds, you must realize that:
- When you write articles / do research / write white papers, **md should be your source of truth**
- 6 downstream formats, handled with one command

→ Shot 04 (any → md) has to show them PDF/DOCX/PPTX/XLSX/HTML all being absorbed into md together. This is the visual embodiment of "source thinking".

**Outer audience C · designers / editors / publishers who are completely unfamiliar with it (about 15%)**

What they see is "a beautiful tech short film", and they won't necessarily follow up. Our promise to them: within 30 seconds, you must leave an impression that:
- What this team makes **has publishing-house taste**
- It's different from the AI tools you've seen before

→ The whole film's anti-AI-slop self-check (Part II.7) is made for them. No purple gradients, emoji icons, or hand-drawn SVG figures, ever.

## 1.4 Rhythm philosophy

The rhythm of Apple promotional films isn't constant. It's a curve of **slow beat, acceleration, peak, gentle resolve** (see the emotion curve chart in Part III).

Specifically for this film:

- **0-3s slow beat**: the viewer enters. The typography breathes one character at a time.
- **3-6s first acceleration**: the md characters are born, and 6 file cards fly in one after another.
- **6-22s second acceleration**: 6 capabilities in one unbroken run, 3 seconds each, never letting go.
- **22-26s peak**: the two-line slogan reveal, with all chrome pulsing in sync.
- **26-30s gentle resolve**: the capability map slowly fades in, and the last second is left for the brand stamp + a very faint piano reverb tail.

**Key decision**: second 22 is the climax of this film (not second 29). Second 29 is the resolution; second 22 is the climax. Don't mix the two up.

## 1.5 What this film does **not** do (anti-AI-slop self-check)

Ranked by importance:

| Don't | Reason |
|------|------|
| No purple gradients | The universal formula for "tech feel" in training data; in 2026 it reads as cyber slop |
| No emoji as icons | The "if it's not professional, patch it with emoji" disease |
| No SVG figures / hands / abstract human forms | SVG figures drawn by AI always have misplaced features and weird proportions |
| No Inter/Roboto/Arial as display | Too common, collides with system fonts |
| No cyber neon / dark navy background #0D1117 | A worn-out copy of the GitHub dark mode aesthetic |
| No stacking effects (blur/glow/particle) | An effect that appears twice is decoration; three times is slop |
| No Lorem ipsum | Every piece of placeholder text uses real readable content (including hooks like "md is the source. Anything else is product.") |
| No stock photos | Not a single real photo appears in the whole film (it's about typography, not lifestyle) |
| No progress bar + timecode + copyright credit bar | These are player chrome, not content chrome; they would collide with the external player |
| Don't let the md characters look the same in every scene | They need 12 states across 12 shots while keeping the same core letterform |

## 1.6 One-line positioning

> **"Markdown is the new typewriter."**
>
> A 30-second film about source-of-truth thinking, made for designers who write and writers who design.

---

# Part II · Visual System

## 2.1 Full palette

Not 3 colors but 10. Every color has a **functional definition** (not "use it because it looks good").

```
Name           HEX        Role                                    Max share of frame
─────────────────────────────────────────────────────────────────────
Ivory paper    #FAFAF6    Main background (ivory, a hint of warmth)   60-70%
Mist           #F2EDE4    Secondary background layer (slight dark under card shadows)  < 15%
Mica           #E6E1D6    Fine lines / dividers / card borders    < 5%
Smoke          #6B6B6B    Secondary text / metadata               < 5%
Cinder         #3D3530    Secondary dark (deep brown-black, not pure black)  < 10%
Ink            #1A1A1A    Main black / main text                  20-25%
Charred        #2A2620    Very deep brown-black (cover cards only)  < 5%
Terracotta     #C2410C    Main accent (Anthropic tone)            5-8%
Terra Hot      #E55D21    Highlight variant (only for the instant the NEW tag lights up)  < 1%
Terra Deep     #8B2D08    Shadow variant (terracotta drop shadow)  < 1%
```

**Iron rules**:
- No shot uses any color outside these 10. **No "adding a bit of cool gray just for this shot"**.
- The terracotta family (Terracotta + variants) together takes up < 10% of the frame, or the visuals overload.
- Any text may only use one of 4 colors: Ink / Cinder / Smoke / Terracotta.

## 2.2 Type system

```
Type level     Typeface              weight    Use                          Tracking (em)
────────────────────────────────────────────────────────────────────────────────────
Display XXL    Newsreader            700       slogan top word (200px)      -0.035
Display XL     Newsreader            700       capability number (48px)     -0.020
Display L      Newsreader            600       hero md characters (300-480px)  -0.040
Display M      Newsreader            600       chapter title (32-44px)     -0.015
Body L         Newsreader            400       essay body (18-22px)         0
Body M (zh)    Noto Serif SC         500       Chinese sub-line (20-26px)   +0.04
Italic         Newsreader italic     400       quotes, subtitles            +0.01
Mono S         JetBrains Mono        500       labels / capability counter  +0.18
Mono XS        JetBrains Mono        700       NEW / version chip (11-14px) +0.22
Caret          (block 3px wide)      —         typing cursor               —
```

**Font loading strategy**:
- Google Fonts preconnect `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
- A single `<link>` request merges all weights, reducing round-trips
- Before recording the MP4, `document.fonts.ready` must complete before timing starts (Stage already implements this)

## 2.3 Grid system

**Main canvas**: 1920 × 1080

**Outer margin (safe zone)**: 80px top, bottom, left and right

**Main content area**: 1760 × 920

**12-column grid**: column-width = 132px, gutter = 16px

**Baseline grid**: 8px base unit. Every vertical position must be a multiple of 8 (unless there's a specific visual reason).

**Golden-ratio anchors**:
- Upper 1/3 line: y = 360
- Lower 1/3 line: y = 720
- Center line: y = 540 (default anchor for hero md)
- Golden ratio upper: y = 412
- Golden ratio lower: y = 668

**Key safe zones**:
- Within the top 60px: chrome element zone (capability counter, version chip)
- Within the bottom 60px: watermark / metadata zone
- Central 800×600 area: main content zone (every shot's hero element must land inside this area)

## 2.4 Animation system

**Easing library** (4 curves in total; all others are banned):

```
Name          Curve formula                      Use
──────────────────────────────────────────────────────────────────
expoOut       1 - 2^(-10t)                       default ease (90% of entrances use this)
overshoot     cubic-bezier(0.34, 1.56, 0.64, 1)  NEW tag pop / button reveal
linear        t                                   background fade / paper texture movement
expoIn        2^(10(t-1))                        exit ease (10% of exits use this)
```

**Duration dictionary**:

```
Event type                Duration      Notes
────────────────────────────────────────────────────────
character stagger         30-50ms       typing effect / slogan characters appearing one by one
small element entrance    300ms         file card / pill / chip
medium element entrance   500ms         destination card / capability number
hero element entrance     700-900ms     md character morph
slogan character entrance 800ms         "ONE SOURCE." as a whole
transition between scenes 300ms overlap cross-dissolve + scale
exit                      200-300ms     exits are always faster than entrances
```

**Stagger rules**:
- When multiple elements enter together, adjacent elements are delayed 30-80ms apart (not 0, and never over 100ms)
- 6 pills entering: cumulative stagger 250ms (50ms each)
- slogan characters entering: cumulative stagger 280ms (~30ms each × 10 characters)

**Transitions between scenes**:
- Always **cross-dissolve + soft scale** (never a hard cut)
- Outgoing shot, within its last 300ms: opacity 1 → 0, scale 1 → 0.96
- Incoming shot, within its first 300ms: opacity 0 → 1, scale 1.04 → 1
- The two shots overlap for 300ms (on the timeline, a Sprite's end is 0.3s later than the next shot's start)

## 2.5 Chrome elements (running through the whole film)

These are **small things that stay in the frame throughout**, giving the feeling that "this is one complete film".

**Chrome A · top-left · capability counter (00-22s)**

```
   ┌─────────────┐
   │  ●  CAP·01  │     pulse dot (terracotta) + label
   │  ●●●●○○○○○  │     6-dot progress (filled = current)
   └─────────────┘
```

- Type: JetBrains Mono 12px, letter-spacing 0.24em
- Color: Ink for label, Terracotta for current dot, Mica for upcoming dots
- Animation: on every scene change, the next dot goes from hollow → filled (500ms expoOut)

**Chrome B · top-right · version chip (02-30s)**

```
   ╔═════════════════════════╗
   ║ ● HUASHU-MD-HTML · v2.0 ║
   ╚═════════════════════════╝
```

- Type: JetBrains Mono 13px Bold, letter-spacing 0.22em
- Color: Terracotta dot + Ink label
- Entrance: at 02s, the whole chip fades in over 600ms
- pulse dot: a very faint breath every 4 seconds (opacity 1 → 0.6 → 1, 1500ms ease-in-out)

**Chrome C · bottom-center · timeline ticker (07-22s)**

```
   any→md  ━━━━●━━━━━━━━━━━━  md→html  ─  html→md  ─  md→docx  ─  md→pdf  ─  md→epub
```

- Type: JetBrains Mono 11px, letter-spacing 0.18em
- The current capability uses Terracotta + bold; the others use Smoke
- A horizontal line connects the 6 names, and the progress dot (●) slides from left to right over time
- Entrance: at 07s, the whole strip fades in over 500ms

**Chrome D · bottom-right · watermark (persistent)**

```
   CREATED BY HUASHU-DESIGN
```

- Type: JetBrains Mono 10px, letter-spacing 0.24em
- Color: rgba(26,26,26,0.32)
- Completely static, never moves

**Chrome E · very faint paper texture (persistent)**

- SVG noise + a very slow 0.3% scale breath
- opacity ≤ 0.04
- Almost invisible on the recording, but it gives the frame a sense of "breathing"

## 2.6 Audio system

### BGM arc (30-second segmented curve)

```
Intensity
 │                            ╱╲
1│                          ╱╱  ╲╲
 │                       ╱╱      ╲╲
 │                    ╱╱             ╲
 │                ╱╱                   ╲
 │            ╱╱                          ╲
 │       ╱╱                                  ╲
 │   ╱╱                                          ╲
0└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴
   0  2  4  6  8 10 12 14 16 18 20 22 24 26 28 30s
   │  │     │              │           │  │
   enter│  strings │   rhythm pulse  │ peak │  decay
   piano    in         joins          swell
```

**Layers (each layer runs the full 30 seconds; intensity changes are controlled by the envelope)**:

- **L0 · Room tone** (00-30s): very faint background noise, giving the frame a breath so it's "not dead silent"
- **L1 · Piano single note** (00-08s): a single piano note struck repeatedly, once every 1.2 seconds, slowly building
- **L2 · Piano arpeggio** (03-22s): piano arpeggios enter, giving a feeling of "picking up the rhythm"
- **L3 · Cello drone** (08-22s): low strings as a bed, giving "weight"
- **L4 · Pulse** (15-22s): a very faint sub-kick in 4/4 (not a dance beat; a cinematic pulse)
- **L5 · String swell** (22-26s): the full string section swells up to the climax
- **L6 · Decay + reverb tail** (26-30s): all layers decay, leaving piano + reverb

**Style target**: Max Richter's *On the Nature of Daylight* + Ólafur Arnalds' *Re:member* + Jóhann Jóhannsson's *Orphée*

### SFX dictionary

```
Cue                          Time        Type               Volume
────────────────────────────────────────────────────────────────────
keyboard click               00.5-02.0   keypress × 12     -18dB (30ms each)
cursor blink                 02.0-02.8   subtle tick        -28dB
md morph swell               02.8-03.2   soft whoosh + bloom -16dB
file card whoosh × 6         05.5-08.0   short whoosh       -20dB (200ms each)
absorb / ink drop             08.0-08.4   "absorb" splash    -16dB
paper rustle                 08.5-09.0   paper turn         -22dB
chime: capability 02 →        09.0       single chime tone  -18dB
chime: capability 03 →        12.0       single chime tone  -18dB
chime: capability 04 →        15.0       single chime tone  -18dB
chime: NEW (05)               18.0       double chime + glow -14dB
chime: NEW (06)               21.0       double chime + glow -14dB
build sweep                  22.0-22.6   ascending sweep    -10dB
impact (slogan ONE)          22.6        deep impact         -8dB
impact (slogan SIX)          23.4        deep impact         -8dB
pen flourish                 24.0-24.4   pen on paper        -22dB
final stamp / sign-off       29.0-29.5   ink stamp           -14dB
```

**SFX frequency band isolation** (so they don't fight each other):
- BGM takes the low frequencies (40Hz-2kHz)
- SFX whooshes / chimes take the mid-high frequencies (2kHz-8kHz)
- SFX impacts take the low sub frequencies (40Hz-120Hz), overlapping the BGM cello, but the BGM ducks -3dB at the same time

## 2.7 Anti-AI-slop checklist (per shot)

Every shot must pass this checklist before it's executed:

```
□  No purple (at any saturation)
□  No rounded card + left border accent combination (except the honest mica border on the destination card)
□  No emoji as icons
□  No SVG-drawn figures / abstract human forms
□  No colors outside the Part II.1 palette
□  No Inter / Roboto / Arial as display
□  Tracking, line height and font size all come from the Part II.2 type system (no values added "by feel")
□  vertical position is a multiple of 8 (except for deliberate visual reasons)
□  Terracotta takes up < 10% of the frame in this shot
□  This shot has at least one detail "worth a screenshot when paused" (the 120% signature)
□  The transition from the previous shot to this one is cross-dissolve + scale, not a hard cut
□  At the end of this shot, it visually "makes way" for the next shot (not "filling the whole frame right to the end")
```

---

# Part III · Story Arc

## 3.1 Three-act structure

**ACT I · SET-UP (00.0 — 06.0s)**

The viewer enters the frame. A question is posed: what is the source of truth?

- SHOT 01 (0.0-1.5s) · BLANK PAGE
- SHOT 02 (1.5-3.0s) · THE CURSOR
- SHOT 03 (3.0-5.0s) · THE TRANSFORMATION
- SHOT 04 (5.0-6.0s) · entering gathering (overlaps with ACT II)

**ACT II · ESCALATION (06.0 — 22.0s)**

The answer unfolds: md is the source. It radiates 6 product chains outward.

- SHOT 04 (5.0-8.5s) · GATHERING (any → md)
- SHOT 05 (8.5-11.5s) · FIRST FLOWER (md → html)
- SHOT 06 (11.5-14.5s) · REVERSE FLOW (html → md)
- SHOT 07 (14.5-17.5s) · PUBLISHER GRADE (md → docx)
- SHOT 08 (17.5-20.5s) · ★ NEW · PRINT (md → pdf)
- SHOT 09 (20.5-22.5s) · ★ NEW · EBOOK (md → epub, overlaps ACT III by 0.5s)

**ACT III · PAYOFF (22.5 — 30.0s)**

The theme is elevated. The slogan appears. The brand stamp.

- SHOT 10 (22.5-24.0s) · THE CONVERGENCE
- SHOT 11 (24.0-26.5s) · ONE SOURCE.
- SHOT 12 (26.5-29.0s) · SIX FORMS.
- SHOT 13 (29.0-30.0s) · SIGN-OFF

## 3.2 Emotion curve

```
Emotional intensity
 │                                       ╔═══╗
 │                                    ╔══╝   ╚══╗
 │                              ╔═════╝         ╚══╗
 │                          ╔═══╝                   ╚══╗
 │                       ╔══╝                          ╚══╗
 │                   ╔═══╝                                 ╚════════╗
 │             ╔═════╝                                              ╚══╗
 │       ╔═════╝                                                       ╚══
 │  ╔════╝
 │══╝
 0──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──>
    0     2     4     6     8    10    12    14    16    18    20    22    24    26    28    30s
    │     │     │            │           │            │            │     │     │
    blank cursor morph      gather       cap 02-04   cap 05/06 ★  slogan slogan sign-off
                                                                  ONE   SIX
                                                                  ──────►
                                                                  PEAK 24.5s
```

**Key emotional beats**:
- **02.0s**: the first keyboard click → the viewer enters
- **03.0s**: the md characters are born → the first "awe"
- **08.0s**: 6 file cards gather into md → the first "oh, so md is the source" click
- **18.0s**: the first NEW tag appears → existing users go "oh"
- **22.5s**: all chrome gathers in, getting ready for Act III → tension build-up peak
- **24.5s**: SIX FORMS. lands → emotional climax
- **30.0s**: the md stamp quietly lingers → resolution

---

# Part IV · Shot-by-Shot Storyboard

Format of each shot:

```
SHOT NN · NAME
[TIMECODE]  |  FUNCTION
[VISUAL]     frame composition
[TYPE]       precise typesetting spec
[ANIM]       in/out/easing/delay for every element
[AUDIO]      music beat + SFX cue
[CHROME]     state of the corner elements
[ANTI-SLOP]  self-check items passed
[WHY]        what it picks up + how it moves things forward
```

---

## SHOT 01 · "BLANK PAGE"

**[TIMECODE]** 00.00-01.50s (1.5s) `|` **FUNCTION** Opening. Draws the viewer in. Gives "emptiness" some time.

**[VISUAL]**

The whole 1920×1080 is Ivory paper #FAFAF6. **There is nothing in the frame**.

The only presence: a very faint layer of paper texture (SVG noise + a very slow 0.3% scale breath), almost invisible, but it gives the frame the subconscious sense that "this is a real sheet of paper".

Composition: completely empty. This is "white" in Kenya Hara's sense: not "not drawn yet" but "the content itself".

**[TYPE]** No text.

**[ANIM]**

- 0.00s · paper texture opacity from 0 → 0.04 (500ms linear)
- 0.50-1.50s · the whole frame holds, no motion. Let the viewer's eyes adjust to this white.
- 1.40-1.50s · left of center in the frame (x=860, y=540), a cursor position begins to emerge (transparent; it only becomes visible in the next shot)

**[AUDIO]**

- BGM: room tone enters (300ms fade-in to -38dB)
- SFX: none

**[CHROME]** All hidden. Chrome A/B/C/D/E are not visible yet.

**[ANTI-SLOP]**

- ✅ No logo, no "Loading...", no up-front branding of any kind
- ✅ No gradients, no effects
- ✅ This shot's "pause-and-look" signature: the frame has texture (paper texture) but never steals the show

**[WHY]**

Apple's "Designed by Apple in California" opens this way too: it gives the blank some time. It tells viewers "this film needs you to slow down". If the opening piles on logo and chrome, the viewer's attention scatters and you can't win it back for the next 30 seconds.

These 1.5 seconds are among the most important 1.5 seconds of this film.

---

## SHOT 02 · "THE CURSOR"

**[TIMECODE]** 01.50-03.00s (1.5s) `|` **FUNCTION** The typewriter is born. The first content.

**[VISUAL]**

Left of center in the frame (x=860, y=540), a vertical black block (3px × 56px, Ink #1A1A1A) starts blinking. This is the cursor.

After blinking twice (0.7s cycle × 2), `# markdown.md` starts appearing character by character after the cursor, in JetBrains Mono 56px, color Ink #1A1A1A, letter-spacing -0.01em.

Each character typed plays one keyboard click. After the last character is typed (13 characters in total), the cursor blinks 1 more time after `.md`.

**[TYPE]**

- Text: `# markdown.md`
- Font: JetBrains Mono 500 weight
- Size: 56px
- Color: Ink #1A1A1A
- Letter-spacing: -0.01em
- Position: horizontal center, y = 540 (baseline; the text's vertical center sits slightly below this)

**[ANIM]**

- 01.50s · cursor block opacity 0 → 1 (200ms)
- 01.50-01.85s · first cursor blink (off 200ms / on 200ms)
- 01.85-02.20s · second cursor blink
- 02.20-02.85s · 13 characters appear staggered, 50ms apart (650ms in total), each with its own fade + 1px slide-down (180ms expoOut)
- 02.85-03.00s · the cursor blinks once more at the end (the last time, marking that input is complete)

**[AUDIO]**

- BGM: first piano note struck at 01.50s (-22dB)
- SFX: keyboard click × 13 (one per character, -18dB, 30ms each)
- SFX: 200ms of silence after the last cursor blink (making way for the next shot's morph)

**[CHROME]** Still hidden.

**[ANTI-SLOP]**

- ✅ The cursor isn't a sci-fi blink (not an ultra-fast 0.1s blink); it's a faithful simulation of the macOS terminal cursor rhythm
- ✅ The typing isn't "all characters appearing at once"; it's real, rhythmic typing
- ✅ The font is JetBrains Mono, not a system default mono like Courier or Menlo
- ✅ pause-and-look signature: the cursor's 3px width (not 2px or 4px), a very precise detail that people in the know will notice as "designed from a real terminal"

**[WHY]**

This shot is the core of the setup: **markdown is not a noun; it's an action**. It is the very act of "striking keys to turn characters into structure".

The cursor is the smallest unit of writing. Starting from a cursor is the birth of "source code".

The next shot's morph builds on the premise that the viewer has already accepted "we're writing markdown".

---

## SHOT 03 · "THE TRANSFORMATION"

**[TIMECODE]** 03.00-05.00s (2.0s) `|` **FUNCTION** Reveal the hero. `# markdown.md` morphs into the hero `md.`

**[VISUAL]**

At 03.00s: `# markdown.md` (56px mono) starts gathering toward the center, scaling up, and transforming.

**The morph process** (detailed breakdown):

- 03.00-03.30s (300ms): the `#` and `arkdown` parts of `# markdown.md` fade out (opacity 1 → 0), while the `m` and the `md` of `d.md` remain.
- 03.30-04.10s (800ms): the remaining `md` morphs from the mono font to Newsreader serif, scales from 56px up to 480px, goes from Ink to Ink (no color change), and keeps its position (still at the center of the frame).
- 04.10-04.80s (700ms): at the bottom right of the `md` characters, a Terracotta period `.` emerges (fade-in + scale 0.6 → 1 + overshoot easing).
- 04.80-05.00s (200ms): the period settles for good and the hero is complete. 30px below, a 320px-wide fine terracotta line appears (terracotta accent rule, 2px thick), extending from the center toward both ends.

**End frame**: `md.` (Newsreader 600 weight, 480px, Ink with Terracotta dot) + a fine terracotta line below. Everything else in the frame is empty.

**[TYPE]**

- Text: `md.` (`md` Ink, `.` Terracotta)
- Font: Newsreader 600 weight
- Size: 480px (display L)
- Letter-spacing: -0.04em
- Color: `m`+`d` Ink #1A1A1A, `.` Terracotta #C2410C
- Centered horizontally and vertically on the hero center line (y = 540)
- accent rule 30px below, width 320px (grows from 0)

**[ANIM]**

- 03.00-03.30s · `#` `arkdown` `md` (middle part) fade out (opacity 1 → 0, expoOut)
- 03.30-04.10s · `md` morph: fontFamily switch, fontSize from 56 → 480, weight from 500 → 600 (800ms expoOut; note that the morph is not an abrupt switch but ghost afterimage overlay + scale up + opacity switch)
- 04.10-04.80s · `.` enters (700ms overshoot, scale 0.6 → 1)
- 04.80-05.00s · accent rule width 0 → 320px (300ms expoOut)

**[AUDIO]**

- BGM: second piano note at 03.00s (-20dB), third note at 04.20s (-18dB), the piano building up
- SFX: 03.00-03.20s soft whoosh (as the morph starts, -16dB)
- SFX: 04.10s subtle bloom (the instant the period appears, -20dB)
- SFX: 04.80s short paper rustle (accent rule extending, -22dB)

**[CHROME]**

- 04.50s · Chrome B (version chip top-right) starts emerging (fade-in 600ms)
  - Form: `● HUASHU-MD-HTML · v2.0`
  - terracotta dot, mono text, Ink color
  - Entry position: top: 78px, right: 80px
- Still hidden: Chrome A, C, E (visible only ≥ 06s)

**[ANTI-SLOP]**

- ✅ The morph is not a cheap "fade out + fade in" transition; it's real character transformation (including ghost afterimage overlay)
- ✅ The period is the hero's "signature detail" (the one done to 120%): the Terracotta period is as small as a fingernail but it's the visual anchor of this film; **in every later shot, this period is kept as the hero's mark**
- ✅ The accent rule isn't decoration; it's the hero's base line. It appears again at the slogan in Shot 11, creating a bookend between the beginning and the end
- ✅ pause-and-look signature: the -0.04em tracking on the 480px Newsreader 'md' puts m and d almost touching but not quite, which is the signature quality of the Newsreader typeface at large sizes

**[WHY]**

This is the hero shot. The "lead" of the whole film for the next 25 seconds (`md.`) is born here.

The design philosophy of the morph: **going from mono to serif is a metaphor for going from "I'm typing" to "I'm writing"**. Mono is the typewriter; serif is publishing. md is both at once: it's typed on a keyboard, but it's the source code of publishing.

The next shot enters ACT II, and the hero has found its footing. It will be pushed to the top of the frame to make room for the "materialized products".

---

## SHOT 04 · "GATHERING" (any → md)

**[TIMECODE]** 05.00-08.50s (3.5s) `|` **FUNCTION** CAPABILITY 01 revealed. Everything → md. Establishes the worldview that "md is the source".

**[VISUAL]**

05.00s: the hero `md.` slides up from the center of the frame (y=540) to y=280 (the 1/4-height position) while shrinking to 220px.

Then 6 file cards appear in the lower half of the frame (the y=520 ~ y=900 area), flying in one by one from outside the frame (below, y=1140) and gathering toward the md hero along an invisible parabolic trajectory.

Design of the 6 cards (**each one is a mini demo of a real file type, not fake bar lines**):

```
.pdf   │ two-column layout + header "doc.pdf" + page number "— 12 —" + a few lines of genuinely typeset small text
.docx  │ heading "On Markdown" + italic subtitle + 6 lines of paragraph ascii
.pptx  │ title "MD AS SOURCE" + a simplified bar chart placeholder
.xlsx  │ a 6×4 spreadsheet grid + some numbers
.epub  │ an Apple Books-style page + chapter title "Chapter 01"
.html  │ a browser chrome (three dots + URL bar "example.com") + title + paragraph
```

Each card is 130×180px, white background + Mica border + a 24° top-right corner fold.

**Flight trajectory**: starts from y=1140 below and converges along a parabola toward the "." of the md hero (about x=960+50, y=280+90). Midway (when in the middle of the frame), the 6 cards form a fan, with 220px between each adjacent pair. Finally all 6 are "absorbed" by md (scale 1 → 0.5 + opacity 1 → 0, while their positions converge to one point).

Absorption timing: starting at 05.60s, one card launches every 0.18s. Each card flies for 1.1s and is then absorbed. The last card finishes absorbing at about 07.60s.

After absorption completes (07.60-08.20s), a tagline appears 60px below: "万物 → md" ("everything → md"; Chinese serif, 36px, Ink, italic)

08.20-08.50s · the whole frame holds, getting ready for Shot 05.

**[TYPE]**

- hero `md.`: shrinks to 220px (same type spec as SHOT 03)
- Typesetting inside the 6 cards: JetBrains Mono 12-14px for labels, Newsreader 12-16px for content
- tagline "万物 → md": Noto Serif SC 36px italic + the → in the middle is Newsreader italic + Terracotta
- Top Chrome A text: JetBrains Mono 12px

**[ANIM]**

- 05.00-05.30s · hero md scales + moves up (300ms expoOut)
- 05.30s · Chrome A capability counter enters (shows CAPABILITY · 01, the first dot filled)
- 05.60-07.60s · 6 cards launch one after another (each card's launch delay = 5.60 + i × 0.18s, flight 1.1s, absorb at launch+1.1)
- 07.60-08.20s · the tagline "万物 → md" enters (fade-in 400ms + slight y slide 12px → 0)
- 08.20-08.50s · hold

**[AUDIO]**

- BGM: piano arpeggio L2 enters at 05.00s (-26dB → -20dB fade-in)
- SFX: file card whoosh × 6 (once per card launch, 200ms each, -20dB)
- SFX: absorb / ink drop (when the last card is absorbed, -16dB)
- SFX: paper rustle (when the tagline enters, -22dB)

**[CHROME]**

- A (top-left capability counter): ON, shows `CAPABILITY · 01`, first dot filled
- B (version chip): ON, shown continuously
- C (timeline ticker): OFF (enters in SHOT 05)
- D (watermark): ON, always ON
- E (paper texture): ON

**[ANTI-SLOP]**

- ✅ The 6 cards are neither emoji nor icons; they're **mini demos with real internal content**, and each one is readable
- ✅ The flight trajectory is a parabola (a sense of gravity), not a straight line (a computer feel)
- ✅ Gathering is "absorption" (scale + position converge together), not "stacking"
- ✅ No glow or particle effects on the md characters (no need to explain "md is absorbing"; viewers can see it for themselves)
- ✅ pause-and-look signature: pause on any card mid-flight and you can read "this is a PDF / this is a DOCX". That's the detail done to 120%
- ✅ The tagline uses "→" rather than "to" or "至" (Chinese for "to"); it's a character native to markdown

**[WHY]**

This is the opening shot of ACT II. If viewers don't realize "oh, md is the source" after these 3.5 seconds, every later shot is wasted.

There are 3 micro-narrative beats in the 3.5 seconds:
1. The hero makes way (md moves up), implying "I'm making way for my products"
2. The 6 products appear, revealing "the things I can take in"
3. They all return to md: "but in the end they're all md"

The next shot enters the forward flow of md → html. Viewers have already accepted "md is the source" and are now ready to see "how md transforms".

---

## SHOT 05 · "FIRST FLOWER · HTML" (md → html)

**[TIMECODE]** 08.50-11.50s (3.0s) `|` **FUNCTION** CAPABILITY 02. The first forward output. Establishes the ScenePipeline pattern (the next 5 shots share this structure).

**[VISUAL]**

08.50s: the hero `md.` slides from its upper-center position to the left side of the frame (x=480, y=540), keeping its 220px size.

At the same time, a destination card appears on the right side of the frame (x=1400, y=540): a simulated "Tufte CSS-style essay html".

Destination card design (**real readable content, not bar lines**):

```
┌─────────────────────────────────┐
│                                  │
│  On Markdown                     │  ← Newsreader 600, 32px, Ink
│  AN ESSAY · 2026                 │  ← Mono 11px, 0.18em, Smoke
│  ▬▬▬                             │  ← Terracotta rule 60×3px
│                                  │
│  md is the source of truth.      │  ← Newsreader 400, 18px, line-height 1.7
│  Anything else is product.       │
│  We write once. Publish six      │
│  ways. The river forks; the      │
│  spring stays the same.          │
│                                  │
│  ─ huashu, 2026.05.11            │  ← italic 14px, Smoke
│                                  │
│  article.html · TUFTE THEME      │  ← Mono 10px, 0.18em, Smoke (bottom)
└─────────────────────────────────┘
   width 480px × height 560px
   white background + Mica border + 24° corner fold
```

The md characters and the destination card are connected by a fine terracotta line, starting from md's dot and growing 380px to the right, with the arrow head reaching the card's left edge. 30px above the line, the label "md → html" is shown (JetBrains Mono 14px Terracotta, letter-spacing 0.14em).

At 09.80s: Chrome C (timeline ticker) enters for the first time, fixed at y=1000.

**[TYPE]**

- See the inline visual description
- label "md → html" size 14px, Mono Bold, Terracotta, letter-spacing 0.14em
- The chapter title at the top of the destination card is Newsreader 600, 32px, Ink
- Small imprint at the bottom of the destination card: mono 10px Smoke 0.18em

**[ANIM]**

- 08.50-08.80s · hero md slides from center-top to left-mid (300ms expoOut)
- 08.80-09.10s · the arrow line grows to the right from the md.dot starting point (300ms expoOut, 0 → 380px)
- 09.10s · arrow head emerges (200ms overshoot)
- 09.20-09.40s · label "md → html" enters (fade-in + 8px y slide-down, 300ms expoOut)
- 09.40-10.10s · the destination card enters as a whole (700ms expoOut, scale 0.85 → 1 + opacity 0 → 1)
- 10.10-10.80s · staggered entrance inside the destination card: title (400ms delay 0) → subtitle metadata (delay 200ms) → terracotta rule (delay 400ms) → 6 lines of body text (each delay 60ms cascade) → signature (delay 1000ms) → bottom mono (delay 1100ms)
- 10.80-11.50s · hold + micro breathing (whole card scale 1 → 1.005 → 1, 600ms ease-in-out infinite, but this shot only plays half a cycle)

**[AUDIO]**

- BGM: cello drone L3 enters at 09.00s (-30dB → -24dB)
- SFX: chime: capability 02 at 09.00s (-18dB)
- SFX: paper rustle (as the card enters, -22dB)
- SFX: micro ticks (as each line of text enters staggered, -26dB each)

**[CHROME]**

- A: advances to `CAPABILITY · 02`, second dot filled
- B: ON
- **C: first entrance** at 09.80s, `any→md  ━━━━●━━━━━  md→html  ─  html→md  ─  md→docx  ─  md→pdf  ─  md→epub`, progress dot ● above the second slot
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ The "On Markdown" essay content on the destination card is a genuinely readable short piece of English philosophy, not Lorem ipsum
- ✅ The small imprint "article.html · TUFTE THEME" is the "detail signature you can read when paused"
- ✅ No glow or particles are used to "emphasize" the md → html conversion; typography and composition tell it clearly on their own
- ✅ The arrow line isn't dashed or dotted (to avoid a "web tutorial" feel); it's a 1.5px solid Terracotta line
- ✅ pause-and-look signature: the "AN ESSAY · 2026" subtitle at the top of the destination card uses Newsreader's small caps OpenType feature with 0.18em tracking. That's this shot's 120% detail

**[WHY]**

This is where the ScenePipeline pattern is first established. The next 5 capability shots all advance with this structure:
1. md on the left, destination on the right
2. arrow + label in the middle
3. staggered entrance inside the destination card (every card has 6-8 text levels)
4. the card content is real and readable, not fake bar lines

By the second time (SHOT 06) viewers will understand the pattern, and by the sixth time (SHOT 09) they'll get the feeling of "ah, here it comes again, but this time it's NEW". That's exactly the rhythm design of ACT II.

---

## SHOT 06 · "REVERSE FLOW · MD" (html → md)

**[TIMECODE]** 11.50-14.50s (3.0s) `|` **FUNCTION** CAPABILITY 03. Reverse archiving: html → md. Establishes the "two-way flow" concept.

**[VISUAL]**

Enters with a cross-dissolve. The previous shot's destination card shrinks and exits to the bottom right within 11.50-11.80s, and a new destination card (this time showing markdown source code) enters from the right.

New destination card design: **a dark-background markdown source view** (a visual contrast with SHOT 05's light-background html).

```
┌─────────────────────────────────┐
│                                  │  ← background Charred #2A2620
│  # On Markdown                   │  ← Terracotta, mono 14px
│                                  │
│  An essay · 2026                 │  ← Smoke, mono 14px
│                                  │
│  > md is the source.             │  ← italic Smoke, mono 14px
│  > Anything else is **product**. │     `**product**` highlighted mica + bold
│                                  │
│  - 1 source                      │  ← mono 14px Smoke
│  - 6 forms                       │
│  - ∞ outputs                     │
│                                  │
│  essay.md · CLEAN MARKDOWN       │  ← bottom Mono 10px Smoke
└─────────────────────────────────┘
   480×560px, Charred background, the 24° top corner fold is Cinder
```

The arrow direction is reversed: from the destination card on the right toward the md characters on the left (a short Terracotta line + arrow head pointing left). The label changes to "html → md".

**Key differences** (forming a visual rhyme with SHOT 05):
- destination on the right, md on the left (same as SHOT 05)
- but the arrow direction is reversed (visual: we're archiving / pulling it back)
- the card has a dark background (visual contrast, emphasizing that this is the source)

**[TYPE]**

- Everything inside the card is JetBrains Mono 14px
- Colors for markdown syntax elements: `#` heading Terracotta, `>` quote italic Smoke, `**bold**` Mica + bold, list dash Smoke
- bottom mono 10px Smoke

**[ANIM]**

- 11.50-11.80s · the previous shot's card exits (shrinks → bottom right, fade out) + md characters stay
- 11.80-12.10s · the arrow line grows in reverse (this time from right to left, 300ms expoOut)
- 12.10s · arrow head (pointing left) emerges
- 12.20-12.40s · label "html → md" enters
- 12.40-13.10s · the new destination card enters (same entrance logic as SHOT 05)
- 13.10-13.80s · the 6 lines inside the markdown enter staggered (100ms delay per line)
  - Special micro-detail: as each line enters it simulates a typewriter, with a character-by-character cascade reveal of the line (so viewers feel "this is markdown being 'written out'")
- 13.80-14.50s · hold

**[AUDIO]**

- BGM: L1+L2+L3 layers continue
- SFX: chime: capability 03 at 12.00s (-18dB)
- SFX: paper rustle (12.40s)
- SFX: a very faint keyboard click ticker as each line enters (-26dB each, 100ms apart)

**[CHROME]**

- A: advances to `CAPABILITY · 03`, third dot filled
- B: ON
- C: progress dot ● slides to the "html→md" position
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ This is the only "dark background" shot in the whole film, a deliberate visual contrast that tells viewers "this is source code", not "yet another destination"
- ✅ The syntax highlighting inside the markdown doesn't use a cyber palette (not the VS Code Dark+ kind); it uses a publishing-house palette (Terracotta + Smoke + Mica)
- ✅ The small imprint "essay.md · CLEAN MARKDOWN" at the bottom → pause-and-look signature
- ✅ The reverse arrow isn't a "U-turn curve"; it's a straight line + reversed arrow, keeping the structure consistent

**[WHY]**

The real job of this shot isn't to "show off capability 03"; it's to **tell viewers this pipeline runs both ways**.

If all 6 capabilities in the film radiated outward from md, viewers would think "md only goes out". The 3rd capability reverses the flow and establishes the worldview that "md is the hub of everything".

That's why I chose the capability order 02 (md→html) → 03 (html→md) → 04 (md→docx): the reverse capability is deliberately wedged into 3rd place to maximize the cognitive surprise of the "two-way flow".

---

## SHOT 07 · "PUBLISHER GRADE · DOCX" (md → docx)

**[TIMECODE]** 14.50-17.50s (3.0s) `|` **FUNCTION** CAPABILITY 04. Publishing-house-grade docx. Establishes the argument that "md isn't just for programmers".

**[VISUAL]**

Back to the light background, back to "md on the left, destination on the right".

Destination card design: **a publishing-house-grade docx chapter opening page** (dense information, but completely restrained).

```
┌─────────────────────────────────┐
│                       ON MARKDOWN│  ← page header, right-aligned, Smoke italic mono 9px
│  CHAPTER · 01                    │  ← Terracotta mono 11px bold 0.22em
│                                  │
│  On Markdown                     │  ← Newsreader 700, 36px, Ink, lh 1.1
│  A short essay on source-of-truth│  ← Newsreader italic 14px, Smoke
│  thinking                        │
│                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━     │  ← Terracotta full-width rule 3px
│                                  │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬       │  ← 10 lines of mica bar paragraphs
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬           │     (varied widths 76-95%)
│  ...                             │
│                                  │
│                — 1 —             │  ← page number, centered, mono 10px Smoke
└─────────────────────────────────┘
   480×580px, white card, Mica border, 24° corner fold
```

**Special details**:
- The "page header" in the top-right corner (book title in italic gray mono) is the detail signature of a real publishing-house docx
- The "CHAPTER · 01" prefix makes viewers realize at a glance "this is a page from a book, not an article"
- The terracotta full-width rule (not a fine line but a thick 3px rule) is the hallmark of a publishing-house chapter opening page
- The dashes around the bottom page number "— 1 —" are Newsreader's em-dash, not a hyphen

**[TYPE]**

- page header: Newsreader italic 9px, Smoke, letter-spacing 0.14em
- CHAPTER · 01: JetBrains Mono Bold 11px, Terracotta, letter-spacing 0.22em
- main title: Newsreader 700, 36px, Ink, line-height 1.05
- subtitle: Newsreader italic 14px, Smoke
- terracotta rule: 3px thick, full card width
- bar paragraphs: Mica color #E6E1D6, height 6px
- page number: JetBrains Mono 10px, Smoke, letter-spacing 0.18em

**[ANIM]**

- 14.50-14.80s · the previous shot's card exits + md stays
- 14.80-15.10s · the arrow line grows forward
- 15.10s · arrow head and label "md → docx" enter
- 15.30-16.10s · the destination card enters as a whole
- 16.10-17.00s · internal stagger: page header (delay 0) → CHAPTER tag (delay 100ms) → title (delay 300ms) → subtitle (delay 500ms) → rule (delay 700ms) → 10-line paragraph cascade (delay 850ms + 60ms cascade) → page number (delay 1600ms)
- 17.00-17.50s · hold

**[AUDIO]**

- BGM: continues; at 15.00s the whole BGM swells +2dB (hinting that we're pushing toward the climax)
- SFX: chime: capability 04 at 15.00s (-18dB)
- SFX: paper rustle (15.30s)

**[CHROME]**

- A: `CAPABILITY · 04`, fourth dot filled
- B/C/D/E: ON

**[ANTI-SLOP]**

- ✅ No explanatory text like "this is a mockup of a book's inner page" (let the typesetting speak for itself)
- ✅ The bar paragraphs use a very pale gray like Mica (#E6E1D6), not black, giving an honest signal that "this is a typesetting style preview, not real content"
- ✅ pause-and-look signature: the right-aligned italic mono page header at the top. 99% of viewers won't look at it; the 1% who are designers will know "this team did its homework"
- ✅ This shot is the most color-saturated of the 6 capabilities (Terracotta takes the page rule + chapter label + top-right chrome counter), landing right in the middle of the story arc, in line with the "build-up toward the climax" curve

**[WHY]**

CAPABILITY 04 is the key shot that links what came before to what comes next:
- It confirms that "md isn't only for the web"; it can produce publishing-house-grade docx
- It establishes the visual context of "print", preparing for SHOT 08 (pdf) and SHOT 09 (epub)

After this shot, viewers are ready for the "md → print" chain. The NEW tags in the next two shots then have something to build on.

---

## SHOT 08 · "★ NEW · PRINT" (md → pdf)

**[TIMECODE]** 17.50-20.50s (3.0s) `|` **FUNCTION** CAPABILITY 05. **NEW**. md → publication-grade PDF. The "upgrade" mark lights up for the first time.

**[VISUAL]**

Enters with a cross-dissolve. The visual intensity of this shot is **noticeably higher** than SHOT 05-07, because this is "something new" and it needs to be remembered.

Visual differences:
1. **NEW tag**: a Terracotta rectangular frame lights up top-left next to the capability counter, containing the characters "★ NEW" (JetBrains Mono Bold 13px, Terracotta, letter-spacing 0.22em, 4px Terracotta border, 6px×12px padding)
2. **The destination isn't a single card but two PDFs fanned out**: A4 at the back (slight +5° rotation) and large 32-kai (大32开, 176×240mm, a common Chinese print-book format) at the front (slight -3° rotation), conveying visually that "both page sizes are supported"
3. **Each PDF has "printer's crop marks"**: a small L-shaped line in each corner, 2px thick, Smoke color. This is a detail of real print-shop PDFs
4. The arrow + label colors are all Terracotta (not Ink), so the overall palette is warmer

**Contents of the two PDFs**:

PDF A (A4, at the back):

```
┌──────────────────────────┐
│ ┌                      ┐ │  ← crop marks
│  A4 · 210×297mm           │  ← Mono Bold 10px Terracotta
│  ─── (Terracotta rule)    │
│  On Markdown              │  ← Newsreader 22px
│  ──────────────────       │
│  ▬▬▬▬▬▬▬▬▬▬▬             │  ← 7 lines mica bars
│  ▬▬▬▬▬▬▬▬▬▬▬▬            │
│  ...                      │
│                           │
│ └                      ┘ │  ← crop marks
└──────────────────────────┘
   360×460px, white card, +5° rotation
```

PDF B (large 32-kai, at the front):

```
┌────────────────────┐
│ ┌                ┐ │  ← crop marks
│  大32开 · 176×240mm│  ← Mono Bold 10px Terracotta
│  ───                │
│  On Markdown        │  ← Newsreader 19px
│  ──────────         │
│  ▬▬▬▬▬▬▬▬▬▬        │  ← 6 lines mica bars
│  ...                │
│ └                ┘ │
└────────────────────┘
   290×410px, white card, -3° rotation
```

**[TYPE]**

- NEW tag: Mono Bold 13px Terracotta, 0.22em letter-spacing, 1.5px Terracotta border
- arrow label "md → pdf": Mono Bold 14px Terracotta, 0.14em
- PDF spec labels (A4 · 210×297mm etc.): Mono Bold 10px Terracotta, 0.2em
- chapter titles inside PDFs: Newsreader 600 weight, 19-22px, Ink

**[ANIM]**

- 17.50-17.80s · the previous shot's card exits + md stays
- 17.70s · **NEW tag lights up** (special treatment: scale 0.8 → 1.1 → 1.0 over 400ms with overshoot easing; at the same time a very faint terracotta glow pulses briefly and then disappears)
- 17.80-18.10s · arrow + label enter (this time with the Terracotta accent, emphasizing "this is NEW")
- 18.20-18.60s · PDF B (the front one) enters (400ms expoOut, scale 0.85 → 1 + clockwise -8° → -3°)
- 18.50-18.90s · PDF A (the back one) follows right after (400ms expoOut, scale 0.85 → 1 + clockwise 0° → +5°, stagger delay 300ms)
- 18.90-19.70s · cascade staggered entrance inside both PDFs
- 19.70s · the 4 crop marks (on PDF B) appear one by one (80ms cascade, the detail signature of "print-shop craft")
- 19.70-20.50s · hold

**[AUDIO]**

- BGM: percussion pulse L4 joins at 18.00s (-32dB) (a very faint sub-kick 4/4 rhythm gets established)
- **SFX: chime: NEW (05) at 17.70s (double chime + soft glow + reverb tail, -14dB)** ← this is one of the most important SFX cues in the whole film
- SFX: paper rustle × 2 (as each PDF enters, -22dB each)
- SFX: subtle "ink stamp" at 19.70s (as the crop marks appear, -22dB)

**[CHROME]**

- A: `CAPABILITY · 05`, fifth dot filled
- A NEW tag is added next to A
- B: ON; at this point the orange dot next to the version chip pulses in sync (emphasizing "new in v2.0")
- C: progress dot ● slides to the "md→pdf" position, and the text at this position gets 0.5px larger for emphasis
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ The NEW tag is neither an emoji nor a sticker; it's a typographic mark (mono + 0.22em + ★ + border)
- ✅ The two PDFs aren't cheaply "stacked on top of each other"; they're fanned + rotated (implying the physical act of "opening it up to look")
- ✅ The crop marks are a visual expression of real print-shop terminology; when paused you can see "ah, this is print-ready"
- ✅ No glow or particles are used to emphasize "NEW"; typography and SFX speak for themselves
- ✅ pause-and-look signature: the mixed Chinese-English "大32开 · 176×240mm" at the top of PDF B is the Huashu ecosystem's respect for Chinese print book formats

**[WHY]**

This is one of the climactic shots of ACT II. Two things must happen at the same time:
1. Viewers must immediately realize "this is a new feature"
2. Visual details must show that "this isn't a filler wkhtmltopdf wrapper; it's genuinely publication-grade"

NEW tag + crop marks + two fanned PDFs + complete A4 / large 32-kai spec labels: four things working together to achieve the two above.

The epub in the next shot is the second of the two NEW shots, and its rhythm and emotional intensity need to go up another notch from this one.

---

## SHOT 09 · "★ NEW · EBOOK" (md → epub)

**[TIMECODE]** 20.50-22.50s (2.0s) `|` **FUNCTION** CAPABILITY 06. **NEW**. md → standard EPUB3. The second new feature. The last capability.

**[VISUAL]**

Enters with a cross-dissolve. This shot is **shorter than the earlier ones** (only 2.0s instead of 3.0s), because we've already established the "NEW + destination" pattern; the second time around viewers get it instantly, so the rhythm can speed up.

Destination card design: **an Apple Books-style EPUB reader frame** (emphasizing the realism of "this book is already in the reader").

```
   ╔════════════════════════════════════╗
   ║ ● ● ●                              ║  ← window chrome (Apple Books)
   ╠════════════════════════════════════╣
   ║                                    ║
   ║  HUASHU · ORANGE BOOK              ║  ← Mono Bold 10px Terracotta 0.22em
   ║                                    ║
   ║                                    ║
   ║  On                                ║  ← Newsreader 700, 30px, Ivory paper
   ║  Markdown                          ║     (on Charred bg)
   ║                                    ║
   ║  ───                               ║  ← Terracotta rule 40×2px
   ║                                    ║
   ║  an essay · 花叔                   ║  ← italic 14px Smoke on Charred
   ║                                    ║
   ╠════════════════════════════════════╣
   ║ Apple Books · 1 of 24    EPUB 3   ║  ← Mono 10px Smoke 0.14em
   ╚════════════════════════════════════╝
   460×470px, ivory paper outer + Charred inner book cover area
   2px Ink border, 22px border-radius (modern app frame)
```

**Key visual differences**:
- The overall frame has a "macOS app window" feel (three dots + 22px rounded corners)
- In the middle is the cover area of an "open e-book" (Charred background + publishing-house-grade typography)
- At the bottom is the "Apple Books · 1 of 24" reader chrome
- The whole card gives the realistic feeling of "I'm reading this book in Apple Books"

**[TYPE]**

- HUASHU · ORANGE BOOK: Mono Bold 10px, Terracotta, 0.22em
- book title (On Markdown): Newsreader 700, 30px, Ivory (on Charred bg), line-height 1.0
- terracotta rule: 40×2px
- author italic: Noto Serif SC italic 14px, Smoke
- Apple Books chrome: Mono 10px, Smoke, 0.14em

**[ANIM]**

- 20.50-20.80s · the previous shot's PDFs exit + md stays
- 20.70s · the NEW tag **stays lit** (it doesn't pop again this time, since it was already established in SHOT 08; just show "★ NEW")
- 20.80-21.10s · arrow + label "md → epub" enter (Terracotta accent, same as SHOT 08)
- 21.20-21.80s · the EPUB destination card enters as a whole (600ms expoOut, scale 0.88 → 1)
- 21.30-22.00s · internal stagger: window chrome dots (delay 0) → top brand label (delay 200ms) → book title "On" (delay 400ms) → "Markdown" (delay 480ms) → rule (delay 700ms) → author italic (delay 850ms) → bottom chrome (delay 1000ms)
- 22.00-22.50s · hold + prepare the transition to ACT III

**[AUDIO]**

- BGM: percussion continues, but at 22.00s the whole BGM swells +3dB (the convergence build-up for SHOT 10)
- **SFX: chime: NEW (06) at 20.70s (double chime + soft glow, a semitone higher than SHOT 08, -14dB)**: the semitone difference gives the two NEW shots a musical relationship
- SFX: window chrome subtle "click" at 21.20s (the feel of a macOS window appearing, -24dB)
- SFX: page turn rustle at 21.40s

**[CHROME]**

- A: `CAPABILITY · 06`, sixth dot filled (**all filled: 6/6**)
- The NEW tag next to A stays
- B: the version chip's orange dot pulses harder (amplitude × 1.5)
- C: progress dot ● reaches the far-right "md→epub" position
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ No real Kindle or Apple Books logo (to avoid IP risk); macOS window chrome is enough to suggest "reader"
- ✅ No e-ink gray filter (to avoid Kindle slop)
- ✅ The "Apple Books · 1 of 24" chrome has the feel of real publication data (24 chapters, chapter 1)
- ✅ pause-and-look signature: the **line break** in the title "On / Markdown", a line-break design for Newsreader at the large 30px size, paying homage to Penguin Classics cover typesetting

**[WHY]**

This shot wraps up ACT II. Two things must be done:
1. All 6 capabilities have been shown (counter 6/6 filled)
2. The emotion starts building toward the ACT III climax

Cutting the shot length from 3.0 → 2.0s is deliberate: the rhythm is speeding up, and viewers sense "we're about to reach the peak".

---

## SHOT 10 · "THE CONVERGENCE"

**[TIMECODE]** 22.50-24.00s (1.5s) `|` **FUNCTION** The transition from ACT II → ACT III. All elements return to place. Getting ready for the slogan.

**[VISUAL]**

22.50s: all the earlier destination cards have exited. Chrome A/C start fading out (the capability counter has completed 6/6; its mission is accomplished).

At the center of the frame, the md characters slide from their left position (x=480) back to dead center (x=960), while growing from 220px → 300px.

The 6 capability labels around md (any→md / md→html / html→md / md→docx / md→pdf / md→epub) emerge one by one from a distance (circle r=380px), surrounding the md characters in a circle, one every 60°, arranged clockwise (starting from "any→md" at the top). These labels are a mix of Mono Bold 14px Smoke (not active) + Terracotta (actually new).

Overall effect: **the md characters are the sun, and the 6 capabilities are the planets.**

But this shot doesn't need viewers to linger long; it's a transition shot.

23.50-24.00s: the 6 capability labels slowly fade out (200ms each, inverse cascade), and the md characters stay at the center, shrinking to 180px, getting ready to make way for the slogan.

**[TYPE]**

- 6 capability labels: JetBrains Mono Bold 14px, letter-spacing 0.16em
  - The first 4 (any→md / md→html / html→md / md→docx): Smoke
  - The last 2 (md→pdf / md→epub): Terracotta

**[ANIM]**

- 22.50-22.80s · the previous shot's EPUB card exits, Chrome A/C fade out (300ms linear)
- 22.50-23.00s · the md characters slide back to center + scale up (500ms expoOut)
- 22.80-23.40s · the 6 capability labels emerge around md (one at each 60° position, r=380px, stagger 80ms each, fade-in 300ms + a slight 20px outward slide)
- 23.40-23.80s · hold (the 6 labels settle around md)
- 23.80-24.00s · the 6 labels fade out together (200ms linear), and the md characters shrink to 180px (200ms expoOut)

**[AUDIO]**

- BGM: at 23.00s, an all-layer swell begins (L1+L2+L3+L4 → +4dB)
- BGM: at 23.50s, the percussion pauses briefly for 1 beat (the tension of sudden silence)
- SFX: a very faint "click" as each of the 6 capability labels enters (-30dB each, staggered)
- SFX: an ascending sweep starts at 23.50s (building up to 24.00s)

**[CHROME]**

- A: fade out at 22.50s (the counter is at 6/6; its mission is complete)
- B: ON, but starts preparing the transition for ACT III (keeps its position, but its internal spacing tightens slightly)
- C: fade out at 22.50s
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ The 6 capability labels don't "orbit around md" (avoiding the cyber slop of a "planet spinner"); they "settle in fixed positions and then fade together" (more restrained)
- ✅ Chrome A/C exit gracefully once their mission is done (rather than "staying on screen forever"). That's a good habit of "making way for the next act"
- ✅ pause-and-look signature: at 23.40s all 6 labels are on screen at once, read in clockwise order. It's the film's only "full capability panorama" frame: if viewers pause here they can see all 6 pipelines. This is the best frame for marketing screenshots

**[WHY]**

This is a bridge.

ACT II ends at 22.50s (NEW (06) has just finished), but the slogan doesn't enter until 24.00s. The 1.5s in between can't be "blank waiting"; it needs narrative motion.

The idea of "convergence": once the 6 pipelines are done, every capability gathers back to md, the source. This is the essence of the film's whole story: **every stream eventually returns to the source**.

In the next shot, md makes way for the slogan. The md characters shrink to 180px, getting ready to become the slogan's "brand stamp".

---

## SHOT 11 · "ONE SOURCE."

**[TIMECODE]** 24.00-26.50s (2.5s) `|` **FUNCTION** First half of the ACT III peak. The slogan's top line enters. Emotional climax.

**[VISUAL]**

The md characters have shrunk to 180px and stay at the center of the frame (y=540).

24.00s: the md characters **keep sliding toward the top-left of the frame** to (x=128, y=88), shrinking to 56px and becoming a "brand stamp" fixed in the top-left corner. This is the brand returning to its place.

24.20s: the hero slogan top line starts to emerge slightly above the center of the frame (y=460):

```
ONE SOURCE.
```

Font: Newsreader 700, **168px**, letter-spacing -0.03em, line-height 0.95, Ink #1A1A1A
Position: horizontally centered (x=960), y=460 (character baseline)

Entrance: **staggered letter reveal**. The 10 characters (O-N-E-space-S-O-U-R-C-E-.) enter one by one with a 30ms stagger, each with fade + 12px y slide-down + scale 0.92 → 1.0 (260ms expoOut each).

26.00s: a short Terracotta rule (320×3px) appears 30px below the slogan, unfolding from the center toward both ends (300ms expoOut).

26.50s: on to the next shot.

**[TYPE]**

- ONE SOURCE.: Newsreader 700, 168px, Ink, letter-spacing -0.03em, line-height 0.95
- terracotta rule: 320×3px, centered, accent

**[ANIM]**

- 24.00-24.30s · the md characters slide to the top-left (300ms expoOut, size 180 → 56)
- 24.20s · the first character of ONE SOURCE., 'O', enters (260ms expoOut)
- 24.23s · 'N' enters
- 24.26s · 'E' enters
- 24.29s · space (nothing visual, but it holds its place in the layout)
- 24.32s · 'S'
- 24.35s · 'O'
- 24.38s · 'U'
- 24.41s · 'R'
- 24.44s · 'C'
- 24.47s · 'E'
- 24.50s · '.' (period)
- 24.20-25.00s · the whole ONE SOURCE. is complete (10 characters × 30ms stagger + 260ms each = total ~560ms)
- 25.00-26.00s · hold (let viewers read "ONE SOURCE.")
- 26.00-26.30s · the Terracotta rule appears (300ms expoOut from 0 → 320px)
- 26.30-26.50s · hold

**[AUDIO]**

- BGM: the swell that began at 22.00s peaks at 24.50s (loudest at -6dB)
- BGM: the full string section enters (L5), with cello + violin + viola layered three deep
- **SFX: impact (slogan ONE) at 24.20s: deep bass impact + short reverb tail (-8dB)** ← this is the strongest SFX cue in the film
- SFX: a very light pen-on-paper stroke at 26.00s (as the rule appears, -22dB)

**[CHROME]**

- A: OFF (already exited)
- B: ON, but with an **important change**: the version chip now cross-dissolves into a new form. It's in the same top-right position, but the chip is slightly larger, with 18px type (16px before), so it stands out more. At the same time the Terracotta dot's pulse amplitude goes × 2 (emphasizing "the v2.0 upgrade moment")
- C: OFF (already exited)
- D: ON
- E: ON

**New chrome**:
- The md characters (top-left, 56px, Newsreader 600 + Terracotta dot) officially take up residence in the corner as the brand stamp

**[ANTI-SLOP]**

- ✅ The slogan isn't a "whole-word fade-in" (cheap); it's a letter-by-letter stagger (cinema-grade)
- ✅ The 30ms per-character stagger is calculated: long enough to see the cascade, but it doesn't drag the rhythm (60ms would feel slow)
- ✅ The 168px size has been verified in the layout: any bigger and it would collide with SIX FORMS. (SHOT 12); any smaller and it wouldn't have enough presence
- ✅ pause-and-look signature: the "." at the end of "ONE SOURCE." is Terracotta (not Ink), echoing the Terracotta dot of the hero md characters, so the brand signature is consistent from start to finish

**[WHY]**

This is the first half of the emotional climax.

"ONE SOURCE." is the film's thesis. If viewers remember just one line from the whole film, it should be this one.

Pulling the md characters back to the top-left at this moment is strategic: the slogan is the lead, and md is the brand stamp. They don't upstage each other.

In the next shot, SIX FORMS. lands, and the thesis is complete.

---

## SHOT 12 · "SIX FORMS."

**[TIMECODE]** 26.50-29.00s (2.5s) `|` **FUNCTION** Second half of the ACT III peak. The slogan's bottom line + the full capability map. The emotional resolution of the whole film.

**[VISUAL]**

26.50s: ONE SOURCE. is still in its upper position in the frame (y=460).

The hero slogan bottom line starts entering in the lower half of the frame (y=720):

```
SIX FORMS.
```

Font: Newsreader 700, 168px, letter-spacing -0.03em, line-height 0.95, **Terracotta #C2410C**
Position: horizontally centered (x=960), y=720 (character baseline)

Entrance: a mirror of SHOT 11. Staggered letter reveal, 9 characters + 1 period (10 in total), with a 30ms stagger each (a slower stagger because this is the climax).

Entrance details: each character uses fade + 12px y **slide-up** (instead of SHOT 11's slide-down, so the directions are symmetrical) + scale 0.92 → 1.0 (260ms expoOut each).

27.20s: SIX FORMS. is complete, and the two-line slogan typography is whole.

27.20-27.80s: 30px below SIX FORMS., 6 capability pills appear, entering one by one:

```
[any→md] [md→html] [html→md] [md→docx] [md→pdf ★NEW] [md→epub ★NEW]
```

Each pill:
- Font: JetBrains Mono Bold 14px, letter-spacing 0.16em
- Size: 10px×18px padding, 1.5px border
- The first 4: Ink text + Ink border + transparent background
- The last 2 (NEW): Terracotta text + Terracotta border + Mist (#FFF7F0) background + a Terra Hot "NEW" mini badge at -8/-10px off the top-right corner

The pills are spaced 14px apart. The whole group is horizontally centered (x=960), y=820.

Entrance: staggered from left to right, 80ms delay each, fade-in + 4px y slide-up (300ms expoOut).

27.80-28.30s: the subtitle line enters (y=890):

```
md 是源代码，万物是产物。   (md is the source code; everything else is product.)
```

Font: Noto Serif SC italic 26px, Ink, letter-spacing 0.04em
Horizontally centered.

Entrance: fade-in + 8px y slide-up (400ms expoOut).

28.30-29.00s: everything holds. This is the most static frame in the film: every element is in place, letting viewers "finish reading it".

**[TYPE]**

- SIX FORMS.: Newsreader 700, 168px, Terracotta, letter-spacing -0.03em, line-height 0.95
- pills: JetBrains Mono Bold 14px, letter-spacing 0.16em, 1.5px border
- subtitle: Noto Serif SC italic 26px, Ink, letter-spacing 0.04em

**[ANIM]**

- 26.50-27.20s · SIX FORMS. character stagger (mirroring SHOT 11)
- 27.20-27.30s · short hold
- 27.30-27.80s · 6 pills cascade (80ms stagger each × 6 = 480ms total + 300ms duration per pill)
- 27.80-28.30s · subtitle enters (400ms)
- 28.30-29.00s · everything holds

**[AUDIO]**

- BGM: the 26.50s peak swell continues, reaching the loudest point of the film at 27.20s (-4dB)
- BGM: after 27.20s the BGM starts to sustain (no longer building, but holding peak intensity)
- **SFX: impact (slogan SIX) at 26.50s: deep bass impact, a semitone heavier than the ONE shot's impact (-7dB)**
- SFX: staggered metallic clicks as the 6 pills enter (-24dB each, 50ms)
- SFX: a very light pen flourish at 27.80s (subtitle enters)

**[CHROME]**

- B: ON, version chip continues
- D: ON, watermark continues
- E: ON
- md stamp (top-left): ON

**[ANTI-SLOP]**

- ✅ ONE SOURCE. is Ink and SIX FORMS. is Terracotta, a color contrast standing for "source" and "product", not decorative color
- ✅ The background of the two NEW pills among the 6 is #FFF7F0 (a very pale mist tint), not an "orange fill". Restrained
- ✅ The NEW mini badge sits at a prominent -8/-10px off the pill's top-right corner, but at only 9px type: the standard position for a detail signature
- ✅ The subtitle uses the Chinese comma "，" + the Chinese full stop "。", out of respect for Chinese typesetting
- ✅ This frame (28.30s) is the film's "most complete frame for marketing": it can be captured as a thumbnail / X poster / WeChat Official Account cover image, with all the information in one frame: slogan + 6 capabilities + subtitle + brand stamp + version

**[WHY]**

This is the resolution shot.

If SHOT 11 is the thesis (ONE SOURCE.), SHOT 12 is the antithesis + synthesis (SIX FORMS. plus the full capability map).

At 27.50s in this frame, viewers should be hearing the string peak while being visually fully absorbed by the typography. These are the film's most rewarding 5 seconds.

The next shot is the close: let the strings decay and let the md stamp shine alone.

---

## SHOT 13 · "SIGN-OFF"

**[TIMECODE]** 29.00-30.00s (1.0s) `|` **FUNCTION** Ending. All slogan elements exit, leaving the md stamp to shine alone. The brand mark.

**[VISUAL]**

29.00s: SIX FORMS. + 6 pills + subtitle begin to hold in place.

29.20-29.60s: ONE SOURCE. + SIX FORMS. + 6 pills + subtitle slowly fade out (400ms linear each, **no stagger**; they fade out in sync, creating the feeling of "the frame settling").

29.40s: the md stamp characters in the top-left slowly grow from 56px to 88px while sliding from (128, 88) toward the center of the frame (960, 540). This is md's "final return".

29.40-29.80s: the md characters settle at the center of the frame, size 88px, color Ink + Terracotta dot.

29.80-30.00s: a short Terracotta rule (120×2px, shorter and more refined than in SHOT 03) appears 30px below the md characters, growing from 0.

30.00s: all elements are in place. The final frame is:

```
                                                                  ● HUASHU-MD-HTML · v2.0
                                                                                              (top-right chrome)


                                            md.                   ← Newsreader 600, 88px, Ink + Terracotta dot
                                          ───                     ← Terracotta rule, 120×2px

                                                                                CREATED BY HUASHU-DESIGN
                                                                                              (bottom-right watermark)
```

The whole frame has only 4 elements: the md stamp, the accent rule, the top-right chrome and the bottom-right watermark. Everything else is empty.

**[TYPE]**

- md.: Newsreader 600, 88px, Ink + Terracotta dot
- accent rule: 120×2px Terracotta

**[ANIM]**

- 29.00-29.20s · the previous shot holds (let viewers fully absorb it)
- 29.20-29.60s · ONE SOURCE. + SIX FORMS. + 6 pills + subtitle fade out in sync (400ms linear, in sync)
- 29.40-29.80s · the md stamp grows + slides to the center (400ms expoOut, size 56 → 88, position (128,88) → (960,540))
- 29.80-30.00s · the accent rule unfolds (200ms expoOut, 0 → 120px)
- 30.00s · final hold (if there's a loop, loop back to 00.00s)

**[AUDIO]**

- BGM: decay begins at 29.00s, moving into L6 (all layers fading)
- BGM: the strings fade at 29.40s, leaving piano + reverb tail
- BGM: 30.00s, everything returns to silence + room tone
- **SFX: final stamp / sign-off at 29.40s (ink stamp + soft reverb, -14dB)**, as md lands at the center
- SFX: a very light paper rustle at 29.80s (accent rule enters)

**[CHROME]**

- B: ON, continues
- D: ON, continues
- E: ON, continues
- Everything else OFF

**[ANTI-SLOP]**

- ✅ No sign-off text like "Thank you" or "Made with love" (cheap)
- ✅ No big logo blow-up (not needed)
- ✅ The md stamp is the true lead of the film's whole story; leaving it alone at the center of the frame at the end is the simplest form of resolution
- ✅ pause-and-look signature: in the final frame's md. in 88px Newsreader, the Terracotta dot is the visual focus of the whole frame. Viewers' eyes naturally rest on the dot, then see the accent rule below, then the version chip at the top-right. This "eye path" is a success of visual hierarchy design
- ✅ The silence in the last 0.2s gives the frame breathing room

**[WHY]**

The whole film begins with a blank page and ends with an md stamp + a touch of terracotta.

This is a bookend (visual rhyme):
- 0.0s: blank ivory page (empty)
- 30.0s: ivory page + md (full)

Viewers travel from "empty" to "full", but "full" is really just one `md.` character. That's the visual manifesto of "source-of-truth": **everything comes from one simple md.**

If the film makes viewers remember one frame, I hope it's this one.

---

# Part V · Production Manifest

## 5.1 Font list + loading method

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=JetBrains+Mono:wght@400;500;700&family=Noto+Serif+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
```

**Measured load time**: about 800-1500ms depending on CDN status. Wait for `document.fonts.ready` to return true before starting the Stage timer (Stage already implements this).

## 5.2 Palette CSS variables

```css
:root {
  --paper:       #FAFAF6;
  --mist:        #F2EDE4;
  --mica:        #E6E1D6;
  --smoke:       #6B6B6B;
  --cinder:      #3D3530;
  --ink:         #1A1A1A;
  --charred:     #2A2620;
  --terracotta:  #C2410C;
  --terra-hot:   #E55D21;
  --terra-deep:  #8B2D08;
}
```

## 5.3 Criteria for choosing the BGM source

**First choice**: generate a 30-second cinematic minimal piece yourself with Suno v6.0 / Udio v1.5, with these prompt keywords:

```
minimal cinematic piano, slow tempo 60bpm, single piano notes,
sparse arpeggio, low cello drone, subtle sub-kick percussion,
swelling strings at climax, decay to silence,
in the style of Max Richter on the nature of daylight,
no vocals, 30 seconds duration, ivory paper mood
```

**Alternatives**: search royalty-free libraries
- artlist.io: "minimal cinematic"
- bensound.com: "cinematic"
- musicbed.com: "Jóhann Jóhannsson style"

**Minimum standard**: BGM 30 seconds long, 44.1kHz sample rate, aim for -16 LUFS integrated loudness.

## 5.4 SFX sources

**First choice**: use the 37 prebuilt assets in the huashu-design skill's `assets/sfx/<category>/*.mp3`:

```
Event                      Recommended SFX file
─────────────────────────────────────────────────────
keyboard clicks            sfx/ui/keyboard-click-*.mp3
cursor blink               sfx/ui/tick-soft.mp3
md morph swell             sfx/cinematic/whoosh-bloom.mp3
file card whoosh           sfx/cinematic/whoosh-short-*.mp3
absorb / ink drop          sfx/foley/ink-drop.mp3
paper rustle               sfx/foley/paper-turn.mp3
chime capability           sfx/melodic/chime-single-*.mp3
chime NEW (double)         sfx/melodic/chime-double-warm.mp3
build sweep                sfx/cinematic/ascending-sweep.mp3
impact (slogan)            sfx/cinematic/deep-impact-*.mp3
pen flourish               sfx/foley/pen-stroke.mp3
final stamp                sfx/foley/ink-stamp.mp3
```

## 5.5 Screenshot verification plan

After implementing the HTML, you must verify the following keyframes (using Playwright + the `?t=NN` URL parameter):

```
t=0.5    ← SHOT 01 mid: blank ivory page (check that the paper texture doesn't upstage)
t=2.5    ← SHOT 02 mid: typing in progress (check cursor blink + JetBrains Mono)
t=3.8    ← SHOT 03 mid: md morphing (check ghost residual + scale curve)
t=5.0    ← SHOT 03 end: hero md settled (check 480px + Terracotta dot)
t=7.0    ← SHOT 04 mid: cards in flight (check the parabola + card content is real and readable)
t=8.4    ← SHOT 04 tagline (check the Chinese italic "万物 → md")
t=10.5   ← SHOT 05 mid: html card complete (check the essay content is readable)
t=13.5   ← SHOT 06 mid: md source visible (check syntax highlighting)
t=16.5   ← SHOT 07 mid: docx page complete (check chapter title + page number)
t=19.0   ← SHOT 08 mid: PDFs fanned out (check crop marks are visible)
t=21.5   ← SHOT 09 mid: EPUB frame complete (check Apple Books chrome)
t=23.4   ← SHOT 10 mid: 6 capability orbit (check the full capability panorama)
t=25.0   ← SHOT 11 mid: ONE SOURCE. complete (check tracking + Terracotta period)
t=27.5   ← SHOT 12 mid: SIX FORMS. + pills (check the complete two-line slogan)
t=28.5   ← SHOT 12 marketing frame (check the overall marketing-ready frame)
t=29.9   ← SHOT 13 final hold (check md stamp + accent rule)
```

Every frame must meet these criteria:
- No element overflows the 1920×1080 canvas
- Tracking and line height are visually correct
- Passes the anti-AI-slop checklist
- Key typography details (such as the Terracotta dot, page number em-dash, chapter title small caps) are recognizable

## 5.6 Recording parameters

```bash
node scripts/render-video.js \
  --file file:///path/to/v5-six-forms.html \
  --duration 30 \
  --fps 25 \
  --width 1920 \
  --height 1080 \
  --out v5-final-silent.mp4
```

**Key codec parameters**:
- video codec: libx264
- pixel format: yuv420p (compatibility)
- bitrate: 12 Mbps (high quality, a 30s file is about 45MB)
- profile: high
- preset: slow (quality > speed)

**Optional frame interpolation** (a smooth 60fps version):

```bash
bash scripts/convert-formats.sh v5-final-silent.mp4 --fps 60
```

## 5.7 Audio mixing

```bash
# Step 1: add BGM
bash scripts/add-music.sh v5-final-silent.mp4 \
  --bgm assets/bgm/cinematic-minimal-30s.mp3 \
  --bgm-volume -18dB \
  --out v5-with-bgm.mp4

# Step 2: add SFX cues (add them cue by cue following the SFX dictionary in Part II.6)
# use ffmpeg's -filter_complex amix for multi-track mixing
ffmpeg -i v5-with-bgm.mp4 \
  -i assets/sfx/ui/keyboard-click-1.mp3 \
  -i assets/sfx/ui/keyboard-click-2.mp3 \
  ... \
  -filter_complex "[1]adelay=500|500[s1];[2]adelay=550|550[s2];...;[0][s1][s2]...amix=inputs=N:duration=longest:dropout_transition=0[out]" \
  -map 0:v -map "[out]" \
  -c:v copy -c:a aac -b:a 192k \
  v5-final.mp4

# Step 3: verify the audio stream
ffprobe -i v5-final.mp4 -show_streams -select_streams a 2>&1 | grep -E "(codec_type|sample_rate|channels|duration)"
```

**Expected output**:
- audio codec: aac
- sample rate: 44100Hz or 48000Hz
- channels: 2 (stereo)
- duration: 30.0s

## 5.8 Deliverables list

```
v5-final.mp4              main deliverable (30s, 1920×1080, 25fps, with audio, ~50MB)
v5-final-60fps.mp4        high frame rate version (60fps interpolated, ~80MB, for X / YouTube)
v5-final.gif              social media version (30s, palette-optimized, < 8MB, for embedding in WeChat Official Account posts)
v5-final-silent.mp4       silent version (backup, for re-voicing / swapping the BGM later)
v5-poster.png             poster version (the frame captured at t=28.5s, for X cards / WeChat Official Account covers)
v5-director-notes.md      this document (director's notes)
v5-six-forms.html         source file (HTML animation)
v5-shot-list.csv          reference table of shot timecodes + key parameters (for pause verification)
```

## 5.9 End-to-end time estimate

| Step | Estimated time |
|-----|----------|
| Writing the director's notes | Done |
| Implementing the HTML animation | 4-6 hours |
| Keyframe screenshots + visual check | 1 hour |
| Recording the silent MP4 | 5-10 minutes (including Playwright startup) |
| Generating / choosing the BGM | 30 minutes |
| Matching SFX to cues + mixing | 2-3 hours |
| Deriving the GIF | 5 minutes |
| Poster screenshot + naming | 10 minutes |
| Final delivery + git commit | 10 minutes |
| **Total** | **8-11 hours** |

---

# Appendix · This film's first principle

If as director I could keep only one sentence about this film, it would be:

> **A typographic film about "the source", whose lead is a single `md.` character.**

Every other design decision (palette, fonts, rhythm, SFX, chrome, anti-slop checklist) is derived from this one sentence.

If a specific decision can't be traced back to this sentence, don't make it.

---

*Director's notes — end of document*
*Total word count: about 11,500 Chinese characters*
*Next: once the user approves it in review, move on to the HTML implementation stage*
