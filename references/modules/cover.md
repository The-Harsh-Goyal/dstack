# Module: covers and single social images (dstack)

> dstack addition. Upstream had no route for one-image deliverables; `scene-templates.md` only covers WeChat covers.

For: X article headers, in-feed images, OG/link cards, video thumbnails, a single poster image. One frame, often no text.

## Sizes (render at exactly these, never scale a screenshot)

| Preset | Size | Use |
|---|---|---|
| `x-article` | 2500×1000 (5:2) | X article header |
| `x-infeed` | 1600×900 (16:9) | X in-feed image / link preview |
| `og` | 1200×630 | Open Graph card |
| `yt-thumb` | 1280×720 | Video thumbnail |
| `square` / `portrait` | 1080×1080 / 1080×1350 | Feed posts |

Keep key elements, and any text, inside an 8% safe area; feeds crop and overlay UI on the edges. A 5:2 header shown in a 16:9 feed loses its sides, so make both from the same master, not by stretching one.

## Flow

1. Core rules 0-2 as usual (facts, what exists, brand). Text is optional: many covers carry none; then thumbnails show composition, not a headline.
2. Three-direction gate (core rule 3). Direction boards are one real rendered image per direction at the final size. No human present: `scripts/gate.py default` (see SKILL.md).
3. Hero asset (core rule 4). Generated images are usually too small: `python3 "$HD/scripts/cover.py" upscale gen.png --preset x-article -o hero.png` (local ffmpeg lanczos, cover-crop, `--gravity`, `--sharpen`).
4. Build the frame as HTML (image + type + procedural layers) and render it at the exact size:
   `python3 "$HD/scripts/cover.py" render cover.html --preset x-article -o final/cover-2500x1000.png`
   The script sets the viewport to the preset, renders at device scale 1, strips metadata and fails if the PNG is not exactly the target size.
5. Check: `python3 "$HD/scripts/cover.py" check final/cover-2500x1000.png --preset x-article` (size, flat image, metadata, safe-area overlay PNG to look at). If the HTML has text, also run `design_lint.py check cover.html`.
6. Look at it at feed size (about 600 px wide) and at 100%.

## Known limits

- `design_lint.py` only reads HTML; a raster cover gets the `cover.py check` basics, not type-size or contrast checks. Judge text on images by eye.
- Upscaling is lanczos, not a learned super-resolution model: above ×2 it is soft. Generate larger, or compose so the soft parts are background.
