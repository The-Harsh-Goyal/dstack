# Visual-draft HTML → editable PPTX: read the rendered result, don't change the HTML

`references/editable-pptx.md` covers **the html2pptx route**: the HTML is written to the 4 hard constraints from the very first line,
and only then can it be converted. That document has one conclusion, "**never force html2pptx onto HTML written with visual freedom**;
in practice the pass rate is < 30%", and gives two fallbacks: produce a PDF, or rewrite an editable HTML version.

**This document covers a third route, which makes that fallback unnecessary.**

The core difference in one sentence: **html2pptx reads the source; this script reads the coordinates after the browser has finished rendering.**
Flex, centering, automatic line wrapping: the browser has already turned all of these into absolute positions, so patterns like "bare text in a div", "used flex"
or "a background on a p" aren't a problem at all. To `getBoundingClientRect` they're all just a rectangle.

---

## Pick a route first: one of three

| Situation | Which route | Why |
|---|---|---|
| **The HTML isn't written yet**, you're building a deck from scratch | `scripts/html2pptx.js` (see `editable-pptx.md`) | A PPTX written to the 4 constraints has the cleanest structure; text box merging and paragraph hierarchy are better suited to later editing |
| **The HTML is already written** and is visually driven (flex / centering / bare text / background images / SVG charts) | **`scripts/pptx_from_rendered.py` (this document)** | Converts directly with zero rework. Rewriting 20 slides of HTML to fit the constraints costs far more than measuring directly |
| **The client requires "you must use our template"** | **Only this document's route works** | pptxgenjs creates the file from scratch and can't use an existing pptx as a base to inherit its master; python-pptx can |

⚠️ **Don't mix the two routes in the same project.** Pick one and follow it to the end, otherwise the two coordinate systems will fight each other.

---

## Usage

```bash
python3 scripts/pptx_from_rendered.py deck.html -o deck.pptx --selector ".slide"
```

When inheriting a client's official template (the most common commercial project scenario):

```bash
python3 scripts/pptx_from_rendered.py deck.html -o deck.pptx \
    --selector ".slide" \
    --template client-official-template.pptx \
    --layout "Content Page" \
    --skip-class logo \
    --bg 05070B
```

Dependencies: `playwright` (with chromium), `python-pptx`, `Pillow`.
Adding `--dump-json dom.json` writes the list of measured elements to disk, which is very useful when troubleshooting position problems.

---

## Inheriting the client's template: so their master changes take effect across the deck

In commercial projects the most common reason for rework isn't "it doesn't look good", it's "**you didn't use our template**".
When the client says that, they usually want two specific things: ① the logo is the latest version;
② **when they change the master, your slides change along with it**.

A PPT with one full-bleed image per slide can do neither; even if you make text boxes, a file built from scratch with pptxgenjs
doesn't have their master. The approach is to use their `.pptx` as the base:

1. Open it with `Presentation(client-template.pptx)`
2. **Delete the template's own sample slides**, leaving the master / layouts / theme / palette untouched (`strip_slides`)
3. For each slide, `add_slide(official layout)`, and delete the empty placeholders the layout brings onto the slide
4. **Don't draw shared elements like the logo into the content layer**: let the layout provide them. When rendering, use `--skip-class logo`
   to skip the logo in the HTML, so only your content is left on the slide and the logo comes from the layout.
   That way, when the client changes the master/layout, every slide changes along with it.

⚠️ **Pitfall: the layout may hide a solid-color rectangle covering the whole screen**, the same color and size as the layout's background (a redundant mask).
If you leave it, anything placed beneath it on the slide gets covered. The script's `unblock_layout` deletes it;
deleting it doesn't change how the layout looks.

**The canvas size follows the template, not the 960×540pt from `editable-pptx.md`.** Whatever size the client template is, use that
(26.67×15 inch has come up in practice); if the sizes don't match, everything gets scaled when the files are merged. The script automatically computes the scale ratio as
`slide width pt ÷ HTML canvas width px`; with a 1920px HTML canvas against 1920pt, the ratio is exactly 1.0,
**1 CSS px = 1 PowerPoint pt**, no mental math needed.

---

## Six typesetting traps (each one has caused real trouble)

None of these are covered by `editable-pptx.md`, because it assumes the HTML is newly written to the constraints.
When reading the rendered result, each of the following will break things outright if you don't handle it:

### 1. Line breaks and indentation in the HTML source become real line breaks in the PPTX

```html
<div>
    <em>68</em>
    <span>projects, and I set up daily data collection</span>
</div>
```

The line breaks and indentation between tags are **real text nodes**. The browser collapses them under `white-space:normal`
(runs of whitespace → one space, leading and trailing whitespace dropped); PPTX has no such rule. That `\n` is carried over as is,
and in PowerPoint it's a real line break, pushing the whole rest of the passage onto the next line where it overlaps other elements.

**Fix**: perform HTML whitespace collapsing during extraction, and discard runs that are empty after collapsing.

### 2. A container's font-size is often inherited, so you can't use it to compute padding and line spacing

The `computedStyle.fontSize` of the div above might be only 16px (inherited from the body),
while the number inside is 132px. Computing text box padding and line spacing from 16px gets everything wrong.

**Fix**: take the **largest** font size among the `runs` as the base size.

### 3. You can't count lines by deduplicating rectangle tops

`Range.getClientRects()` returns multiple rectangles for runs of different font sizes on the same line: they share a baseline,
but their top edges differ a lot. Deduplicating by `top` counts one line as several (in testing, one line was counted as 4).

**Fix**: cluster by whether the y ranges overlap.

### 4. Several paragraphs of different font sizes in one box can't share one line spacing

