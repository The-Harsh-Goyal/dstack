# Animation Pitfalls: Pitfalls We've Hit in HTML Animation, and the Rules

The bugs most often hit when making animations, and how to avoid them. Every rule comes from a real failure case.

Reading this before you write an animation can save you a round of iteration.

## 1. Stacked layouts: `position: relative` is a default obligation

**The pitfall**: a sentence-wrap element contained 3 bracket-layers (`position: absolute`). sentence-wrap had no `position: relative`, so the absolute brackets used `.canvas` as their coordinate system and drifted 200px past the bottom of the screen.

**Rules**:
- Any container with `position: absolute` children **must** explicitly set `position: relative`
- Even if you don't visually need an "offset", write `position: relative` as the coordinate-system anchor
- If you're writing `.parent { ... }` and its children include `.child { position: absolute }`, reflexively add relative to the parent

**Quick check**: for every `position: absolute`, count up through the ancestors and make sure the nearest positioned ancestor is the coordinate system you *want*.

## 2. Character traps: don't rely on rare Unicode

**The pitfall**: we wanted to use `␣` (U+2423 OPEN BOX) to visualize a "space token". Neither Noto Serif SC nor Cormorant Garamond has this glyph, so it rendered as blank/tofu and viewers couldn't see it at all.

**Rules**:
- **Every character that appears in the animation must exist in the font you've chosen**
- Blacklist of common rare characters: `␣ ␀ ␐ ␋ ␨ ↩ ⏎ ⌘ ⌥ ⌃ ⇧ ␦ ␖ ␛`
- To express meta-characters like "space / return / tab", use a **semantic box built with CSS**:
  ```html
  <span class="space-key">Space</span>
  ```
  ```css
  .space-key {
    display: inline-flex;
    padding: 4px 14px;
    border: 1.5px solid var(--accent);
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.3em;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  ```
- Verify emoji too: some emoji fall back to gray boxes in fonts other than Noto Emoji; it's best to use the `emoji` font-family or SVG

## 3. Data-driven Grid/Flex templates

**The pitfall**: the code had `const N = 6` tokens, but the CSS hard-coded `grid-template-columns: 80px repeat(5, 1fr)`. The 6th token had no column, and the whole matrix was misaligned.

**Rules**:
- When the count comes from a JS array (`TOKENS.length`), the CSS template should be data-driven too
- Option A: inject it from JS via a CSS variable
  ```js
  el.style.setProperty('--cols', N);
  ```
  ```css
  .grid { grid-template-columns: 80px repeat(var(--cols), 1fr); }
  ```
- Option B: use `grid-auto-flow: column` and let the browser expand automatically
- **Never combine "a hard-coded number + a JS constant"**; when N changes, the CSS won't update with it

## 4. Transition gaps: scene changes must be continuous

**The pitfall**: between zoom1 (13-19s) → zoom2 (19.2-23s), the main sentence was already hidden, and zoom1 fade out (0.6s) + zoom2 fade in (0.6s) + stagger delay (0.2s+) = about 1 second of pure blank screen. Viewers thought the animation had frozen.

**Rules**:
- When switching scenes back to back, fade out and fade in should **cross-overlap**, not wait for the previous one to fully disappear before starting the next
  ```js
  // Bad:
  if (t >= 19) hideZoom('zoom1');      // 19.0s out
  if (t >= 19.4) showZoom('zoom2');    // 19.4s in → 0.4s blank in between

  // Good:
  if (t >= 18.6) hideZoom('zoom1');    // Start fading out 0.4s early
  if (t >= 18.6) showZoom('zoom2');    // Fade in at the same time (cross-fade)
  ```
- Or use an "anchor element" (such as the main sentence) as the visual link between scenes, briefly showing it again during the zoom switch
- Work out the durations of the CSS transitions so the next one isn't triggered before the current transition ends

## 5. The Pure Render principle: animation state should be seekable

**The pitfall**: animation states were triggered in a chain with `setTimeout` + `fireOnce(key, fn)`. Normal playback was fine, but when recording frame by frame/seeking to an arbitrary point in time, setTimeouts that had already run couldn't "go back in time".

