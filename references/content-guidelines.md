# Content Guidelines: Anti-AI Slop, Content Rules, Scale Specs

AI slop is the default; if you don't actively avoid it, it happens. But "the default" changes over time: in 2024 it was purple gradients and emoji, and in 2026 it has become a more "tasteful" look. Banning only the previous generation's slop means fighting the last war.

## The 2026 AI default look (read this first)

Anthropic's official frontend-design skill (2026) spells out the current clusters of AI-generated pages clearly ([original](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)):

1. **Warm cream background (close to #F4F1EA) + high-contrast serif headings + terracotta accent (close to #D97757)**. This is Claude's own interface palette, and also the place where you, the model, most easily slide into: don't let it be the one you land on without thinking.
2. **Near-black background + a single bright accent** (acid green or vermilion).
3. **Newspaper-style layout**: hairline column rules, zero border radius, dense newspaper columns.
4. **SaaS card kit**: content chopped into identical rounded cards, everything with the same radius and the same light gray shadow, gradients as decoration.
5. **Template chrome**: a widely tracked all-caps small label above every heading; "A · B · C" joined by middle dots; "WORD — fragment" style labels; #0B0B0B or #111 instead of black; monospace for small data labels; a "→" after links and buttons.

There are also three default typographic moves: recoloring or italicizing just one word in a heading; making every small label all caps; adding unnecessary small labels above content. Use numbering (01 / 02 / 03) only when the content really is a sequence.

**Treat the two kinds separately:**

- **1–4 are look families.** They became defaults precisely because they look good; dark-background single-accent and warm-paper serif directions still win user approval in blind picks. Using them isn't wrong; what's wrong is all three directions crowding into the same family, or every project looking like this. `design_lint.py check` only lists them as "notes"; what actually governs them is `compare` (the three versions crowding together) and the look ledger (colliding with recent projects). We once dodged them as yellow lights, and all three versions retreated together into light, cool and orderly, and got judged "too orderly, too boring".
- **5 and the three typographic moves above are template chrome.** They're small habitual moves that cost almost nothing to delete; `check` lists them as yellow lights: if the brief asks for one, do it, otherwise delete that structure. What can't be measured (like #111 instead of black) is up to your own eye.

## The previous generation of slop (around 2024, still to be avoided)

### Visual traps

**❌ Aggressive gradient backgrounds**
- Purple → pink → blue full-screen gradients (the typical flavor of AI-generated web pages)
- Rainbow gradients in any direction
- Mesh gradients covering the background
- ✅ If you use a gradient: subtle, single color family, an intentional accent (e.g. button hover)

**❌ Rounded cards + left border accent color**
```css
/* This is the typical signature of an AI-flavored card */
.card {
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  padding: 16px;
}
```
These cards are everywhere in AI-generated dashboards. Want emphasis? Use more designed approaches: background color contrast, weight/size contrast, plain divider lines, or simply no cards at all.

**❌ Emoji decoration**
Unless the brand itself uses emoji (e.g. Notion, Slack), don't put emoji in the UI. **Especially not**:
- 🚀 ⚡️ ✨ 🎯 💡 before headings
- ✅ in feature lists
- → in CTA buttons (a standalone arrow is OK; an emoji arrow is not)

If you have no icons, use a real icon library (Lucide/Heroicons/Phosphor), or use a placeholder.

**❌ Drawing imagery with SVG**
Don't try to draw people, scenes, devices, objects, or abstract art in SVG. AI-drawn SVG imagery reads as AI at a glance: childish and cheap. **A gray rectangle + a text label reading "Illustration slot 1200×800" is 100 times better than a clumsy SVG hero illustration**.

The only places SVG is acceptable:
- Real icons (16×16 to 32×32 scale)
- Geometric shapes as decorative elements
- Data viz charts

**❌ Too much iconography**
Not every heading/feature/section needs an icon. Overusing icons makes the interface look like a toy. Less is more.

**❌ "Data slop"**
Made-up stats as decoration:
- "10,000+ happy customers" (you don't even know whether there are any)
- "99.9% uptime" (don't write it without real data)
- Decorative "metric cards" made of icon + number + word
- Fake data in mock tables dressed up flashily

If there's no real data, leave a placeholder or ask the user for it.

**❌ "Quote slop"**
Made-up user testimonials and celebrity quotes decorating the page. Leave a placeholder and ask the user for real quotes.

### Font traps

**❌ Avoid these overused fonts**:
- Inter (the default for AI-generated web pages)
- Roboto
- Arial / Helvetica
- Pure system font stacks
- Fraunces (AI discovered it and overused it)
- Space Grotesk (AI's recent favorite)

**✅ Use distinctive display + body pairings**. Directions for inspiration:
- Serif display + sans body (editorial feel)
- Mono display + sans body (technical feel)
- Heavy display + light body (contrast)
- Variable fonts for weight animation in the hero

Font resources:
- Lesser-known good options on Google Fonts (Instrument Serif, Cormorant, Bricolage Grotesque, JetBrains Mono)
- Open-source font sites (Fraunces's sibling fonts, Adobe Fonts)
- Don't invent font names out of thin air

### Color traps

**❌ Inventing colors out of thin air**
Don't design a whole unfamiliar palette from scratch. It's usually inharmonious.

**✅ Strategy**:
1. There's a brand color → use the brand color, and interpolate missing color tokens with oklch
2. No brand color but there's a reference → sample colors from screenshots of the reference product
3. Starting from zero → sample colors from the subject (its materials, place of origin, objects, the dominant colors in real images), following the "color derivation protocol" in `references/design-styles.md`: sample → converge → justify. **Don't treat Anthropic / Claude's brand colors as a "safe default"**: that is exactly item one of the 2026 AI default look

**Defining colors in oklch** is the most modern approach:
```css
:root {
  --primary: oklch(0.62 0.14 155);      /* Example: a moss green sampled from real images of the subject; the value changes with the content */
  --primary-light: oklch(0.85 0.06 155); /* Light shade of the same color family */
  --primary-dark: oklch(0.42 0.15 155);  /* Dark shade of the same color family */
}
```
oklch guarantees the hue doesn't drift when you adjust lightness; it works better than hsl.

**❌ Tossing in inverted colors for dark mode**
It's not simply inverting the colors. Good dark mode requires readjusting saturation, contrast, and accent colors. If you don't want to do dark mode properly, don't do it.

### Layout traps

**❌ Bento grid overload**
Every AI-generated landing page wants a bento. Unless your information structure really suits bento, use another layout.

**❌ Big hero + 3-column features + testimonials + CTA**
This landing page template is worn out. If you want to innovate, really innovate.

**❌ Every card in a card grid looks the same**
Asymmetric, cards of different sizes, some with images and some text only, some spanning columns: that's what looks like a real designer's work.

## What to do instead

- **Spend boldness in one place only**: let one element be the one that's remembered, with everything around it quiet and restrained. Taste means being refined enough in the right places, not applying even effort everywhere: one detail at 120%, the rest at 80%. Look in the mirror before leaving the house and take off one accessory.
- **Structural elements should carry information**: borders, numbering, dividers, and small labels encode relationships in the content; they aren't decoration. Before adding one, ask what it says.
- Typographic details are the "taste tax": `text-wrap: pretty`, CSS Grid, `oklch()`; Chinese text uses 「」 quotation marks (`references/typography.md`).
- Don't invent colors out of thin air: sample from brand assets, from real images of the content, from the subject's cultural context (`references/design-styles.md` color derivation protocol).

**Counterexamples must be recognizable as counterexamples**: when the task itself needs to show anti-design (explaining "what is AI slop", doing a comparison review), don't pile slop over the whole page; isolate it in an honest counterexample container: a dashed border plus a "Counterexample · Don't do this" corner tag, so the counterexample serves the narrative without polluting the page's main tone.

## Content rules

### 1. Don't add filler content

Every element must earn its place. Empty space is a design problem, solved with **composition** (contrast, rhythm, white space), **not** by filling it with content.

**Questions for judging filler**:
- If this content were removed, would the design get worse? If the answer is "no", remove it.
- What real problem does this element solve? If it's "making the page feel less empty", delete it.
- Is this stat/quote/feature backed by real data? If not, don't make it up.

"One thousand no's for every yes".

### 2. Ask before adding material

Think an extra paragraph/page/section would make it better? Ask the user first; don't add it unilaterally.

Reasons:
- The user knows their audience better than you do
- Adding content has a cost, and the user may not want it
- Adding content unilaterally violates the "junior designer reporting on their work" relationship

### 3. Create a system up front

After exploring the design context, **first state out loud the system you'll use**, and have the user confirm:

```markdown
My design system:
- Color: #14261F main + #E6EDE4 background + #C8553D accent (background and main taken from the moss green in your product images, accent taken from the logo)
- Type: Schibsted Grotesk for display + Source Serif 4 for body
- Rhythm: section titles use full-bleed colored backgrounds + white text; regular sections use white backgrounds
- Imagery: full-bleed photo for the hero, placeholders in feature sections until you provide images
- At most 2 background colors, to avoid clutter

Confirm this direction and I'll start building.
```

Start only after the user confirms. This check-in avoids "finding out halfway through that the direction was wrong".

## Scale specs

### Slides (1920×1080)

- Body text at least **24px**, ideally 28-36px
- Headings 60-120px
- Section titles 80-160px
- Hero headlines can use large type at 180-240px
- Body text never <24px; labels, annotations, and chart ticks no smaller than 16px

### Print documents

- Body text at least **10pt** (≈13.3px), ideally 11-12pt
- Headings 18-36pt
- Captions 8-9pt

### Web and mobile

- Body text at least **14px** (16px for senior-friendly)
- Mobile body text **16px** (avoids iOS auto-zoom)
- Hit targets (clickable elements) at least **44×44px**
- Line height 1.5-1.7 (1.7-1.8 for Chinese)

### Contrast

- Body text vs background **at least 4.5:1** (WCAG AA)
- Large text vs background **at least 3:1**
- Check with Chrome DevTools' accessibility tools

## CSS power tools

**Advanced CSS features** are a designer's good friends; use them boldly:

### Typography

```css
/* Makes headings wrap more naturally, without a lonely single word on the last line */
h1, h2, h3 { text-wrap: balance; }

/* Body text wrapping, avoiding widows and orphans */
p { text-wrap: pretty; }

/* Power tool for Chinese typesetting: punctuation compression, line-start/line-end control */
p { 
  text-spacing-trim: space-all;
  hanging-punctuation: first;
}
```

### Layout

```css
/* CSS Grid + named areas = off-the-charts readability */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
}

/* Subgrid to align card contents */
.card { display: grid; grid-template-rows: subgrid; }
```

### Visual effects

```css
/* A designed scrollbar */
* { scrollbar-width: thin; scrollbar-color: #666 transparent; }

/* Glassmorphism (use with restraint) */
.glass {
  backdrop-filter: blur(20px) saturate(150%);
  background: color-mix(in oklch, white 70%, transparent);
}

/* The View Transitions API makes page transitions silky smooth */
@view-transition { navigation: auto; }
```

### Interaction

```css
/* The :has() selector makes conditional styling easy */
.card:has(img) { padding-top: 0; } /* Cards with images get no top padding */

/* Container queries make components truly responsive */
@container (min-width: 500px) { ... }

/* The new color-mix function */
.button:hover {
  background: color-mix(in oklch, var(--primary) 85%, black);
}
```

## Quick decisions: when you're hesitating

- Want to add a gradient? → Most likely don't
- Want to add an emoji? → Don't
- Want to give cards rounded corners + a border-left accent? → Don't; use another approach
- Want to draw a hero illustration in SVG? → Don't draw it; use a placeholder
- Want to add a decorative quote? → First ask the user whether they have a real quote
- Want to add a row of icon features? → First ask whether icons are wanted; they may not be needed
- Using Inter? → Switch to something more distinctive
- Using a purple gradient? → Switch to a palette with a real basis

**When you feel "adding this would look better", that's usually a sign of AI slop**. Make the simplest version first, and add only when the user asks.
