# App / iOS Prototype Rules · Complete Operating Manual

> The complete App / iOS prototype manual that SKILL.md routes to here: architecture choice, image sourcing channels and code, the AppPhone JSX skeleton, ios_frame usage, taste anchors.
> For the three technical red lines of single-file inline React (style objects must have unique names, such as `const terminalStyles = {}`; share components between multiple babel scripts with `Object.assign(window, …)`; don't use `scrollIntoView`) and the pinned versions, see `references/react-setup.md`, and read it before writing. The three-directions gate still applies (`references/directions.md`); when three versions of phones sit side by side, add `--ignore-layout` to compare.


When making iOS/Android/mobile app prototypes (triggers: "app prototype", "iOS mockup", "mobile app", "make an app"), the four rules below **override** the general placeholder principle. An app prototype is a live demo, and static staged shots and off-white placeholder cards aren't convincing.

### 0. Architecture choice (must be decided first)

**Default to single-file inline React**: write all the JSX/data/styles directly into the `<script type="text/babel">...</script>` tag of the main HTML, and **don't** load externally with `<script src="components.jsx">`. Reason: under the `file://` protocol, the browser blocks external JS as cross-origin, and forcing the user to start an HTTP server violates the prototype intuition of "double-click and it opens". Local images must be embedded as base64 data URLs; don't assume there's a server.

**Split into external files only in two cases**:
- (a) A single file >1000 lines is hard to maintain → split into `components.jsx` + `data.js`, with clear delivery instructions (the `python3 -m http.server` command + the URL to visit)
- (b) Multiple subagents need to write different screens in parallel → `index.html` + a separate HTML per screen (`today.html`/`graph.html`...), aggregated with iframes, with every screen also a self-contained single file

**Quick selection**:

| Scenario | Architecture | Delivery |
|------|------|----------|
| One person making a 4-6 screen prototype (the common case) | Single-file inline | One `.html`, double-click to open |
| One person making a large app (>10 screens) | Multiple jsx + server | Include the startup command |
| Multiple agents in parallel | Multiple HTML + iframe | `index.html` aggregates; each screen opens on its own |

### 1. Find real images first; don't leave placeholders sitting there

By default, proactively fetch real images to fill things in. Don't draw SVGs, don't leave off-white cards sitting there, and don't wait for the user to ask. Common channels:

| Scenario | Preferred channel |
|------|---------|
| Art/museum/historical content | Wikimedia Commons (public domain), Met Museum Open Access, Art Institute of Chicago API |
| General lifestyle/photography | Unsplash, Pexels (royalty-free) |
| Assets the user already has locally | `~/Downloads`, the project's `_archive/`, or an asset library the user has configured |

Avoiding pitfalls when downloading from Wikimedia (curl on this machine blows up on TLS through the proxy; Python urllib works directly):

```python
# A compliant User-Agent is a hard requirement, or you get 429
UA = 'ProjectName/0.1 (https://github.com/you; you@example.com)'
# Use the MediaWiki API to look up the real URL
api = 'https://commons.wikimedia.org/w/api.php'
# action=query&list=categorymembers to fetch a series in bulk / prop=imageinfo+iiurlwidth to get the thumburl at a given width
```

**Only** when every channel fails / the copyright is unclear / the user explicitly asks should you fall back to an honest placeholder (and still don't draw bad SVGs).

**Real-image honesty test** (key): before fetching an image, ask yourself: "If this image were removed, would information be lost?"

| Scenario | Judgment | Action |
|------|------|------|
| Covers in an article/essay list, a scenic header on a profile page, a decorative banner on a settings page | Decoration, no intrinsic connection to the content | **Don't add it**. Adding it is AI slop, the same as a purple gradient |
| Portraits for museum/people content, the physical item on a product detail page, the place on a map card | The content itself, intrinsically connected | **Must add it** |
| A very faint texture behind a graph/visualization | Atmosphere, subordinate to the content and not stealing the show | Add it, but opacity ≤ 0.08 |

**Counterexamples**: pairing a text essay with an Unsplash "inspiration image", pairing a notes app with stock photo models. Both are AI slop. Permission to fetch real images isn't a license to abuse them.

### 2. Delivery form: default to "laid out flat + interactive"; don't ask the user

An iOS app prototype has **only one default delivery form; don't ask the user "do you want it laid out flat or interactive"**: **lay out 4-6 main screens flat, and make every one interactive**. You see the whole picture at a glance (several iPhones side by side), and every phone can switch tabs and do basic operations on screen (expand, switch, select, open a sheet). Deliver both benefits at once; don't make the user choose.

| Dimension | Default approach |
|------|---------|
| **Number of screens** | Lay out **4-6 main screens** flat (covering the app's core features, not a random handful). If there are more than 6, pick the 4-6 most important; the rest can be reached within a single phone via tabs/navigation |
| **Layout** | A composed presentation board, not a row of same-size phones (see "Presentation board" below); each phone has a one-line label next to it saying which screen it is |
| **Per-phone interaction** | Each phone is an independent mini state machine: the tab bar switches, buttons/cards/toggles on screen are clickable, and modals can pop up. Not static staged shots |

**Only two special cases depart from the default** (take them only if the user says so explicitly; otherwise always use the default):
- The user explicitly says "just static screenshots / doesn't need to be clickable / just want to see the layout" → fall back to a purely static overview (each phone renders only `ScreenComponent`, with no state machine attached)
- The user explicitly says "just demo one flow / walk through onboarding / single-phone demo" → a single `AppPhone` runs the complete flow

**Default skeleton** (several phones laid out flat, each with its own stateful AppPhone):

```jsx
// Each phone = an independent state machine, starting on the main screen it's responsible for
function AppPhone({ initial }) {
  const [screen, setScreen] = React.useState(initial);
  const [modal, setModal] = React.useState(null);
  // Render the matching ScreenComponent by screen, passing callbacks such as onTabChange/onOpen/onClose/onToggle
  return (
    <IosFrame>
      <ScreenComponent
        screen={screen}
        onTabChange={setScreen}
        onOpen={setModal}
        onClose={() => setModal(null)}
      />
    </IosFrame>
  );
}

// Laid out flat: 4-6 phones side by side, each with initial on a different main screen
<div style={{display: 'flex', gap: 32, flexWrap: 'wrap', padding: 48, alignItems: 'flex-start'}}>
  {mainScreens.map(s => (
    <div key={s.id}>
      <div style={{fontSize: 13, color: '#666', marginBottom: 8, fontStyle: 'italic'}}>{s.label}</div>
      <AppPhone initial={s.id} />
    </div>
  ))}
</div>
```

Screen components take callback props (`onTabChange`, `onOpen`, `onClose`, `onToggle`, `onAnnotation`) and don't hard-code state. TabBars, buttons, work cards, and toggles get `cursor: pointer` + hover feedback. Each phone starts on a different main screen, but they can reach each other through tab switches: the flat layout gives the whole picture, and clicking gives depth.

The flex above is just the minimal skeleton that runs; replace it with a presentation board composition before delivery.

#### Presentation board: don't line the phones up in a row

In blind picks, for app prototypes in any direction, whenever five or six same-size phones were spaced evenly in a row, the user's verdict was "too regular, too boring". No matter how good the screens themselves are, the first thing you see is a regular table. The presentation board is the first poster of this direction, and it needs design of its own:

| Technique | How | Suits |
|---|---|---|
| Primary and secondary | Enlarge the screen that best represents this app to 1.2–1.4x and put it at the visual center; shrink the rest and stagger them around it at uneven heights | Applies almost everywhere; first choice |
| Flow chaining | Arrange in the order of the user's real task, with thin lines between screens from "where they tapped" to "which screen it went to", and annotations written beside the lines | Apps with one main task flow (ordering, logging, travel mode) |
| Detail close-up | Next to one screen, place a 2–3x close-up of a key component: a signature interaction, a data visualization, a carefully crafted control | There's one detail worth remembering |
| Context background | The board's background uses the app's context of use: real images, subject colors, its materials, instead of a white canvas | The subject has a strong setting (outdoors, kitchen, night) |
| Board layout | The board has its own title area: app name, a one-line positioning statement, screen labels, with fonts and colors from this direction's own system | Applies everywhere |

There are only three rules: the board's background color and fonts follow this direction (dark directions use a dark board, not a uniform white canvas); every phone is still clickable; screens aren't shrunk until the text is illegible (each phone at least 300px wide). The board compositions of the three directions should also differ; this is the most easily overlooked difference among the three directions.

### 3. Run real click tests before delivery

Static screenshots only show the layout; interaction bugs only surface when you click through. Use Playwright to run 3 minimal click tests: enter a detail view / a key annotation point / a tab switch. Check that `pageerror` is 0 before delivering. Playwright can be invoked with `npx playwright`, or via the global install path on this machine (`npm root -g` + `/playwright`).

### 4. Taste anchors (pursue list, the preferred fallback)

When there's no design system, head in these directions by default to avoid running into AI slop:

| Dimension | Preferred | Avoid |
|------|------|------|
| **Type** | Choose the display face by subject (pairing table in `references/typography.md`), `-apple-system` for body | SF Pro or Inter everywhere: too much like the system default |
| **Color** | Sample colors from the product's subject and real images (color derivation protocol), with one main color running throughout | Multicolor clusters (unless the data truly has ≥3 categorical dimensions) |
| **Information density · restrained** (default) | One less container, one less border, one less **decorative** icon; leave the content room to breathe | Every card gets a meaningless icon + tag + status dot |
| **Information density · high-density** (exception) | When the product's core selling point is "intelligence / data / context awareness" (AI tools, Dashboards, Trackers, Copilots, Pomodoro timers, health monitoring, bookkeeping), each screen needs **at least 3 visible pieces of product-differentiating information**: non-decorative data, conversation/reasoning snippets, state inferences, contextual links | Just one button and one clock: the AI's intelligence doesn't come across, and it's no different from an ordinary app |
| **Signature detail** | Leave one "screenshot-worthy" texture: a very faint oil-painting ground / a serif italic pull quote / a full-screen recording waveform on black | Even effort everywhere, so everything ends up flat |

**Two principles apply at the same time**:
1. Taste = one detail at 120%, everything else at 80%. Not everything is refined; it's refined enough in the right places
2. Subtraction is a fallback, not a universal law. When the product's core selling point needs information density to back it up (AI / data / context-aware products), addition takes priority over restraint. See "Information density types" below for details

### 5. iOS device frames must use `assets/ios_frame.jsx`: no hand-written Dynamic Island / status bar

When making an iPhone mockup, you are **hard-bound** to `assets/ios_frame.jsx`. It's the standard shell already aligned to the exact iPhone 15 Pro specs: bezel, Dynamic Island (124×36, top:12, centered), status bar (time/signal/battery, clearing the island on both sides, vertically centered on the island's midline), Home Indicator, and the content area's top padding are all handled.

**Don't write any of the following yourself** in your HTML:
- `.dynamic-island` / `.island` / `position: absolute; top: 11/12px; width: ~120; a centered black rounded rectangle`
- `.status-bar` with hand-written time/signal/battery icons
- `.home-indicator` / a bottom home bar
- The rounded outer frame of an iPhone bezel + black stroke + shadow

Writing these yourself will hit positioning bugs 99% of the time: the status bar's time/battery gets squeezed by the island, or the content top padding is miscalculated so the first line of content sits under the island. The iPhone 15 Pro's notch is a **fixed 124×36 pixels**, and the usable width left for the status bar on either side is narrow, not something you can estimate out of thin air.

**Usage (strictly three steps)**:

```jsx
// Step 1: Read this skill's assets/ios_frame.jsx (path relative to this SKILL.md)
// Step 2: Paste the whole iosFrameStyles constant + the IosFrame component into your <script type="text/babel">
// Step 3: Wrap your own screen component in <IosFrame>...</IosFrame>, and don't touch the island/status bar/home indicator
<IosFrame time="9:41" battery={85}>
  <YourScreen />  {/* Content renders starting at top 54, with the bottom left for the home indicator; you don't need to handle it */}
</IosFrame>
```

**Exception**: bypass it only when the user explicitly asks to "pretend it's the notch of a non-Pro iPhone 14", "make Android, not iOS", or "a custom device form". In that case, read the corresponding `android_frame.jsx` or modify the constants in `ios_frame.jsx`; **don't** start a separate island/status bar in the project HTML.