**Rules**:
- The `render(t)` function should ideally be a **pure function**: given t, it outputs exactly one DOM state
- If you must use side effects (such as class toggles), use a `fired` set together with an explicit reset:
  ```js
  const fired = new Set();
  function fireOnce(key, fn) { if (!fired.has(key)) { fired.add(key); fn(); } }
  function reset() { fired.clear(); /* clear all .show classes */ }
  ```
- Expose `window.__seek(t)` for Playwright / debugging:
  ```js
  window.__seek = (t) => { reset(); render(t); };
  ```
- Animation-related setTimeouts shouldn't span >1 second, or seeking backward will make a mess

## 6. Measuring before fonts load = measuring wrong

**The pitfall**: the page called `charRect(idx)` to measure bracket positions as soon as DOMContentLoaded fired. The font hadn't loaded yet, so every character width was the fallback font's width and all positions were wrong. Once the font loaded (about 500ms later), the brackets' `left: Xpx` still held the old values, permanently offset.

**Rules**:
- Any layout code that depends on DOM measurement (`getBoundingClientRect`, `offsetWidth`) **must** be wrapped in `document.fonts.ready.then()`
  ```js
  document.fonts.ready.then(() => {
    requestAnimationFrame(() => {
      buildBrackets(...);  // Fonts are ready now, so measurements are accurate
      tick();              // Animation starts
    });
  });
  ```
- The extra `requestAnimationFrame` gives the browser one frame to commit the layout
- If you use the Google Fonts CDN, `<link rel="preconnect">` speeds up the first load

## 7. Recording prep: leave handles for video export

**The pitfall**: Playwright `recordVideo` defaults to 25fps and starts recording from context creation. The first 2 seconds of page loading and font loading all got recorded. The delivered video had 2 seconds of blank/white flash at the start.

**Rules**:
- Provide a `render-video.js` tool to handle it: warmup navigate → reload to restart the animation → wait for the duration → ffmpeg trims the head + converts to H.264 MP4
- The animation's **frame 0** must be the complete initial state with the final layout in place (not blank or loading)
- Want 60fps? Post-process with ffmpeg `minterpolate`; don't count on the browser's source frame rate
- Want a GIF? Use a two-stage palette (`palettegen` + `paletteuse`); a 30s 1080p animation can compress to 3MB

See `video-export.md` for how to call the full script.

## 8. Batch export: tmp directories must include the PID to avoid concurrency conflicts

**The pitfall**: we used `render-video.js` with 3 processes recording 3 HTML files in parallel. Because TMP_DIR was named with only `Date.now()`, the 3 processes started in the same millisecond and shared one tmp directory. The first process to finish cleaned up tmp, the other two got `ENOENT` reading the directory, and they all crashed.

**Rules**:
- Any temp directory that multiple processes might share must be named with a **PID or random suffix**:
  ```js
  const TMP_DIR = path.join(DIR, '.video-tmp-' + Date.now() + '-' + process.pid);
  ```
- If you really want multiple files in parallel, use the shell's `&` + `wait` instead of forking inside one node script
- When batch-recording multiple HTML files, the conservative approach: run them **serially** (up to 2 can run in parallel; with 3 or more, queue them up)

## 9. Progress bars/replay buttons in the recording: chrome elements polluting the video

**The pitfall**: the animation HTML had a `.progress` progress bar, a `.replay` button, and a `.counter` timestamp to make playback easy for humans to debug. When recorded to MP4 for delivery, these elements showed up at the bottom of the video, as if developer tools had been captured in it.

**Rules**:
- Manage the "chrome elements" meant for humans in the HTML (progress bar / replay button / footer / masthead / counter / phase labels) separately from the video content itself
- **Agreed class name** `.no-record`: the recording script automatically hides any element with this class
- On the script side (`render-video.js`), CSS is injected by default to hide common chrome class names:
  ```
  .progress .counter .phases .replay .masthead .footer .no-record [data-role="chrome"]
  ```
- Inject it with Playwright's `addInitScript` (takes effect before every navigate, and holds up across reloads)
- Add the `--keep-chrome` flag when you want to see the HTML as is (with chrome)

## 10. Animation repeats in the first few seconds of the recording: warmup frame leakage

