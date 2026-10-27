# Assets first: the star of the frame shouldn't be only text and cards

If the materials pure HTML/CSS has to work with come down to just "text + cards + tables + hairlines", every style will look monotonous. This is the second root cause of the old version's monotonous output. This file solves two things: every direction settles its hero asset first; and work is tiered by the capabilities the user actually has, recommending installs for missing ones but never getting stuck on them.

## Principles

1. **Every direction settles its hero asset first**, written into the direction card (`references/directions.md`). Don't let all three directions be "pure typography"; when you do use pure typography, it has to be deliberate typography, where the type itself becomes the image (giant type, vertical setting, cropping), not the default arrangement of a heading plus body text.
2. **Gather the images the content requires before designing.** For designs that introduce animals, places, people, products or history, the images are content, not decoration; a parrot website without parrots = failure. When unsure, treat it as content-required.
3. **Real-image honesty test**: remove this image; is any information lost? No loss = decoration, so don't add it. Don't add stock "inspiration images".
4. **Don't hand-draw people, animals, physical objects or scenes in SVG**: the features come out misaligned and the proportions weird. Use real images, generated images, or an honest placeholder. Geometry, icons, data charts and map wireframes are not included in this; silhouette masks are only for composition (cropping photos, making shapes) and can't stand in for product images.

**When the design involves the user themselves or their products, real assets come first**: first check `personal-asset-index.json` in the user's private memory / config directory (on first use, copy `assets/personal-asset-index.example.json` there and fill in real data; real data doesn't go in the skill directory, so it doesn't leak when the skill is shared). If you can't find it, ask the user for it; don't make it up.

## Probe capabilities first

```bash
# $HD = this skill's root directory (where SKILL.md lives), not the user's project directory
python3 "$HD/scripts/capabilities.py"
# dstack: a script can't see tools built into your runtime; declare them so the tier is right:
python3 "$HD/scripts/capabilities.py" --image-tool GenerateImage   # or DSTACK_IMAGE_TOOL=GenerateImage
```

It checks which related skills are installed locally, whether there's an image-generation key, and whether ffmpeg / playwright are present, then gives a tier and install suggestions for what's missing. Not detecting something doesn't mean it isn't there (for example, Codex has image_gen built in); if the user says they have it, go with the user.

## Three tiers

### T0 · Every user has these (default, no extra capabilities needed)

- **Real images**: `python3 "$HD/scripts/fetch_images.py" --query "English keywords" --out project/assets/img --count 2 --width 1600` (Wikimedia Commons, Met / Art Institute open-access collections, Biodiversity Heritage Library, Unsplash, Pexels, with license output and failure fallback). For the user's own products, follow the brand asset protocol to get official images.
- **Logos for named products**: get one for every recognizable product that appears in the design (svgl → simpleicons → favicon, see `references/brand-asset-protocol.md`). If one on the list wasn't fetched, fill it in; only fall back to an honest placeholder when it truly can't be found, and say so.
- **Procedural textures** (usable in a single file, no fetch needed):
  - SVG filters: `feTurbulence` + `feDisplacementMap` for paper grain, noise, ink bleed, print misregistration
  - CSS: layered `radial-gradient` for lighting and volume, `mask-image` / `clip-path` for silhouettes and cropping, `mix-blend-mode` for overprinting
  - canvas-generated images: contour lines, dot grids, flow fields, star maps, fabric textures (fixed random seed, so screenshots are reproducible)
  - Three.js (loaded via `<script src>` from cdnjs, works under `file://`) for procedural geometry, materials and lighting
- **Data as image**: turn the numbers in the content into the main visual (a scale spanning the whole page, a physical object scaled to proportion, a route on a map) instead of three big-number cards
- **Physical replicas**: use HTML to make tickets, labels, ID cards, manuals, postcards and newspaper layouts, with paper, punch holes, stamps and creases
- **Type as image**: oversized letterforms cutting through the frame, vertical setting, letterforms interlocking with images

### T1 · Has AI image generation

How to tell: an image-generation skill such as `huashu-gpt-image` or `nano-banana-pro` is installed locally, or the runtime you're in has a built-in image tool (such as Codex's image_gen; you know whether you have it), or the user says so explicitly. Having only an API key doesn't count: this skill has no script that calls an image-generation API directly.

- **At the direction-board stage, produce probe images first**: generate one mood or main-visual image per direction (material, light, subject), and lay it out for the user together with the first HTML draft. Have the visual layer before writing code, so what the user picks is "a look they can see".
- **After the choice, generate main visuals, illustrations, textures, people and scenes.** Prompts should describe concrete visual traits and real reference names, not adjectives like "premium feel" or "minimalist"; see `huashu-gpt-image` for the method.
- **Generations are often smaller than the deliverable** (dstack: e.g. 1024×576 for a 2500×1000 X header). Upscale locally: `python3 "$HD/scripts/cover.py" upscale gen.png --preset x-article -o hero.png [--gravity top] [--sharpen]` (ffmpeg lanczos + cover-crop, no network). Expect some softness above ×2; fine at feed size, check at 100% before print. Compose so the crop keeps the subject (5:2 from 16:9 loses ~30% of the height).
- Generated images must pass the real-image honesty test; brand product images must be generated using official reference images as the base, never drawing a product out of thin air.

### T2 · Sibling skills installed

| skill | What more it can do | Public address (dstack: not installed; installing needs the user's OK) |
|---|---|---|
| huashu-gpt-image | Image-generation prompt methodology; illustrations, posters, infographics, UI mockups | `npx skills add alchaincyf/huashu-gpt-image` |
| huashu-art-motion | 36 art and explainer animation styles, whole films driven by voiceover | `npx skills add alchaincyf/huashu-art-motion` |
| huashu-md-html | md to publication-grade html / PDF / EPUB | `npx skills add alchaincyf/huashu-md-html` |
| huashu-3djs, huashu-flow-diagram | Procedural 3D scenes, flowing architecture diagrams | Not public yet; use them if installed locally |

## What to say when a capability is missing

Don't block. Drop to T0 and carry on, and when you deliver, tell the user in one sentence what more they could get:

> This version's main visual uses procedural paper grain + public-domain illustrations. With an image-generation tool available, next time I can generate the main visual and probe images directly.

Recommend only the one that's relevant to this task; don't list a catalog and sell.

## Three-level fallback when image fetching fails

1. Not found in public-domain libraries → switch to Unsplash / Pexels
2. Nothing suitable anywhere on the web → if you have T1, generate using a reference image as the base
3. Still no good → honest placeholder "image to come" and carry on, and say so when delivering. A failed image fetch means degrade and continue, not stop
