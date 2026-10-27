# Typography: a typesetting reasoning system

> **This isn't a font list; it's a set of reasoning rules for pairing and typesetting.** `design-styles.md` already gives the font names for each of its 60 styles; this document answers "why pair them this way" and "given any content, how do you derive the font size / line length / weight". Goal: the same style label, applied to different content, should derive different typesetting results, rather than copying the same set of font sizes every time.
>
> The prerequisite discipline is unchanged: if there's design context, lift the user's own fonts first (see `design-context.md`); everything in this document applies only when "the user has no font guidelines".

## 0. Typesetting decision order

Once you have the content, reason in this order, with each step determined by the previous one. Skipping to "just pick a nice-looking font" isn't allowed:

1. **Content type** → long-form reading / data-dense / big marketing type / UI, which determines the scale ratio and body font size
2. **Language makeup** → Chinese only / mixed Chinese and Latin / Latin only, which determines how the fallback chain is written and the line-height baseline
3. **Style temperature** (aligned with the quiet/neutral/bold tiers in `design-styles.md`) → determines where the pairing's contrast comes from
4. **Font names come last** → pick from the pairing table in section 3 below, or take them from the matching entry in the style library

Why: picking the font name first means "what the content is" has zero effect on typesetting, which is exactly the root cause of everything looking the same.

## 1. Font size scale (modular scale)

Font sizes aren't guesswork; they're derived step by step by multiplying the body size by a fixed ratio. The ratio determines the page's "drama":

| Ratio | Name | Character | Use for |
|------|------|------|------|
| 1.2 | Minor third | Gentle, many levels without noise | Dashboards, documentation sites, information-dense UI |
| 1.25 | Major third | General-purpose, safe | Most web pages, product landing pages |
| 1.333 | Perfect fourth | Headings clearly stand out | Editorial long-form, marketing pages, reports |
| 1.5 | Perfect fifth | Dramatic, very few levels | Big-type posters, slides, one-sentence-per-screen heroes |

**Derivation rule**: set body text at 16-18px (17-18px recommended for Chinese body text, since Chinese characters have dense strokes and look more cramped than Latin at the same size), then scale headings up and captions down by the ratio. More than 5 levels means it's out of control; cut some.

| Level | Reference value at a 1.25 ratio | Use |
|------|--------------------|------|
| caption | 12-13px | Figure captions, meta info, EXIF-style small text |
| small | 14px | Supporting notes, tables |
| body | 16-18px | Body text, the basis for everything |
| h3 | ≈1.25x | Subsection headings |
| h2 | ≈1.56x | Section headings |
| h1 | ≈1.95x | Page title |
| display | 3x-8x, free of the scale | Giant hero type, determined by the layout rather than the scale |

**Fluid font sizes** (mandatory for the display level, to avoid rigidity on large screens and overflow on small ones):

```css
/* clamp(min, preferred, max): preferred = base rem + viewport coefficient */
h1 { font-size: clamp(2rem, 1.2rem + 3.5vw, 4.5rem); }
.display { font-size: clamp(3rem, 1rem + 9vw, 9rem); }
/* don't let body text clamp over a wide range; a narrow 16→18 range is enough */
body { font-size: clamp(1rem, 0.95rem + 0.3vw, 1.125rem); }
```

Why display breaks free of the scale: giant hero type is a layout element, not a text level. Its size is determined by "what fraction of the viewport it fills", so deriving it from vw makes more sense than deriving it from the scale.

## 2. Line length and line height

### Line length (affects readability more than font choice)

| Language | Comfort zone | CSS implementation |
|------|--------|----------|
| Latin body text | 45-75 characters, 66 ideal | `max-width: 65ch` |
| Chinese body text | 22-38 characters per line, 28-32 ideal | `max-width: 36em` (em scales with font size) |
| Captions/sidebars | Shorter, 15-20 Chinese characters | Naturally limited by the narrow container |

Why Chinese is shorter: Chinese characters are dense square glyphs with no spaces, carrying noticeably more information than Latin text at the same width. With the same number of eye saccades, Chinese takes in more content, and if lines are too long, the reader can't find the start of the next line when returning.

### Line height moves with line length

Line height isn't a constant; it's a function of line length. The longer the line, the farther the eye travels to return, so it needs more line spacing as a "track":

