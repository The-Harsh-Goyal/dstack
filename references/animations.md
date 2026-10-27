# Animations: Timeline Animation Engine

Read this when making animation/motion design HTML. Principles, usage, typical patterns.

## Core pattern: Stage + Sprite

Our animation system (`assets/animations.jsx`) provides a timeline-driven engine:

- **`<Stage>`**: the container for the whole animation, automatically providing auto-scale (fit viewport) + scrubber + play/pause/loop controls
- **`<Sprite start end>`**: a time segment. A Sprite is only shown between `start` and `end`. Inside, it can read its own local progress `t` (0→1) through the `useSprite()` hook
- **`useTime()`**: reads the current global time (seconds)
- **`Easing.easeInOut` / `Easing.easeOut` / ...**: easing functions
- **`interpolate(t, from, to, easing?)`**: interpolates based on t

This pattern borrows from the Remotion/After Effects approach, but is lightweight with zero dependencies.

## Getting started

```html
<script type="text/babel" src="animations.jsx"></script>
<script type="text/babel">
  const { Stage, Sprite, useTime, useSprite, Easing, interpolate } = window.Animations;

  function Title() {
    const { t } = useSprite();  // Local progress 0→1
    const opacity = interpolate(t, [0, 1], [0, 1], Easing.easeOut);
    const y = interpolate(t, [0, 1], [40, 0], Easing.easeOut);
    return (
      <h1 style={{ 
        opacity, 
        transform: `translateY(${y}px)`,
        fontSize: 120,
        fontWeight: 900,
      }}>
        Hello.
      </h1>
    );
  }

  function Scene() {
    return (
      <Stage duration={10}>  {/* 10-second animation */}
        <Sprite start={0} end={3}>
          <Title />
        </Sprite>
        <Sprite start={2} end={5}>
          <SubTitle />
        </Sprite>
        {/* ... */}
      </Stage>
    );
  }

  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<Scene />);
</script>
```

## Common animation patterns

### 1. Fade In / Fade Out

```jsx
function FadeIn({ children }) {
  const { t } = useSprite();
  const opacity = interpolate(t, [0, 0.3], [0, 1], Easing.easeOut);
  return <div style={{ opacity }}>{children}</div>;
}
```

**Mind the range**: `[0, 0.3]` means the fade-in completes in the first 30% of the sprite's time, and opacity stays at 1 after that.

### 2. Slide In

```jsx
function SlideIn({ children, from = 'left' }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, 0.4], [0, 1], Easing.easeOut);
  const offset = (1 - progress) * 100;
  const directions = {
    left: `translateX(-${offset}px)`,
    right: `translateX(${offset}px)`,
    top: `translateY(-${offset}px)`,
    bottom: `translateY(${offset}px)`,
  };
  return (
    <div style={{
      transform: directions[from],
      opacity: progress,
    }}>
      {children}
    </div>
  );
}
```

### 3. Typing effects (⚠️ tell the two scenarios apart first, and don't pop out one character at a time)

A constant-speed, character-by-character typewriter is an official counterexample (the best-practices "AI slop" list: looks like old movie subtitles). Choose the right approach by content:

- **AI output** (token streaming) → Chunk Reveal: irregular chunked emergence; see `animation-best-practices.md` §4.5 / `gsap-recipes.md` §3.4
- **User input** (a real person typing in an input box) → 3f/character + a cursor that's solid and then blinks + occasional backspaces; see technique ③ of the eight in `ui-demo-animation.md`

### 4. Number counting

```jsx
function CountUp({ from = 0, to = 100, duration = 0.6 }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, duration], [0, 1], Easing.easeOut);
  const value = Math.floor(from + (to - from) * progress);
  return <span>{value.toLocaleString()}</span>;
}
```

### 5. Step-by-step explanation (typical teaching animation)

```jsx
function Scene() {
  return (
    <Stage duration={20}>
      {/* Phase 1: show the problem */}
      <Sprite start={0} end={4}>
        <Problem />
      </Sprite>

      {/* Phase 2: show the approach */}
      <Sprite start={4} end={10}>
        <Approach />
      </Sprite>

      {/* Phase 3: show the result */}
      <Sprite start={10} end={16}>
        <Result />
      </Sprite>

      {/* Captions shown throughout */}
      <Sprite start={0} end={20}>
        <Caption />
      </Sprite>
    </Stage>
  );
}
```

