# Editable PPTX export: HTML hard constraints + size decisions + common errors

This document covers the route of **using `scripts/html2pptx.js` + `pptxgenjs` to translate HTML element by element into truly editable PowerPoint text boxes**, which is also the only route `export_deck_pptx.mjs` supports.

> ## 🔴 Pick your route first: this document covers only one of two routes
>
> | Situation | Which route |
> |---|---|
> | **The HTML isn't written yet**, building a deck from scratch | **This document** (write to the 4 hard constraints → `html2pptx.js`). Cleanest structure, best for later editing |
> | **The HTML is already written** and is visually driven (flex / centering / bare text / background images / SVG charts) | → `references/pptx-from-rendered-html.md` (reads rendered coordinates, **zero rework**) |
> | **The client insists "you must use our template"** | → Same as above, **that's the only route**. pptxgenjs can't use an existing pptx as a base to inherit its master |
>
> Don't mix the two routes in the same project. The 4 constraints below hold only for this document's route.
> Visual drafts that are already written **don't need** to be rewritten into a compliant structure just to convert to PPTX.
>
> **Core premise**: to take this route, the HTML must follow the 4 constraints below from the very first line. **Not write it first and convert later**: fixing it afterwards triggers 2-3 hours of rework (a pitfall hit for real on a real client deck for an options-investing peer advisory group, 2026-04-20).

---

## Canvas size: use 960×540pt (LAYOUT_WIDE)

