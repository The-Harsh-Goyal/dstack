# Core Asset Protocol (full version)

> The full version of SKILL.md's "Core rule 2 · Brand asset protocol". SKILL.md keeps the trigger conditions + the 5 step titles; this file holds the detailed 5-step procedure, download commands, the brand-spec template, fallbacks for when the whole process fails, counterexamples, and the cost comparison.
> Trigger: mandatory when a task involves a specific brand/product. Go back to SKILL.md for the condensed version and context.

#### 1.a Core Asset Protocol (mandatory when a specific brand is involved)

> **This is v1's most central constraint, and the lifeline of stability.** Whether the agent follows this protocol through directly decides whether the output scores 40 or 90. Don't skip any step.
>
> **v1.1 restructure (2026-04-20)**: upgraded from "Brand Asset Protocol" to "Core Asset Protocol". Earlier versions focused too heavily on color values and fonts, and missed the most basic elements of design: the logo / product images / UI screenshots. In Huashu's own words: "Beyond the so-called brand colors, we obviously should find and use DJI's logo and the Pocket 4 product images. For non-physical products like websites or apps, the logo at least should be mandatory. This may be more important basic logic than a so-called brand design spec. Otherwise, what are we even expressing?"

**Trigger condition**: the task involves a specific brand: the user names a product/company/specific client (Stripe, Linear, Anthropic, Notion, Lovart, DJI, their own company, etc.), whether or not the user has provided brand materials themselves.

**Hard precondition**: before running the protocol you must already have confirmed, via "#0 Verify facts before assuming", that the brand/product exists and its status is known. If you're still unsure whether the product has launched, or about its specs/version, go back and search first.

##### Core idea: assets > specs

**The essence of a brand is "being recognized"**. What drives recognition? Ranked by recognizability:

| Asset type | Contribution to recognition | Necessity |
|---|---|---|
| **Logo** | Highest · any brand is recognized at a glance once its logo appears | **Required for every brand** |
| **Product images/product renders** | Very high · the "protagonist" of a physical product is the product itself | **Required for physical products (hardware/packaging/consumer goods)** |
| **UI screenshots/interface assets** | Very high · the "protagonist" of a digital product is its interface | **Required for digital products (App/website/SaaS)** |
| **Color values** | Medium · aids recognition; without the first three they often clash with other brands | Supporting |
| **Fonts** | Low · need the above to establish recognition | Supporting |
| **Vibe keywords** | Low · for the agent's self-check | Supporting |

**Translated into execution rules**:
- Extracting only color values + fonts without finding the logo / product images / UI → **violates this protocol**
- Substituting CSS silhouettes/hand-drawn SVG for real product images → **violates this protocol** (what you generate is a "generic tech animation" that looks the same for any brand)
- Not finding assets, not telling the user, not using AI generation either, and just forcing it → **violates this protocol**
- Better to stop and ask the user for materials than to fill in with something generic

##### 5-step hard procedure (every step has a fallback; never skip silently)

##### Step 1 · Ask (ask for the full asset list at once)

Don't just ask "Do you have brand guidelines?": it's too broad and the user won't know what to give. Ask item by item from the list:

```
For <brand/product>, which of the following materials do you have? Listed in priority order:
1. Logo (SVG / high-res PNG): required for any brand
2. Product images / official renders: required for physical products (e.g. product photos of the DJI Pocket 4)
3. UI screenshots / interface assets: required for digital products (e.g. screenshots of the App's main screens)
4. Color value list (HEX / RGB / brand palette)
5. Font list (Display / Body)
6. Brand guidelines PDF / Figma design system / link to the brand's official website

Send me whatever you have; whatever you don't, I'll search for, grab, or generate.
```

##### Step 2 · Search official channels (by asset type)

| Asset | Search path |
|---|---|
| **Logo** | `<brand>.com/brand` · `<brand>.com/press` · `<brand>.com/press-kit` · `brand.<brand>.com` · inline SVG in the official site's header |
| **Product images/renders** | Hero image + gallery on the `<brand>.com/<product>` product detail page · frames grabbed from the official YouTube launch film · images attached to official press releases |
| **UI screenshots** | Screenshots on the App Store / Google Play product page · the official site's screenshots section · frames grabbed from the product's official demo video |
| **Color values** | The official site's inline CSS / Tailwind config / brand guidelines PDF |
| **Fonts** | The official site's `<link rel="stylesheet">` references · Google Fonts tracing · brand guidelines |