**The pitfall**: the old flow in `render-video.js` was `goto → wait fonts 1.5s → reload → wait duration`. Recording started from context creation, so the animation had already played for a while during warmup, then restarted from 0 after the reload. The first few seconds of the video were "mid-animation + a switch + the animation starting from 0", with a strong sense of repetition.

**Rules**:
- **Warmup and Record must use separate contexts**:
  - Warmup context (no `recordVideo` option): only loads the url, waits for fonts, then closes
  - Record context (with `recordVideo`): starts from a fresh state, recording the animation from t=0
- ffmpeg `-ss trim` can only trim a tiny bit of Playwright startup latency (~0.3s); it **cannot** be used to cover warmup frames. The source has to be clean
- Closing the recording context = writing the webm file to disk; this is a Playwright constraint
- Relevant code pattern:
  ```js
  // Phase 1: warmup (throwaway)
  const warmupCtx = await browser.newContext({ viewport });
  const warmupPage = await warmupCtx.newPage();
  await warmupPage.goto(url, { waitUntil: 'networkidle' });
  await warmupPage.waitForTimeout(1200);
  await warmupCtx.close();

  // Phase 2: record (fresh)
  const recordCtx = await browser.newContext({ viewport, recordVideo });
  const page = await recordCtx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(DURATION * 1000);
  await page.close();
  await recordCtx.close();
  ```

## 11. Don't draw "fake chrome" in the frame: decorative player UI colliding with real chrome

**The pitfall**: the animation used the `Stage` component, which already comes with a scrubber + timecode + pause button (they're `.no-record` chrome, automatically hidden on export). I also drew a "`00:60 ──── CLAUDE-DESIGN / ANATOMY`" "magazine-folio-style decorative progress bar" at the bottom of the frame and felt pretty good about it. **Result**: the user saw two progress bars, one the Stage controller and one my decoration. Visually they collided completely, and it was taken as a bug: "Why is there another progress bar inside the video?"

**Rules**:

- Stage already provides: scrubber + timecode + pause/replay buttons. **Don't draw in the frame** progress indicators, a current timecode, a copyright credit strip, or chapter counters. They either collide with the chrome or are just filler slop (violating the "earn its place" principle).
- **Decorative urges** like "folio feel", "magazine feel", and "bottom credit strip" are high-frequency filler that AI adds automatically. Be wary of every one that appears: does it really convey irreplaceable information? Or is it just filling empty space?
- If you're convinced some bottom strip must exist (for example, the animation's subject is player UI), it must be **narratively necessary** and **visually distinct from the Stage scrubber** (different position, different form, different color tone).

**Element ownership test** (every element drawn into the canvas must be able to answer this):

| What it belongs to | Handling |
|------------|------|
| Narrative content of some scene | OK, keep it |
| Global chrome (for control/debugging) | Add the `.no-record` class, hidden on export |
| **Belongs to no scene and isn't chrome** | **Delete**. It's an ownerless thing and inevitably filler slop |

**Self-check (3 seconds before delivery)**: take a still screenshot and ask yourself:

- Is there anything in the frame that "looks like video player UI" (a horizontal progress bar, a timecode, things shaped like control buttons)?
- If so, would deleting it hurt the narrative? If not, delete it.
- Does the same kind of information (progress/time/credit) appear twice? Merge it into one place in the chrome.

**Counterexamples**: drawing `00:42 ──── PROJECT NAME` at the bottom, drawing a "CH 03 / 06" chapter counter in the bottom-right corner, drawing a version number "v0.3.1" at the edge of the frame. These are all fake-chrome filler.

## 12. Leading blank + recording start offset: the `__ready` × tick × lastTick triple trap

**The pitfall (A · leading blank)**: a 60-second animation exported to MP4 had 2-3 seconds of blank page at the start. `ffmpeg --trim=0.3` couldn't cut it.

**The pitfall (B · start offset, a real incident on 2026-04-20)**: a 24-second video was exported, and to the user it felt like "the video only starts playing its first frame at 19 seconds". In reality, the animation started recording at t=5, recorded to t=24, looped back to t=0, then recorded another 5 seconds to the end, so the last 5 seconds of the video were actually the animation's real beginning.

**Root cause** (both pitfalls share one root cause):