| Scenario | Latin | Chinese |
|------|------|------|
| Display type (1-2 lines) | 0.95-1.1 | 1.1-1.25 |
| Headings (h1-h3) | 1.1-1.3 | 1.3-1.4 |
| Short-line body (<30 characters/line) | 1.4-1.5 | 1.6-1.7 |
| Long-line body (near the upper limit) | 1.6 | 1.8-2.0 |

Chinese runs about 0.2 higher than Latin across the board: Chinese characters fill the full em square and lack the natural gaps between Latin lowercase letters, so with too little line spacing everything blurs together.

### text-wrap (supported by all browsers since 2024+, free typesetting quality)

```css
h1, h2, h3 { text-wrap: balance; }  /* balances line lengths in multi-line headings, eliminating orphan lines */
p { text-wrap: pretty; }            /* eliminates orphan words at the end of body text (strong effect in Latin, slight in Chinese) */
```

Use balance only for headings of ≤4 lines (the algorithm is limited to 6 lines and has a performance cost); pretty can be applied globally to body text with no side effects.

## 3. Ten open-source font pairings (Latin)

There are three sources of contrast in a pairing; decide which one you're using before you pair:

- **Form contrast**: serif display x sans-serif body (the most classic, but x-heights must mesh, or the visual font size jumps)
- **Same-family meshing**: a superfamily sharing the same design skeleton (zero risk, at the cost of blandness)
- **Era contrast**: classical letterforms x modern letterforms (there's only tension when the lineages are 200+ years apart; 50 years apart just looks messy)

| # | Pairing (display + body) | Pairing logic | Temperature | Source |
|---|------------------------|----------|------|------|
| 1 | Newsreader + Geist | Form contrast: a transitional serif optimized for screens, with a high x-height that meshes well with Geist; **the proper alternative to Fraunces** | Quiet | Google Fonts / Vercel official repo |
| 2 | Source Serif 4 + Source Sans 3 | Same-family meshing: the same Adobe design system, with fully aligned heights, weights and rhythm; zero failures for reports and documents | Quiet | Google Fonts |
| 3 | EB Garamond + IBM Plex Sans | Era contrast: a 16th-century French old-style serif x a 2017 rational grotesque, 400 years of tension; note Garamond's low x-height, so mixing them on the same line needs size compensation (+8% is an empirical starting point; the systematic fix is `font-size-adjust`, see section 4) | Quiet · literary | Google Fonts |
| 4 | Lora + Hanken Grotesk | Form contrast: Lora is a brush-flavored serif with medium contrast that holds up on screen; Hanken is an open-source close relative with a Söhne feel | Neutral | Google Fonts |
| 5 | Instrument Serif + Geist | Form contrast: only one weight (400), naturally display-only, so body text must go to the sans. ⚠️ On its way to being overused by AI tools; in 2026, use it cautiously where you "want to look distinctive" | Neutral | Google Fonts |
| 6 | Schibsted Grotesk + Source Serif 4 | Reversed structure: grotesque as display, serif as body, for a media feel; **the alternative now that Space Grotesk is everywhere** (custom-made open source from Norway's Schibsted newspaper group, with news-industry pedigree) | Neutral | Google Fonts |
| 7 | Bricolage Grotesque + Newsreader | Form contrast: Bricolage's ink traps and irregular details only show at large sizes, making it a natural display face; paired with a quiet serif body it creates rough x refined | Bold | Google Fonts |
| 8 | Archivo (Expanded/Black) + Inter | Big-poster structure: Archivo's wide, heavy black weights dominate the space, while Inter only works as the 14-16px body-text worker bee (that's Inter's correct use, see anti-patterns) | Bold | Google Fonts |
| 9 | Cormorant Garamond + Work Sans | High-contrast luxury: Cormorant's strokes are extremely thin, so it **only works at ≥40px**; at small sizes the strokes break; suits a fashion/space-catalog style | Bold | Google Fonts |
| 10 | Geist Mono / JetBrains Mono + Geist | Monospace as the star: a command-line, engineering feel; use monospace only for labels/numbering/code, since setting whole paragraphs of body text in monospace is a disaster (line length swells by 30%) | Neutral · technical | Vercel / JetBrains official, both OFL |

**Overused list** (single fonts AI tools have used to the point of saturation; switching to an alternative is usually better):

| Overused | Why it's overused | Alternative |
|--------|----------|------|
| Fraunces as display | The default "tasteful" option of every AI design tool in 2023-2025 | Newsreader, Libre Caslon Text |
| Inter as display | Inter was designed for small UI text; at large sizes it's uniform and expressionless | Archivo, Anton, Schibsted Grotesk |
| Space Grotesk | The lazy answer for "techy", everywhere on crypto/AI landing pages | Schibsted Grotesk, Familjen Grotesk |
| Playfair Display | The lazy answer for "elegant", with a wedding-invitation feel | Cormorant (more extreme), DM Serif Display (chunkier) |

The **combination** "high-contrast serif × warm cream background" isn't on this list: it's a look family, not an overused font. You can use it; just don't crowd all three directions into it or use it on every project. That's what the look ledger is for (`references/content-guidelines.md`).

## 4. Chinese typesetting (the heaviest section of this document)

Latin typesetting has a century-old mature toolchain; Chinese doesn't. AI design tools have collectively given up on Chinese (handing it to system fonts by default, applying Latin rules directly), and this is where you can stand out.

### 4.1 Map of open-source / free-for-commercial-use Chinese fonts

| Font | Category | Character | Temperature | Source |
|------|------|------|------|------|
| Source Han Serif (Noto Serif SC) | Song (serif) | Orthodox publishing, a full set of 7 weights, Heavy can serve as display | Quiet to neutral | Google Fonts, OFL |
| Source Han Sans (Noto Sans SC) | Hei (sans) | The Inter of the Chinese world: reliable, expressionless; not wrong as the default body text, but no personality | Fallback for all temperatures | Google Fonts, OFL |
| LXGW WenKai | Kai (script) | Handwritten warmth, approachable; suits body text and quotations for literary/educational/personal blogs | Quiet · warm | GitHub lxgw/LxgwWenKai, OFL |
| LXGW Neo XiHei | Hei (sans) | A screen sans thinner and airier than Source Han Sans; body text that doesn't tire you over long reads | Quiet | GitHub lxgw/LxgwNeoXiHei |
| Smiley Sans | Oblique sans | **A rare native oblique in the Chinese world**, with a sense of motion, for headings only; body text in it is dizzying | Bold | GitHub atelier-anchor/smiley-sans, OFL |
| Huiwen Mincho | Old-form Mincho | The feel of old letterpress type, retro publishing; suits book covers/cultural display | Neutral to bold · retro | Maoken / GitHub, free for commercial use |
| KingHwa OldSong | Old Song | A heading Song with square, hard strokes, with a newspaper-masthead feel | Bold · retro | Maoken, free for commercial use |
| GenRyuMin / GenYoMin | Mincho (traditional-leaning) | A recut of Source Han Serif that keeps traditional glyph details; first choice for Traditional Chinese content | Quiet · classical | GitHub ButTaiwan, OFL |
| Glow Sans | Geometric sans | A modern geometric sans derived from Source Han Sans, in multiple widths (Compressed works for narrow, tall display) | Neutral to bold · modern | GitHub welai/glow-sans, OFL |
| MiSans / HarmonyOS Sans / OPPO Sans | Vendor UI sans | UI sans faces with slightly more personality than Source Han Sans, good for app prototypes | Neutral | Each vendor's official site, free for commercial use |

Selection reasoning: **pick body text only from Song/Hei/Kai** (all the others are display fonts and are tiring in whole paragraphs); only reach for Smiley Sans / Old Song / Mincho when the display needs personality. One Chinese font weighs as much as ten Latin fonts (5-15MB per file), so use at most two Chinese font families per page, for both loading and consistency reasons.

### 4.2 Rules for mixed Chinese and Latin text

**The fallback chain is the first lever**: the Latin glyphs bundled with Chinese fonts are generally unattractive (Source Han Sans's Latin letters are stiff). Put the Latin font first so it catches Latin characters and numbers, and Chinese characters automatically fall through to the Chinese font behind it:

```css
/* Latin first, Chinese after, system Chinese as fallback, generic family last */
font-family: "Geist", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
/* same for serif (font names are only examples; pick by the pairing table and subject) */
font-family: "Source Serif 4", "Noto Serif SC", "Songti SC", serif;
```

Why this order: font-family matching is per character, and Latin fonts don't contain CJK code points, so Chinese characters naturally pass through to the Chinese font. Written the other way around (Chinese first), every Latin character gets eaten by the Chinese font, and your pairing is wasted.

**Size compensation**: at the same font size, Latin lowercase looks smaller (the x-height takes up only half the body, while Chinese characters fill it). Two fixes:

```css
/* Fix 1: font-size-adjust normalizes fallback fonts by x-height (Chrome 127+/FF/Safari 17+) */
:root { font-size-adjust: from-font; }
/* Fix 2: choose a Latin face with a high x-height (Geist/Inter/Source Sans are all high), so mixed text lines up naturally */
```

**Baseline alignment**: when the Chinese and Latin baselines don't match, the symptom is English words "sinking" in Chinese lines. Prefer switching to a Latin face with a higher x-height; for individual display cases, nudge the Latin span with `vertical-align: -0.02em~-0.06em`, but don't fix body text this way (the maintenance cost exceeds the benefit).

**Number rule**: numbers always go through the Latin font (the fallback chain guarantees this), and data tables must add `font-variant-numeric: tabular-nums`, otherwise 1 and 8 have different widths and columns jitter.

**No spaces between Chinese and English**: this is this repo's convention (inherited from upstream: no "Pangu spacing"); rely on the spacing built into the fonts in the fallback chain, not manually typed spaces.

### 4.3 Chinese has no italics

Chinese letterforms have no italic tradition. When the browser meets `font-style: italic`, it mechanically slants the Chinese characters (faux italic), distorting the strokes, and it looks terrible. Replacement table for means of emphasis:

| Latin habit | Chinese substitute | CSS |
|----------|----------|-----|
| italic for emphasis | Change the weight | `font-weight: 600` (provided the font really has that weight) |
| italic for titles/citations | Background highlight | `background: linear-gradient(transparent 60%, #FFE9A8 60%)` highlighter style |
| italic for quotation blocks | Change the font | Set the whole quotation in LXGW WenKai; Kai script itself is Chinese's "quoting voice" |
| italic for proper names | Color / emphasis dots | `text-emphasis: dot` (emphasis dots, native Chinese emphasis, support is now usable) |

Safety fuse: `font-synthesis: none;` globally disables synthesized italics and synthesized bold. Better no emphasis than distorted glyphs.

### 4.4 Punctuation rules

| Rule | How | Why |
|------|------|--------|
| Quotation marks | Corner brackets 「」『』, not curly quotes "" | Curly quotes take a full-width slot in Chinese fonts but have a Latin shape, so they look like they're floating; 「」 is a hard rule in this repo |
| Line-start/line-end prohibition (kinsoku) | `line-break: strict;` | Prevents full stops and commas at the start of a line and opening quotes at the end of a line; this is the baseline of Chinese typesetting |
| Hanging punctuation | `hanging-punctuation: first allow-end;` (Safari only); cross-browser, handle opening quotes at the start of paragraphs with `text-indent: -0.5em` | If the opening quote at the start of a paragraph doesn't hang, the first line looks indented by half a character, and the visual left edge isn't flush |
| Consecutive punctuation compression | `font-feature-settings: "halt";` (line-end compression) or `"palt"` (proportional width, needs letter-spacing to go with it) | Runs of full-width punctuation (like 」）。) leave a gap one and a half characters wide; halt narrows it |

### 4.5 Chinese letter-spacing ranges

| Scenario | Range | Why |
|------|------|--------|
| Body text | 0 to 0.05em | A little extra tracking adds airiness; beyond 0.05em the gestalt of words breaks up and reading speed drops |
| Headings (24-48px) | 0 | Square Chinese characters have naturally even spacing and don't need Latin-style tracking adjustments |
| Giant display type (>60px) | -0.02em to 0 | At large sizes the gaps between glyph faces are magnified, so tightening slightly is more compact; any more negative and the strokes collide |
| All-caps Latin small labels | 0.08-0.15em | The only scenario that needs large positive tracking, and it only applies to Latin capitals |

**Never use the Latin "tighten display by -0.05em" habit on Chinese**: Chinese characters are designed to fill the square, and negative tracking makes the strokes clash directly.

### 4.6 Chinese display type

Chinese lacks the Latin ecosystem of display fonts running from Ultra Thin to Black, so the drama of large type has to be manufactured through reasoning:

- **Weight contrast is the main weapon**: Source Han Serif Heavy 900 over Light 300, two extreme weights of the same font on the same screen, has more tension than switching fonts and zero loading cost
- **Stroke density determines the lower limit of usable sizes**: fonts with thin strokes/high contrast (Song's thin horizontals, Cormorant-style faces) only work at large sizes; below 24px the thin strokes start to break, so body text must go back to Hei/medium-stroke faces
- **The reverse also holds**: heavy-stroke characters (Hei Black, Old Song) carry too much ink at very large sizes, and the ink difference between 「一」 and 「灥」 gets magnified; for headings with uneven density, consider dropping one weight
- **Vertical text is a display weapon unique to Chinese**: `writing-mode: vertical-rl` for book-spine headings, poetry and tables of contents, which Latin can't do; note that Latin text and numbers in vertical text use `text-orientation: upright` or `text-combine-upright: all` (two-digit numbers combined and set upright)

## 5. Anti-pattern list

| ❌ Anti-pattern | Why it's wrong |
|-----------|----------|
| Inter everywhere (display+body, all in) | Inter is a tool for small UI text, uniform and expressionless as display; this is the number one fingerprint of an "AI-generated page" |
| Leaving Chinese to the system default `sans-serif` | Windows falls back to SimSun/YaHei and macOS to PingFang, so the same page shows two completely different faces across devices, which is the same as not designing it |
| faux italic / faux bold | The browser synthesizes distortions: italics warp Chinese characters, and synthesized bold blurs strokes into ink blobs; cut it off at the root with `font-synthesis: none` |
| Overly loose tracking on large headings | Latin display needs tightening (gaps are magnified at large sizes), but AI often does the opposite and adds +0.05em, so headings look loose, like temporary placeholders |
| Out-of-control line length (no max-width) | 60 Chinese characters per line on a big screen, and readers are sure to get lost when returning to the next line; of all readability problems, out-of-control line length ranks first, doing more damage than choosing the wrong font |
| >6 font size levels | Hierarchy loses its value, and readers can't tell what matters; the whole point of a scale is to enforce restraint |
| Only two weights, 400/700 | The hierarchy relies entirely on font size and the page goes flat; in the variable font era, 300-900 are all free dimensions of expression |
| Tables/data without tabular-nums | Number widths vary, columns jitter left and right, and the data's credibility takes a direct hit |
| Display fonts for Chinese body text (whole paragraphs set in Smiley Sans / Old Song) | The personality of a display font becomes reading resistance in body text; you're tired after 200 characters |
| Putting the Chinese font first in the fallback chain for mixed text | Every Latin character gets eaten by the Chinese font's bundled, unattractive Latin glyphs, and the Latin face you paired never gets its turn |

## 6. CSS implementation essentials

```css
:root {
  /* 1. fallback chain: Latin → Chinese → system Chinese → generic (the order is the rule, see 4.2) */
  --font-body: "Geist", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-display: "<pick for this subject from the pairing table>", "Noto Serif SC", "Songti SC", serif;  /* don't fill in a serif by default */

  /* 2. no synthesis: don't accept browser-faked italics/bold (must be on for Chinese) */
  font-synthesis: none;

  /* 3. baseline Chinese line breaking */
  line-break: strict;        /* line-start/line-end prohibition */
  overflow-wrap: break-word; /* long URLs/English strings don't burst the container */
}

body {
  font-family: var(--font-body);
  font-size: 17px;           /* Chinese body text baseline, see section 1 */
  line-height: 1.8;          /* Chinese line-height baseline, see section 2 */
  /* enable standard ligatures for body text, turn off fancy features */
  font-feature-settings: "liga" 1, "calt" 1;
}

/* data scenarios: tabular numbers + slashed zero (so 0 and O don't get confused) */
.data, table { font-variant-numeric: tabular-nums slashed-zero; }

/* Latin small labels: the only legitimate scenario for all caps + wide tracking */
.label { text-transform: uppercase; letter-spacing: 0.1em; font-size: 12px; }

/* punctuation compression: narrow the gaps of full-width punctuation in Chinese display type */
.display-cjk { font-feature-settings: "halt" 1; }
```

**Loading Chinese fonts** (5-15MB per file; loading the full set directly ruins the first screen):

- Prefer Google Fonts' Noto SC family (already split automatically by unicode-range into hundreds of slices, so the browser downloads only the characters it uses)
- Self-hosted personality fonts (LXGW, Smiley Sans, etc.) must be subset first: `cn-font-split` or fonttools' `pyftsubset`; cut body fonts to the 3,500 common characters, and display fonts to the characters that actually appear (a poster often has only 20 characters, so the subset can get under 50KB)
- `font-display: swap` as a safeguard: Chinese fonts download slowly, and a blank screen waiting for fonts is the worst experience
