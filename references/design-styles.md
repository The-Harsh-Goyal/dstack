# Design style library: web 20 + PPT 20 + infographic 20 + App 12 + Chinese & East Asian 12 (HTML-native first, each with a specimen)

> **Rebuilt 2026-06.** Reverse-engineered from research into the top 5 recognized best designs in each of the 10 major website types + 10 major presentation types (100 real cases in total).
> The fatal problem with the old library of 20 "graphic/installation designer philosophies": nearly all the bold styles were AI-generation-only (particles/light and shadow/hand-drawn). **When the user has no image generation by default and the default is all HTML, the bold half is wiped out entirely and only minimalism is left. That is the root cause of "the default is all the same".** Every style in this library is marked with its **fidelity** under "pure HTML/CSS, no image generation".
>
> ⚖️ **But remember the positioning**: this is **"ammunition to flip through when you have no ideas", not "a list you must choose from"**. When the user gives content/brand/references, the design unfolds from there; don't apply the library. The skill's job is to help the user avoid the worst, not to dictate what good design looks like. Good design grows out of the user's real needs.

## How to use this library

0. **Look at the specimen first, then read the text.** Each section has an overview `assets/style-specimens/sheet-<web|ppt|info|app|east>.jpg`, and the "Specimen" at the end of each style entry is a single large image (the .html with the same name is the source; you can read its CSS directly to learn how it's done). The text description tells you what it is; the specimen tells you what doing it properly looks like. A model that reads only the name produces its average impression of the style. The subjects and numbers in the specimens are fictional; borrow the layout and character, not the content.
1. **First choose the section by output type**: web pages/landing pages/official sites → the 20 web styles; PPT/deck/presentations → the 20 PPT styles; infographics/data visualization/single long images → the 20 infographic styles; App/mobile prototypes → the 12 App styles. **The 12 Chinese & East Asian styles are cross-media**: any format can choose from them, and they're especially worth it for Chinese content.
   - The criterion is **output form, not subject**: clickable sites go to the web section, things that page through go to the PPT section, and **an image (or set of images) with data as the protagonist that can be read on its own without interaction goes to the infographic section**.
   - Two common cases when you're unsure: a dashboard prototype goes to the web section (it's a product UI); a data slide embedded in a deck still goes to the PPT section (it pages through).
2. **Temperature system**: each style is marked `Bold / Neutral / Quiet`. **Bold styles are deliberately the majority**: the model's determinism bias naturally leans quiet and minimal, so the library's ratio has to push it toward bold.
   - This library is the pool for the "seconds roulette" in the three directions (see `references/directions.md`); the best designer and real-world reference logics can also flip through it when they have no ideas.
   - ❌ Don't let all three directions land in the same character (e.g. all "off-white + white space + one accent color").
3. **Fidelity**: ≥90% do it with your eyes closed; 70-90% the main body is doable, with a few details downgraded; <70% (e.g. Memphis distressed textures) you must **clearly state in the output which parts are downgraded to flat color blocks**, and not pretend you can reproduce the original texture.
4. **Fonts**: each gives open-source substitutes (Inter/Geist/Manrope/Space Grotesk/Fraunces/Playfair etc.); don't specify paid fonts (Söhne/Circular etc.).
5. Related: the "seconds roulette" in the three directions draws from this library (`references/directions.md`); for styles that need real photos (dark gallery, white-cube gallery, map as protagonist, etc.), the specimens contain honest placeholders, and when doing it for real you must get the images first.

---

## Color derivation protocol (go through these three steps before using any style)

> ⚠️ **The hex values in all the style entries below are example anchors, not recipes.** The same style used for different content should derive different color values through this protocol. Copying an entry's hex directly is just producing slop with better taste. Why: hard-coded recipes give 100 users 100 outputs in the same colors, and the information carried by color drops to zero; derivation makes color evidence of "unique to this content".
>
> **The same goes for fonts**: the font names in the entries are also example anchors. After choosing a style, run the display+body pairing through the pairing logic and the "overused list" in `references/typography.md` first. **When the list conflicts with an entry, typography.md wins** (e.g. if the entry says Fraunces, swap in a substitute per the list).

### Three-step method: sample → converge → justify