Playwright `recordVideo` starts writing the WebM the moment `newContext()` is called, while Babel/React/font loading takes L seconds in total (2-6s). The recording script waits for `window.__ready = true` as the anchor for "the animation starts here", and it must be strictly paired with the animation's `time = 0`. There are two common ways to get it wrong:

| Wrong way | Symptom |
|------|------|
| `__ready` is set in `useEffect` or the synchronous setup phase (before the first tick frame) | The recording script thinks the animation has started, but the WebM is actually still recording a blank page → **leading blank** |
| tick's `lastTick = performance.now()` is initialized at the **top level of the script** | The L seconds of font loading are counted into the first frame's `dt`, `time` instantly jumps to L → the whole recording lags by L seconds → **start offset** |

**✅ The correct complete starter tick template** (hand-written animation must use this skeleton):

```js
// ━━━━━━ state ━━━━━━
let time = 0;
let playing = false;   // ❗ Don't play by default; start once fonts are ready
let lastTick = null;   // ❗ sentinel: forces dt to 0 on tick's first frame (don't use performance.now())
const fired = new Set();

// ━━━━━━ tick ━━━━━━
function tick(now) {
  if (lastTick === null) {
    lastTick = now;
    window.__ready = true;   // ✅ pair: "recording start" and "animation t=0" on the same frame
    render(0);               // Render once more to make sure the DOM is ready (fonts are ready now)
    requestAnimationFrame(tick);
    return;
  }
  const dt = (now - lastTick) / 1000;   // dt only starts advancing after the first frame
  lastTick = now;

  if (playing) {
    let t = time + dt;
    if (t >= DURATION) {
      t = window.__recording ? DURATION - 0.001 : 0;  // Don't loop while recording; keep 0.001s to preserve the last frame
      if (!window.__recording) fired.clear();
    }
    time = t;
    render(time);
  }
  requestAnimationFrame(tick);
}

// ━━━━━━ boot ━━━━━━
// Don't rAF immediately at the top level; start only after fonts finish loading
document.fonts.ready.then(() => {
  render(0);                 // Draw the initial frame first (fonts are ready)
  playing = true;
  requestAnimationFrame(tick);  // The first tick pairs __ready + t=0
});

// ━━━━━━ seek interface (for render-video's defensive correction) ━━━━━━
window.__seek = (t) => { fired.clear(); time = t; lastTick = null; render(t); };
```

**Why this template is right**:

| Piece | Why it has to be this way |
|------|-------------|
| `lastTick = null` + `return` on the first frame | Prevents the L seconds between "script load and tick's first run" from being counted as animation time |
| `playing = false` by default | Even if `tick` runs during font loading, it doesn't advance time, preventing misaligned rendering |
| `__ready` set on tick's first frame | The recording script starts timing at this moment, and the corresponding frame is the animation's real t=0 |
| tick only starts inside `document.fonts.ready.then(...)` | Avoids measuring with fallback font widths and avoids a font jump on the first frame |
| `window.__seek` exists | Lets `render-video.js` actively correct things: the second line of defense |

**Matching defenses on the recording script side**:
1. `addInitScript` injects `window.__recording = true` (before page goto)
2. `waitForFunction(() => window.__ready === true)`, recording the offset at this moment as the ffmpeg trim
3. **Additionally**: after `__ready`, actively run `page.evaluate(() => window.__seek && window.__seek(0))` to force any possible time deviation in the HTML back to zero. This is the second line of defense, for HTML that doesn't strictly follow the starter template

**Verification**: after exporting the MP4
```bash
ffmpeg -i video.mp4 -ss 0 -vframes 1 frame-0.png
ffmpeg -i video.mp4 -ss $DURATION-0.1 -vframes 1 frame-end.png
```
The first frame must be the animation's initial state at t=0 (not the middle, not black), and the last frame must be the animation's final state (not some moment in a second loop).

**Reference implementation**: the Stage component in `assets/animations.jsx` and `scripts/render-video.js` both already implement this protocol. Hand-written HTML must use the starter tick template; every line guards against a specific bug.

## 13. No looping while recording: the `window.__recording` signal