## Easing functions

Preset easing curves:

| Easing | Character | Used for |
|--------|------|------|
| `linear` | Constant speed | Scrolling credits, continuous animation |
| `easeIn` | Slow→fast | Exits and disappearing |
| `easeOut` | Fast→slow | Entrances and appearing |
| `easeInOut` | Slow→fast→slow | Position changes |
| **`expoOut`** ⭐ | **Exponential ease-out** | **Anthropic-level main easing** (physical weight) |
| **`overshoot`** ⭐ | **Elastic rebound** | **Toggle / button pop / emphasized interaction** |
| `spring` | Spring | Interaction feedback, geometry settling into place |
| `anticipation` | Reverse first, then forward | Emphasized actions |

**Use `expoOut` as the default main easing** (not `easeOut`); see `animation-best-practices.md` §2.
`expoOut` for entrances, `easeIn` for exits, `overshoot` for toggles: the basic pattern of Anthropic-level animation.

## Rhythm and duration guide

### Micro-interactions (0.1-0.3 seconds)
- Button hover
- Card expand
- Tooltip appearing

### UI transitions (0.3-0.8 seconds)
- Page switches
- Modal appearing
- List item added

### Narrative animation (2-10 seconds per segment)
- One phase of a concept explanation
- A data chart reveal
- Scene transitions

### A single narrative animation segment is at most 10 seconds
Human attention is limited. Use 10 seconds to say one thing, then move on to the next.

## The order of thinking when designing animation

### 1. Content/story first, animation second

**Wrong**: first decide you want a fancy animation, then stuff content into it
**Right**: first work out what information you want to convey, then use animation to serve that information

Animation is a **signal**, not **decoration**. A fade-in emphasizes "this is important, look here"; if everything fades in, the signal stops working.

### 2. Write the timeline by scene

```
0:00 - 0:03   Problem appears (fade in)
0:03 - 0:06   Problem zooms in/unfolds (zoom+pan)
0:06 - 0:09   Solution appears (slide in from right)
0:09 - 0:12   Solution is explained (typewriter)
0:12 - 0:15   Result demo (counter up + chart reveal)
0:15 - 0:18   One-sentence summary (static, 3 seconds to read)
0:18 - 0:20   CTA or fade out
```

Write the timeline first, then the components.

### 3. Assets first

Get the images/icons/fonts the animation needs ready **first**. Don't go looking for assets halfway through; it breaks your rhythm.

## Common problems

**Animation stutters**
→ Mostly layout thrashing. Use `transform` and `opacity`; don't animate `top`/`left`/`width`/`height`/`margin`. The browser GPU-accelerates `transform`.

**Animation is too fast to follow**
→ It takes a person 100-150ms to read one Chinese character and 300-500ms for a word. If you tell a story with text, leave at least 3 seconds per sentence.

**Animation is too slow and viewers get bored**
→ Interesting visual changes need to be dense. A static frame gets dull after more than 5 seconds.

**Multiple animations interfere with each other**
→ Use CSS `will-change: transform` to tell the browser in advance that the element will move, reducing reflow.

**Recording to video**
→ Use the skill's built-in toolchain (one command outputs three formats): see `video-export.md`
- `scripts/render-video.js`: HTML → 25fps MP4 (Playwright + ffmpeg)
- `scripts/convert-formats.sh`: 25fps MP4 → 60fps MP4 + optimized GIF
- Want more precise frame rendering? Make render(t) a pure function; see item 5 in `animation-pitfalls.md`

## Working with video tools

This skill makes **HTML animation** (running in the browser). If the final output will be used as video footage:

- **Short animations/concept demos**: make the HTML animation with the methods here → screen recording
- **Long videos/narrative** (5-20 minutes with narration): follow the narration-driven line in `references/modules/motion.md` (`voiceover-pipeline.md`); don't hand it off to other tools
- **Motion graphics**: professional After Effects/Motion Canvas is a better fit

## When you need physics animation (spring / decay)

Don't pull in Popmotion (its CDN is guaranteed to fail on restricted networks, violating the self-contained principle; see `animation-pitfalls.md` #17). Handle spring needs with GSAP: for `elastic.out` / `back.out` and the custom springEase mapping, see `gsap-recipes.md` §1.2; for landing aftershocks, use the closed-form dampedSettle solution (`camera-language.md` §9).