PowerPoint line spacing is **paragraph level**, while visual drafts often put lines of different font sizes in the same div:

```html
<div>The one I put the most into<br>took over a week, forty thousand lines of code<br><em class="big">never got it running</em></div>
```

Apply one line spacing to the whole box and the small-text lines get stretched while the large-text line gets squashed; in testing, adjacent lines ended up overlapping.

**Fix**: **split into paragraphs at each `<br>`, and make each paragraph its own text box**, each with its own position and line height.
The number of text boxes goes up (137 → 175 in testing), but that's the necessary price of correctness.

### 5. Flex shrink-wrapped boxes have zero slack, so the last character drops to the next line

A flex child under `align-items:center` shrinks to the actual width of its text, **with no slack at all**.
Once in PowerPoint, the slightest difference in font metrics squeezes the last character onto the next line
(in testing, the last character of "...gets put to use" and of "what's scarce is judgment" both dropped).

**Fix**: measure whether this passage actually wrapped in the HTML; if it was a single line to begin with, **turn off word wrap outright** in the PPT
(`word_wrap = False`), so wrapping becomes impossible at the root. In testing, 150 of 175 boxes fell into this category.

### 6. Don't set exact line spacing on single-line paragraphs

The measured line box height is larger than the actual line spacing (that's the **font's line box**, not the CSS line height; 185 vs 148 in testing).
Using it as exact line spacing pushes the whole text down.

**Fix**: only set line spacing on paragraphs that "wrapped by themselves"; leave single-line paragraphs to PowerPoint to lay out naturally by font size.
The text then sits flush with the top of the box, and its position is actually the most accurate.

---

## 🔴 Verification: first verify your verification tool

**This is the biggest lesson of this route, worth more than all the technical details above.**

The same PPTX can come out completely differently in different renderers. Use the wrong tool, and **not one** of pitfalls 1, 3, 4 and 6 above
will show up: all 20 slides look right, and the moment the client opens it, things overlap.

| Tool | Trustworthy? | Notes |
|---|---|---|
| **macOS `qlmanage -t` thumbnails** | ❌ **No** | Uses a simplified rendering path that's far more forgiving of line spacing than real PowerPoint. In testing it let through 4 bugs that cause overlapping text |
| **LibreOffice (macOS)** | ⚠️ Layout is trustworthy, but Chinese text may vanish entirely | It can't access macOS system Chinese fonts, so it renders tofu boxes or even blanks |
| **Keynote + AppleScript** | ✅ **First choice for automation** | Real presentation-engine layout; can be scripted to export PDF and then render slide by slide |
| **Opening in WPS / PowerPoint** | ✅ **Final confirmation** | Clients mostly use these. Check by eye |

**Keynote automation (the only route on this machine that's both fully automatic and trustworthy)**:

```bash
osascript <<'EOF'
tell application "Keynote"
  activate
  set d to open POSIX file "/abs/path/deck.pptx"
  delay 4
  export d to POSIX file "/abs/path/out.pdf" as PDF
  close d saving no
  quit
end tell
EOF
pdftoppm -png -r 54 out.pdf page     # then compare slide by slide, side by side with the original HTML
```

**To judge whether a renderer is trustworthy, use a control experiment**: give the **client's original template file** to the same renderer.
If it also loses all the Chinese text when rendering the official template, that's an environment problem, not a problem with your file. This step can save
hours of troubleshooting in the wrong direction.

⚠️ **Don't use System Events to inject keystrokes to page through and take screenshots.** The keys go into whatever window the user is currently typing in.

**Also run a mechanical check** (independent of any renderer):

- Dropped-text check: **runs automatically by default after the script exports** (`verify_text()`). It compares the page's rendered `innerText` with the text in the pptx slide by slide (ignoring whitespace and case), and if anything's missing it prints "⚠️ Dropped-text check: N pieces of text are visible in the browser but missing from the PPTX" and the missing fragments ("slide N missing: …"). When nothing is missing it prints "🔍 Dropped-text check: all rendered page text is in the PPTX, no text dropped". It's on by default because missing text is silent: there's no error, and relying on someone remembering to check is the same as not checking
- Count comparison: image counts and shape counts match slide by slide

**The reference source must be independent of the extraction logic; you can't compare against the `--dump-json` list.** The list and the pptx both come from the same DOM extraction:
text missed at the extraction stage (for example mixed content like "`<svg>` + bare text" inside an element, which once lost an entire passage) is absent from both,
so the comparison is bound to pass: the verification tool and the thing being verified share the same blind spot. `innerText` is text the browser renders itself
(with `text-transform` already applied) and doesn't go through any extraction code, so only it can reveal what extraction missed.
Exclusions: elements skipped with `--skip-class` are reported as missing (expected); text inside svg/canvas is exported as an image and is already excluded from the comparison.

---

## Fonts: delivery font ≠ typesetting font

Client guidelines often specify a font you don't have on your machine (for example Microsoft YaHei, a commercial font distributed with Windows licenses).
**Don't change the HTML's `font-family` to it just for that**: it isn't installed locally, so the preview and PDF fall back,
and **the layout breaks on the spot** (in testing, an entire line of numbers got squeezed onto the next line).

The right approach is to **keep the two separate**:

- Typeset HTML / PDF with a font actually installed on your machine, so what you see is what you get
- Write the font name specified by the client's guidelines in the PPTX (their machines have it)

**Separating them works because full-width Chinese characters are monospaced**: switching fonts doesn't change the number of characters per line or where lines break; the differences are only in Latin text and punctuation.
Drafts that are mainly Chinese can safely separate them; drafts that are mainly Latin text need separate verification.
