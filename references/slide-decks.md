# Slide Decks: HTML slide production standards

Making slides is a high-frequency scenario in design work. This document explains how to make HTML slides well, from choosing an architecture and designing single pages to the full path for PDF/PPTX export.

**What this skill covers**:
- **HTML presentation version (the base output, always done by default)** → an independent HTML per page + `assets/deck_index.html` aggregation, with keyboard page-turning and full-screen presenting in the browser
- HTML → PDF export → `scripts/export_deck_pdf.mjs` / `scripts/export_deck_stage_pdf.mjs`
- HTML → editable PPTX export → `references/editable-pptx.md` + `scripts/html2pptx.js` + `scripts/export_deck_pptx.mjs` (requires the HTML to be written to the 4 hard constraints)

> **⚠️ HTML is the base; PDF/PPTX are derivatives.** Whatever format the final delivery is, you **must** first make the aggregated HTML presentation version (`index.html` + `slides/*.html`); it is the "source" of the slide work. PDF/PPTX are snapshots exported from the HTML with one command.
>
> **Why HTML first**:
> - It works best at the live talk or demo (full screen straight on the projector / shared screen, keyboard page-turning, no dependency on Keynote/PPT software)
> - During development each page can be opened and verified on its own with a double-click, without rerunning the export every time
> - It is the single upstream for PDF/PPTX export (avoiding the endless loop of "only discovering after export that the HTML needs changes, then exporting again")
> - The deliverable can be a pair, "HTML + PDF" or "HTML + PPTX", and the recipient can use whichever they prefer
>
> 2026-04-22 moxt brochure, measured: after finishing 13 pages of HTML + the index.html aggregation, `export_deck_pdf.mjs` exported the PDF with one command, zero changes. The HTML version itself is a deliverable that can be presented directly in the browser.

---

## 🛑 Confirm the delivery format before you start (the hardest checkpoint)

**This decision comes before "single file or multiple files".** Measured on a real client deck (2026-04-20, for an options-investing peer advisory group): **not confirming the delivery format before starting = 2-3 hours of rework.**

### Decision tree (HTML-first architecture)

Every delivery starts from the same set of aggregated HTML pages (`index.html` + `slides/*.html`). The delivery format only determines **the writing constraints on the HTML** and **the export command**:

```
[Always the default · required] Aggregated HTML presentation version (index.html + slides/*.html)
   │
   ├── Only browser presenting / local HTML archive   → Already done at this point, maximum HTML visual freedom
   │
   ├── Also needs PDF (print / send to a group / archive)  → Run export_deck_pdf.mjs, one-click output
   │                                          HTML written freely, no visual constraints
   │
   └── Also needs editable PPTX (colleagues will edit text)  → Write to the 4 hard constraints from the first line of HTML
                                              Run export_deck_pptx.mjs, one-click output
                                              Gives up gradients / web components / complex SVG
```

### Kickoff script (copy and use as is)

> Whether the final delivery is HTML, PDF or PPTX, I'll first make an aggregated HTML version you can switch through and present in the browser (`index.html` plus keyboard page-turning). This is always the default base output. On top of that, I'll ask whether you want an extra PDF / PPTX snapshot.
>
> Which export format do you need?
> - **HTML only** (presenting/archiving) → complete visual freedom
> - **Also PDF** → same as above, plus one export command
> - **Also editable PPTX** (colleagues will edit text in PPT) → I have to write to the 4 hard constraints from the first line of HTML, which gives up some visual capability (no gradients, no web components, no complex SVG).

### Why "needing PPTX means following the 4 hard constraints from the start"

PPTX being editable depends on `html2pptx.js` being able to translate the DOM element by element into PowerPoint objects. It needs **4 hard constraints**:

1. body fixed at 960pt × 540pt (matching `LAYOUT_WIDE`, 13.333″ × 7.5″, not 1920×1080px)
2. All text wrapped in `<p>`/`<h1>`-`<h6>` (no text directly inside a div, no `<span>` carrying main text)
3. `<p>`/`<h*>` themselves can't have background/border/shadow (put it on an outer div)
4. `<div>` can't use `background-image` (use an `<img>` tag)
5. No CSS gradients, no web components, no complex SVG decoration

**This skill's default HTML has a lot of visual freedom**: lots of spans, nested flex, complex SVG, web components (like `<deck-stage>`), CSS gradients. **Almost none of it naturally passes html2pptx's constraints** (measured: feeding visually driven HTML straight into html2pptx, the pass rate is < 30%).

### Cost comparison of the two real paths (a real pitfall, 2026-04-20)