The PPTX unit is the **inch** (physical size), not px. Decision principle: the body's computedStyle size must **match the presentation layout's size in inches** (±0.1", enforced by `validateDimensions` in `html2pptx.js`).

### Comparing 3 candidate sizes

| HTML body | Physical size | Corresponding PPT layout | When to choose |
|---|---|---|---|
| **`960pt × 540pt`** | **13.333″ × 7.5″** | **pptxgenjs `LAYOUT_WIDE`** | ✅ **Default recommendation** (the standard for modern PowerPoint 16:9) |
| `720pt × 405pt` | 10″ × 5.625″ | Custom | Only when the user specifies the "old PowerPoint Widescreen" template |
| `1920px × 1080px` | 20″ × 11.25″ | Custom | ❌ On this document's route it's a non-standard size, and fonts look unusually small when projected. ⚠️ But **when inheriting a client template, the canvas must follow the template** (26.67″×15″ has come up in practice); for that route see `pptx-from-rendered-html.md` |

**Don't think of the HTML size as a resolution.** A PPTX is a vector document; the body size determines the **physical size**, not the sharpness. An oversized body (20″×11.25″) won't make text sharper; it only makes the pt font sizes smaller relative to the canvas, which looks worse when projected/printed.

### Three equivalent ways to write the body

```css
body { width: 960pt;  height: 540pt; }    /* clearest, recommended */
body { width: 1280px; height: 720px; }    /* equivalent, for px habits */
body { width: 13.333in; height: 7.5in; }  /* equivalent, for inch intuition */
```

The matching pptxgenjs code:

```js
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch, no custom layout needed
```

---

## 4 hard constraints (violations throw errors directly)

`html2pptx.js` walks the DOM once and, based on tag and computed style, classifies each element as "text box / shape / image / ignore". Behind the classification rules are limits of the PowerPoint file format itself; projected onto HTML, they become the 4 rules below. Run through them in your head as you write, and you'll save the time of reworking slide by slide after converting.

### Rule 1: text can't sit directly in a DIV; wrap it in `<p>` or `<h1>`-`<h6>`

```html
<!-- ❌ Wrong: the text is a direct child text node of the div -->
<div class="metric">DAU 124K, +8% MoM</div>

<!-- ✅ Right: text wrapped in <p>/<h1>-<h6>, the div only handles positioning/background -->
<div class="metric"><p>DAU 124K, +8% MoM</p></div>
```

**How it's judged**: the script checks whether the div's **direct child nodes** include a non-whitespace text node. Text nested inside `<p>`/`<h1>`-`<h6>` doesn't count; only "text stuck directly on the div" is a violation. The error includes the first 50 characters of the offending text (ending in `...` if longer), making it easy to locate which passage.

**Likewise, a span can't stand on its own**: a span is an inline element, and the script only treats it as a local style override inside a `<p>`/`<h1>`-`<h6>` (bold, color change, underline); it won't pull it out as a separate text box. If you want an independently editable piece of text, it must have a `<p>`/`<h1>`-`<h6>` around it.

### Rule 2: CSS gradients aren't supported (essentially a case of "background-image isn't supported")

```css
/* ❌ Wrong: linear-gradient/radial-gradient both count as background-image */
.banner { background: linear-gradient(135deg, #FF6B6B, #4ECDC4); }

/* ✅ Right: solid color */
.banner { background: #FF6B6B; }

/* ✅ If you need the look of a multi-color transition, stagger several solid-color flex children and simulate the gradient with opacity or color steps */
.banner { display: flex; }
.banner div { flex: 1; }
.banner .c1 { background: #FF6B6B; }
.banner .c2 { background: #FF9B6B; }
.banner .c3 { background: #4ECDC4; }
```

**Why**: the script's div check only looks at whether the computed `background-image` is `none`. If it isn't `none`, whether it's an image or a CSS gradient function, it gets blocked (a gradient is essentially a special kind of background-image). Of PowerPoint's native shape fills, solid color is the only one pptxgenjs supports reliably; gradients need a separate OOXML structure that the toolchain doesn't implement yet.

### Rule 3: backgrounds/borders/shadows can only go on DIVs, never on text tags (including `<ul>`/`<ol>`)

```html
<!-- ❌ Wrong: the <h2> carries its own background and rounded corners -->
<h2 style="background: #FFD700; border-radius: 6pt; padding: 6pt 10pt;">Key conclusion</h2>

<!-- ✅ Right: the outer div carries the background/border, the <h2> only handles text -->
<div style="background: #FFD700; border-radius: 6pt; padding: 6pt 10pt;">
  <h2>Key conclusion</h2>
</div>
```

**Why**: for every `<p>`/`<h1>`-`<h6>`/`<ul>`/`<ol>` (and the `<li>` elements they absorb), the script first checks its own background/border/box-shadow on its own. If any of the three is non-empty, it throws an error straight away; it doesn't even consider whether other rules also match, such as "placeholder" (`placeholder` in the `class`), and simply marks it as a violation. This check happens before all other classification, because in PowerPoint "a shape that can draw a background/border/shadow" and "a text frame that can hold text" are two different objects. `<p>`/`<h*>` only ever become the latter, so there's nowhere to put the former's properties.

### Rule 4: DIVs can't use `background-image`; images always use the `<img>` tag

```html
<!-- ❌ Wrong -->
<div style="background-image: url('trend.png'); width: 300pt; height: 200pt;"></div>

<!-- ✅ Right -->
<img src="trend.png" style="position: absolute; left: 60pt; top: 80pt; width: 300pt; height: 200pt;" />
```

**Why**: the script only reads the absolute `src` (as resolved by the browser) from `<img>` elements to generate image objects; it doesn't parse the `url(...)` inside a div's `background-image` property at all. When this rule is hit, the script doesn't drag the div's descendants down with it: the `div` itself produces nothing, but any `<p>`/`<img>` etc. it contains are still processed individually; only that background image layer is lost. If you want an image and text layered together, lay out the `<img>` and the text layer as two separate elements and align them with positioning.

---

## Merging text boxes (`data-pptx-merge`)

**Default behavior**: every `<p>`/`<h1>`-`<h6>` in the HTML becomes an **independent text box** in the PPTX. Write 3 `<p>` in a card → 3 text boxes stacked in the PPT, and when editing you can't press Enter to add paragraphs across the whole passage; you have to change font size/alignment one by one.

**Fix**: add `data-pptx-merge="true"` to the outer div, and all `<p>/<h*>` inside the container are merged into **one editable text box**, with paragraph separators between them, so in the PPT you edit them paragraph after paragraph continuously.

```html
<!-- ✅ Merged form: all 4 paragraphs in one text box -->
<div class="card" data-pptx-merge="true"
     style="position: absolute; top: 60pt; left: 60pt; width: 420pt;
            background: #1A4A8A; border-radius: 8pt; padding: 20pt 24pt;">
  <h2 style="font-size: 24pt; color: #FFFFFF;">Title</h2>
  <p  style="font-size: 14pt; color: #DDEEFF;">First paragraph of body text.</p>
  <p  style="font-size: 14pt; color: #FFD166;">Second paragraph: a color change for emphasis.</p>
  <p  style="font-size: 14pt; color: #DDEEFF;">Third paragraph: keep writing in the same text box.</p>
</div>
```

**Styles preserved** (written per paragraph as run options): `font-size`, `color`, `font-family`, `font-weight` (bold), `font-style` (italic), `text-decoration: underline`, and inline styles from `<b>/<i>/<u>/<strong>/<em>/<span>`.

**Taken from the first paragraph and applied to the whole box**: `text-align`, `line-height`. That's because PowerPoint alignment and line spacing are paragraph/textbox level: one box can only have one alignment. If the paragraphs have different alignments, don't use merge; keep them independent.

**The container's own `background`/`border`/`box-shadow`/`border-radius`** still render as a shape, behaving exactly like an ordinary div. In other words, a blue card background + text is still two layers, "shape + text frame"; only the text layer collapses from 3-4 text boxes into 1.

**Limits**:
- `data-pptx-merge` can't be nested (it throws an error).
- The container can't use `background-image` (same as rule 4 of the 4 hard constraints).
- Don't put child divs with a `background`/`border` inside the container: they'll still be rendered as independent shapes, but their text has already been merged away, which may cause visual misalignment.

**When to use it**: content that will be revised repeatedly and edited further in PPT. Not needed for one-off exports for archiving; the behavior is the same.

---

## Path A HTML template skeleton

One independent HTML file per slide, with scopes isolated from each other (avoiding CSS pollution in a single-file deck).

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 960pt; height: 540pt;           /* ⚠️ matches LAYOUT_WIDE */
    font-family: system-ui, -apple-system, "PingFang SC", sans-serif;
    background: #FEFEF9;                    /* solid color, no gradients */
    overflow: hidden;
  }
  /* DIVs handle layout/background/borders */
  .card {
    position: absolute;
    background: #1A4A8A;                    /* background on the DIV */
    border-radius: 4pt;
    padding: 12pt 16pt;
  }
  /* text tags only handle font styling, no background/border */
  .card h2 { font-size: 24pt; color: #FFFFFF; font-weight: 700; }
  .card p  { font-size: 14pt; color: rgba(255,255,255,0.85); }
</style>
</head>
<body>

  <!-- title area: outer div for positioning, inner text tags -->
  <div style="position: absolute; top: 40pt; left: 60pt; right: 60pt;">
    <h1 style="font-size: 36pt; color: #1A1A1A; font-weight: 700;">Titles are assertions, not topic words</h1>
    <p style="font-size: 16pt; color: #555555; margin-top: 10pt;">Subtitle with supporting detail</p>
  </div>

  <!-- content card: div handles the background, h2/p handle the text -->
  <div class="card" style="top: 130pt; left: 60pt; width: 240pt; height: 160pt;">
    <h2>Point one</h2>
    <p>Short explanatory text</p>
  </div>

  <!-- list: use ul/li, not hand-typed • symbols -->
  <div style="position: absolute; top: 320pt; left: 60pt; width: 540pt;">
    <ul style="font-size: 16pt; color: #1A1A1A; padding-left: 24pt; list-style: disc;">
      <li>First point</li>
      <li>Second point</li>
      <li>Third point</li>
    </ul>
  </div>

  <!-- illustration: use the <img> tag, not background-image -->
  <img src="illustration.png" style="position: absolute; right: 60pt; top: 110pt; width: 320pt; height: 240pt;" />

</body>
</html>
```

---

## Common errors quick reference

| Error message | Cause | Fix |
|---------|------|---------|
| `Text "XXX" is written directly inside a <div>` | Bare text in a div | Wrap the text in `<p>` or `<h1>`-`<h6>` |
| `<div> backgrounds can't use CSS gradients` | Used linear/radial-gradient | Change to a solid color, or split into flex children |
| `Text tag <p> has background set` | A background color was added to a `<p>` tag | Wrap it in a `<div>` to carry the background; the `<p>` holds only text |
| `<div> can't use background-image` | A div used background-image | Change to an `<img>` tag |
| `Content overflows the page vertically by Xpt` | Content exceeds 540pt | Reduce content or shrink font sizes, or truncate with `overflow: hidden` |
| `Page size mismatch` | The body size doesn't match the pres layout | Use `960pt × 540pt` for the body with `LAYOUT_WIDE`; or a custom size with defineLayout |
| `Text box "XXX" is only X inches from the bottom edge of the page` | A large-font `<p>` is < 0.5 inch from the bottom of the body | Move it up and leave enough bottom margin; the bottom of a PPT slide gets partly covered anyway |

---

## Basic workflow (PPTX in 3 steps)

### Step 1: write each slide as independent HTML following the constraints

```
MyDeck/
├── slides/
│   ├── 01-cover.html    # each file is a complete 960×540pt HTML
│   ├── 02-agenda.html
│   └── ...
└── illustration/        # all images referenced by <img>
    ├── chart1.png
    └── ...
```

### Step 2: write build.js that calls `html2pptx.js`

```js
const pptxgen = require('pptxgenjs');
const html2pptx = require('../scripts/html2pptx.js');  // this skill's script

(async () => {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch, matches the HTML's 960×540pt

  const slides = ['01-cover.html', '02-agenda.html', '03-content.html'];
  for (const file of slides) {
    await html2pptx(`./slides/${file}`, pres);
  }

  await pres.writeFile({ fileName: 'deck.pptx' });
})();
```

### Step 3: open and check

- Open the exported PPTX in PowerPoint/Keynote
- Double-clicking any text should let you edit it directly (if it's an image, rule 1 was violated)
- Verify overflow: every slide should stay within the body bounds, with nothing cut off

---

## This route vs other options (when to choose what)

| Need | What to choose |
|------|------|
| Colleagues will change the text in the PPTX / sending it to non-technical people to keep editing | **This document's route** (editable; the HTML must be written to the 4 constraints from the start) |
| Only for presenting / sending for archive, no further changes | `export_deck_pdf.mjs` (multi-file) or `export_deck_stage_pdf.mjs` (single-file deck-stage), producing a vector PDF |
| Visual freedom comes first (animation, web components, CSS gradients, complex SVG), and not being editable is acceptable | **PDF** (same as above): a PDF is both faithful and cross-platform, more suitable than an "image PPTX" |

**Never force html2pptx onto HTML written with visual freedom**: in practice the pass rate for visually driven HTML is < 30%, and reworking the rest slide by slide is slower than rewriting. In that situation, produce a PDF instead of forcing a PPTX.

---

## Fallback: a visual draft already exists but the user insists on an editable PPTX

You'll occasionally hit this: you/the user have already written a visually driven HTML (with gradients, web components and complex SVG), where a PDF would be the best fit, but the user explicitly says "no, it has to be an editable PPTX".

**Don't force `html2pptx` and hope it passes**: in practice visually driven HTML passes html2pptx < 30% of the time, and the other 70% will throw errors or come out distorted.

> 🔴 **Since 2026-09, try the third route before considering A/B below**: `scripts/pptx_from_rendered.py` reads coordinates
> **after the browser has rendered**, not the source, so visually driven HTML can be converted directly with zero rework (20 slides all passed in testing),
> and there's no need to make the user choose between "losing the visuals" and "losing editability". See `references/pptx-from-rendered-html.md`.
> Only bring up A/B below when that route doesn't apply either.

The correct fallback is:

### Step 1 · State the limitations first (transparent communication)

Tell the user three things clearly in one go:

> "Your current HTML uses [list specifically: gradients / web components / complex SVG / ...], so converting it directly to an editable PPTX will fail. I have two options:
> - A. **Produce a PDF** (recommended): 100% of the visuals are kept; recipients can view and print it but can't edit the text
> - B. **Use the visual draft as a blueprint and rewrite an editable HTML** (keeps the design decisions on color/layout/copy, but reorganizes the HTML structure to the 4 hard constraints, **sacrificing** visual capabilities like gradients, web components and complex SVG) → then export an editable PPTX
>
> Which do you choose?"

Don't make option B sound trivial: state clearly **what will be lost**. Let the user make the trade-off.

### Step 2 · If the user chooses B: the AI rewrites it proactively; don't ask the user to write it

The doctrine here is: **the user provides the design intent, and you're responsible for translating it into a compliant implementation**. Not having the user learn the 4 hard constraints and rewrite it themselves.

Principles to follow when rewriting:
- **Keep**: the color system (primary/secondary/neutral colors), information hierarchy (title/subtitle/body/notes), core copy, the layout skeleton (top-middle-bottom / left-right columns / grid), page rhythm
- **Downgrade**: CSS gradients → solid colors or flex segments, web components → paragraph-level HTML, complex SVG → simplified `<img>` or solid-color geometry, shadows → delete or reduce to very faint, custom fonts → move toward system fonts
- **Rewrite**: bare text → wrap in `<p>` / `<h*>`, `background-image` → `<img>` tags, backgrounds/borders on `<p>` → carried by an outer div

### Step 3 · Produce a comparison list (transparent delivery)

After rewriting, give the user a before/after comparison so they know which visual details were simplified:

```
Original design → adjustments in the editable version
- Purple gradient in the title area → solid background in primary color #5B3DE8
- Data card shadows → deleted (replaced with a 2pt stroke to separate them)
- Complex SVG line chart → simplified to an <img> PNG (generated from an HTML screenshot)
- Web component motion in the Hero area → static first frame (web components can't be translated)
```

### Step 4 · Export & deliver in two formats

- `editable` HTML → run `scripts/export_deck_pptx.mjs` for an editable PPTX
- **We recommend also keeping** the original visual draft → run `scripts/export_deck_pdf.mjs` for a high-fidelity PDF
- Deliver both formats to the user: a PDF of the visual draft + an editable PPTX, each doing its own job

### When to refuse option B outright

In some situations the rewrite costs too much, and you should persuade the user to give up on an editable PPTX:
- The HTML's core value is animation or interaction (after rewriting, only a static first frame remains, losing 50%+ of the information)
- More than 30 slides, where the rewrite would take over 2 hours
- The visual design depends heavily on precise SVG / custom filters (after rewriting it would bear almost no relation to the original)

In that case tell the user: "Rewriting this deck costs too much; I suggest a PDF rather than a PPTX. If the recipient really needs the pptx format, then accept that the visuals will become much plainer. Do you want to switch to PDF?"

---

## Why the 4 constraints aren't bugs but physical constraints

These 4 aren't the `html2pptx.js` author cutting corners: they're the result of **constraints of the PowerPoint file format (OOXML) itself** projected onto HTML:

- In a PPTX, text must be in a text frame (`<a:txBody>`), which corresponds to paragraph-level HTML elements
- A PPTX shape and a text frame are two objects; you can't draw a background and write text on the same element
- PPTX shape fills have limited gradient support (only certain preset gradients, no CSS arbitrary-angle gradients)
- A PPTX picture object must reference a real image file, not a CSS property

Once you understand this, **don't expect the tool to get smarter**: the HTML has to adapt to the PPTX format, not the other way around.