`WebSearch` fallback keywords:
- Can't find the logo → `<brand> logo download SVG`, `<brand> press kit`
- Can't find product images → `<brand> <product> official renders`, `<brand> <product> product photography`
- Can't find UI → `<brand> app screenshots`, `<brand> dashboard UI`

##### Step 3 · Download assets · three fallback paths by type

**3.1 Logo (required for every brand)**

> ⚠️ **Don't just try `curl <brand>.com/logo.svg` and give up**: most official sites today are SPAs, and direct requests to static paths mostly return an empty HTML shell (measured 2026-06-06: all 5 direct paths on the Trae official site were empty shells). **For digital products / SaaS / AI tools, prefer icon aggregator sources**: they have the highest hit rate and output clean SVG directly.

In decreasing order of success rate:
0. **Icon aggregator sources (first choice for well-known digital products/SaaS/AI tools, highest hit rate)**:
   ```bash
   unset ALL_PROXY HTTP_PROXY HTTPS_PROXY all_proxy http_proxy https_proxy   # Clear the proxy, otherwise TLS tends to blow up
   # svgl: the most complete coverage of AI/developer brands (Claude/Cursor/OpenAI/Copilot/Anthropic/Vercel…), includes light/dark + wordmark
   curl -s "https://api.svgl.app?search=<brand>"   # Returns JSON; take the svg URL from route(.light/.dark), then download it
   # simpleicons: monochrome glyphs that can be colored directly with the brand color
   curl -o logo.svg "https://cdn.simpleicons.org/<slug>/<hexcolor>"
   ```
1. Standalone SVG/PNG files / the official brand page (e.g. `<brand>.com/brand`, `/press`):
   ```bash
   curl -A "Mozilla/5.0" -L -o assets/<brand>-brand/logo.svg "<official-logo-url>"
   ```
2. Extract the inline SVG from the official site's full HTML:
   ```bash
   curl -A "Mozilla/5.0" -L https://<brand>.com -o assets/<brand>-brand/homepage.html
   # Then grep <svg>...</svg> to extract the logo node
   ```