| Path | Method | Result | Cost |
|------|------|------|------|
| ❌ **Write HTML freely first, rescue the PPTX afterwards** | Single-file deck-stage + lots of SVG/span decoration | For an editable PPTX only two paths remain:<br>A. Hand-write a few hundred lines of pptxgenjs with hardcoded coordinates<br>B. Rewrite 17 pages of HTML into the Path A format | 2-3 hours of rework, and the hand-written version has a **perpetual maintenance cost** (change one character in the HTML and the PPTX has to be synced by hand again) |
| ✅ **Write to the Path A constraints from the first step** | An independent HTML per page + 4 hard constraints + 960×540pt | One command exports a 100% editable PPTX, and it can also be presented full screen in the browser (Path A HTML is standard browser-playable HTML) | 5 extra minutes while writing the HTML thinking about "how to wrap the text in `<p>`", zero rework |

### What about mixed deliveries

The user says "I want HTML presenting **and** an editable PPTX": **this isn't mixed**, the PPTX requirement covers the HTML requirement. HTML written to Path A can itself be presented full screen in the browser (just add a `deck_index.html` stitcher). **No extra cost.**

The user says "I want PPTX **and** animation / web components": **this is a real conflict**. Tell the user: an editable PPTX means giving up these visual capabilities. Let them make the trade-off; don't quietly go for a hand-written pptxgenjs approach (it becomes perpetual maintenance debt).

### What if you only learn afterwards that PPTX is needed (emergency rescue)

In rare cases: the HTML is already written when you discover PPTX is needed. The recommended route is the **fallback process** (full explanation at the end of `references/editable-pptx.md`, "Fallback: an existing visual draft, but the user insists on an editable PPTX"):

1. **First choice: deliver PDF instead** (100% of the visuals kept, cross-platform, the recipient can view and print it). If the recipient's actual need is "presenting/archiving", PDF is the best deliverable
2. **Second choice: the AI rewrites an editable HTML version using the visual draft as the blueprint** → export an editable PPTX. This keeps the design decisions about color/layout/copy, and gives up visual capabilities like gradients, web components and complex SVG
3. **Not recommended: rebuilding by hand-writing pptxgenjs**. Positions, fonts and alignment all need manual tuning, the maintenance cost is high, and every later one-character change to the HTML has to be synced by hand again

Always tell the user the options and let them decide. **Never start hand-writing pptxgenjs as your first reaction**; it's the last-resort fallback.

---

## 🛑 Before batch production: make a 2-page showcase first to set the grammar

**Whenever a deck has ≥ 5 pages, never write straight from page 1 to the last page.** The correct order, validated in practice on the 2026-04-22 moxt brochure:

1. Pick the **2 page types with the biggest visual difference** to make a showcase first (e.g. "cover" + "mood/quote page", or "cover" + "product showcase page")
2. Take screenshots and have the user confirm the grammar (masthead / fonts / color / spacing / structure / the Chinese-English bilingual ratio)
3. Once the direction passes, batch out the remaining N-2 pages, each reusing the established grammar
4. When everything is done, assemble the HTML aggregation + the PDF / PPTX derivatives together

**Why**: writing all 13 pages straight through → the user says "the direction is wrong" = 13 pages of rework. Making a 2-page showcase first → wrong direction = 2 pages of rework. Once the visual grammar is established, the decision space for the remaining N pages narrows sharply, leaving only "how to fit the content in".

**Principle for choosing showcase pages**: pick the two pages with the most different visual structures. If these two pass = every intermediate state will pass too.

| Deck type | Recommended showcase page pair |
|-----------|---------------------|
| B2B brochure / product marketing | Cover + content page (philosophy/emotional page) |
| Brand launch | Cover + product feature page |
| Data report | Big data visual page + analysis conclusion page |
| Tutorial courseware | Chapter cover page + specific knowledge point page |

---

## 📐 Publication grammar template (measured on moxt, reusable)

Suited to B2B brochure / product marketing / long report decks. Reusing this structure on every page = 13 pages fully visually consistent, 0 rework.

### Per-page skeleton

```
┌─ masthead (top strip + rule) ─────────────┐
│  [logo 22-28px] · A Product Brochure                Issue · Date · URL │
├──────────────────────────────────────────┤
│                                          │
│  ── kicker (short green dash + uppercase label) │
│  CHAPTER XX · SECTION NAME                 │
│                                          │
│  H1 (Chinese in Noto Serif SC 900)        │
│  Key words alone in the brand color       │
│                                          │
│  English subtitle (Lora italic, subtitle) │
│  ─────────── divider ──────────           │
│                                          │
│  [Content: two columns 60/40 / 2x2 grid / list] │
│                                          │
├──────────────────────────────────────────┤
│ section name                     XX / total │
└──────────────────────────────────────────┘
```

### Style conventions (copy them as is)