**The pitfall**: the animation's Stage defaults to `loop=true` (handy for viewing in the browser). `render-video.js` waits an extra 300ms buffer after recording the duration before stopping, and those 300ms let Stage enter the next loop. When ffmpeg cuts with `-t DURATION`, the last 0.5-1s falls into the next loop: the end of the video suddenly jumps back to the first frame (Scene 1), and viewers think the video is buggy.

**Root cause**: there's no "I'm recording" handshake protocol between the recording script and the HTML. The HTML doesn't know it's being recorded and keeps looping as in an interactive browser scenario.

**Rules**:

1. **Recording script**: inject `window.__recording = true` in `addInitScript` (before page goto):
   ```js
   await recordCtx.addInitScript(() => { window.__recording = true; });
   ```

2. **Stage component**: recognize this signal and force loop=false:
   ```js
   const effectiveLoop = (typeof window !== 'undefined' && window.__recording) ? false : loop;
   // ...
   if (next >= duration) return effectiveLoop ? 0 : duration - 0.001;
   //                                                       ↑ keep 0.001 so a Sprite with end=duration isn't switched off
   ```

3. **fadeOut on the final Sprite**: when recording, set `fadeOut={0}`, or the end of the video fades to transparent/dark. Users expect it to stop on a clear last frame, not fade out. When hand-writing HTML, it's recommended that final Sprites all use `fadeOut={0}`.

**Reference implementation**: the Stage in `assets/animations.jsx` / `scripts/render-video.js` both have the handshake built in. A hand-written Stage must implement `__recording` detection, or recording will definitely hit this pitfall.

**Verification**: after exporting the MP4, run `ffmpeg -ss 19.8 -i video.mp4 -frames:v 1 end.png` and check that the last 0.2 seconds are still the expected final frame, with no sudden switch to another scene.

## 14. 60fps video defaults to frame duplication: minterpolate has poor compatibility

**The pitfall**: 60fps MP4s generated by `convert-formats.sh` with `minterpolate=fps=60:mi_mode=mci...` couldn't be opened in some versions of macOS QuickTime / Safari (all black or refused outright). VLC / Chrome could open them.

**Root cause**: the H.264 elementary stream output by minterpolate contains certain SEI / SPS fields that some players have trouble parsing.

**Rules**:

- For 60fps by default, use the simple `fps=60` filter (frame duplication), which is widely compatible (QuickTime/Safari/Chrome/VLC can all open it)
- Enable high-quality frame interpolation explicitly with the `--minterpolate` flag, but you **must test it locally** in the target player before delivering
- The value of the 60fps label is **algorithmic recognition by upload platforms** (on Bilibili / YouTube, the 60fps tag gets streaming priority); for CSS animation, the actual perceived smoothness improvement is marginal
- Add `-profile:v high -level 4.0` to improve general H.264 compatibility

**`convert-formats.sh` now defaults to compatibility mode**. If you need high-quality interpolation, add the `--minterpolate` flag:
```bash
bash convert-formats.sh input.mp4 --minterpolate
```

## 15. The CORS trap of `file://` + external `.jsx`: single-file delivery must inline the engine

**The pitfall**: the animation HTML loaded the engine externally with `<script type="text/babel" src="animations.jsx"></script>`. Double-clicking to open it locally (`file://` protocol) → Babel Standalone fetches the `.jsx` via XHR → Chrome reports `Cross origin requests are only supported for protocol schemes: http, https, chrome, chrome-extension...` → the whole page goes black. It doesn't raise a `pageerror`, only a console error, so it's easy to misdiagnose as "the animation didn't trigger".

Starting an HTTP server won't necessarily save you either: when the machine has a global proxy, `localhost` also goes through the proxy and returns 502 / connection failures.

**Rules**:

- **Single-file delivery (HTML that works by double-clicking)** → `animations.jsx` must be **inlined** inside a `<script type="text/babel">...</script>` tag; don't use `src="animations.jsx"`
- **Multi-file projects (demoed by starting an HTTP server)** → external loading is fine, but state the `python3 -m http.server 8000` command clearly at delivery
- The test: are you delivering an "HTML file" or "a project directory with a server" to the user? Use inlining for the former
- The Stage component / animations.jsx is often 200+ lines; pasting it into an HTML `<script>` block is perfectly acceptable, so don't worry about size