| Step | What to do | Why |
|------|--------|--------|
| **1. Sample** | Take the main colors from three sources instead of inventing them: ① brand assets (pick colors directly from the logo/existing VI) ② real content images (the dominant colors in product screenshots/photography) ③ cultural context (the color memory the content's theme carries; see the table below) | Picking colors from nothing = drawing lots from the model's priors, and what comes out is always the same few influencer colors; colors sampled from the content come with a built-in "why" |
| **2. Converge** | Use oklch to compress the palette to **2-3 chromatic colors + 1 set of neutrals**. Write the neutrals as a lightness sequence (e.g. L 0.15/0.35/0.65/0.92/0.98), and separate the chromatic colors by an oklch hue angle H ≥60° or a lightness L difference ≥0.3 | Too many colors means chaos; oklch's L channel is perceptually uniform, so a written lightness sequence is a hierarchy system, easier to reason about than a pile of isolated hex values |
| **3. Justify** | Write one sentence on "why this color" in the output comments or delivery notes. Example: "The main color is taken from the ochre in the user's logo, with chroma lowered to 0.08 to simulate ink" | **If you can't write this sentence = you're copying a recipe.** Justification is a self-check gate against slop, not a ritual |

### Print color texture: why low saturation looks more refined than pure screen color

Ink printed on paper never reaches the maximum saturation of screen RGB. The narrower CMYK gamut, paper absorbing ink and ambient light reflection all "press colors toward gray". The "refined feel" the human eye has been trained into by decades of print is essentially this layer of physical grayness. So deliberately lowering chroma in screen design amounts to borrowing the texture memory of print.

| Use | oklch chroma reference | Effect |
|------|------------------|------|
| Large background areas | 0.01–0.04 | Paper-like, easy on the eyes |
| Brand main color/emphasis | 0.08–0.15 | Ink-like, eye-catching enough without looking plastic |
| Small accents (buttons/links) | 0.15–0.22 | Keeps vibrancy, small areas only |
| >0.25 full-bleed | Use with caution | Screen fluorescence, only for deliberately "digital-native" styles like Wrapped/candy |

### Cultural context quick reference: same hue, different context

Choosing a color isn't just choosing a hue; it's choosing the cultural coordinates behind it. Even for "red", where it lands differs enormously:

| Hue | Context A | Context B | The difference |
|------|--------|--------|--------|
| Red | Forbidden City vermilion (leaning orange, grayed, low L low C in oklch, darker and murkier than Coca-Cola red) → traditional/solemn | Coca-Cola red (high-saturation pure red) → consumer/excitement | Lower the chroma and it jumps from the store shelf to the palace wall |
| Blue | Japanese indigo dye/ruri-kon lapis (deep, leaning purple-gray) → handcraft/calm | Tech blue #0066FF family → SaaS/efficiency | The latter is the model's favorite default blue; before using it, ask yourself whether you're drawing lots |
| Green | Matcha/moss green (yellow-leaning, low saturation) → nature/Japanese | Fluorescent green #39FF14 → terminal/hacker | Both green, one drinks tea and one writes code |
| Yellow | Gamboge/mustard (with brown-gray) → vintage print | Warning yellow/Mailchimp yellow → eye-catching/playful | The gray level decides whether it's an old book page or a hard hat |
| White | Cream paper white #F5F0E8 → publications/warm | Pure white #FFF → laboratory/Swiss | A 2% color temperature difference in the background is the dividing line of character |

---

## Web style library (20 styles)

#### Bold styles

**Editorial Brutalism (giant Helvetica pressing down on small body text)** `Bold · 98% fidelity`
- Reference: Bloomberg Businessweek (Richard Turley's 2010-2014 redesign, executed by Code and Theory); the Neue Haas Grotesk lineage
- Fits: media/content publishing, AI product launches, brand site heroes, research report covers, header images for opinion long-reads
- Visual DNA: palette of pure black #000 + pure white #FFF + hyperlink blue #0000EE, accented with signal orange-red #FF433D/terminal green #00A33E. Font Helvetica/Neue Haas Grotesk, a 120px+ giant left-aligned tightly tracked headline pressing directly on 14px small body text, extreme type-size contrast. Layout is a modular grid + 1px rule lines dividing columns, high information density with white space deliberately withheld. Signature elements: rule-line column dividers, hyperlink-blue underlines, large black and white color blocks.
- HTML implementation: pure CSS can reproduce it 1:1. CSS Grid for the modular grid + borders for rule-line columns, clamp() for oversized responsive type + tightened letter-spacing, system Helvetica/Arial stack or Inter as fallback, hyperlinks directly #0000EE underlined. Zero asset dependencies.
- Fonts: Inter (replacing Helvetica/Neue Haas Grotesk), Geist Mono for code
- Specimen: assets/style-specimens/web/01-editorial-brutalism.jpg

**Neo-Brutalism (thick black-outlined cards + high-saturation clashing colors)** `Bold · 95% fidelity`
- Reference: The Verge 2022 redesign (in-house team, PolySans + Mānuka)
- Fits: media/content sites, AI product aggregator pages, event landings, community leaderboard pages, Xiaohongshu-style info cards
- Visual DNA: palette of electric purple #5200FF~magenta #E1306C high-saturation main colors + bright yellow #F8E000 emphasis + pure black #08080D + white, large clashing color blocks deliberately not softened. Font: geometric sans-serif headlines contrasted with serif body text. Layout is a card-based feed, 2-4px thick black outlines, hard color-block zones, almost no rounded corners. Signature elements: thick-outlined cards that flip to a clashing color on hover, an unfinished-interface character.
- HTML implementation: a pure CSS strength. border:3px solid #000 thick outline + box-shadow hard offset shadow (4px 4px 0 #000) + grid/flex card feed + :hover switching background for the clashing-color flip. No 3D/lighting obstacles.
- Fonts: Space Grotesk (replacing PolySans) + any serif such as Fraunces
- Specimen: assets/style-specimens/web/02-neo-brutalism.jpg

**Memphis Maximalism (clashing color blocks + offset overlapping + retro fonts)** `Bold · 72% fidelity`
- Reference: Gucci Vault concept store (Alessandro Michele); the Memphis design movement / Sagmeister's rebellious DNA
- Fits: e-commerce concept stores, creative event pages, brand experiment campaigns, Y2K retro themes, holiday marketing pages
- Visual DNA: palette of retro red/mustard yellow/royal blue/purple/olive green juxtaposed in large clashing areas + a distressed warm beige base, intense and deliberately discordant. Fonts: retro serifs + decorative fonts mixed, print texture, offset overlapping that breaks the grid. Layout is anti-grid collage curation, modules of different sizes staggered and overlapping, like wandering a digital room. Signature elements: clashing color blocks, offset overlapping, unconventional navigation easter eggs.
- HTML implementation: transform:rotate() for offset overlapping + position:absolute for layering + high-saturation background color blocks + retro Google Fonts. Real distressed textures can't be reproduced in CSS; downgrade to flat color blocks + mix-blend-mode/contrast filters to simulate texture. The geometric collage version works; the archival distressed version gets downgraded.
- Fonts: DM Serif Display + Bungee (decorative) + Space Mono
- Specimen: assets/style-specimens/web/03-memphis-maximalism.jpg

**Friendly Geometric Candy (candy-colored raised 3D buttons, gamified)** `Bold · 85% fidelity`
- Reference: Duolingo (Johnson Banks + Monotype, the Feather Bold typeface); anti-Silicon Valley minimalism
- Fits: education and language learning, consumer App landings, gamified products, approachable mass-market products, event sign-up pages
- Visual DNA: palette of Duo green #58CC02 + duck yellow #FFC800 + sky blue #1CB0F6 high-saturation candy colors + white background, rounded and friendly. Font: extra-bold rounded type (a Feather Bold feel). Layout of large rounded cards, raised 3D buttons (a hard bottom shadow = a pressable feel), a mascot slot + progress bubbles. Signature elements: 3D buttons with a 3px solid shadow, a press-down shift animation, extra-round corners.
- HTML implementation: pure CSS. box-shadow:0 4px 0 hard bottom shadow for the raised button + :active translateY(4px) removing the shadow to simulate pressing, large border-radius, flat color blocks. Without image generation, the mascot uses CSS geometric shapes or an emoji placeholder (slight downgrade).
- Fonts: Baloo 2 / Nunito (extra-bold rounded, replacing Feather)
- Specimen: assets/style-specimens/web/04-friendly-candy.jpg

**Pure-CSS Art (pure CSS geometric illustration + responsive morphing easter eggs)** `Bold · 80% fidelity`
- Reference: Lynn Fisher (lynnandtonic.com, a pure CSS art legend, featured by Adobe)
- Fits: personal homepages, creative 404/easter-egg pages, playful brand landings, tech blog header images, designer self-showcases
- Visual DNA: palette of 2-4 high-contrast flat colors (the palette changes at each breakpoint). Font: bold geometric sans-serif headings. The core of the layout is "the picture morphs with the viewport": a set of CSS shapes recombines into different pictures at different breakpoints (e.g. a building whose number of floors changes with screen width). Signature elements: geometric illustration drawn in pure CSS, breakpoint-driven rearrangement easter eggs, zero images.
- HTML implementation: a showcase battlefield for pure CSS, where zero assets is an advantage. Stack geometric shapes with div + border-radius/clip-path/transform/box-shadow, and use @media breakpoints to change shape size and position for the morphing. The difficulty is in the design concept rather than the technology, but every shape has to be carefully hand-built.
- Fonts: Rubik / Archivo (bold geometric, replacing custom fonts)
- Specimen: assets/style-specimens/web/05-pure-css-art.jpg

**Bold Big-Type Editorial (giant black-and-white high-contrast fashion big-type poster)** `Bold · 88% fidelity`
- Reference: the Jacquemus site / Rik Oostenbroek / Domestika; fashion magazine big-type posters
- Fits: fashion e-commerce, portfolios, media features, brand manifesto pages, video course covers, big-type editions of research reports
- Visual DNA: palette of minimal black and white + a single restrained accent color (nude pink #E8C4C0 or true red). Fonts: oversized display sans-serif/high-contrast serif, headings filling the entire screen. Layout of a full-width grid, giant type playing off negative space, 1:1 image-text splits. Signature elements: headlines taking up most of the screen, luxury-level white space, left-right counterpoint typesetting.
- HTML implementation: pure CSS reproduces it perfectly. clamp() giant type + CSS Grid full-width splits + lots of padding for white space + vh units so headings fill the viewport. Without images, use flat color blocks/text blocks in place of fashion editorial shots (slight downgrade, but the layout works).
- Fonts: Archivo Expanded / Anton (display) + Playfair Display (high-contrast serif)
- Specimen: assets/style-specimens/web/06-bold-big-type.jpg

**Cosmic Retro-Futurism (retro-futurist space atlas)** `Bold · 75% fidelity`
- Reference: the Perplexity Comet browser launch site (The Brand Identity: Black/Blue/Cream; a *2001: A Space Odyssey* character)
- Fits: AI product launch sites, tech brand manifesto pages, event countdown pages, futuristic landings, concept launch events
- Visual DNA: palette of pure black #0A0A0A + cream paper white #F0EAD8 + a touch of cobalt-peacock blue #2B4F91, low saturation like an old astronomical atlas. Fonts: high-contrast serif (the feel of a classical astronomical atlas) + white space. Layout of line-drawn orbit/parabola SVG, planet dots, black type on a cream base, antique-book typesetting. Signature elements: SVG celestial orbit lines, cream + blue + black tricolor, large retro serif type, astronomical-atlas texture.
- HTML implementation: pure CSS + SVG reproduces about 80% of the character of the static version. SVG paths draw orbit parabolas + CSS radial positioning of planet dots + three color variables + high-contrast serif. The gap is the full-screen video transition of "space landing on Earth" (the soul of it), downgraded to CSS scroll parallax + SVG orbit rotation as an approximation.
- Fonts: Cormorant Garamond / EB Garamond (high-contrast serif) + Space Mono
- Specimen: assets/style-specimens/web/07-cosmic-retro-futurism.jpg

**Cinematic Sound-Viz Dark (cinematic sound-wave visualization)** `Bold · 72% fidelity`
- Reference: ElevenLabs; film title sequences (Saul Bass-style minimal motion) × audio engineering interfaces
- Fits: audio/voice AI products, music tech sites, podcast platforms, media launch pages, cinema-grade brand heroes
- Visual DNA: palette of pure black #000 background + pure white text + blue-purple gradient accent waveforms. Font: large sans-serif headings, Saul Bass-style minimal. Layout of full-width dark field, sound-wave/spectrum visualization running throughout, giant headings pressing down on waveforms, card-based feature zones. Signature elements: colored audio-waveform bands, title-sequence minimalism, high-contrast black and white + a single gradient, the sound-visualization motif.
- HTML implementation: pure CSS + SVG reproduces 70% of the character (the skeleton is perfect; the waveform is the downgrade point). SVG polyline for a static waveform, or an array of div bars of uneven heights + CSS animation for a "fake waveform" bouncing approximation. Gap: a Web Audio/Canvas spectrum that bounces in real time with the sound can't be reproduced in pure CSS; the static version looks right, but the dynamic soul can't be recovered.
- Fonts: Inter / Sora (large sans-serif)
- Specimen: assets/style-specimens/web/08-cinematic-sound-viz.jpg

**Pixel-Game Side-Scroller (pixel-game side-scrolling narrative)** `Bold · 70% fidelity`
- Reference: Robby Leonardi's interactive résumé (8/16-bit platformer narrative, a tribute to the Nintendo SNES)
- Fits: creative résumés/portfolios, playful brand campaigns, gamified landings, event easter-egg pages, fun personal homepages
- Visual DNA: palette of retro-game multi-segment zones: forest green #4CAF50 grass + sky blue #5DADE2, transitioning to space purple #2C2A4A, volcano orange-red #E8743B, undersea teal #1ABC9C, with a new high-saturation cartoon palette for each "level". Fonts: pixel fonts (8-bit feel) + bold sans-serif. Layout of horizontal/vertical scrolling level scenes, parallax layers, scroll-triggered displacement. Signature elements: color changes per level, pixel aesthetics, parallax scrolling, game-HUD-style UI.
- HTML implementation: pure CSS + a little JS reproduces the skeleton (the original is HTML + CSS + jQuery with no WebGL). Parallax layers via position + scroll displacement, image-rendering:pixelated, CSS frame-by-frame background-position for sprite animation, segmented background colors. Gap: original hand-drawn pixel illustrations of characters/scenes; without image generation, replace them with simple pixel icons assembled from CSS squares (the art is downgraded, the technology isn't).
- Fonts: Press Start 2P / VT323 (pixel fonts) + Inter
- Specimen: assets/style-specimens/web/09-pixel-side-scroller.jpg


#### Neutral styles

**Bauhaus Geometric (Bauhaus geometric logo + flat illustration system)** `Neutral · 90% fidelity`
- Reference: the Khan Academy rebrand (hexagon + petal logomark + the Wonder Blocks design system); Bauhaus geometric composition
- Fits: education course sites, brand logo systems, infographics, child-friendly products, event key visuals
- Visual DNA: palette of the primary color family: Bauhaus red #E63946/yellow #FFB703/blue #0077B6 + black and white, flat color blocks pieced together. Font: geometric sans-serif (rounded geometric feel). Layout builds illustrations from basic geometric units of circle/triangle/square, aligned to a grid, modular puzzle pieces. Signature elements: purely geometric logomarks, flat gradient-free illustration, primary color block composition.
- HTML implementation: pure CSS handles all the geometry. border-radius:50% for circles, clip-path/border for triangles, square divs assembled into geometric illustrations, CSS Grid for grid alignment, flat color fills with no assets needed. Illustrations are hand-built from CSS shapes or inline SVG geometric paths.
- Fonts: Poppins / Manrope (rounded geometric, replacing Wonder Blocks)
- Specimen: assets/style-specimens/web/10-bauhaus-geometric.jpg

**Dark Editorial (dark two-tone sidebar developer portfolio: dark background + single neon accent + monospace)** `Neutral · 96% fidelity`
- Reference: Brittany Chiang (brittanychiang.com v4, the de facto standard for dev portfolios)
- Fits: portfolio personal homepages, developer-facing products, tech brand sites, résumé pages, AI tool landings
- Visual DNA: palette of deep ink green/navy background #0A192F + slate gray text #8892B0 + a single neon teal accent #64FFDA. Fonts: sans-serif body + monospace (numbers/labels). Layout of a fixed left sidebar navigation + scrolling right main area in two columns, section numbers 01/02, link underlines sliding in on hover. Signature elements: a single accent color, monospace numbered labels, sidebar anchor highlighting.
- HTML implementation: pure CSS reproduces it completely. position:sticky for the fixed sidebar + CSS Grid two columns + a single accent variable + monospace labels + :hover underline sliding in via transform. Zero assets, pure layout and micro-interaction.
- Fonts: Inter + JetBrains Mono (monospace)
- Specimen: assets/style-specimens/web/11-dark-editorial.jpg

**Warm Editorial (warm publication: cream paper base + terracotta orange + mixed serif and sans-serif)** `Neutral · 97% fidelity`
- Reference: Anthropic / Claude (DBCo + Geist Studio, Styrene × Tiempos); Penguin/Pelican paperback typesetting
- Fits: AI product sites, brand official sites, long-form reading pages, Orange Book e-books, research reports, training materials
- Visual DNA: palette of cream paper base #F5F0E8 + terracotta orange #CC785C/#D97757 accents + near-black text #191919, warm and low saturation. Fonts: serif headings (Tiempos feel) × sans-serif body (Styrene feel) mixed. Layout of a book-like single-column reading flow, comfortable line height, restrained dividers. Signature elements: warm paper-like base, terracotta orange, publication-grade typographic rhythm.
- HTML implementation: pure CSS reproduces it 100%, zero assets. Background color variables + mixed serif and sans-serif font stacks + max-width to limit reading width + line-height 1.7 for comfortable leading.
- Note: this is also the look the model most easily falls into without thinking (Claude's own palette, see `references/content-guidelines.md`). Using it is fine, provided you chose it rather than slid into it: don't crowd all three directions here, and if the look ledger shows it was used recently, switch to another.
- Fonts: Fraunces / Newsreader (replacing the Tiempos serif) + Inter (replacing Styrene)
- Specimen: assets/style-specimens/web/12-warm-editorial.jpg

**Glassmorphism Bento (Linear-style dark glow + Bento grid)** `Neutral · 85% fidelity`
- Reference: Linear / Cursor ("The Linear Look", a phenomenon-level school; Frontend Horse has a code recipe)
- Fits: SaaS/AI product sites, developer tools, tech brand heroes, product feature showcases, dark dashboard demos
- Visual DNA: palette of near-black background #08090A + desaturated blue-purple brand #5E6AD2 + low-saturation cyan-purple glimmer gradient #4EA7FC→#B59AFF. Font: geometric sans-serif with negative tracking, compact. Layout of bento-box grid blocks, hairline dividers, glassmorphism cards. Signature elements: glowing gradient borders on a dark background, bento blocks, light streamers, frosted glass.
- HTML implementation: pure CSS reproduces it strongly. box-shadow/filter blur + radial-gradient for glow halos, backdrop-filter:blur for glassmorphism, conic/linear-gradient borders, CSS Grid to assemble the bento. The only gap is "real product UI screenshots"; replace them with simplified fake UI built from color blocks + text (this part is downgraded).
- Fonts: Inter / Geist (negative tracking) + Geist Mono
- Specimen: assets/style-specimens/web/13-glassmorphism-bento.jpg

**Angled Fluid Gradient (angled fluid gradient band)** `Neutral · 92% fidelity`
- Reference: Stripe (the signature angled gradient banner, the Söhne typeface customized by Klim)
- Fits: SaaS/fintech landing pages, brand site heroes, product launch pages, event banners, AI product marketing pages
- Visual DNA: palette of a multicolor fluid gradient (indigo #635BFF → cyan → pink → warm orange) as the hero background + pure white content area + near-black text. Font: refined sans-serif (Söhne feel). Layout of angled split color blocks (skewed corner zones), a gradient hero pressing on a structured grid of body content. Signature elements: angled boundaries, multicolor fluid gradient, a rational grid holding down an expressive gradient.
- HTML implementation: pure CSS. transform:skewY() or clip-path:polygon() for angled zones, layered multicolor linear-gradient (CSS animation can add a slow flow) for the fluid gradient band, Grid for the structured body below. Zero assets.
- Fonts: Inter / Hanken Grotesk (replacing Söhne)
- Specimen: assets/style-specimens/web/14-angled-fluid-gradient.jpg

**Utility-First Colorful Docs (utilitarian rainbow-categorized docs)** `Neutral · 98% fidelity`
- Reference: Tailwind CSS Docs (Sky/Cyan brand colors + rainbow hue bars for feature categories)
- Fits: technical documentation, API references, design system sites, tutorial sites, developer knowledge bases, SaaS help centers
- Visual DNA: palette of Sky blue #38BDF8 brand + teal→cyan→sky blue-green gradient + Slate grayscale #0F172A/#64748B/#F8FAFC, with the docs using rainbow hue bars to distinguish feature categories (pink #EC4899/purple #A855F7/green #10B981/orange). Fonts: clean sans-serif + monospace code. Layout of left sidebar navigation + center body + right TOC in three columns, colorfully highlighted code blocks, category color tags. Signature elements: blue-green gradient hero, rainbow category colors, three-column docs skeleton, syntax-highlighted code blocks.
- HTML implementation: pure CSS reproduces 98% (it is itself the docs of a CSS framework). Grid three columns + linear-gradient blue-green hero + category color variables + code-block syntax colors via colored spans. Inter is open source; only the dark mode toggle/copy needs light JS. Zero lighting/3D/hand-drawing.
- Fonts: Inter + JetBrains Mono / Fira Code (code)
- Specimen: assets/style-specimens/web/15-utility-colorful-docs.jpg

**Terminal-Core Soft-Futurism (monospace + isometric cubes)** `Neutral · 80% fidelity`
- Reference: Cursor (Anysphere); developer terminal aesthetics × Teenage Engineering industrial minimalism
- Fits: AI coding tool sites, CLI product landings, developer infrastructure, tech brand heroes, terminal-type products
- Visual DNA: palette of charcoal #0B0D14 background + warm white text #F2F0EF + a restrained blue-purple gradient accent on buttons and glows. Fonts: monospace as the protagonist (command-line feel) + sans-serif in support. Layout of command-line/code blocks in the foreground, bento zones, 2.5D isometric cube diagrams. Signature elements: monospace command lines, isometric projection cubes, warm white × charcoal, restrained gradient glows, industrial minimalism.
- HTML implementation: pure CSS reproduces 80%. Monospace code blocks + dark bento + box-shadow glows; 2.5D isometric cubes hand-built with CSS 3D transforms (rotateX/Y + skew) or SVG isometric projection. Gap: a clickable multi-interface demo needs JS + stitched fake UI. No hard requirement for WebGL.
- Fonts: Geist Mono / JetBrains Mono (protagonist) + Inter (support)
- Specimen: assets/style-specimens/web/16-terminal-core.jpg


#### Quiet styles

**Functional Brutalism (functionalist grid community: gray line dividers + system fonts + blue links)** `Quiet · 98% fidelity`
- Reference: Are.na / Lobsters / Quartz; Müller-Brockmann's grid brought to digital + Tufte's information density
- Fits: community/UGC platforms, content aggregators, documentation knowledge bases, mobile-first content feeds, geek-oriented products
- Visual DNA: palette of near-white background #FBFBFB + black text + 1px gray dividers #E0E0E0 + classic link blue #0000EE/visited purple. Font: system font stack (-apple-system/no decoration). Layout of high-density information lists, thin gray line columns, minimal white space, compact line spacing. Signature elements: hairline gray dividers, blue links, system fonts, information density first.
- HTML implementation: the easiest to reproduce in pure CSS; this is the true nature of the Brutalist Web. border-bottom:1px gray line lists + system-ui font stack + compact padding + blue links. Needs almost no assets or JS, pure structure.
- Fonts: system-ui system font stack / IBM Plex Sans (fallback)
- Specimen: assets/style-specimens/web/17-functional-brutalism.jpg

**Gallery Dark (dark gallery framing: deep black negative space + single-column large images + small EXIF text)** `Quiet · 75% fidelity`
- Reference: Glass (glass.photo) / Bottega Veneta; the art gallery darkroom + Apple Photos' content-first approach
- Fits: photography portfolios, luxury e-commerce, immersive visual content showcases, personal gallery pages, high-end product displays
- Visual DNA: palette of pure black background #0A0A0A + the artwork itself providing the only color + very faint gray small EXIF text #666. Font: very thin small sans-serif. Layout of single centered column of large images, huge negative-space framing, small metadata text below each image. Signature elements: darkroom black background, content-first UI that recedes, EXIF-style small footnotes, large images owning the viewport.
- HTML implementation: pure CSS reproduces the layout skeleton. Pure black background + centered max-width single column + huge padding for framing white space + small metadata text. The gap is the "real photographic work" itself: replacing it with placeholder images/flat color blocks loses the soul, but the darkroom atmosphere and layout are 100% buildable.
- Fonts: Inter (thin weight 300) / Cormorant (optional serif for a luxury feel)
- Specimen: assets/style-specimens/web/18-gallery-dark.jpg

**Swiss Monochrome (extreme Swiss black and white: Vercel-style pure black and white + Geist + sharp corners)** `Quiet · 98% fidelity`
- Reference: Vercel / Next.js Docs (the in-house Geist, now open source); Massimo Vignelli's less is more
- Fits: developer tool documentation, tech brand official sites, AI product sites, SaaS landing pages, minimal research reports
- Visual DNA: palette of pure black #000 + pure white #FFF + grayscale #888, zero color or just a touch of blue links. Fonts: Geist geometric sans-serif + Geist Mono. Layout of sharp right angles (no rounded corners, or very small), high contrast, precise grid, restrained white space. Signature elements: pure black and white, sharp corners, the Geist typeface, triangle/arrow geometric marks.
- HTML implementation: pure CSS reproduces it 100%; Geist is open source and can be referenced directly. CSS Grid precise grid + pure black and white variables + border-radius:0 sharp corners + hairline borders. This is HTML's most comfortable minimal home turf, with zero asset dependencies.
- Fonts: Geist + Geist Mono (Vercel's open-source originals)
- Specimen: assets/style-specimens/web/19-swiss-monochrome.jpg

**Kenya Hara White Gallery (Japanese white-space white-cube gallery)** `Quiet · 80% fidelity`
- Reference: Cosmos (cosmos.so) / the Aesop site; Kenya Hara's emptiness of "white" + a hybrid with the Swiss grid
- Fits: high-end e-commerce, creative galleries, content curation platforms, designer portfolios, brand boutiques, moodboard sites
- Visual DNA: palette of near-total white background #FAFAFA + pure black text #0A0A0A + very faint gray dividers #EFEFEF, with content images providing all the color and the UI receding into the background. Font: minimal system/geometric sans-serif in small sizes with wide tracking. Layout of a masonry waterfall grid, extreme white space, faint gray hairline separators, Eastern emptiness. Signature elements: white-cube aesthetics, luxurious white space, content-first UI that recedes, waterfall-feed curation.
- HTML implementation: pure CSS reproduces the static layout (what distinguishes it from the dark gallery is the "white"). CSS columns or Grid for masonry + near-white variables + large padding for white space + faint gray separators. The gap is Lenis/GSAP silky inertial scrolling and image entrance easing (60% of the refined feel lives here); CSS has only basic transitions, so the motion layer is downgraded.
- Fonts: Inter (thin weight) / Cooper Hewitt (the same open-source font Aesop uses)
- Specimen: assets/style-specimens/web/20-kenya-hara-white-gallery.jpg


## PPT style library (20 styles)

#### Bold styles

**Neo-Swiss Billboard Editorial (new Swiss big-type poster)** `Bold · 98% fidelity`
- Reference: the Big-Number Editorial school of AI/SaaS pitch decks such as Scribe $75M and Flock Safety $47M; Bloomberg Businessweek infographics; Pentagram
- Fits: fundraising pitches, QBRs/business reviews, annual trend retrospectives, key product launch slides
- Visual DNA: palette = pure white (#FFFFFF) or near-black (#0A0A0A) background + a single high-saturation accent (electric blue #2D5BFF/fluorescent green #00E676/brand orange #FF6B2C) + neutral grid lines #E5E5E5. Font = oversized bold sans-serif, headings taking half the screen, numbers in tabular-nums monospaced figures with tightened tracking. Masters = ① big color-block section slide with one word ② giant number taking half the screen (3.2x) + small note ③ left-right split comparison ④ full-bleed flat line/bar chart. Signature = billboarding big type, strict baseline grid, big color-block section slides
- HTML implementation: clamp() for oversized numbers; CSS Grid for the strict grid; background-color for big color-block section slides; line/bar charts with plain divs + CSS or inline SVG (sharper than pasted images); number alignment with font-variant-numeric:tabular-nums. Zero illustration, zero 3D
- Fonts: Inter / Geist / Söhne replacing Neue Haas Grotesk; Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/01-neo-swiss-billboard.jpg

**Black Big-Number Stage (black-background giant-number theater)** `Bold · 97% fidelity`
- Reference: Steve Jobs' 2007 iPhone keynote, Lei Jun's Xiaomi SU7 Ultra launch event, Spotify Wrapped, Presentation Zen (Garr Reynolds)
- Fits: product launch keynotes, thought-leadership talks, all-hands town halls, emotional year-in-review
- Visual DNA: palette = pure black #000000 background + pure white #FFFFFF text in high contrast, with only one brand accent highlight per slide (Xiaomi orange #FF6900/Spotify green #1ED760/Apple blue #2997FF). Font = bold geometric sans-serif, one word or one oversized number per screen filling the view, tightened tracking. Masters = ① title slide, a single centered line of big type on black ② data climax slide, giant number + unit + one-line note ③ left-right two-column spec comparison (accent vs gray) ④ single-slogan slide. Lots of negative space
- HTML implementation: white on black in a few lines of CSS; giant numbers with clamp() + flex centering; accent highlight in a separate span; left-right comparison with CSS Grid two columns + highlighted bars; tabular-nums. Dropping the product photos for pure text actually gets closer to the essence of Zen
- Fonts: Geist / Inter / Source Han Sans replacing SF Pro
- Specimen: assets/style-specimens/ppt/02-black-big-number-stage.jpg

**Mono-Brand Type-as-Hero (high-saturation single-color brand clash poster)** `Bold · 96% fidelity`
- Reference: the Spotify Wrapped visual system, Mailchimp Brand Book (Collins), a modern remake of Netflix red and black, the COLLINS brand systems
- Fits: brand/marketing strategy, campaign presentations, town hall culture slides, event key visuals
- Visual DNA: palette = a single brand main color as a full-bleed background (Spotify green #1ED760/Mailchimp yellow #FFE01B/Netflix red #E50914) + contrasting black or white type, two clashing layers. Font = oversized type as the main visual (type-as-hero), filling top to bottom. Masters = ① full color-block background + reversed-out giant type ② two color blocks split top/bottom or left/right ③ giant number filling the slide. Signature = single color full-bleed, type as image, high-contrast clashing colors
- HTML implementation: full-bleed background-color; oversized type with clamp() filling the slide; two colors via two 100vh color blocks; type as image relies on font-weight 900 + negative letter-spacing. Flat color blocks, zero assets, the most satisfying in native HTML
- Fonts: Inter / Manrope / Archivo (extra bold) replacing Circular/Cavendish
- Specimen: assets/style-specimens/ppt/03-mono-brand-type-hero.jpg

**Full-Bleed Gradient Manifesto (full-bleed gradient manifesto layout)** `Bold · 82% fidelity`
- Reference: Zuora's "Tell a Different Story" sales deck (as broken down by Andy Raskin), Nike's "Just Do It" campaign, National Geographic spreads
- Fits: vision slides in sales proposals, brand manifestos, keynote turning-point slides, single mission/vision slides
- Visual DNA: palette = full-bleed CSS gradient (warm orange → magenta / deep blue → cyan) or solid color bleed + reversed-out big manifesto type + hashtag slogan (#shifthappens). Font = heavy all-caps sans-serif slogans running across. Masters = ① full-bleed gradient + centered reversed-out manifesto ② promised-land vision slide ③ customer logo wall. Signature = full-bleed, reversed-out big slogans, hashtag slogans
- HTML implementation: full-bleed linear-gradient/radial-gradient (no particles/lighting; pure CSS gradients are allowed); reversed-out text centered with position; logo wall as a grid of grayscale SVGs/text placeholders. The parts that originally relied on large documentary photos are downgraded to a CSS gradient background + big type; the missing photos lower fidelity by about 15%
- Fonts: Archivo / Anton / Manrope (extra bold)
- Specimen: assets/style-specimens/ppt/04-full-bleed-gradient-manifesto.jpg

**Candy-Color Lecture Stage (CS50 single-concept candy stage)** `Bold · 94% fidelity`
- Reference: Harvard CS50 (David Malan), the Lessig Method/Takahashi method, Presentation Zen
- Fits: educational course slides, technical lectures, concept explanations, coding instruction
- Visual DNA: palette = deep black background #0A0A0A + rotating high-saturation candy-colored big type (magenta #FF2D95/cyan #00E5FF/bright yellow #FFD500/green #39FF14). Font = oversized sans-serif floating in the center, one concept per screen, very little text. Masters = ① a single candy-colored big word on deep black ② monospace code block with syntax highlighting ③ big type with a stage spotlight feel. Signature = candy-colored big type floating on deep black, monospace code highlighting, strong stage spotlight, very little text
- HTML implementation: deep black background + single-color oversized type with clamp() centered; code blocks with pre + monospace + colored spans for syntax highlighting; the spotlight feel uses a very faint radial-gradient vignette (not particle light effects). High fidelity
- Fonts: Inter extra bold + JetBrains Mono (code)
- Specimen: assets/style-specimens/ppt/05-candy-lecture-stage.jpg

**Playful Maximalist Editorial (Collins-style) (playful hand-drawn minimalism)** `Bold · 75% fidelity`
- Reference: Mailchimp Brand Book (Collins 2018), the New Yorker cartoon character, Cooper rounded serif, Cavendish fluorescent yellow
- Fits: brand decks with attitude, creative agency proposals, culture-oriented town halls, marketing pages that push back against SaaS minimalism
- Visual DNA: palette = Cavendish fluorescent yellow #FFE01B in large areas + black + a few clashing colors, anti-SaaS minimalism. Font = Cooper-style rounded serif headings (playful) + magazine-style white-space layout. Masters = ① fluorescent yellow full background + quirky headline ② magazine-style irregular white-space layout ③ big-type joke copy. Signature = fluorescent yellow, rounded serif, playful layout, a quirky hand-drawn character (downgraded to geometric color blocks/emoji instead of real illustrations)
- HTML implementation: fluorescent yellow background; rounded serif font-family; asymmetric Grid for magazine white space. The core element of hand-drawn gorillas/illustrations can't be made without AI image generation; it's downgraded to CSS geometric color blocks + large emoji + text blocks with irregular transform rotations, and the missing illustrations lower fidelity by about 20%
- Fonts: Fraunces (adjustable roundness) / Bree Serif replacing Cooper; Inter for body
- Specimen: assets/style-specimens/ppt/06-playful-collins-editorial.jpg

**Irreverent Pop (Reddit-style) (irreverent meme-driven pop edition)** `Bold · 80% fidelity`
- Reference: the Reddit Ads sales deck (listed by Dock as the one with the most personality), David Carson-style irreverent typesetting, 90s web retro, Memphis playfulness
- Fits: Gen Z brands, meme-driven marketing decks, community/creator-oriented work, proposals that dare to be unserious
- Visual DNA: palette = Reddit orange-red #FF4500 + clashing colors, 90s web retro colors. Font = mixed/grid-breaking David Carson-style typesetting, meme-heavy colloquial copy. Masters = ① fun slide with big meme type ② facts slide, a rhythmic turn to serious data ③ colloquial headings. Signature = grid-breaking mixed typesetting, orange-red, meme colloquialism, a fun→facts rhythm reversal, retro web texture
- HTML implementation: deliberately break the grid with transform rotations/overlapping positioning/mixed type sizes; orange-red + clashing color blocks; retro texture with thick black border + hard box-shadow (no blur). Custom meme illustrations are downgraded to emoji + geometric collage, but the mixed typesetting itself can be reproduced in HTML
- Fonts: Archivo / Space Grotesk + Inter mixed in for contrast
- Specimen: assets/style-specimens/ppt/07-irreverent-pop.jpg

**Maximalist 3D-Type (Wrapped-style) (Y2K inflated big type)** `Bold · 78% fidelity`
- Reference: Spotify Wrapped 2022/2023/2025, Memphis clashing colors, Y2K/Maximalism, duotone portrait gradients
- Fits: year-in-review (emotional, viral-oriented), personalized data cards, vertical social share cards, brand year-end pieces
- Visual DNA: palette = high-saturation clashing full-bleed backgrounds (magenta + cyan + orange) + Spotify green accent + duotone two-color gradients. Font = giant numbers filling top to bottom, years/numbers with a 3D inflated/metallic texture. Masters = ① clashing full-bleed + giant inflated number ② duotone portrait/color-block background + reversed-out big type ③ vertical shareable card. Signature = giant inflated 3D numbers, clashing full-bleed, duotone gradients, metallic year texture, vertical story cards
- HTML implementation: clashing full-bleed background; 3D inflated numbers via layered CSS text-shadow + transform:perspective or SVG + stroke for depth (not real 3D rendering); duotone via mix-blend-mode + gradient over grayscale placeholder blocks. The metallic texture is downgraded to gradient-filled text with background-clip:text, lowering fidelity by about 15%
- Fonts: Archivo Black / Anton extra bold + Clash Display for numbers
- Specimen: assets/style-specimens/ppt/08-y2k-inflated-wrapped.jpg


#### Neutral styles

**Bento Grid (bento-box modular grid)** `Neutral · 95% fidelity`
- Reference: the Apple Keynote Bento Grid era, the new generation of MBB Bento/Big-Type decks (2024-2026), the Stripe annual report metric card matrix, Pitch.com QBR templates
- Fits: product feature summaries, consulting/QBR data reports, sales results slides, town hall metrics slides
- Visual DNA: palette = light gray/cream background (#F5F5F7/cream) or near-black background + brand main color + 1-2 accent colors, cards with light zoned backgrounds + rounded corners + subtle outlines/subtle shadows. Font = oversized display headings + regular body, strong weight contrast, tabular figures for KPI numbers. Masters = ① title slide, one giant sentence + white space ② bento slide, 2×2/3-column cards of uneven heights with one insight per card (number/line icon/sparkline) ③ one-insight oversized number slide. Signature = uneven-height card grid, rounded corners with subtle outlines, breathing room
- HTML implementation: CSS Grid grid-template-areas for the uneven-height bento; cards with border-radius + subtle box-shadow + 1px hairline; sparklines in inline SVG; line icons with inline SVG stroke. Zero pasted images
- Fonts: Inter / Geist + Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/09-bento-grid.jpg

**Dark Hairline Terminal (Neo-Swiss dark terminal aesthetics)** `Neutral · 94% fidelity`
- Reference: the Linear pitch deck, Vercel's design language, CS50 deep-black stage course slides; fonts Inter Tight + JetBrains Mono
- Fits: developer tool/technical product launches, technical pitches, engineering-oriented reports
- Visual DNA: palette = near-black background (#0D0D0F/#111113) + hairline #262629 grid + a single purple-blue accent (#5B5BD6/#7C7CFF). Font = Inter Tight headings + JetBrains Mono for labels/data. Masters = ① minimal title slide with one sentence + a small mono label ② data grid separated by hairlines ③ feature list with mono labels. Signature = 1px hairline grid, single monospace labels, extreme white space, near-black rather than pure black
- HTML implementation: near-black background + border:1px solid hairline grid; mono labels with a monospace font-family; glimmer via very faint box-shadow/border highlight rather than real light effects (a downgrade that steers clear of the cyber-neon no-go zone). Be careful to avoid the #0D1117 dark-blue no-go zone and use a neutral near-black
- Fonts: Inter Tight + JetBrains Mono / IBM Plex Mono
- Specimen: assets/style-specimens/ppt/10-dark-hairline-terminal.jpg

**Two-Font Consulting (Bower-style) (two-font consulting edition)** `Neutral · 90% fidelity`
- Reference: the McKinsey 2019 brand system (designed by Wolff Olins, Bower serif + sans-serif), BCG Executive Perspectives, deep blue thin-line patterns
- Fits: consulting reports, executive briefings, industry research, proposals from authoritative institutions
- Visual DNA: palette = deep blue (#051C2C/McKinsey deep blue) × white binary + a single brand color highlight (BCG green #00805A), a warm gray background with breathing room. Font = characterful serif headings (Bower-style) set in high contrast beside sans-serif body. Masters = ① conclusion-style action title in the top left ② blue thin-line pattern decoration ③ magazine-style left-right division of labor (conclusion text + visual) ④ big-number data-point cards. Signature = high-contrast serif × sans-serif, deep blue thin-line pattern, action titles, warm gray refinement
- HTML implementation: two font-families side by side (serif headings + sans-serif body); thin-line patterns with repeating-linear-gradient or SVG lines; data-point cards in pure CSS; grayscale photo treatment can be omitted when there are no photos. The blue-purple edge shimmer is downgraded to a solid edge
- Fonts: Playfair Display / Fraunces serif headings + Inter body (replacing Bower)
- Specimen: assets/style-specimens/ppt/11-two-font-consulting.jpg

**Diagram-Driven Isotype (enterprise diagram-and-arrow edition)** `Neutral · 88% fidelity`
- Reference: Salesforce sales decks, the Isotype (Otto Neurath) lineage, Gene Zelazny's *Say It With Charts*, Hans Rosling/Gapminder
- Fits: platform/architecture explanations, customer journeys, process methodologies, ecosystem maps
- Visual DNA: palette = enterprise blue color blocks + distinct colors per product line + iconized capability grid. Font = clear sans-serif. Masters = ① horizontal customer-journey arrow flow ② layered platform architecture diagram ③ iconized capability grid ④ 2×2/waterfall/pyramid structure diagrams. Signature = arrow flows, layered architecture boxes, Isotype icon grids, the process as the narrative
- HTML implementation: arrow flows with Flexbox + CSS clip-path triangles or SVG arrows; architecture layers with nested bordered divs; icons in inline SVG with uniform strokes; waterfall/pyramid with Grid + angled cuts. Bubble charts can use CSS circles + positioning. Pure vector drawing
- Fonts: Inter / IBM Plex Sans (chart-friendly)
- Specimen: assets/style-specimens/ppt/12-diagram-isotype.jpg

**Diagrammatic Minimalism (single master-diagram concept explainer)** `Neutral · 95% fidelity`
- Reference: Simon Sinek's Golden Circle TED talk, Bauhaus geometric abstraction, the information-architecture idea of "one diagram commands the whole room"
- Fits: theoretical framework explanations, TED-style idea spreading, model/methodology visualization, single-concept keynotes
- Visual DNA: palette = minimal white/light background + black + 1 accent color, flat geometric colors. Font = sans-serif, uppercase labels embedded in the shapes. Masters = ① a single geometric master diagram (concentric circles/triangle/matrix) carrying every concept ② arrows from the inside out ③ contrasting cases. Signature = a single geometric master diagram, nested concentric circles/triangles, uppercase labels, one diagram carrying the concept
- HTML implementation: concentric circles with nested border-radius:50% divs or SVG circles; triangles with clip-path/SVG polygon; arrows with SVG markers; labels absolutely positioned on the shapes. Pure geometry, reproduced perfectly in HTML
- Fonts: Manrope / the Futura family (Jost as the open-source substitute), geometric feel
- Specimen: assets/style-specimens/ppt/13-diagrammatic-minimalism.jpg

**Narrative Sparkline (Duarte-style) (sparkline narrative waveform)** `Neutral · 91% fidelity`
- Reference: the Sparkline narrative map in Nancy Duarte's *Resonate*, Al Gore's *An Inconvenient Truth*, Duarte Inc. data storytelling
- Fits: talk structure design, change narratives, before/after comparisons, data story arcs
- Visual DNA: palette = dark or white background + brand orange emphasizing turning points + grayed-out comparisons. Font = sans-serif, annotation points. Masters = ① an oscillating waveform line running across the full screen ② text annotation points on the waveform ③ comparison waveforms stacked top and bottom ④ a single data line suspended alone on full black ⑤ step-by-step reveal. Signature = a waveform line running across, annotation points on the waveform, orange turning points, comparison waveforms, a curve that climbs out of the frame
- HTML implementation: waveform line as an inline SVG path (smooth Bézier); annotation points positioned with SVG circle + text; comparison waveforms as two paths top and bottom; reveal via CSS animation of stroke-dashoffset. Pure SVG drawing, no assets
- Fonts: Inter + Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/14-narrative-sparkline.jpg


#### Quiet styles

**Assertion-Evidence / Tufte information design** `Quiet · 93% fidelity`
- Reference: Michael Alley's Assertion-Evidence (empirically validated at Penn State), McKinsey/BCG action titles, Edward Tufte's data-ink ratio, Barbara Minto's Pyramid Principle
- Fits: academic/engineering reports, data-rigorous consulting slides, policy research reports, technical reviews
- Visual DNA: palette = white/very light gray background + black body text + a single restrained accent color (deep blue/brick red). Font = full-sentence headings (not noun phrases), a single image owning the space beneath the heading, text annotations embedded in the image. Masters = ① full-sentence action title ② single-image evidence beneath the heading ③ zero bullets. Signature = full-sentence headings, single-image evidence, embedded annotations, zero chartjunk, high data-ink ratio
- HTML implementation: full-sentence headings rely on typographic hierarchy; charts drawn as minimal lines/scatter plots in pure CSS/inline SVG (remove grid lines and legends, position annotation text directly beside the data points); zero decoration. Tufte's restraint is exactly HTML's strength
- Fonts: Source Serif / Lora headings + Inter body (two fonts, reading-grade)
- Specimen: assets/style-specimens/ppt/15-assertion-evidence.jpg

**Institutional Swiss Minimal (Swiss institutional minimalism)** `Quiet · 96% fidelity`
- Reference: Sequoia's official 10-slide pitch template, Airbnb's 2009 seed-round deck, the Müller-Brockmann grid, Massimo Vignelli
- Fits: investment pitches, standard business proposals, problem-solution narratives, de-decorated brand proposals
- Visual DNA: palette = pure white background + black and gray body text + a single brand accent (Airbnb coral red #FF5A3C/neutral blue). Font = Helvetica-family sans-serif, headings a single medium-sized bold sentence, body in short sentences with generous spacing. Masters = ① centered logo + slogan ② a one-sentence heading band at the top + 3 parallel columns below (Problem/Solution in three points) ③ layered TAM big numbers ④ 2×2 competitor matrix. Signature = top heading band, three parallel columns, single-color emphasis, 2×2 matrix
- HTML implementation: Flexbox for three parallel columns; the 2×2 matrix drawn with pure CSS Grid + borders; TAM layers with nested divs or concentric squares; one message per slide. Almost pure typographic grid, an ideal subject for HTML
- Fonts: Inter / Helvetica Now replacing Helvetica; Inter for body
- Specimen: assets/style-specimens/ppt/16-institutional-swiss.jpg

**Editorial Longform (magazine editorial long-form flow)** `Quiet · 95% fidelity`
- Reference: the Stripe Annual Letter ($1.9T), Amazon's six-page narrative memo, Benedict Evans' "X eats the world", Stripe Press
- Fits: annual letters/retrospective narratives, in-depth long-form thought pieces, internal updates, research-report-style reading material
- Visual DNA: palette = cream/off-white background (#FBFAF8) + deep ink text + brand color accent (Stripe purple #635BFF). Font = serif or high-quality sans-serif, prose paragraphs + inline data cards, with oversized display numbers interspersed. Masters = ① masthead big heading ② multi-column prose + inline metric cards ③ oversized-number paragraph anchors. Signature = publication reading rhythm, inline data cards, restrained white space, prose rather than bullets
- HTML implementation: multiple columns with column-count or Grid; inline data cards embedded in the body via float/inline-block; serif body with max-width limiting line length to 65ch; oversized numbers interspersed. Pure typesetting, zero assets
- Fonts: Newsreader / Source Serif body + Inter in support; tabular numbers
- Specimen: assets/style-specimens/ppt/17-editorial-longform.jpg

**Humanist Rounded Cards (Khan-style) (humanist rounded cards)** `Quiet · 80% fidelity`
- Reference: the Khan Academy Wonder Blocks design system, Source Serif Pro serif, forest green brand, friendly humanism
- Fits: education products, approachable course slides, charity/nonprofit decks, warm brand proposals
- Visual DNA: palette = forest green #14BF96/#0A5C4B + off-white background + warm supporting colors, soft and easy on the eyes. Font = Source Serif headings (humanist feel) + sans-serif body. Masters = ① groups of rounded card components ② serif heading + approachable body ③ real photography slot (downgraded to green-family geometric/rounded color blocks). Signature = forest green, serif headings, large rounded cards, humanist warmth, an imperfect approachable texture
- HTML implementation: large border-radius cards + soft box-shadow; serif heading font-family; warm off-white background. The real teacher-and-student photography can't be done without AI image generation, so it's downgraded to green-family geometric illustration blocks/large rounded solid placeholders + emoji people; the missing photos lower fidelity by about 18%
- Fonts: Source Serif 4 headings + Nunito Sans / Inter body (Nunito's roundness echoes the humanism)
- Specimen: assets/style-specimens/ppt/18-humanist-rounded-cards.jpg

**Dense Research Report (Meeker-style) (dense research report charts)** `Quiet · 92% fidelity`
- Reference: Mary Meeker's *Internet Trends* (BOND), CB Insights' *State of AI*, McKinsey Global Institute's *Year in Charts*, FT/Bloomberg data journalism
- Fits: trend research reports, industry data retrospectives, dense data reports, market maps
- Visual DNA: palette = white background + brand color (BOND/CB Insights bright blue #0066FF) as a stepped single-color highlight with everything else grayed out, almost zero white space. Font = conclusion-sentence headings, a density of 1 chart per slide, tiny source footnotes. Masters = ① conclusion-sentence heading + one full-slide chart ② logo-grid market map ③ big-number KPI cards ④ dense multi-chart grid + footnotes. Signature = conclusion-sentence headings, zero-white-space research report feel, stepped single-color highlights, logo market maps, disciplined source footnotes
- HTML implementation: all the dense charts drawn in pure CSS/inline SVG (bar/line/stacked/scatter); logo market map with Grid + text/SVG placeholder cells; KPI cards in CSS; small footnote text. Extreme information density is exactly what HTML is good at, with zero assets
- Fonts: Inter + IBM Plex Sans + tabular Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/19-dense-research-report.jpg

**All-Text Manifesto (Netflix/Amazon-style) (all-text manifesto memo)** `Quiet · 97% fidelity`
- Reference: the Netflix Culture Deck (2009, 125 slides), Amazon's six-page narrative memo (Bezos), Tufte's anti-PowerPoint stance, Matthew Carter's reading-grade typography
- Fits: culture manifestos, values presentations, in-depth memos, anti-PPT pure-document presentations
- Visual DNA: palette = pure white or pure black background + a single accent color (Netflix red #E50914) as the only highlight, extremely restrained. Font = reading-grade typesetting, one point per slide, punchy assertions/pure prose with zero bullets and zero images. Masters = ① full background + punchy assertion ② colloquial, candid paragraphs ③ highlighted policy terms (Keeper Test) ④ six pages of prose + appendix table. Signature = pure text with one point per slide, zero images and zero bullets, single-color highlighted punchlines, colloquial candor, a silent-read document feel
- HTML implementation: pure typesetting: punchlines in left-aligned big type with clamp() hierarchy; prose with max-width limiting line length; the only accent color as a span highlighting key phrases; a minimal table for the appendix. Zero assets and zero images; pure text is HTML's most reliable reproduction
- Fonts: Newsreader / Source Serif (reading-grade) or Inter (manifesto-style); headings can use Archivo extra bold
- Specimen: assets/style-specimens/ppt/20-all-text-manifesto.jpg


---

## Infographic style library (20 styles)

> **Added 2026-08.** Before this, the library had only two halves, web and PPT, but "infographics/visualization" is one of the four main use cases in the SKILL. When making an infographic, the roulette could only land in the web half and draw community-site/landing-page styles, which got forced onto it. This half fills that hole.
> Criterion: **if the output is an image (or set of images) with data as the protagonist that can be read on its own without interaction**, it goes here; clickable sites go to the web section, and things that page through go to the PPT section.

#### Bold styles

**Personal Annual Report (Feltron-style) (personal data printed annual report)** `Bold · 94% fidelity`
- Reference: Nicholas Felton's *Feltron Annual Report* 2005–2014 (the 2006-2011 volumes are in MoMA's permanent collection); Stefanie Posavec; Bloomberg Businessweek annual specials
- Fits: personal or team year-end summaries, quantified-self, product year-in-review, Wrapped-style retrospectives, long-cycle self-audits
- Visual DNA: palette = warm white uncoated-paper background + a single vermilion as the running accent + slate blue as the second data series + a third color bound to only one meaning and never reused. Font = tightly set Helvetica family, giant numbers pressing down from the top, dense small-print footnotes. The four-piece master set: ① giant-number module strip ② polar cycle chart (24h/12 months) ③ calendar heatmap grid ④ a time or geography band running across the full width. Signature = the contrast of treating trivial personal data like a corporate annual report, a modular print grid, 1px dividers, still readable printed in black and white
- HTML implementation: CSS Grid modules + 1px borders cutting the grid; polar charts in inline SVG with polar angles calculated by hand (no chart library); calendar with Grid + child element height fills. Pure typesetting + SVG, zero assets, a very strong point for HTML
- Fonts: Archivo / Helvetica Neue (tightly set giant numbers) + Inter (small footnotes)
- Specimen: assets/style-specimens/info/01-personal-annual-report.jpg

**Explanation Graphics (Nigel Holmes-style) (explanatory diagrams)** `Bold · 76% fidelity`
- Reference: Nigel Holmes (TIME's graphics director 1978–1994, founded Explanation Graphics in 1994); he advocated explaining abstract numbers with pictures and humor, and was also the bullseye of the chartjunk debate
- Fits: science explainers, explaining complex concepts to laypeople, illustrations for mass-media columns, children's and education-oriented work
- Visual DNA: palette = three or four high-saturation flat colors + black outlines. Font = rounded sans-serif + handwritten-style annotations. Master = drawing the chart itself as a real-object metaphor (banknotes stacked into bars, a thermometer as the scale, a running track as the progress bar). Signature = skeuomorphic charts, humor, little figures, thick outlines, zero gradients
- HTML implementation: the chart skeleton can be done in CSS/SVG, but **the soul is in the hand-drawn illustration**. In pure HTML it can only be downgraded to geometric color blocks, and the downgrade must be clearly stated; with image generation, use an image-generation tool to generate the illustration elements and then composite them
- Fonts: Nunito / Baloo 2 (rounded) + Caveat (handwritten annotations)
- Specimen: assets/style-specimens/info/02-explanation-graphics.jpg

**Cross-Section Epic (SCMP Arranz-style) (giant hand-drawn cross-section)** `Bold · 55% fidelity`
- Reference: Adolfo Arranz (senior graphics editor at SCMP, multiple gold medals at the Malofiej International Infographics Awards, best known for *City of Anarchy*, a cross-section of Kowloon Walled City); Malofiej is called the Pulitzer of infographics
- Fits: anatomy of buildings/history/objects, a single long scroll that takes ten minutes to read, museum-grade science explainers
- Visual DNA: palette = dark background (deep ink/dark brown) + warm highlights + an aged paper texture. Composition = a single giant image, isometric or straight cross-section view, dense leader-line annotations surrounding the subject. Signature = hand-drawn detail, leader-line annotations, cross-section view, one image telling the whole story
- HTML implementation: 🔴 **pure HTML can't produce a hand-drawn cross-section**. This style must have illustration assets; without them, don't pretend. HTML only handles the leader-line annotation layer and zoom/scroll interaction. If you can't get the assets, switch styles
- Fonts: Source Serif (headings) + Inter (annotations)
- Specimen: assets/style-specimens/info/03-cross-section-epic.jpg

**Magazine Pop Data (Businessweek-style) (magazine clashing-color data page)** `Bold · 90% fidelity`
- Reference: Bloomberg Businessweek (the Richard Turley era), WIRED chart pages, The Economist's Graphic Detail column
- Fits: business/tech media charts, illustrations for opinion columns, square social media graphics, data graphics embedded in WeChat Official Account articles
- Visual DNA: palette = two clashing main colors (fluorescent yellow + black, magenta + navy) + paper-white white space, with no third color to harmonize. Font = extra-bold condensed headings + tiny caption text, a type-size contrast of more than 10x. Master = one argument per graphic, the chart itself as the protagonist of the layout, the heading stating the conclusion directly. Signature = extreme type-size contrast, clashing colors, charts bleeding beyond the type area, conclusion-style headings
- HTML implementation: pure CSS can reproduce it completely; charts with inline SVG or CSS Grid bars; bleeds via negative margins. Zero assets
- Fonts: Archivo Black / Anton (condensed bold) + IBM Plex Sans (captions)
- Specimen: assets/style-specimens/info/04-magazine-pop-data.jpg

**Neurath–Arntz (ISOTYPE pictorial statistics)** `Bold · 88% fidelity`
- Reference: the ISOTYPE international pictorial education system founded by Otto Neurath and Gerd Arntz in 1920s Vienna
- Fits: population/social/public policy data, public communication aimed at low literacy thresholds, educational posters
- Visual DNA: palette = a limited set of flat colors (black + red + blue + ochre), no gradients, no shadows. Master = the same icon repeated N times to represent quantity. **Enlarging an icon to mean "more" is wrong**; this is the most central rule of the system. Signature = arrays of silhouette icons, horizontal arrangement, text labels on the left, a very strong sense of order
- HTML implementation: icons as inline SVG silhouettes + CSS repeat layouts; HTML is a natural fit. Icons can be self-drawn geometric silhouettes with no external assets needed
- Fonts: Jost / Archivo (replacing Futura)
- Specimen: assets/style-specimens/info/05-isotype.jpg

**Data Humanism (Lupi-style) (data humanism hand-drawn maps)** `Bold · 80% fidelity`
- Reference: Giorgia Lupi (Pentagram partner) and Stefanie Posavec's *Dear Data*; Lupi's Data Humanism manifesto holds that "data is people, not numbers"
- Fits: personal, emotional data, thick description of small samples, turning private experience into readable maps, subjects with many non-quantified dimensions
- Visual DNA: palette = journal off-white background + 4-5 soft colors each bound to a meaning (coral/pine green/mustard/ink purple); **not one color is decoration**. Masters = ① first define a visual language (size/shape/spikes/tails each encode one dimension) ② always include a legend that teaches the reader to decode it ③ elements arranged along organic paths, not on a grid. Signature = decodable custom symbols, a mandatory legend, organic arrangement
- HTML implementation: symbols generated parametrically in inline SVG (radius/spike count/tail length bound to data fields); paths as Bézier curves threaded through the points. Pure SVG, zero assets; the only thing it can't do is real hand-drawn strokes
- Fonts: Georgia / Source Serif (headings) + Inter (legend)
- Specimen: assets/style-specimens/info/06-data-humanism.jpg

**Scrollytelling (The Pudding-style) (scroll-driven data long scroll)** `Bold · 85% fidelity`
- Reference: The Pudding (a data journalism magazine), NYT The Upshot, Reuters Graphics scroll features
- Fits: complex arguments that need to be revealed step by step, long-form data stories, web features
- Visual DNA: palette switches by chapter but keeps a single accent running throughout. Master = text stepping on the left, graphics on the right morphing with scroll; each screen advances only one variable. Signature = the graphic doesn't change, it morphs; text and graphics strictly bound; color changes by chapter; a complete panorama at the end
- HTML implementation: IntersectionObserver triggering state changes + CSS transitions or SVG attribute interpolation; the pure frontend can reproduce it completely. ⚠️ The delivery form must be a web page; **exporting to PDF/PNG loses all the narrative**, so don't choose it when the user wants a static image
- Fonts: Inter / Source Serif (long-form readability first)
- Specimen: assets/style-specimens/info/07-scrollytelling.jpg

**Cartographic Lead (Stamen-style) (map as protagonist)** `Bold · 65% fidelity`
- Reference: Stamen Design (founded in San Francisco in 2001 by Eric Rodenbeck, clients include National Geographic), whose Watercolor/Toner map tiles are public classics
- Fits: geographic distribution data, city/transport/environment subjects, content where location is the narrative
- Visual DNA: palette = the base map sets the tone (watercolor or monochrome Toner) + the data layer in high-contrast points and lines. Master = the map fills the type area, data overlaid as point density or flow lines, a tiny legend tucked in a corner. Signature = a base map with authorship of its own, a restrained data layer, geographic shape as the composition
- HTML implementation: 🔴 **needs real geographic data (GeoJSON) and a base map**; pure HTML can't generate correct terrain from nothing. If you can't get the data, switch styles, and **never hand-draw a fake map**. With data, it can be drawn as inline SVG projections
- Fonts: Inter / IBM Plex Sans (place-name labels need a lot of small text)
- Specimen: assets/style-specimens/info/08-cartographic-lead.jpg

#### Neutral styles

**Newsroom Chart System (FT-style) (data journalism chart standards)** `Neutral · 96% fidelity`
- Reference: the Financial Times' Chart Doctor team and its public Visual Vocabulary (choosing charts by Deviation/Correlation/Ranking/Distribution/Change-over-Time/Part-to-Whole/Magnitude/Spatial)
- Fits: financial and industry data, situations where "choosing the right chart type" matters more than "looking good", when a series of charts needs a unified standard
- Visual DNA: palette = the signature salmon-pink newspaper background + an ordered set of color steps (a single-hue gradient for continuous quantities, two contrasting colors for deviation). Masters = ① heading as conclusion ② subheading explaining the measurement basis ③ the chart itself with borders and gridlines removed ④ data source always noted in the bottom left. Signature = choose the chart type by data relationship before talking about aesthetics, source notes can't be omitted, minimal axes
- HTML implementation: lines and bars drawn in pure CSS/SVG; the key is to **check the Visual Vocabulary to choose the right chart type first**, then start. Zero assets
- Fonts: Inter / Source Sans (body) + monospace for numbers
- Specimen: assets/style-specimens/info/09-newsroom-chart.jpg

**Computational Portrait (Fathom-style) (computational data portrait)** `Neutral · 78% fidelity`
- Reference: Ben Fry and his Boston studio Fathom Information Design (Fry co-created Processing and wrote *Visualizing Data*; his work has been in the Whitney Biennial)
- Fits: very large datasets, subjects that need "the data to grow its own shape", genetics/transport/time series
- Visual DNA: palette = white or near-black background + very thin lines + density built up by layering a single color's transparency. Master = present everything rather than a summary, with the layered density of masses of fine elements forming the graphic. Signature = hairlines, transparency stacking, no decoration, shape decided by the algorithm rather than the layout
- HTML implementation: drawn procedurally with Canvas or many SVG paths; Canvas is required when the data volume is large. **Requires real, complete data**; a small sample can't produce this style's sense of density
- Fonts: Inter / Roboto Mono (data labels)
- Specimen: assets/style-specimens/info/10-computational-portrait.jpg

**Beautiful Information (McCandless-style)** `Neutral · 90% fidelity`
- Reference: David McCandless' *Information is Beautiful* and the website of the same name, known for "turning big datasets into colorful graphics comparable at a glance"
- Fits: science comparisons, rankings, mass-market data aggregation, charts built for social sharing
- Visual DNA: palette = many colors on a harmonious color wheel at the same lightness and saturation (not random clashing). Master = mainly "area equals quantity" chart types such as bubble charts/treemaps/Sankey diagrams, with labels placed directly on the color blocks. Signature = area encoding, multiple colors in harmony, embedded legend, dozens of entries in one graphic
- HTML implementation: treemaps and bubbles with layout computed in CSS Grid or SVG (you need to write a simple packing algorithm yourself); Sankey diagrams with SVG Béziers. Zero assets
- Fonts: Nunito Sans / Inter
- Specimen: assets/style-specimens/info/11-beautiful-information.jpg

**Open Research Data (Our World in Data-style) (academic open data)** `Neutral · 94% fidelity`
- Reference: Our World in Data (Oxford's Global Change Data Lab), whose principles are interactive charts, clearly stated measurement bases and downloadable data
- Fits: rigorous topics, data presentations that need to withstand scrutiny, long-term trend comparisons
- Visual DNA: palette = white background + a set of categorical colors that are highly distinguishable but not glaring + gray for non-focus series. Masters = ① one-sentence conclusion heading ② measurement basis and time range in the subheading ③ labels placed directly at line ends inside the chart (no legend) ④ source and license noted at the bottom. Signature = line-end labels instead of a legend, non-focus series grayed out, transparent measurement basis, restraint
- HTML implementation: pure SVG lines + text positioned at the ends, the most reliable kind for HTML. Zero assets
- Fonts: Inter / Lato
- Specimen: assets/style-specimens/info/12-open-research-data.jpg

**Speculative Tech Diagram (Takram-style) (Eastern speculative tech diagram)** `Neutral · 84% fidelity`
- Reference: Takram (a design engineering studio in Tokyo and London, practicing speculative design across design and engineering)
- Fits: technology concept diagrams, future scenario projections, illustrations for research white papers, product architecture narratives
- Visual DNA: palette = beige-gray sand base + low-saturation natural colors (moss green/terracotta) + one touch of metallic gray. Font = light weights, wide tracking, carefully crafted mixed Chinese and English typesetting. Master = charts arranged as artworks, lots of white space, geometric shapes with a sense of precision. Signature = soft tech feel, precise geometry, restrained natural colors, charts like installations
- HTML implementation: pure CSS/SVG can reproduce it; the key is the white-space ratio and restrained line widths (0.5-1px). Zero assets
- Fonts: Inter (light weight) / Noto Sans JP + Cormorant (optional for headings)
- Specimen: assets/style-specimens/info/13-speculative-tech-diagram.jpg

**Pictogram System (Otl Aicher-style) (systematic pictogram diagrams)** `Neutral · 92% fidelity`
- Reference: Otl Aicher's pictogram system for the 1972 Munich Olympics and the Ulm School grid method
- Fits: flowcharts, wayfinding and guide-type infographics, multilingual settings, when a whole set of icons must stay consistent
- Visual DNA: palette = a constrained palette (the Olympic version is light blue/green/silver) + black. Master = all icons share the same grid and the same stroke angles (0/45/90° only), icons appear paired with short labels. Signature = strict angle constraints, system consistency, short sans-serif labels, a visible grid
- HTML implementation: icons self-drawn in inline SVG under the 45° constraint; the grid with CSS Grid. Zero assets, but you have to hold to the angle discipline yourself
- Fonts: Jost / Archivo (replacing Univers)
- Specimen: assets/style-specimens/info/14-pictogram-system.jpg

#### Quiet styles

**Small Multiples (Tufte small-multiples matrix)** `Quiet · 95% fidelity`
- Reference: the small multiples and sparkline concepts from Edward Tufte's *Envisioning Information*
- Fits: horizontal comparison across many dimensions, grouped time series, how one variable behaves across dozens of slices
- Visual DNA: palette = white background + black lines + one accent color marking outliers. Master = the same small chart repeated N times with only the data changed, **sharing the same axis ranges. If the ranges aren't unified, comparability is lost; this is the one fatal mistake in this school**; tiny labels placed beside the charts. Signature = gridded repeated small charts, shared scales, zero legends, zero gridlines, high data-ink ratio
- HTML implementation: CSS Grid arranging the small charts + an inline SVG line in each cell. Be sure to unify the domain. Zero assets
- Fonts: Source Serif (headings) + Inter (small labels)
- Specimen: assets/style-specimens/info/15-small-multiples.jpg

**Topological Transit Map (Beck/Vignelli-style) (topologically simplified network map)** `Quiet · 86% fidelity`
- Reference: Harry Beck's 1933 London Underground map, Massimo Vignelli's 1972 New York subway map
- Fits: processes and relationship networks, org charts, system topologies, any diagram where "connections matter more than real distances"
- Visual DNA: palette = white or light background + one high-saturation solid color per line. Master = all segments run only at 0/45/90°, stations evenly spaced. **Sacrificing geographic accuracy for readability** is the foundation of this school; interchanges use hollow circles. Signature = eight-direction constraint, evenly spaced nodes, solid-colored lines, hollow nodes
- HTML implementation: inline SVG polylines with strictly constrained angles; nodes as circles. Pure geometry, a perfect fit for HTML
- Fonts: Jost / Inter (station names can be all caps)
- Specimen: assets/style-specimens/info/16-topological-transit-map.jpg

**Ma & Emptiness (Kenya Hara-style) (white-space infographic of "white")** `Quiet · 82% fidelity`
- Reference: Kenya Hara's *White* and the MUJI visual system: "emptiness is not nothing; it is a vessel that holds imagination"
- Fits: brand annual reports, slow-paced narratives, small amounts of important data, occasions that call for solemnity
- Visual DNA: palette = pure white or rice-paper white + very light gray + one tiny point of ink or vermilion. Master = one data point per screen, huge white space, elements placed at the edges or at golden-ratio positions, never filled up. Signature = extreme white space, single-point emphasis, lines so fine they almost aren't there, the Eastern sense of "ma" (間, the interval)
- HTML implementation: pure CSS typesetting. 🔴 **The riskiest style in this library**: the white space must be composition (with a clear visual anchor); overdo it and it looks like "the page failed to render". Body text must still be ≥14px; shrinking type for the sake of character is not allowed
- Fonts: Noto Serif SC / Source Han Serif + Inter
- Specimen: assets/style-specimens/info/17-ma-emptiness.jpg

**Bookcraft Data (Irma Boom-style) (book-grade information typesetting)** `Quiet · 80% fidelity`
- Reference: Irma Boom (Dutch book designer whose work is in MoMA's permanent collection, known for extreme typographic and material experiments)
- Fits: long data reports, annual reports meant to be collected as publications, in-depth content mixing text and images
- Visual DNA: palette = paper color + one or two ink colors, large color blocks covering the page. Font = typesetting itself is the protagonist, with an extremely wide type-size range, asymmetric margins, and text that can run vertically or rotate. Master = data embedded in the text flow, chapter pages separated by full-bleed color blocks. Signature = asymmetric type area, extreme type-size range, typographic experiment, publication feel
- HTML implementation: CSS multi-column + writing-mode can do vertical text; Grid for the asymmetric type area. **What it can't do is paper material and trimming**; on screen this has to be compensated for with typographic tension
- Fonts: Fraunces / EB Garamond + Archivo (contrast)
- Specimen: assets/style-specimens/info/18-bookcraft-data.jpg

**Scientific Figure Plate (scientific journal figure plate)** `Quiet · 96% fidelity`
- Reference: Nature and Science figure guidelines, public scientific figure plates from USGS and NASA
- Fits: research conclusions, method comparisons, rigorous data that needs a peer-reviewed feel, multi-panel figures
- Visual DNA: palette = white background + a colorblind-friendly palette (blue-orange contrast rather than red-green) + grayscale. Master = panels labeled (a)(b)(c), the caption as a paragraph under the figure, error bars and sample size always shown, axes with tick marks. Signature = panel numbering, long caption under the figure, error bars, colorblind-safe, zero decoration
- HTML implementation: CSS Grid arranging the panels + SVG for the plots and error bars; captions as small-text paragraphs. Zero assets, HTML is fully up to it
- Fonts: Inter / Source Sans + Roboto Mono (numbers)
- Specimen: assets/style-specimens/info/19-scientific-figure-plate.jpg

**Swiss Grid Report (Müller-Brockmann-style) (Swiss grid annual report)** `Quiet · 97% fidelity`
- Reference: Josef Müller-Brockmann's *Grid Systems in Graphic Design*, the Ulm School, the Swiss International Style annual report tradition
- Fits: corporate annual reports, institutional reports, series documents that need to keep one layout over the long term
- Visual DNA: palette = white background + black + a single accent color. Master = a strict modular grid (often 12 columns), every element snapping to the column lines, flush-left ragged-right, lots of breathing white space without feeling empty. Signature = visible grid logic, the Helvetica family, non-centered layouts, hierarchy from type size and spacing rather than decoration
- HTML implementation: CSS Grid maps directly onto the column grid; this is the style in the library most isomorphic to HTML. Zero assets
- Fonts: Inter / Archivo (replacing Helvetica)
- Specimen: assets/style-specimens/info/20-swiss-grid-report.jpg

---

## App style library (12 styles)

> Added 2026-10. Use this section for App / mobile prototypes (previously you could only borrow from the web section, and what you drew were landing-page styles). Each specimen is a display board: two or three phone screens, and the composition itself is also a demonstration (see "display board" in `references/app-prototype.md`).

#### Bold styles

**Hardware Panel (Teenage Engineering-style, the interface language of the OP-1 / EP-133)** `Bold · 85% fidelity`
- Reference: Teenage Engineering OP-1 / EP-133 K.O. II (orange, black and gray palette, the dot-matrix hybrid "super segment hybrid display", square keys and knobs arranged on a grid, silkscreen-style labels)
- Fits: audio/creative tools, samplers, metronomes, recording and hardware companion apps, geeky small tools
- Visual DNA: palette = near-black #0B0B0B screen + signal orange #FF5A1F + beige-gray-white #E9E9E4 keys, light gray #D8D8D4 base plate with fine grid lines. Font = dot-matrix/monospace, numbers like LCD readouts, labels like silkscreen (all caps + wide tracking). Layout = a strict square grid, 4×4 key arrays, round knobs with single-color pointers, faders with orange tick lines; keys express physicality through "pressed-down thickness" (an inset 4px bottom-edge shadow). Signature elements: big dot-matrix readouts, square keys, small silkscreen labels, orange as the only accent color on screen.
- HTML implementation: CSS Grid for the key array + aspect-ratio:1; knobs with radial-gradient + a rotated pseudo-element pointer; faders as absolutely positioned bars; the dot-matrix font is Doto, falling back to Space Mono; the display board background uses repeating grid lines to simulate a panel. Note: orange is only for "currently active"; don't paint the whole screen with it.
- Fonts: Doto (dot-matrix readouts) + Space Mono (labels), Noto Sans SC for Chinese labels
- Specimen: assets/style-specimens/app/01-hardware-panel.jpg

**Liquid Glass (Apple's new iOS 26 design language)** `Bold · 70% fidelity`
- Reference: Apple Liquid Glass, announced at WWDC 2025 and launched alongside iOS 26 / macOS Tahoe 26 and others; Apple describes it as a translucent material that refracts the content around it and responds dynamically to touch, used for controls, navigation, icons and widgets
- Fits: native-feeling weather/fitness/media apps, system-style tools, interfaces that need "content first, floating controls", concept demos
- Visual DNA: the palette is decided by the background content itself: a high-saturation gradient background (coral orange → magenta → indigo, or teal → mint), with controls as translucent white glass. Font = system sans-serif, big numbers with tight tracking. Layout = content fills the full screen, and controls (back button, tab bar, bottom sheet) "float" over the content as rounded capsules/large rounded panels; the tab bar is a floating capsule rather than a full-width strip stuck to the bottom. Signature elements: white gradient highlight strokes, a top inner highlight, background blur + saturation boost, circular/capsule-shaped controls.
- HTML implementation: backdrop-filter:blur(22px) saturate(180%) + a translucent white gradient background + a 1px white stroke + an inset highlight shadow is the core; the background must be a gradient with color depth for the glass to show at all; on a solid background glass is just a gray block. CSS can't do the refraction and specular light effects, so they can only be downgraded to highlight strokes, which must be stated in the output.
- Fonts: Inter (replacing SF Pro) + Noto Sans SC
- Specimen: assets/style-specimens/app/02-liquid-glass.jpg

**Playful Tactile (Not Boring series-style, Andy Works) (playful 3D materials)** `Bold · 70% fidelity`
- Reference: the (Not Boring) series of apps (Andy Works, founders Andy Allen and Mark Dawson; includes Weather, Calculator, Timer, Habits); (Not Boring) Habits won a 2022 Apple Design Award; they're known for saturated palettes, haptic feedback and 3D animation, turning plain tools into "bold, loud" experiences
- Fits: small tools such as timers/habits/weather/calculators, light tools aimed at young people, apps that want one feature to be "fun enough to screenshot"
- Visual DNA: one full-bleed saturated main color per screen (orange #FF7A2D, lavender #B6A2FF, acid green #D4FF3F), paired with near-black #1B1330 text. Font = bold, rounded large numbers with tight tracking. Layout = one protagonist per screen (a giant dial/temperature tube/switch) with other elements around it; cards slightly rotated, screens staggered and rotated relative to each other. Signature elements: buttons with thickness (a solid hard shadow on the bottom edge), raised dials with highlights, switches that "press down".
- HTML implementation: layered box-shadows building up thickness (solid lower edge + inner highlight + soft outer shadow), radial-gradient for spherical highlights, rotate for the staggering. A static image can only show the material; haptic feedback and motion are only written as transitions in HTML, and this should be stated honestly.
- Fonts: Bricolage Grotesque (800) + Noto Sans SC (900)
- Specimen: assets/style-specimens/app/03-playful-3d.jpg

**Friendly Fintech (Monzo-style, high-saturation brand color + large rounded corners)** `Bold · 90% fidelity`
- Reference: Monzo (brand main color Hot Coral around #FF4F40, from its signature translucent coral bank card; paired with deep navy #091723 to #14233C, a rounded humanist sans-serif, capsule-shaped buttons, colloquial copy)
- Fits: personal expense tracking, savings/budgeting, payments and transfers, financial products for young users, any situation where "serious money" needs to sound friendly
- Visual DNA: palette = coral red #FF4F40 covering a large area at the top + a white rounded bottom panel, with pots/categories in pastel color blocks (yellow #FFD66B, blue #9AD8FF, green #C8F0CE, pink #F9B9E8, purple #D8CBFF). Font = rounded geometric/humanist sans-serif, balance in bold at 58px or larger. Layout = the colored top area holds the balance and three capsule actions, and the white panel below rises like a drawer; budgets are 2-column large rounded square "pots". Signature elements: full-bleed brand color, large rounded corners of 34px or more, capsule buttons, initial-letter/color-block icons, colloquial small headings ("where the money went").
- HTML implementation: pure CSS reproduces it 1:1. border-radius:28~34px, a two-column grid, solid color blocks, progress bars as two layered divs. Don't draw specific icon shapes; use a single character + a lighter/darker background of the same hue.
- Fonts: Figtree (replacing Monzo's own MonzoSans) + Noto Sans SC
- Specimen: assets/style-specimens/app/04-friendly-fintech.jpg

**Pro Camera (Halide-style, dark + yellow accent + dense scales)** `Bold · 85% fidelity`
- Reference: Halide (Lux Optics, Apple Design Award winner; the interface is designed for one-handed use and inspired by the controls on professional camera bodies; the custom font Ambrotype imitates the etched lettering on film camera bodies; it offers professional views such as a histogram, waveform, colored zebra stripes (highlight clipping warnings) and focus peaking)
- Fits: professional tools for camera/recording/measurement/oscilloscope work, interfaces that need "read at a glance, adjust one-handed", apps used in low light
- Visual DNA: palette = pure black #000 background + bright yellow #FFCC00 accent (only for "the currently selected parameter" and the center tick line) + gray-white #EDEDED readouts. The yellow is this style's own choice, not a claim about Halide's palette. Font = monospace numbers, small parameter labels with wide tracking. Layout = viewfinder on the top half, the bottom half fixed as "a parameter row (shutter/ISO/exposure/white balance) + a horizontal scale + the shutter button"; the scale fades out at both ends with one yellow line in the center. Signature elements: dense scales, zebra-stripe highlight warnings, a translucent histogram, only one yellow focal point per screen.
- HTML implementation: repeating-linear-gradient to draw the ticks (short ticks 2px/14px, long ticks 2px/70px, two layers), mask-image for the fades at both ends; zebra stripes with repeating-linear-gradient at 135deg; the viewfinder area as a gradient placeholder + "photo slot". Don't use yellow in more than three places.
- Fonts: JetBrains Mono (numbers and scales) + Noto Sans SC (labels)
- Specimen: assets/style-specimens/app/05-pro-camera.jpg

#### Neutral styles

**Topo Outdoor (Gaia GPS / AllTrails-style contour lines and tracks)** `Neutral · 90% fidelity`
- Reference: Gaia GPS (known for its Gaia Topo terrain map with contour lines and hillshading); AllTrails (route pages put distance, difficulty and elevation gain first)
- Fits: hiking/cycling/trail routes, outdoor logging, camping and map tools, mobile interfaces where "the map is the protagonist"
- Visual DNA: palette = parchment beige #EFEBDA background + contour brown #C09A68 (every fifth line bolder as an index contour) + woodland light green #D8E4C4 + water light blue #BFDDE6, with the track in high-contrast orange-red #E4572E plus a white outline. Font = condensed numbers (large readouts) + Chinese sans-serif. Layout = the map fills the screen, with a white panel at the bottom holding three big numbers (distance/elevation gain/time) and an elevation profile; on list pages each card has a mini contour thumbnail + a difficulty color tag (yellow/green/red). Signature elements: contour lines, a track line with a white outline, an elevation profile area chart, difficulty color tags.
- HTML implementation: SVG paths for contour lines (nested irregular closed curves, with a thicker stroke on index contours), the track as two path layers (a thick white line under a thin orange line); the display board background continues the same set of contour lines. Contour lines must be irregular curves; concentric perfect circles/ellipses look fake at a glance.
- Fonts: Barlow Condensed (readouts) + Noto Sans SC
- Specimen: assets/style-specimens/app/06-topo-outdoor.jpg

**Feed Waterfall (Xiaohongshu-style two-column card feed) (Chinese content waterfall feed)** `Neutral · 92% fidelity`
- Reference: the two-column waterfall feed on Xiaohongshu's "Discover" home page (cards staggered at their real aspect ratios, image on top, a two-line title, author and likes below, channel tabs at the top, a red plus sign in the middle of the bottom navigation)
- Fits: content communities, recommendation/guide/place-review apps, e-commerce content feeds, any Chinese product that uses "cover image + title" as the decision entry point
- Visual DNA: palette = white cards #FFF + light gray background #F5F5F7, with brand red #FF2442 used only for the selected underline, the plus button, follow and the liked state. Font = system Chinese sans-serif, titles 15px / truncated at two lines. Layout = two columns, 6px column gap, 10px card corner radius, cover aspect ratios varying (from about 1:1 to 3:4) to create the stagger; a fixed row at the bottom of each card with author avatar + nickname + like count. Signature elements: staggered cover heights, two-line titles, the avatar + nickname + likes row, the red plus sign.
- HTML implementation: two flex columns, each with flex-direction:column, cards flex:none, covers as gradient placeholders of different heights labeled "photo slot"; titles with -webkit-line-clamp:2; avatars as initial-letter dots, no drawn portraits.
- Fonts: Noto Sans SC
- Specimen: assets/style-specimens/app/07-feed-waterfall.jpg

**Command Palette (Raycast-style) (keyboard-first command palette)** `Neutral · 90% fidelity`
- Reference: Raycast (near-black background around #07080A, 1px hairline borders around #242728, Inter body plus monospace keycaps; commands identified by small color-block icons, shortcuts right-aligned; hierarchy distinguished by color steps rather than shadows)
- Fits: developer tools, productivity tools, command-line companion apps, internal ops panels, any "search is the action" product
- Visual DNA: palette = near-black #07080A canvas + panel #121315 + selected row #202225, command icons as small saturated color blocks (red #FF6363, blue #52A9FF, green #59D499, purple #8A63F5, yellow #FFC531). Font = Inter body + monospace keycaps/logs. Layout = a single-line input at the top (cursor as a red vertical bar), below it a single-line list grouped into "Suggestions/Commands", each row: small color-block icon + name + gray subtitle + right-aligned keycaps; a fixed action bar at the bottom ("Open Command ↵", "More Actions ⌘K"). Signature elements: gradient keycaps, small group headings, light gray highlight on the selected row, the bottom action bar. Raycast itself is a desktop app, so the specimen presents it as "a partial desktop panel + a phone adaptation".
- HTML implementation: flex rows + hairline borders; keycaps with a gradient background + a darker border-bottom + a 0 2px 0 shadow; no large shadows overall, only one dark drop shadow on the outer layer.
- Fonts: Inter + JetBrains Mono (keycaps and logs) + Noto Sans SC
- Specimen: assets/style-specimens/app/08-command-palette.jpg

**Health Color-Code (Apple Health / Oura-style)** `Neutral · 92% fidelity`
- Reference: Apple Health/Activity rings (red, green and blue concentric rings on black, for Move, Exercise and Stand respectively); Oura (three 0–100 scores for Readiness/Sleep/Activity, blue meaning on target, yellow meaning fair, red meaning needs attention)
- Fits: health/sleep/fitness/vital-sign data products, any dashboard that compresses a pile of metrics into "how's today", wearable companion apps
- Visual DNA: palette = pure black #000 background + cards #1C1C1E, semantic status colors (blue #3498FF optimal, yellow #FFCC00 fair, red #FF453A attention), ring colors (#FA114F, #92E82A, #1EEAEF). Font = big bold scores (76px or more) + small gray labels. Layout = one big ring/big score at the top as the protagonist, with cards below: contributor bars, sleep stage columns, a trend line over a normal-range color band; a small status capsule next to each data point (good/low/high). Signature elements: ring progress, status capsules, a translucent "normal range" band, color as the conclusion.
- HTML implementation: SVG circle + stroke-dasharray for rings (the track in the same color at low brightness), bars as two layered divs, the range band as a translucent rect; status capsule = translucent background + text in the same color. Within one screen, use the status colors and ring colors separately; don't blend them into a rainbow mess.
- Fonts: Inter + Noto Sans SC
- Specimen: assets/style-specimens/app/09-health-color-code.jpg

#### Quiet styles

**Native Polish (Things 3-style, Cultured Code)** `Quiet · 95% fidelity`
- Reference: Things 3 (Cultured Code, Stuttgart, Germany; two-time Apple Design Award winner; the official site quotes a review saying its interface is "like a clean, crisp sheet of paper"; "Today" has a "This Evening" section, lists can have headings as dividers, tasks expand into cards, and there's a draggable Magic Plus button in the bottom right)
- Fits: native productivity apps for tasks/to-dos/notes/schedules, heavily used personal tools, products aiming for "doesn't tire you out after long use"
- Visual DNA: palette = pure white #FFF + near-black text #1D1D1F + one blue #3478F6 (only for checkmarks, links and the plus button), a yellow star #F6C21B for "Today", gray #8A8F9B for secondary information. Font = system sans-serif, large 32px bold headings with tight tracking. Layout = mainly lists, with an indented hairline between rows (starting to the right of the checkbox), group headings in small bold + underline; tasks expand into raised cards with a large shadow, containing notes, a checklist, tags and a deadline. Signature elements: rounded square checkboxes, indented hairlines, the "This Evening" moon section, raised task cards, the blue round plus button.
- HTML implementation: pure CSS reproduces it. Checkboxes with border:2px + border-radius:7px, the completed state as a gray fill + a pseudo-element checkmark; row dividers with a left-indented :after; task cards with a two-layer shadow (0 2px 6px + 0 26px 60px). Motion (expanding, checking off) can't come through in a static image, so only do the structure.
- Fonts: Inter (can fall back to the system stack for an iOS style) + Noto Sans SC
- Specimen: assets/style-specimens/app/10-native-polish.jpg

**Gentle Encouragement (Gentler Streak-style, dark variant)** `Quiet · 80% fidelity`
- Reference: Gentler Streak (Gentler Stories, Slovenia; 2024 Apple Design Award winner in the "Social Impact" category; emphasizes personal progress rather than comparison with others; the core visual is the "Activity Path", which represents the day's state as a range from "rest" to "active"; the tone is soft blue-green). Note: the main interface in the official description leans bright and airy; this entry's late-night blue background is a dark variant built on its soft blue-green, rounded, non-judgmental tone
- Fits: fitness/rehab/sleep/mindfulness apps, habit products for people who "give up easily", any situation that wants to turn "falling behind" from guilt into understanding
- Visual DNA: palette = late-night blue gradient #18213A → #202C4A, cards #26335A, accent colors soft mint #9BE0CC, lavender #BAC3FA, peach #F4D0A8 (all three low-saturation pastels). Font = rounded sans-serif, large headings use suggestion sentences like "Today is good for…", never "X% complete". Layout = all large 28px-radius rounded cards stacked vertically; the core card is a round-capped gradient curved path + a white position dot; the monthly view uses a dot calendar, with rest days in peach, never a broken streak. Signature elements: round-capped curved path, pastel status capsules, the dot calendar, copy in the style of "No broken streak, rest is part of the plan too".
- HTML implementation: an SVG path for the path (a dark base track + an upper gradient stroke truncated with stroke-dasharray), the dot calendar with grid + border-radius:50%. The key is the tone of the copy: statements and suggestions throughout, no red, no exclamation marks, no rankings.
- Fonts: Nunito (rounded) + Noto Sans SC
- Specimen: assets/style-specimens/app/11-gentle-encouraging.jpg

**Editorial Reader (Matter / Readwise Reader-style) (editorial reading)** `Quiet · 90% fidelity`
- Reference: Matter (offers about 10 reading fonts, including New York, Valkyrie, Lyon and Literata, and multiple themes; restrained spacing and type sizes on the queue home page; long-press and drag to highlight); Readwise Reader (double-tap a paragraph to highlight, highlights and notes sync)
- Fits: read-later, long-form reading, note and highlight management, podcast/article aggregation, any content product whose goal is "finishing the read"
- Visual DNA: palette = warm paper white #FBF8F1 + ink black #26221C + one ochre red #B5532A (source names, progress bars, setting values), highlights in fluorescent yellow #F4D35E. Font = serif body (18px / line height 1.85), UI labels in small sans-serif + wide tracking. Layout = the reading queue is pure text entries: source/duration, serif title, a two-line summary, a thin progress line, no thumbnails; the reading page is a narrow centered column of body text, and selecting text pops up a small dark toolbar (highlight/note/copy); a highlight can be enlarged on its own into a card with notes. Signature elements: serif titles, highlighter-underline-style highlights, the dark selection toolbar, thin progress lines.
- HTML implementation: mark with linear-gradient(transparent 12%, yellow 12%, yellow 92%, transparent 92%) to simulate a highlighter, which looks more hand-drawn than a plain background color; the toolbar with white-space:nowrap to stop Chinese from wrapping vertically; Noto Serif SC for Chinese serif text.
- Fonts: Literata + Noto Serif SC (body), Inter (labels)
- Specimen: assets/style-specimens/app/12-editorial-reader.jpg

---

## Chinese & East Asian design (12 styles)

> Added 2026-10. A cross-media section: usable for web pages, decks, posters, covers and infographics, and each entry's "Fits" says what it suits. Each time, besides drawing one number from the section matching the output form, the seconds roulette also draws one number here. Chinese content especially deserves a look here: when Western references are used for Chinese layouts, often only the palette survives.

> The premise of this section: Chinese layout has its own grammar (vertical text, the type area, column rules, title slips (the pasted-on title label of a traditional Chinese book cover), the structure of Chinese characters); it isn't "a Western style + swap in a Chinese font". Usage is the same as the other sections: look at the specimen first, and run the color derivation protocol first.
> On fidelity: handwritten title slips, aged paper, real photos, and the textures of letterpress type/woodblock editions can't be done in pure HTML/CSS; they're all handled with honest downgrades, stated in each entry's "HTML implementation".
> Fact-checking: designers and works are only listed where a source was found; each entry's "Visual DNA" is a summary of that style's layout language, not a pixel-by-pixel description of any one page.

**Lü Jingren Bookcraft (Lü Jingren book design)** `Quiet · 85% fidelity`
- Reference: Lü Jingren (Chinese book designer, called a "master of book covers"); *Zhu Xi's Thousand Character Classic* (using paper texture to convey the feel of stele rubbings), *Memory of China: Treasures of Five Thousand Years of Civilization* (Honorary Award, Best Book Design from all over the World 2009), *Huai Xiu Ya Wu: Suzhou Folding Fans* (Most Beautiful Book in China 2010). He treats book design as a systems project of interacting with the text and coordinating editing, binding and printing, not just the cover.
- Fits: album/annual report spreads, long-form feature pages, oral history and archival content, exhibition catalogs, in-depth content that calls for "slow reading"; on the web it suits long-form reading pages, in a deck it suits chapter title pages
- Visual DNA: warm paper-colored background (around #F4EFE4), deep ink-black body text, **cinnabar red used in only one place** (one large character or one seal). The layout move is "a breathing type area": the type area isn't centered but raised and set toward the gutter, with a small top margin and a very large bottom margin; a narrow marginal note column on the fore-edge side holds annotations; chapter title pages hold only one large character plus one line with the book title, with everything else white space. A gradient at the gutter simulates the dip of the binding. Line spacing 2 or more, tiny page numbers and running heads.
- HTML implementation: CSS Grid/absolute positioning to set two 560px pages side by side, with the gutter shadow done by a dark-to-light linear-gradient; the marginal note column as its own absolutely positioned column; the vermilion seal as a solid square + one character. Paper fiber, hot-foil stamping, slipcases and physical page turning can't be done and are downgraded to a flat paper color + shadows.
- Fonts: Noto Serif SC (Chinese headings and body; Latin and numbers also use its built-in glyphs) + Noto Sans SC (small text such as running heads and marginal note labels)
- Specimen: assets/style-specimens/east/01-lu-jingren-bookcraft.jpg

**Song Block-Print Leaf (Song woodblock edition layout)** `Quiet · 80% fidelity`
- Reference: the leaf format of Song dynasty woodblock-printed editions: the block frame (Northern Song mostly double-ruled left and right, Southern Song gradually adding thin black mouths and book ears), ruled column grids, the fish-tail marks in the center fold (the block heart) (Southern Song introduced single black fish-tails, double black fish-tails and patterned fish-tails) along with the book title and page number; Zhejiang editions are neat, Sichuan editions have dignified, vigorous characters and an airy layout; collectors' vermilion-brush collation notes are a common layer in old books.
- Fits: observation/archival/document content pages, the "original records" pages of research reports, content pages for cultural brands, quote slides in decks, features that need an "ancient book" feel
- Visual DNA: one whole leaf centered, the block frame around it thick outside and thin inside (double outside, single inside, or thick outside, thin inside), vertical text with thin rules between each column; the center fold (block heart) centered, with black-mouth horizontal lines and inverted-triangle fish-tails at top and bottom, between them a vertical abbreviated title and page number, with the carver's name optionally at the bottom; slightly yellow paper (around #EDE0BC) + ink black; **vermilion annotations** written vertically in small red text in the top margin, with vermilion circles beside key sentences (can be done with text-emphasis). The whole page has no decoration at all; all the information is inside the grid lines.
- HTML implementation: writing-mode:vertical-rl with one div per column, a row-reverse flex to ensure right-to-left reading; column rules with border-left; fish-tails with clip-path triangles; vermilion circles with text-emphasis. The varying ink density and uneven stroke thickness of carved printing and damaged paper can't be done, and are downgraded to even ink color and a pale yellow paper color.
- Fonts: Noto Serif TC (traditional-character woodblock body text, closest to the skeleton of Song-style woodblock type); Noto Serif SC for simplified-character content. English is basically not used; if needed, use the same family as the body
- Specimen: assets/style-specimens/east/02-song-block-print.jpg

**Republic-Era Book Jacket (Republic of China-era book covers)** `Neutral · 70% fidelity`
- Reference: book and magazine covers from the generation of Lu Xun and Tao Yuanqing. Tao Yuanqing designed *Wandering* (1926), *The Grave*, *Dawn Blossoms Plucked at Dusk*, *Collection of Tang and Song Tales* and others for Lu Xun; Lu Xun also designed covers himself (such as *Call to Arms*), mostly text-led, simple and elegant.
- Fits: book covers and flat-lay book images, album/screenplay collection/travelogue covers, the first screen of cultural landing pages, exhibition posters, cultural and creative packaging
- Visual DNA: a low-saturation ochre/gray-green paper background, three colors in total: ink black + a touch of vermilion; a **white title slip** pasted on the cover with the title set vertically; plus a thin double-line border; the imagery is flat, geometric shapes (mountains, sun, water patterns), not realistic, with hatching; large areas of white space; front cover, spine and back cover laid out flat.
- HTML implementation: flex for the three columns of back cover/spine/front cover, the double-line frame with border + pseudo-element, the title slip as a light block with a thin frame; imagery as SVG geometric polygons and lines. **A handwritten title slip can't be done** and is downgraded to LXGW WenKai (handwritten kaishu); aged paper, hot-foil stamping and color misregistration can't be done and are downgraded to flat paper color.
- Fonts: LXGW WenKai for the title and title slip (alternative: Ma Shan Zheng, bolder and rougher); Noto Serif SC for author and descriptions; English basically doesn't appear
- Specimen: assets/style-specimens/east/03-republic-book-jacket.jpg

**Shanghai Moderne Deco (Shanghai modern Art Deco)** `Bold · 78% fidelity`
- Reference: yuefenpai (calendar posters) were advertising posters that originated in late-Qing Shanghai and peaked in the 1920s–30s, with representative painters Zheng Mantuo, Hang Zhiying and Xu Yongqing, using the "rubbed-charcoal watercolor" technique; Art Deco in 1930s–40s Shanghai was understood as "modeng" (modern), and influenced architecture and commercial art.
- Fits: posters, brand promotion pages, coffee/tea/food packaging and event pages, retro-themed landing pages, calendars and seasonal materials
- Visual DNA: deep ink green #17352F + gold #C9A24A + vermilion #9E2A1D + beige paper color; symmetric geometry of **radiating fans (sunbursts) + stepped towers**; a double frame (gold outer frame + dark inner line); headings in bold decorative lettering with a 3D drop shadow; a **calendar** inset on the right (a yuefenpai is essentially advertisement + calendar); a vermilion full-width band at the bottom holding the shop name and address.
- HTML implementation: SVG for the fans, concentric circles and stepped rectangles; heading text-shadow for the offset 3D effect; the calendar as a seven-column CSS Grid. The rubbed-charcoal watercolor portraits and textures unique to yuefenpai can't be done (and portraits shouldn't be drawn in SVG), so they're downgraded to pure geometry + flat color; use a geometric coffee cup in place of the figure.
- Fonts: ZCOOL XiaoWei (decorative heading lettering) + Noto Serif SC 900 (subheading) + Noto Sans SC (calendar and small text, Latin numbers included; for more of a Deco flavor, swap the Latin to Josefin Sans)
- Specimen: assets/style-specimens/east/04-shanghai-deco-calendar.jpg

**Experimental Hanzi Poster (experimental Chinese type poster)** `Bold · 85% fidelity`
- Reference: the lineage of contemporary Chinese graphic designers who build layouts from the structure of Chinese characters. Two have been verified: Han Jiaying (born 1961 in Tianjin, AGI member; his early posters systematically present his understanding of Chinese characters "from stroke to structure, from character to text, from surface to space", and his work is in collections including the V&A); Kan Tai-keung (born 1942, Hong Kong, fusing Chinese character forms with ink wash; the Bank of China logo takes the image of an ancient coin). What this lineage shares is treating Chinese characters as structural material that can be taken apart.
- Fits: exhibition/event posters, brand manifesto pages, deck covers or chapter slides, the key visual of feature long images, course covers
- Visual DNA: **one character enlarged to fill half the frame**, broken into independent geometric blocks stroke by stroke, with some strokes displaced or swapped for a dash of high-saturation color (vermilion #E4351E); a small stroke-breakdown diagram on the right (strokes numbered 1–5) explaining the "taking apart" process; black + paper white + one accent color, with everything else being the thin lines and small text of the information column; the heading in bold heiti (sans-serif), with emphasized words recolored.
- HTML implementation: each stroke built by hand from SVG rect/path, so the glyph is your own construction (first confirm the stroke count and stroke order are correct); the breakdown diagram uses the same set of paths, highlighting only one stroke. Characters with complex forms aren't suitable; choose characters with 4–6 strokes.
- Fonts: Noto Sans SC 900 (heading) + Noto Serif SC (lead text); the big character uses no font, it's built from geometric blocks yourself
- Specimen: assets/style-specimens/east/05-hanzi-experimental-poster.jpg

**Hong Kong Street Signs (Hong Kong street posters and shop signs)** `Bold · 80% fidelity`
- Reference: the visual language of Hong Kong's handwritten and neon shop signs. From the 1940s to 70s, "Northern Wei style" (Beiwei) sign lettering was common (distinct entry, exit and turning strokes, square and upright, popularized by calligraphers such as Au Kin-kung, So Sai-kit and Cheuk Siu-hang); signs are often vertical, densely stacked and layered, with mixed Chinese and English; since 2015 Hong Kong neon sign archives have documented more than 400 surviving neon signs.
- Fits: brand pages for retail/restaurants/record shops/night markets, event posters, promotional landing pages, city nightlife features, the "on-the-scene" slides of a deck
- Visual DNA: a late-night wall as the background, with **layer upon layer of signs** on one building: a vertical sign overlapping another vertical sign, horizontal signs stacked one over another; each sign has a solid high-saturation background color (red, yellow, blue, green; this palette is a generalization from nighttime signage, and sources weren't found for each one) with a cream border and an outer glow; the lettering is bold black traditional characters with hard drop shadows; a small red LED sign; a handwritten chalkboard price list at the bottom; electric wires running across the frame. Dense information, big lettering, signs occluding each other.
- HTML implementation: absolute positioning to place each block, box-shadow for the lightbox outer glow, text-shadow for hard drop shadows on the lettering, writing-mode:vertical-rl for the vertical signs. Real handwritten Beiwei strokes and the bends of neon tubes can't be done and are downgraded to a combination of Noto bold sans and Noto Serif black weight.
- Fonts: Noto Sans TC 900 (bold black traditional characters for vertical and small signs) + Noto Serif TC 900 (main horizontal sign heading) + Archivo Black (English subheadings)
- Specimen: assets/style-specimens/east/06-hk-street-signs.jpg

**Solar-Term Palette (Chinese traditional colors · solar-term color spectrum)** `Neutral · 90% fidelity`
- Reference: *Chinese Traditional Colors: The Color Aesthetics of the Forbidden City* (by Guo Hao and Li Jianming, with a table of contents arranged by the four seasons, collecting 384 traditional colors, plus color cards for the twenty-four solar terms); Lichun (Beginning of Spring) corresponds to traditional color names such as Piaobi, Huangbaiyou, Songhua, Xiangye and Haitianxia.
- Fits: web first screens, seasonal/time-based products, deck table-of-contents slides, cultural tourism and outdoor content, brand color card pages, infographics with a built-in timeline
- Visual DNA: organize the whole palette with **traditional color names** rather than "red, green, blue": 24 vertical color bars run across the bottom of the page, each labeled with the solar term name and color name, and the bar for the current solar term rises taller and wider and becomes the accent color of the whole page; the body uses a warm paper background + ink color, with patterns restrained to almost nothing. "Solar terms = navigation" is the layout move unique to this style.
- HTML implementation: flex with 24 equal color bars, the current bar flex:1.6 + taller; text automatically takes a dark/light color based on the bar's lightness. The color values are approximations of each color name (different sources give slightly different hex values for the same name); for real projects, go by the colors you sample yourself, and don't treat these as a standard color card.
- Fonts: Noto Serif SC (headings, color names, body) + Noto Sans SC (navigation, small labels)
- Specimen: assets/style-specimens/east/07-traditional-colors-solar-terms.jpg

**Sugiura Information Mandala (Kohei Sugiura information mandala)** `Bold · 72% fidelity`
- Reference: Kohei Sugiura (born 1932, Tokyo, Japanese graphic designer and researcher of Asian imagery). His research centers on the mandala and Asian cosmology, and he describes traditional Asian imagery as a world of "all things corresponding"; he designed about 5000 books, including about 1700 covers for Kodansha's "Gendai Shinsho" series; he made the *Time-Distance Map* diagram experiments and the "Mandala" exhibition (1980).
- Fits: infographics, event posters, annual/periodic data pages, science features, overview slides in decks
- Visual DNA: **a centered disc of concentric rings**: the outer ring is solar terms/scale, the middle ring is color-block sectors, the inner ring is small moon-phase circles, with a single red dot at the center; around it are leader lines and captions with numbered dots, a large vertical heading and a time-distance map, with high information density but every block corresponding to a position on the disc. The palette takes a near-black warm background + gold + vermilion + off-white. Vertical and horizontal text coexisting is a common Asian layout (this point is a generalization; no page-by-page source was found this time).
- HTML implementation: generate the SVG sectors, scales and text rotated along the circumference with a script; captions absolutely positioned, leader lines as SVG paths. Sugiura's overprinting, special inks and spine designs spanning spreads in print can't be done, and are downgraded to flat solid color.
- Fonts: Noto Serif SC (the large vertical heading and text on the rings) + Noto Sans SC (captions and the time map)
- Specimen: assets/style-specimens/east/08-sugiura-info-mandala.jpg

**Ikko Tanaka Geometric (Ikko Tanaka geometric graphic composition)** `Neutral · 90% fidelity`
- Reference: Ikko Tanaka (1930–2002). He fused Japanese tradition with the International Style; the *Nihon Buyo* poster (1981, which composes a geisha's hairstyle and face from squares and rectangles on a grid) is his signature work; from 1973 he made posters for the Seibu Theater, from 1975 he was creative director of the Seibu Group, and from 1980 he helped found MUJI and long led its visual identity; his style was influenced by the Rinpa school.
- Fits: exhibition/film festival/performance posters, brand manifesto pages, deck covers, first screens of cultural institutions' websites
- Visual DNA: **squares, circles and quarter circles on a grid** assembled into an abstract key image, in red #D9381E / black / mustard / a touch of steel blue, on a rice-paper background; a large vertical heading in bold Song (Ming) type; information on the right broken into blocks by small red labels for "Dates / Venue / Theme / Tickets"; a thin black line at the bottom. Fans, round suns and stripes (curtains) are geometric translations of traditional motifs.
- HTML implementation: a 560px square grid in 70px units, using border-radius for quarter circles and semicircles; stripes with repeating-linear-gradient. The color separations and paper grain of screen printing can't be done and are downgraded to flat solid color.
- Fonts: Noto Serif SC 900 (large vertical heading) + Noto Sans SC (information) + Zen Kaku Gothic New (small English text)
- Specimen: assets/style-specimens/east/09-tanaka-geometric-poster.jpg

**Hattori Playful Offset (Kazunari Hattori playful offset)** `Bold · 75% fidelity`
- Reference: Kazunari Hattori (born 1964, Tokyo, art director and professor at Tama Art University). His key works include the Kewpie Half advertisements, art direction for *Ryuko Tsushin*, and the Mitsubishi Ichigokan Museum logo; he won the Yusaku Kamekura Award in 2004; one of his signature techniques is **replacing printed halftone dots with stripes** (starting from the 2007 "Flag" poster).
- Fits: posters, covers, event and media brand pages, weather/lifestyle content that needs to be "not serious but very carefully crafted"
- Visual DNA: one character set extremely large, filled with **horizontal stripes** in two layers of different colors offset by a few pixels (like misregistered printing), the stripes themselves being the texture; beside it, tilted solid color blocks (yellow, black, a coral red circle) and one thick black hand-drawn wavy line; heading lettering with a handwritten feel, each character offset up or down; the information column, by contrast, is laid out plainly and properly. The playfulness is concentrated in one place and doesn't spread.
- HTML implementation: the giant character with background-clip:text + repeating-linear-gradient to fill the stripes, with an offset copied layer; color blocks with rotate; the thick line with SVG stroke-linecap:round. Real handwritten strokes and ink overprinting can't be done, and are downgraded to round-capped thick lines and offset stripes. Choose giant characters with few strokes (水 water, 山 mountain, 云 cloud); complex characters turn to mush.
- Fonts: Noto Sans SC 900 (giant character and numbers) + ZCOOL KuaiLe (playful heading) + Noto Sans SC (information column)
- Specimen: assets/style-specimens/east/10-hattori-playful-offset.jpg

**Sato Minimal Symbol (Kashiwa Sato minimalist symbol)** `Neutral · 92% fidelity`
- Reference: Kashiwa Sato (creative director). His 2006 rebrand for Uniqlo: a red square + bold white letters + katakana, with red and white chosen because they evoke the Hinomaru flag; he was also art director of the Cup Noodles Museum for Nissin. His position is that a brand needs one strong symbol (based on an interview with Design Singapore).
- Fits: brand launch pages, product landing pages, deck covers, app launch screens, the first screen of a startup's official site
- Visual DNA: **one character (or one logo) taking up half the layout**, a full solid color fill (around #E60012); the other half is a pure white information area with almost no decoration; headings in bold black sans-serif; a small four-color square swatch (red/black/white/blue) hinting at the system; data rows divided into cells by thick top rules in three colors. At most three colors on the whole page.
- HTML implementation: left and right columns, the giant character centered with flex; zero images, zero gradients. Almost no downgrade; the difficulty is restraint, not implementation.
- Fonts: Noto Sans SC 900 (Chinese headings and logo characters) + Archivo 800/900 (Latin and numbers)
- Specimen: assets/style-specimens/east/11-sato-minimal-symbol.jpg

**Japanese Lifestyle Magazine Dense (Japanese lifestyle magazine dense layout)** `Neutral · 78% fidelity`
- Reference: POPEYE (launched 1976, Magazine House, subtitled "Magazine for City Boys") and BRUTUS (launched 1980); both magazines' logos are by art director Makoto Horiuchi, who designed POPEYE's logo in 1976 and did every issue in the 70s. Makoto Horiuchi was also the art director of an・an.
- Fits: annual report/data feature spreads, city and lifestyle content, data slides in decks, guide and list-type long images, infographics
- Visual DNA: black text on white paper, **high-density diagrams**: a big heading on the left page (with a yellow marker underline) + a route map, with numbered dots and **handwritten red and blue pen annotations** on it; the right page has a 3×3 data grid (thick black grid lines, with one or two yellow cells and black cells for emphasis) + a heatmap + a short note on how to read the chart; running heads and page numbers in condensed Latin, spanning both pages. The "handwritten annotations + diagrams" feature is a generalization of this kind of layout; no page-by-page source was found this time, so don't treat it as a reproduction of any particular issue of POPEYE.
- HTML implementation: two 600px pages side by side, CSS Grid for the data grid, SVG for the route map, the heatmap as a 24×7 Grid of cells. Real magazine photo collages and print halftone dots can't be done; mark photo slots honestly with color blocks.
- Fonts: Noto Serif SC 900 (big heading) + Noto Sans SC (body and data) + Long Cang (handwritten annotations) + Archivo Narrow (running heads, page numbers, big data numbers)
- Specimen: assets/style-specimens/east/12-japan-magazine-dense.jpg

---

## ⚠️ Styles exclusive to AI image generation (only recommend once you've confirmed the user has image generation; not selectable by default)

The soul of the styles below lies in **dynamically generated visuals / 3D / particles / cinematic lighting / hand-drawn illustration**. In pure HTML/CSS without image generation, you can only make a badly degraded mock, so they are **removed from the default recommendation pool**. Only when the user clearly has image generation (an image-generation tool) are they candidates:

| Style | Soul | Why HTML can't do it |
|------|------|------------------|
| Active Theory (WebGL particles) | 3D particle systems/real-time rendering | Impossible in pure CSS |
| Field.io (generative art) | Algorithmically generated graphics | Static SVG can only make a stiff, simplified version |
| Resn (illustrated interaction) | Character illustration + gamification | Depends on hand-drawn assets |
| Zach Lieberman (real-time generation) | Creative coding strokes | Depends on real-time generation |
| Raven Kwok (fractal parameters) | Recursive fractals | CSS can't produce the complexity |
| Ash Thorp (cinematic lighting) | Cinematic volumetric light/concept art | CSS lighting is a degradation |
| Territory Studio (FUI holograms) | Sci-fi holographic interfaces | Depends on lots of layered glowing assets |
| Neo Shen (ink wash bleeds) | Organic ink wash bleeds | CSS gradients ≠ ink wash |
| Sagmeister & Walsh (color explosions) | Handmade physical objects + experimental typography | The clashing-color skeleton is doable (already merged into the web "Memphis" style and the PPT "single-color clash poster" style), but the handmade texture can't be done |

> These aren't "bad"; they're "on the wrong medium". Their native medium is images output directly by AI, not the browser DOM.

---

## Default aesthetic no-go zones (users can override for their own brand)

- ❌ **The lazy GitHub-dark solution**: a uniform dark navy background (#0D1117) + generic cyan/purple neon glow. Only this one overused combination is banned, not "all dark themes"
- ✅ **Not in the no-go zone**: cinematic dramatic lighting, warm cyberpunk (Ash Thorp orange/teal), dark-stage storytelling of athletic poetry. Dark themes with authorial intent are kept (this library's "Linear dark glow", "black-background giant-number theater" and "CS50 candy stage" are all legitimate dark themes)
- ❌ The aggressive purple gradient catch-all formula, emoji as icons, rounded cards + a colored left-border accent (unless the brand itself uses them)
- ❌ Adding a personal byline/watermark to cover images

---

## Prompting principles when image generation is available (Mood, Not Layout)

> Applies only when taking the AI image generation path; on the HTML path, write code directly following each style's "HTML implementation" above.

Short prompts > long prompts. Describing mood and content works better than piling on 30 lines of layout details.

| Writing that kills diversity | Writing that sparks creativity |
|----------------|----------------|
| Specifying color ratios (60%/25%/15%) | Describing mood ("warm like Sunday morning") |
| Prescribing layout positions | Citing a specific aesthetic ("Pentagram editorial feel") |
| Listing every visual element | Describing what the audience should feel |

Full AI image generation methodology → whatever image-generation tool the runtime has (see `materials.md` T1).

---

**Version**: v3.2 (2026-06 restructured into an HTML-native library; 2026-08 added the infographic section, 40 → 60 styles; 2026-10 added the App and Chinese & East Asian sections with a specimen for each style, 60 → 84 styles)
**Applies to**: the default HTML path for all visual design, including web/PPT/PDF/infographics/covers/App