- **H1**: Chinese in Noto Serif SC 900, font size 80-140px depending on the amount of information, key words alone in the brand color (don't pile color on all the text)
- **English subtitle**: Lora italic 26-46px, with brand signature words (like "AI team") in bold + brand-color italic
- **Body text**: Noto Serif SC 17-21px, line-height 1.75-1.85
- **Accent highlights**: mark keywords in the body with bold brand color, no more than 3 per page (too many and they lose their role as anchors)
- **Background**: warm off-white #FAFAFA + an extremely faint radial-gradient noise (`rgba(33,33,33,0.015)`) for a paper feel

### The visual star must vary

If all 13 pages are "text + one screenshot", it's too monotonous. **Rotate the type of visual star on each page**:

| Visual type | Suitable section |
|---------|---------------|
| Cover typography (big type + masthead + pillar) | Home page / chapter cover |
| Single-character portrait (one oversized momo, etc.) | Introducing a single concept/character |
| Multi-character group photo / avatar cards side by side | Team / user cases |
| Timeline cards in progression | Showing "long-term relationships", "evolution" |
| Knowledge graph / connected node diagram | Showing "collaboration", "flow" |
| Before/After comparison cards + an arrow in the middle | Showing "change", "difference" |
| Product UI screenshot + outlined device frame | Showing a specific feature |
| big-quote (half-page big type) | Mood page / question page / quotation page |
| Real headshot + quote card (2×2 or 1×4) | User testimonials / usage scenarios |
| Big-type back cover + URL pill button | CTA / ending |

---

## ⚠️ Common pitfalls (lessons from moxt in practice)

### 1. Emoji don't render in Chromium / Playwright exports

Chromium doesn't ship a color emoji font by default, so with `page.pdf()` or `page.screenshot()` emoji show up as empty boxes.

**Fix**: replace them with Unicode text symbols (`✦` `✓` `✕` `→` `·` `—`), or switch to plain text ("Email · 23" rather than "📧 23 emails").

### 2. `export_deck_pdf.mjs` errors with `Cannot find package 'playwright'`

Cause: ESM module resolution looks for `node_modules` upward from where the script lives. The script is in the pack's `scripts/` folder; if the pack has no `node_modules` it can't resolve.

**Fix (dstack)**: run `npm ci` once in `/workspace/dstack` (local `node_modules`, Playwright pinned), then run the script from its own folder. Or copy the script into the deck project directory (e.g. `brochure/build-pdf.mjs`), run `npm install playwright pdf-lib` at the project root, then `node build-pdf.mjs --slides slides --out output/deck.pdf`.

### 3. Screenshots taken before Google Fonts finish loading → Chinese shows in the system default sans

Before a Playwright screenshot/PDF, wait at least `wait-for-timeout=3500` for the webfont to download and paint. Or self-host the fonts in `shared/fonts/` to reduce the network dependency.

### 4. Unbalanced information density: content pages stuffed too full

The first version of the moxt philosophy page used 2×2 = 4 paragraphs + 3 tenets at the bottom = 7 blocks of content, cramped and repetitive. After changing it to 1×3 = 3 paragraphs, the sense of breathing room came right back.

**Fix**: keep each page to "1 core message + 3-4 supporting points + 1 visual star", and split onto a new page if it goes over. **Less is more**: the audience looks at a page for 10 seconds, and 1 takeaway is easier to remember than 4.

---

## 🛑 Settle the architecture first: single file or multiple files?

**This choice is the first step in making slides, and getting it wrong means hitting the same pitfalls over and over. Read this whole section before you start.**

### Comparing the two architectures

| Dimension | Single file + `deck_stage.js` | **Multiple files + `deck_index.html` stitcher** |
|------|--------------------------|--------------------------------------|
| Code structure | One HTML, every slide is a `<section>` | An independent HTML per page, `index.html` stitches them with iframes |
| CSS scope | ❌ Global, one page's styles can affect every page | ✅ Naturally isolated, each iframe is its own world |
| Verification granularity | ❌ Needs JS goTo to switch to a page | ✅ Double-click a single page file to view it in the browser |
| Parallel development | ❌ One file, multiple agents editing will conflict | ✅ Multiple agents can work on different pages in parallel, zero-conflict merge |
| Debugging difficulty | ❌ One CSS error and the whole deck breaks | ✅ An error on one page only affects that page |
| Embedded interaction | ✅ Sharing state across pages is easy | 🟡 iframes need postMessage between them |
| Print to PDF | ✅ Built in | ✅ The stitcher iterates over iframes on beforeprint |
| Keyboard navigation | ✅ Built in | ✅ Built into the stitcher |

### Which one? (decision tree)

```
│ Q: How many pages is the deck expected to have?
├── ≤10 pages, needs in-deck animation or cross-page interaction, pitch deck → single file
└── ≥10 pages, academic lecture, courseware, long deck, multiple agents in parallel → multiple files (recommended)
```

**Take the multi-file path by default**. It isn't "the alternative"; it's **the main path for long decks and team collaboration**. The reason: every advantage of the single-file architecture (keyboard navigation, printing, scale) is also available with multiple files, while the scope isolation and verifiability of multiple files can't be added back to a single file.

### Why is this rule so strict? (a record of real incidents)

The single-file architecture once hit four pitfalls in a row while making the AI psychology lecture deck:

1. **CSS specificity override**: `.emotion-slide { display: grid }` (specificity 10) beat `deck-stage > section { display: none }` (specificity 2), so every page rendered at once, stacked on top of each other.
2. **Shadow DOM slot rules overridden by outer CSS**: `::slotted(section) { display: none }` couldn't hold off the outer rule's override, and the sections refused to hide.
3. **localStorage + hash navigation race**: after a refresh it didn't jump to the hash position, but stopped at the old position recorded in localStorage.
4. **High verification cost**: you had to `page.evaluate(d => d.goTo(n))` to capture a page, twice as slow as going straight to `goto(file://.../slides/05-X.html)`, and it often errored.

The root cause of all of them is **a single global namespace**; the multi-file architecture eliminates these problems at the physical level.

---

## Path A (default): multi-file architecture

### Directory structure

```
MyDeck/
├── index.html              # Copied from assets/deck_index.html, edit MANIFEST
├── shared/
│   ├── tokens.css          # Shared design tokens (palette/font sizes/common chrome)
│   └── fonts.html          # <link> loading Google Fonts (included on every page)
└── slides/
    ├── 01-cover.html       # Every file is a complete 1920×1080 HTML
    ├── 02-agenda.html
    ├── 03-problem.html
    └── ...
```

### Template skeleton for each slide

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>P05 · Chapter Title</title>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
<link rel="stylesheet" href="../shared/tokens.css">
<style>
  /* Styles unique to this page. No class name you use here will pollute other pages. */
  body { padding: 120px; }
  .my-thing { ... }
</style>
</head>
<body>
  <!-- 1920×1080 content (locked by the body width/height in tokens.css) -->
  <div class="page-header">...</div>
  <div>...</div>
  <div class="page-footer">...</div>
</body>
</html>
```

**Key constraints**:
- `<body>` is the canvas; lay out directly on it. Don't wrap it in a `<section>` or any other wrapper.
- `width: 1920px; height: 1080px` is locked by the `body` rule in `shared/tokens.css`.
- Link `shared/tokens.css` for the shared design tokens (palette, font sizes, page-header/footer, etc.).
- Each page writes its own font `<link>` (importing fonts separately isn't expensive, and it guarantees every page can be opened on its own).

### The stitcher: `deck_index.html`

**Copy it straight from `assets/deck_index.html`**. You only need to change one thing: the `window.DECK_MANIFEST` array, listing every slide file name and a human-readable label in order:

```js
window.DECK_MANIFEST = [
  { file: "slides/01-cover.html",    label: "Cover" },
  { file: "slides/02-agenda.html",   label: "Agenda" },
  { file: "slides/03-problem.html",  label: "Problem Statement" },
  // ...
];
```

The stitcher has built in: keyboard navigation (←/→/Home/End/number keys/P to print), scale + letterbox, a counter in the bottom right, localStorage memory, hash page jumps, and print mode (iterating over iframes to output the PDF page by page).

#### Two overview modes (adaptive + pitfall-proof, rewritten 2026-06)

Opening the deck goes into the **overview** by default, and when the user hasn't specified one it's chosen at random by the second: **grid 60% / infinite gallery 40%** (can be pinned with the URL `?ov=grid|gallery` or `window.DECK_OVERVIEW='grid'|'gallery'`).

- **Grid (the default workhorse)**: uses **iframes to render the real child pages** (sharp, what you see is what you get, no thumbnails needed). **Adaptive**: if they fit on one screen → tilted diagonally, centered and filling the screen; if there are too many pages to fit → cards keep a comfortable size and **scroll vertically** (never cram dozens of pages onto one screen shrunk to postage stamps).
- **Infinite gallery**: every page is **tiled seamlessly and infinitely + drifting slowly + with a subtle breathing scale**, one tile containing all the pages (shuffled, repeating only after every page has been seen). There are many tiles, so it **must use `<img>` thumbnails** to carry the performance (see below), falling back to iframes when there's no thumb.

🛑 **Three hard constraints from real practice (must read before changing this file, or you'll repeat the same mistakes)**:
1. **Never build the overview wall as a card wall with `transform-style: preserve-3d`**. In a preserve-3d 3D scene, the browser's hit testing for "cards receding into the distance" (the top row) is unreliable → the top row can't be clicked, the middle row works sometimes. **The right answer**: make the whole wall **a single plane tilted in 3D** (no preserve-3d), all cards coplanar, so clicks back-project onto one plane → reliable. For hover use 2D `scale`, not `translateZ`.
2. **Adapt to any number of pages**: with a fixed column count + a hardcoded strong tilt on the whole wall, once there are many pages the corners overflow and collapse and the perspective distorts. You must compute the column count from the page count + viewport, flatten the tilt when there are many rows, and scroll when it doesn't fit on one screen.
3. **Don't make the thumbnail resolution too low**: gallery thumbnails < 1000px look soft when magnified on hover. The default is 1600px.

**Generating thumbnails for the gallery**: use `scripts/gen_deck_thumbs.mjs` (playwright captures each page + sharp downsamples):
```bash
npm install playwright sharp
node gen_deck_thumbs.mjs --slides slides --out thumbs --width 1600
```
Then add `thumb: "thumbs/<same name>.jpg"` to each MANIFEST entry. Grid mode ignores thumb (always iframes); only gallery mode uses it.

### Single-page verification (the killer advantage of the multi-file architecture)

Every slide is an independent HTML. **As soon as you finish one, double-click it to open it in the browser**:

```bash
open slides/05-personas.html
```

Playwright screenshots also just `goto(file://.../slides/05-personas.html)`, with no JS page jump needed and no interference from other pages' CSS. This brings the cost of a "change a little, verify a little" workflow close to zero.

### Parallel development

Split each slide's task out to a different agent and run them at the same time: the HTML files are independent of each other, so there are no conflicts at merge time. For a long deck, this kind of parallelism can cut production time to 1/N.

### What goes in `shared/tokens.css`

Only things that are **truly shared across pages**:

- CSS variables (palette, font size scale, spacing scale)
- A canvas lock like `body { width: 1920px; height: 1080px; }`
- Chrome that's exactly the same on every page, like `.page-header` / `.page-footer`

**Don't** stuff single-page layout classes in here; that degrades back into the single-file architecture's global pollution problem.

---

## Path B (small decks): single file + `deck_stage.js`

Suited to ≤10 pages, needing state shared across pages (e.g. one React tweaks panel controlling every page), or extremely compact scenarios like a pitch deck demo.

### Basic usage

1. Read the contents of `assets/deck_stage.js` and embed it in the HTML's `<script>` (or `<script src="deck_stage.js">`)
2. Wrap the slides in `<deck-stage>` inside the body
3. 🛑 **The script tag must go after `</deck-stage>`** (see the hard constraint below)

```html
<body>

  <deck-stage>
    <section>
      <h1>Slide 1</h1>
    </section>
    <section>
      <h1>Slide 2</h1>
    </section>
  </deck-stage>

  <!-- ✅ Correct: script after deck-stage -->
  <script src="deck_stage.js"></script>

</body>
```

### 🛑 Hard constraint on script position (a real pitfall, 2026-04-20)

**You can't put `<script src="deck_stage.js">` in `<head>`.** Even though it can define `customElements` from `<head>`, the parser triggers `connectedCallback` as soon as it parses the `<deck-stage>` opening tag. At that point the child `<section>` elements haven't been parsed yet, `_collectSlides()` gets an empty array, the counter shows `1 / 0`, and every page renders stacked at once.

**Three compliant ways to write it** (pick any one):

```html
<!-- ✅ Most recommended: script after </deck-stage> -->
</deck-stage>
<script src="deck_stage.js"></script>

<!-- ✅ Also fine: script in head but with defer -->
<head><script src="deck_stage.js" defer></script></head>

<!-- ✅ Also fine: module scripts are deferred by nature -->
<head><script src="deck_stage.js" type="module"></script></head>
```

`deck_stage.js` itself has a built-in `DOMContentLoaded` deferred-collection defense, so even with the script in head it won't blow up completely. But `defer` or placing it at the bottom of body is still the cleaner approach, avoiding reliance on the defensive branch.

### ⚠️ CSS traps of the single-file architecture (be sure to read)

The most common pitfall of the single-file architecture: **the `display` property gets stolen by single-page styles**.

Common mistake 1 (writing display: flex directly on section):

```css
/* ❌ The external CSS has specificity 2 and overrides the shadow DOM's ::slotted(section){display:none} (also 2) */
deck-stage > section {
  display: flex;            /* Every page will render stacked at once! */
  flex-direction: column;
  padding: 80px;
  ...
}
```

Common mistake 2 (the section has a class with higher specificity):

```css
.emotion-slide { display: grid; }   /* Specificity: 10, even worse */
```

Both make **every slide render stacked at once**. The counter may show `1 / 10` and pretend everything is normal, but visually the first page covers the second, which covers the third.

### ✅ Starter CSS (copy it straight in at kickoff, no pitfalls)

**The section itself** only handles "visible/invisible"; **put the layout (flex/grid, etc.) on `.active`**:

```css
/* section only defines general styles other than display */
deck-stage > section {
  background: var(--paper);
  padding: 80px 120px;
  overflow: hidden;
  position: relative;
  /* ⚠️ Don't write display here! */
}

/* Lock down "hidden unless active": specificity + !important as a double safeguard */
deck-stage > section:not(.active) {
  display: none !important;
}

/* Only the active page gets the display + layout it needs */
deck-stage > section.active {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Print mode: every page must show, overriding :not(.active) */
@media print {
  deck-stage > section { display: flex !important; }
  deck-stage > section:not(.active) { display: flex !important; }
}
```

The alternative: **put the single page's flex/grid on an inner wrapper `<div>`**, and the section itself is only ever a `display: block/none` switch. This is the cleanest approach:

```html
<deck-stage>
  <section>
    <div class="slide-content flex-layout">...</div>
  </section>
</deck-stage>
```

### Custom dimensions

```html
<deck-stage width="1080" height="1920">
  <!-- 9:16 portrait -->
</deck-stage>
```

---

## Slide Labels

Both deck_stage and deck_index put a label on every page (shown in the counter). Give them **more meaningful** labels:

**Multiple files**: write `{ file, label: "04 Problem Statement" }` in the `MANIFEST`
**Single file**: add `<section data-screen-label="04 Problem Statement">` on the section

**Key: slide numbers start at 1, not 0**.

When the user says "slide 5", they mean the 5th slide, never array position `[4]`. Humans don't speak 0-indexed.

---

## Speaker Notes

**Not added by default**; only add them when the user explicitly asks.

With speaker notes, you can cut the text on the slide to a minimum and focus on impactful visuals: the notes carry the full script.

### Format

**Multiple files**: write this in the `<head>` of `index.html`:

```html
<script type="application/json" id="speaker-notes">
[
  "Script for slide 1...",
  "Script for slide 2...",
  "..."
]
</script>
```

**Single file**: same location.

### Key points for writing notes

- **Complete**: not an outline, but the words you'll actually say
- **Conversational**: like everyday speech, not written language
- **Matched**: the Nth item in the array corresponds to the Nth slide
- **Length**: 200-400 characters is best
- **Emotional line**: mark stresses, pauses and points of emphasis

---

## Slide design patterns

### 1. Establish a system (required)

After exploring the design context, **first state the system you're going to use**:

```markdown
Deck system:
- Background colors: 2 at most (90% white + 10% dark section dividers)
- Typefaces: Instrument Serif for display, Geist Sans for body
- Rhythm: section dividers are full-bleed color + white text, regular slides on white
- Imagery: full-bleed photos for hero slides, charts for data slides

I'll work to this system; let me know if anything's off.
```

Continue only after the user confirms.

### 2. Common slide layouts

- **Title slide**: solid background + a huge title + subtitle + author/date
- **Section divider**: colored background + section number + section title
- **Content slide**: white background + title + 1-3 bullet points
- **Data slide**: title + a big chart/number + a short explanation
- **Image slide**: full-bleed photo + a small caption at the bottom
- **Quote slide**: white space + a huge quote + attribution
- **Two-column**: left-right comparison (vs / before-after / problem-solution)

Use at most 4-5 layouts in one deck.

### 3. Scale (stressed again)

- Body text at least **24px**, ideally 28-36px
- Titles **60-120px**
- Hero text **180-240px**
- Slides are viewed from 10 meters away, so the text has to be big enough

### 4. Visual rhythm

A deck needs **intentional variety**:

- Color rhythm: mostly white backgrounds + the occasional colored section divider + the occasional dark segment
- Density rhythm: a few text-heavy slides + a few image-heavy slides + a few quote slides with white space
- Font size rhythm: normal titles + the occasional giant hero text

**Don't make every slide look the same**; that's a PPT template, not design.

### 5. Breathing room (must read for data-dense pages)

**The pitfall beginners fall into most easily**: stuffing every piece of information that fits onto one page.

Information density ≠ effective communication. Academic/talk decks especially need restraint:

- List/matrix pages: don't draw all N elements at the same size. Use a **primary-secondary hierarchy**: enlarge the 5 you're talking about today as the stars, and shrink the remaining 16 as background hints.
- Big-number pages: the number itself is the visual star. Keep the caption around it to 3 lines at most, or the audience's eyes jump back and forth.
- Quote pages: separate the quote and the attribution with white space; don't stick them together.

Review yourself against two questions, "is the data the star?" and "is the text crammed together?", and keep revising until the white space makes you a little uneasy.

---

## Printing to PDF

**Multiple files**: `deck_index.html` already handles the `beforeprint` event and outputs the PDF page by page.

**Single file**: `deck_stage.js` handles it the same way.

The print styles are already written, so you don't need to write any extra `@media print` CSS.

---

## Exporting to PPTX / PDF (self-serve scripts)

HTML first is the first-class citizen. But users often need PPTX/PDF deliveries. Two general-purpose scripts are provided, **usable with any multi-file deck**, under `scripts/`:

### `export_deck_pdf.mjs`: export a vector PDF (multi-file architecture)

```bash
node scripts/export_deck_pdf.mjs --slides <slides-dir> --out deck.pdf
```

**Features**:
- Text **stays vector** (copyable, searchable)
- 100% visual fidelity (printed after rendering in Playwright's embedded Chromium)
- **No need to change a single character of the HTML**
- Each slide gets its own `page.pdf()`, then they're merged with `pdf-lib`

**Dependencies**: `npm install playwright pdf-lib`

**Limitation**: the text in the PDF can't be edited any more; to change it, go back and change the HTML.

### `export_deck_stage_pdf.mjs`: only for the single-file deck-stage architecture ⚠️

**When to use it**: the deck is a single HTML file + a `<deck-stage>` web component wrapping N `<section>` elements (i.e. the Path B architecture). In that case the `export_deck_pdf.mjs` approach of "one `page.pdf()` per HTML" doesn't work, and you need this dedicated script.

```bash
node scripts/export_deck_stage_pdf.mjs --html deck.html --out deck.pdf
```

**Why export_deck_pdf.mjs can't be reused** (a record of a real pitfall, 2026-04-20):

1. **Shadow DOM beats `!important`**: deck-stage's shadow CSS has `::slotted(section) { display: none }` (only the active one gets `display: block`). Even `@media print { deck-stage > section { display: block !important } }` in the light DOM can't override it. After `page.pdf()` triggers the print media, Chromium's final render has only the active slide, so **the whole PDF has just 1 page** (a repeat of the currently active slide).

2. **Looping goto over each page still only produces 1 page**: the intuitive fix, "navigate once to each `#slide-N` then `page.pdf({pageRanges:'1'})`", also fails, because once the print CSS's `deck-stage > section { display: block }` rule outside the shadow DOM gets overridden, the final render is always the first section in the list (not the page you navigated to). The result: 17 loops give 17 copies of the P01 cover.

3. **absolute children run onto the next page**: even if you get every section to render, if the section itself is `position: static`, its absolutely positioned `cover-footer`/`slide-footer` is positioned relative to the initial containing block. When print forces the section to a 1080px height, the absolute footer can get pushed onto the next page (showing up as the PDF having 1 more page than there are sections, with the extra page containing only an orphaned footer).

**Fix strategy** (already implemented in the script):

```js
// After opening the HTML, use page.evaluate to pull the sections out of the deck-stage slot,
// attach them directly to a plain div under body, and inline styles to guarantee position:relative + fixed dimensions
await page.evaluate(() => {
  const stage = document.querySelector('deck-stage');
  const sections = Array.from(stage.querySelectorAll(':scope > section'));
  document.head.appendChild(Object.assign(document.createElement('style'), {
    textContent: `
      @page { size: 1920px 1080px; margin: 0; }
      html, body { margin: 0 !important; padding: 0 !important; }
      deck-stage { display: none !important; }
    `,
  }));
  const container = document.createElement('div');
  sections.forEach(s => {
    s.style.cssText = 'width:1920px!important;height:1080px!important;display:block!important;position:relative!important;overflow:hidden!important;page-break-after:always!important;break-after:page!important;background:#F7F4EF;margin:0!important;padding:0!important;';
    container.appendChild(s);
  });
  // No page break after the last page, to avoid a trailing blank page
  sections[sections.length - 1].style.pageBreakAfter = 'auto';
  sections[sections.length - 1].style.breakAfter = 'auto';
  document.body.appendChild(container);
});

await page.pdf({ width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
```

**Why this works**:
- It pulls the sections out of the shadow DOM slot into a plain div in the light DOM, completely bypassing the `::slotted(section) { display: none }` rule
- Inline `position: relative` makes absolute children position relative to the section, so they don't overflow
- `page-break-after: always` makes the browser put each section on its own page when printing
- No page break on `:last-child` avoids a trailing blank page

**A caution when verifying with `mdls -name kMDItemNumberOfPages`**: macOS Spotlight metadata is cached, so after the PDF is rewritten you need to run `mdimport file.pdf` to force a refresh, or it shows the old page count. Counting with `pdfinfo` or the number of files from `pdftoppm` gives the real number.

---

### `export_deck_pptx.mjs`: export an editable PPTX

```bash
# The only mode: native editable text boxes (fonts fall back to system fonts)
node scripts/export_deck_pptx.mjs --slides <dir> --out deck.pptx
```

How it works: `html2pptx` reads the computedStyle element by element and translates the DOM into PowerPoint objects (text frame / shape / picture). Text becomes real text boxes, editable with a double-click in PPT.

**Hard constraints** (the HTML must satisfy them, or that page is skipped; see `references/editable-pptx.md` for details):
- All text must be inside `<p>`/`<h1>`-`<h6>`/`<ul>`/`<ol>` (no bare-text divs)
- `<p>`/`<h*>` tags themselves can't have background/border/shadow (put it on an outer div)
- Don't insert decorative text with `::before`/`::after` (pseudo-elements can't be extracted)
- Inline elements (span/em/strong) can't have margin
- No CSS gradients (can't be rendered)
- No `background-image` on divs (use `<img>`)

The script has a built-in **automatic preprocessor** that automatically wraps "bare text inside leaf divs" in `<p>` (keeping the class). This fixes the most common violation (bare text). But other violations (a border on a p, margin on a span, etc.) still need to be fixed at the HTML source.

**Font fallback caveat**:
- Playwright measures text-box sizes with the webfont; PowerPoint/Keynote render with the local machine's fonts
- When the two differ there will be **overflow or misalignment**, so every page needs a visual pass
- It's best to install the fonts used in the HTML on the target machine, or fall back to `system-ui`

**Don't take this path for visuals-first scenarios** → use `export_deck_pdf.mjs` to produce a PDF instead. A PDF has 100% visual fidelity, is vector, cross-platform and text-searchable: it's the real home for a visuals-first deck, not some "non-editable compromise".

### Make the HTML export-friendly from the start

The most robust kind of deck: **write the HTML to the 4 editable hard constraints from the start**. That way `export_deck_pptx.mjs` passes everything directly. The extra cost is small:

```html
<!-- ❌ Bad -->
<div class="title">Key Findings</div>

<!-- ✅ Good (wrapped in p, class inherited) -->
<p class="title">Key Findings</p>

<!-- ❌ Bad (border on the p) -->
<p class="stat" style="border-left: 3px solid red;">41%</p>

<!-- ✅ Good (border on the outer div) -->
<div class="stat-wrap" style="border-left: 3px solid red;">
  <p class="stat">41%</p>
</div>
```

### When to choose which

| Scenario | Recommendation |
|------|------|
| For the organizer/archive | **PDF** (universal, high fidelity, text-searchable) |
| Sending to collaborators so they can tweak the text | **PPTX editable** (accept font fallback) |
| Presenting live, no content changes | **PDF** (vector fidelity, cross-platform) |
| HTML is the preferred presentation medium | Play it straight in the browser; the export is only a backup |

## The in-depth path for exporting to editable PPTX (long-term projects only)

If your deck will be maintained long term, revised repeatedly and worked on by a team, it's best to **write the HTML to the html2pptx constraints from the start**, so `export_deck_pptx.mjs` passes everything directly. See `references/editable-pptx.md` for details (4 hard constraints + HTML template + quick reference for common errors + the fallback process for an existing visual draft).

---

## Common questions

**Multiple files: a page in the iframe won't open / is a white screen**
→ Check whether the `file` path in the `MANIFEST` is correct relative to `index.html`. Use the browser's DevTools to see whether the iframe's src can be accessed directly.

**Multiple files: one page's styles conflict with another page's**
→ Impossible (iframe isolation). If it seems like a conflict, it's the cache: hard refresh with Cmd+Shift+R.

**Single file: multiple slides render stacked at once**
→ A CSS specificity problem. See the section "CSS traps of the single-file architecture" above.

**Single file: the scaling looks wrong**
→ Check whether every slide is attached directly under `<deck-stage>` as a `<section>`. There can't be a `<div>` wrapped in between.

**Single file: want to jump to a specific slide**
→ Add a hash to the URL: `index.html#slide-5` jumps to slide 5.

**Applies to both architectures: text sits in different positions on different screens**
→ Use fixed dimensions (1920×1080) and `px` units, not `vw`/`vh` or `%`. Scaling is handled in one place.

---

## Verification checklist (every deck must pass it when done)

1. [ ] Open `index.html` (or the main HTML) directly in the browser, and check that the first page has no broken images and the fonts have loaded
2. [ ] Press → to go through every page: no blank pages, no layout misalignment
3. [ ] Press P for print preview: each page is exactly one A4 (or 1920×1080) with no cropping
4. [ ] Pick 3 pages at random and hard refresh with Cmd+Shift+R; the localStorage memory works correctly
5. [ ] Batch screenshots with Playwright (single-page architecture: iterate over `slides/*.html`; single-file architecture: switch with goTo), and go over them by eye
6. [ ] Search for leftover `TODO` / `placeholder` and confirm they've all been cleaned up