3. **Google favicon service (fallback for the site's real mark, almost never fails)**:
   ```bash
   curl -o logo.png "https://www.google.com/s2/favicons?domain=<brand-domain>&sz=256"   # 256px official site icon
   ```
4. Official social media avatar (last resort): company avatars on GitHub/Twitter/LinkedIn are usually 400×400 or 800×800 transparent PNGs

After downloading, **check each one**: `file <logo>` to confirm it's a real SVG/PNG (not a 106-byte placeholder or an empty HTML shell), and `head -c 90 <logo.svg>` to see whether it starts with `<svg`.

**3.2 Product images/renders (required for physical products)**

By priority:
1. **Hero image on the official product page** (highest priority): right-click to copy the image address / fetch with curl. Resolution is usually 2000px+
2. **Official press kit**: `<brand>.com/press` often has high-res product images to download
3. **Frames from the official launch video**: download the YouTube video with `yt-dlp` and extract a few high-res frames with ffmpeg
4. **Wikimedia Commons**: often has public domain material
5. **AI generation fallback** (nano-banana-pro): send the real product image to the AI as a reference and have it generate variants that fit the animation scene. **Don't substitute hand-drawn CSS/SVG**

```bash
# Example: download the product hero image from DJI's official site
curl -A "Mozilla/5.0" -L "<hero-image-url>" -o assets/<brand>-brand/product-hero.png
```

**3.3 UI screenshots (required for digital products)**

- Product screenshots on the App Store / Google Play (note: these may be mockups rather than the real UI; compare them)
- The official site's screenshots section
- Frames from product demo videos
- Launch screenshots from the product's official Twitter/X (often the latest version)
- If the user has an account, take screenshots of the real product interface directly

**3.4 · The "5-10-2-8" asset quality threshold (iron rule)**

> **The logo's rules differ from other assets**. If there's a logo, you must use it (if there isn't, stop and ask the user); other assets (product images/UI/reference images/illustrations) follow the "5-10-2-8" quality threshold.
>
> Huashu's own words on 2026-04-20: "Our principle is to search 5 rounds, find 10 assets, and choose 2 good ones. Each must score 8/10 or higher. Better to have fewer than to pad things out just to finish the task."

| Dimension | Standard | Anti-pattern |
|---|---|---|
| **5 rounds of search** | Cross-search multiple channels (official site / press kit / official social media / YouTube frames / Wikimedia / screenshots from the user's account); not one round grabbing the top 2 and stopping | Using the first page of results directly |
| **10 candidates** | Gather at least 10 candidates before starting to filter | Grabbing only 2, leaving no choice |
| **Choose 2 good ones** | Hand-pick 2 of the 10 as the final assets | Using all of them = visual overload + diluted taste |
| **Each 8/10 or higher** | Below 8, **better not to use it**; use an honest placeholder (gray block + text label) or AI generation (nano-banana-pro based on an official reference) | Padding brand-spec.md with 7-point assets |

**8/10 scoring dimensions** (record them in `brand-spec.md` when scoring):

1. **Resolution** · ≥2000px (≥3000px for print/large-screen scenarios)
2. **Copyright clarity** · official source > public domain > free stock > suspected stolen images (suspected stolen images score 0 outright)
3. **Fit with the brand vibe** · consistent with the "vibe keywords" in brand-spec.md
4. **Consistency of lighting/composition/style** · the 2 assets don't fight when placed together
5. **Standalone narrative ability** · can carry a narrative role on its own (not decoration)

**Why this threshold is an iron rule**:
- Huashu's philosophy: **better nothing than something shoddy**. Padding assets are worse than none: they pollute the visual taste and send an "unprofessional" signal
- **The quantified version of "take one detail to 120%, everything else to 80%"**: 8 points is the floor for "everything else at 80%"; true hero assets need 9-10 points
- When consumers look at work, every visual element is **adding or subtracting points**. A 7-point asset = a deduction; better to leave the space empty

**Logo exception** (restated): if there's a logo, you must use it; "5-10-2-8" doesn't apply. Because the logo isn't a "pick one of many" problem but a "foundation of recognition" problem: even if the logo itself only scores 6, it's 10 times better than having no logo.

##### Step 4 · Verify + extract (not just grepping color values)

| Asset | Verification action |
|---|---|
| **Logo** | File exists + SVG/PNG opens + at least two versions (for dark/light backgrounds) + transparent background |
| **Product images** | At least one at 2000px+ resolution + background removed or clean background + multiple angles (main view, details, in context) |
| **UI screenshots** | True resolution (1x / 2x) + latest version (not an old one) + no contamination from user data |
| **Color values** | `grep -hoE '#[0-9A-Fa-f]{6}' assets/<brand>-brand/*.{svg,html,css} \| sort \| uniq -c \| sort -rn \| head -20`, filtering out black/white/gray |

**Watch out for demo brand contamination**: product screenshots often contain the brand colors of a user's demo (e.g. a tool's screenshot demoing HEYTEA red); that isn't the tool's color. **When two strong colors appear together, you must tell them apart**.

**Multiple brand facets**: the same brand's marketing colors on its official site and its product UI colors often differ (Lovart's official site is warm off-white + orange, its product UI is Charcoal + Lime). **Both are real**: choose the facet that fits the delivery scenario.

##### Step 5 · Lock it in as a `brand-spec.md` file (the template must cover every asset)

```markdown
# <Brand> · Brand Spec
> Collected on: YYYY-MM-DD
> Asset sources: <list download sources>
> Asset completeness: <complete / partial / inferred>

## 🎯 Core assets (first-class citizens)

### Logo
- Main version: `assets/<brand>-brand/logo.svg`
- Reversed version for light backgrounds: `assets/<brand>-brand/logo-white.svg`
- Usage: <opening/closing/corner watermark/global>
- Forbidden alterations: <no stretching/recoloring/adding outlines>

### Product images (required for physical products)
- Main view: `assets/<brand>-brand/product-hero.png` (2000×1500)
- Detail images: `assets/<brand>-brand/product-detail-1.png` / `product-detail-2.png`
- Scene image: `assets/<brand>-brand/product-scene.png`
- Usage: <close-up/rotation/comparison>

### UI screenshots (required for digital products)
- Home: `assets/<brand>-brand/ui-home.png`
- Core feature: `assets/<brand>-brand/ui-feature-<name>.png`
- Usage: <product showcase/Dashboard fade-in/comparison demo>

## 🎨 Supporting assets

### Palette
- Primary: #XXXXXX  <source note>
- Background: #XXXXXX
- Ink: #XXXXXX
- Accent: #XXXXXX
- Forbidden colors: <color families the brand explicitly avoids>

### Typography
- Display: <font stack>
- Body: <font stack>
- Mono (for data HUDs): <font stack>

### Signature details
- <which details are "done to 120%">

### No-go zones
- <explicit don'ts: e.g. Lovart doesn't use blue, Stripe doesn't use low-saturation warm colors>

### Vibe keywords
- <3-5 adjectives>
```

**Execution discipline after writing the spec (hard requirement)**:
- All HTML must **reference** the asset file paths in `brand-spec.md`; substituting CSS silhouettes/hand-drawn SVG is not allowed
- The logo is referenced as an `<img>` pointing at the real file, not redrawn
- Product images are referenced as `<img>` pointing at the real files, not replaced with CSS silhouettes
- CSS variables are injected from the spec: `:root { --brand-primary: ...; }`, and the HTML uses only `var(--brand-*)`
- This turns brand consistency from "relying on self-discipline" into "relying on structure": to add a color on the fly, you have to change the spec first

##### Fallbacks when the whole process fails

Handle each asset type separately:

| Missing | Handling |
|---|---|
| **Logo can't be found at all** | **Stop and ask the user**; don't force it (the logo is the foundation of brand recognition) |
| **Product images (physical product) can't be found** | First choice nano-banana-pro AI generation (based on official reference images) → second choice ask the user → only as a last resort an honest placeholder (gray block + text label, clearly marked "product image pending") |
| **UI screenshots (digital product) can't be found** | Ask the user for screenshots from their own account → frames from official demo videos. Don't pad with mockup generators |
| **Color values can't be found at all** | Follow the three directions (`references/directions.md`); sample the colors for the three direction cards from the subject and real images, and label them as assumptions |

**Forbidden**: when assets can't be found, silently forcing it with CSS silhouettes/generic gradients: this is the protocol's biggest anti-pattern. **Better to stop and ask than to pad**.

##### Counterexamples (pitfalls we actually hit)

- **Kimi animation**: guessed from memory that "it should be orange"; Kimi is actually `#1783FF` blue. Had to redo it once
- **Lovart design**: took the HEYTEA red of a demo brand in a product screenshot as Lovart's own color. Nearly ruined the whole design
- **DJI Pocket 4 launch animation (2026-04-20, the real case that triggered this protocol upgrade)**: followed the old protocol that only extracted color values, didn't download the DJI logo, didn't find Pocket 4 product images, and used a CSS silhouette in place of the product. The result was a "generic black background + orange accent tech animation" with no DJI recognizability. Huashu's own words: "Otherwise, what are we even expressing?" → protocol upgraded.
- Extracted colors but didn't write them into brand-spec.md; by page three the main color value was forgotten and a "close but not quite" hex was added on the spot. Brand consistency collapsed
- **Top five coding agents comparison PPT (2026-06-06, the real case that triggered the trigger-condition expansion)**: the agent judged the task as "PPT + no style reference" and took the Fallback Design Direction Advisor path, extracted only the five brands' colors and then spawned three sets of design logic, and **didn't fetch a single one of the five product logos (Claude Code / Cursor / Codex / Copilot / Trae)**. Huashu caught it red-handed: "Why didn't we go fetch these products' logos?" Root cause: misjudged a "comparison / ranking deck" as not triggering §1.a (assuming §1.a only covered "making materials for a single client"), and the Fallback path had no logo checkpoint at all. → Fix: ① expanded the trigger condition into two types (including "real products named/placed side by side in the design") ② the Fallback doesn't exempt fetching logos ③ Phase 3.5 adds a "named-product logo sub-gate" that must pass before spawning ④ Step 3.1 adds the reliable svgl/simpleicons/Google favicon logo-fetching chain.

##### Cost of the protocol vs cost of skipping it

| Scenario | Time |
|---|---|
| Following the protocol correctly | Download logo 5 min + download 3-5 product images/UI 10 min + grep color values 5 min + write spec 10 min = **30 minutes** |
| Cost of skipping the protocol | Producing a generic animation with no recognizability → the user spends 1-2 hours on rework, or even a full redo |

**This is the cheapest investment in stability**. Especially for commercial work/launch events/important client projects, the 30-minute asset protocol is insurance money.