**Minimal verification**: double-click the HTML you generated, and **don't** open it through any server. It only passes if Stage displays the animation's first frame correctly.

## 16. Inverted-color context across scenes: don't hard-code colors on in-frame elements

**The pitfall**: in a multi-scene animation, elements that **appear across scenes**, like `ChapterLabel` / `SceneNumber` / `Watermark`, had `color: '#1A1A1A'` (dark text) hard-coded in the component. The first 4 scenes had light backgrounds and were fine, but in the 5th scene with a black background, the "05" and the watermark simply vanished. No error, no check triggered, and key information became invisible.

**Rules**:

- **In-frame elements reused across multiple scenes** (chapter labels / scene numbers / timecodes / watermarks / copyright strips) **must not have hard-coded color values**
- Use one of three approaches instead:
  1. **`currentColor` inheritance**: the element only sets `color: currentColor`, and the parent scene container sets `color: computed-value`
  2. **invert prop**: the component accepts `<ChapterLabel invert />` to switch between dark and light manually
  3. **Auto-compute from the background**: `color: contrast-color(var(--scene-bg))` (a new CSS 4 API, or decide in JS)
- Before delivery, use Playwright to grab **a representative frame of each scene** and check by eye that all the "cross-scene elements" are visible

What makes this pitfall sneaky is that **there's no bug alarm**. Only the human eye or OCR can catch it.

## 17. Truly self-contained offline/no-CDN: inline React/Babel fully, and transpile the engine too

**The pitfall (the 2026-05 Miyou promo animation)**: the animation HTML used `<script src="https://unpkg.com/react...">` + `<script src=".../@babel/standalone">` via CDN. The machine had a global proxy, and during Playwright recording, chromium's connections to unpkg / Google Fonts all failed with `net::ERR_CONNECTION_CLOSED`:

1. React/ReactDOM didn't load → `window.React undefined`
2. Babel didn't load → the JSX in `<script type="text/babel">` ran as plain JS → `Unexpected token '<'`

After fixing React/Babel, we hit a second pitfall: **inlining the `animations.jsx` engine as a plain `<script>` still raised `Unexpected token '<'` → `window.Animations is undefined`**. Root cause: **the `animations.jsx` engine itself contains JSX** (the `Stage`/`Sprite` components `return (<div>...)`); it was originally designed to be loaded through Babel transpilation via `<script type="text/babel">`. Only the app code was transpiled and the engine was forgotten → the engine's JSX was never compiled.

**Rules** (when making a truly self-contained single file that "opens on double-click / works offline / can be recorded by Playwright"):

- **Inline React + ReactDOM locally**: `curl` download `react.production.min.js` (~10KB) + `react-dom.production.min.js` (~131KB) locally and inline them into `<script>`; don't use a CDN
- **Precompile with Babel at build time, ship no Babel at runtime**: use `@babel/standalone` (downloaded once, build-only) in node with `Babel.transform(src,{presets:['react']}).code` to turn JSX → `React.createElement`. **Both the app and the `animations.jsx` engine must go through the transform**; the engine contains JSX, and missing it will definitely raise `Unexpected token '<'`
- **Switch to system fonts**: the Google Fonts CDN also gets cut off by the proxy. Chinese animations use the system fonts `'PingFang SC'` (sans) / `'Songti SC'` (serif), with no network dependency. `document.fonts.ready` resolves immediately for system fonts, so recording doesn't stall
- **Inline image assets as base64**: a relative `<img src="png/x.png">` path renders under `file://`, but to be truly portable (no lost images when the file moves), inline it as a base64 data URL; convert large background images to JPEG to compress them before base64
- **Templatize the build**: leave `__REACT__/__REACTDOM__/__ASSETS__/__ENGINE__` tokens in the HTML template + a block of app source with `type="text/jsx-source"`; a node build script reads the tokens and injects them (vendor code as is, engine + app through Babel) → writes out the final single file. To change the animation, edit only the template and rerun the build

**Verification**: Playwright `page.evaluate(()=>({React:typeof window.React, Animations:typeof window.Animations}))`; both should be `object`. If either is `undefined` → the corresponding `<script>` threw an error (most likely untranspiled JSX).

**Relationship to pitfall #15**: #15 says "don't link an external `.jsx` with `src=` in a single file (file:// CORS)"; this pitfall goes further: even the **remote CDNs** for React/Babel/fonts **break on restricted networks**, so to be truly self-contained you must inline everything + transpile at build time.

## 18. [HyperFrames] CSS transition + class toggles are nondeterministic under seek rendering

CSS `transition` runs on the wall clock, not the timeline. In frame-by-frame seek rendering, every frame is an independent screenshot, and a transition's intermediate state depends on "how much wall-clock time has passed when seeking to this frame". It's completely nondeterministic: it may stay stuck at the start value forever, or stop randomly in the middle. Measured during the c3 migration (2026-07-17): `.watermark-br` used `transition: opacity 0.6s` + a class toggle, and its opacity misbehaved under seek rendering.

**Fix**: express every state change on the render path as a tween or a pure function of t. When migrating old demos, search the whole file for `transition:` and change each one into a lerp inside `render(t)`; in new compositions, don't write transitions from the start. Transitions on interactive states like hover don't matter (they aren't triggered during rendering).

## 19. [HyperFrames] Proxy tweens don't fire on the first frame: add `render(0)` manually

When you hook `render(t)` into a GSAP timeline with a proxy tween (the old-demo adapter route), `onUpdate` isn't necessarily called while the timeline sits at t=0, so the first frame may be the HTML's static uninitialized state rather than the `render(0)` frame.

**Fix**: after registering the timeline, manually call `render(0)` once synchronously. For the full recipe, see `references/hyperframes-backend.md`.

## 20. [HyperFrames] The contrast gate conflicts with dark cinematic style: use `--no-contrast`, the other four gates must have 0 errors

The contrast gate in `npm run check` checks all text against WCAG AA 4.5:1. In dark cinematic designs, watermarks, mono labels, and decorative text at 16-40% opacity are **deliberately** low contrast (part of the cinematic feel), so they produce errors en masse, and the framework has no per-element exemption mechanism. In c3, all 42 measured contrast errors were by design.

**Fix**: for dark cinematic output use `npx hyperframes check --no-contrast`; the lint/runtime/layout/motion gates must still have 0 errors. **Don't skip contrast for light-background informational output**: errors in that scenario are usually real readability problems (for the hard readability floor, see core rule 5 in SKILL.md).

## 21. [HyperFrames/GSAP] The immediateRender phantom of fromTo: elements appear seconds early

GSAP's `fromTo()` defaults to `immediateRender: true`: it renders the from state onto the element when the timeline is built. If the from state itself is visible (`autoAlpha > 0`), the element appears in the frame before its tween starts. "Short bursts of effects" like sparks, click rings, ripples, and dust are the most prone to this (in B00 we measured 4 occurrences at once: effects hung in the frame for several seconds before the moment they were meant to land).

**Fix**: explicitly add `immediateRender: false` to every `fromTo()` whose from state is visible; or switch to "set initially hidden + to". How to check yourself: after rendering, pull the opening frame of each scene and look for "effect elements that shouldn't be there".

## 22. [Camera] Blurry text in 3D/magnified mode: magnify with CSS zoom, not transform scale

**Symptom**: pushing in on the page with `transform: scale()` (especially in 3D perspective mode) makes text blurry; the higher the magnification, the blurrier, and above 2x it's undeliverable.

**Root cause**: Chromium rasterizes at the element's **layout size**, then enlarges the bitmap. scale only enlarges the bitmap.

**Solution** (shotcraft precedent, the most expensive knowledge in the whole library): magnify the camera layer with the **CSS `zoom` property** (layout-level scaling that re-lays out and rasterizes at the enlarged size, so text is sharp at any magnification). For coordinate conversion and the full formulas, see `camera-language.md` §3.4 and `gsap-recipes.md` §9.2. Note: `zoom` triggers a re-layout every frame and is the only legitimate exception to "no tweening layout properties", allowed only on the `#world` camera layer; slower render times under offline frame-by-frame rendering are normal, and output quality comes first. Supporting measures: full-page screenshots at 2x or more, plus separate 4x slices of close-ups crossfaded in over 6f during the push-in.

## 23. [Camera] perspective broken by an intermediate layer: 3D instantly goes flat

**Symptom**: `perspective` + `preserve-3d` are set up, but the render has no 3D feel at all; all layers lie flat.

**Root cause**: **any intermediate layer** between `#camera` and the 3D child elements that has any of `overflow: hidden`, `filter`, `opacity < 1`, or `clip-path` creates a new stacking context and flattens preserve-3d.

**Solution**: in 3D mode, apply filter/opacity effects only to the **innermost elements**; check every layer in the container chain for the four kinds of properties above. Troubleshooting mantra: from `#camera` to the problem element, run `getComputedStyle` on every layer in between and check these four.

## 24. [Camera] Pan exposes the edges: blank space outside the canvas shows during a pan

**Symptom**: white or black edges show at the edge of the frame when the camera pans/sweeps.

**Root cause**: `#world` is only as big as the viewport, so it goes out of bounds as soon as the camera moves.

**Solution**: extend `#world` on all sides with bleed ≥ the maximum pan amplitude + an 8% safe margin (camera-language §3.3). Background/atmosphere layers must fill the bleed area too, not just the viewport. Self-check: seek the timeline to both endpoints of each pan, take screenshots, and look at all four edges.

## Quick self-check list (5 seconds before starting)

- [ ] Does every parent of a `position: absolute` element have `position: relative`?
- [ ] Do all the special characters in the animation (`␣` `⌘` `emoji`) exist in the font?
- [ ] Does the Grid/Flex template count match the length of the JS data?
- [ ] Is there a cross-fade between scene changes, with no pure blank >0.3s?
- [ ] Is DOM measurement code wrapped in `document.fonts.ready.then()`?
- [ ] Is `render(t)` pure, or does it have a clear reset mechanism?
- [ ] Is frame 0 the complete initial state, not blank?
- [ ] Is there no "fake chrome" decoration in the frame (progress bar/timecode/bottom credit strip colliding with the Stage scrubber)?
- [ ] Does the animation's first tick frame synchronously set `window.__ready = true`? (built into animations.jsx; add it yourself in hand-written HTML)
- [ ] Does Stage detect `window.__recording` and force loop=false? (required in hand-written HTML)
- [ ] Is the final Sprite's `fadeOut` set to 0 (so the video ends on a clear frame)?
- [ ] Do 60fps MP4s default to frame-duplication mode (compatibility), adding `--minterpolate` only for high-quality interpolation?
- [ ] After export, did you pull frame 0 + the last frame to verify they're the animation's initial/final states?
- [ ] For a specific brand (Stripe/Anthropic/Lovart/...): did you go through the whole "Brand Asset Protocol" (core rule 2 in SKILL.md, five steps)? Did you write `brand-spec.md`?
- [ ] For single-file HTML delivery: is `animations.jsx` inlined, not `src="..."`? (an external .jsx under file:// goes black from CORS)
- [ ] Do elements that appear across scenes (chapter labels/watermarks/scene numbers) have no hard-coded colors? Are they visible on every scene's background?
- [ ] For offline/truly self-contained: React+ReactDOM inlined locally, **both the app and the `animations.jsx` engine transpiled with Babel**, system fonts? (see pitfall #17; the engine contains JSX, and missing the transpile will definitely raise `Unexpected token '<'`)
- [ ] [HyperFrames] No CSS `transition` on the render path? All state changes are tweens or pure functions of t? (pitfall #18)
- [ ] [HyperFrames] Added `render(0)` after registering in proxy-tween scenarios? (pitfall #19)
- [ ] [HyperFrames] Did check pass? For dark cinematic style, `--no-contrast`, with 0 errors on the other four gates? (pitfall #20)
- [ ] [HyperFrames/GSAP] Did every `fromTo()` with a visible from state get `immediateRender:false`? (pitfall #21, 4 phantoms measured in B00)
- [ ] [Camera] Do 3D/magnified close-ups use CSS `zoom`, not blurry scale enlargement? (pitfall #22)
- [ ] [Camera] No overflow/filter/opacity/clip-path on the intermediate layers from `#camera` to the 3D elements? (pitfall #23)
- [ ] [Camera] Is `#world` extended with bleed, with no blank edges in screenshots at the pan endpoints? (pitfall #24)
