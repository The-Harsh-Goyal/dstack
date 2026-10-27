# Module · Infographics / Data Visualization / Long Images

A single image or a set of images with data or knowledge as the protagonist, readable on its own without interaction, goes through here: infographics, data report illustrations, Xiaohongshu long images, poster-style science explainers. First pass through the core rules in SKILL.md, then follow this manual.

## First decide viewing distance and container

- Scrolled past in a mobile feed (Xiaohongshu, WeChat Moments): 1080 wide, and the first screen (about 1080×1350) must stand on its own: title, main visual, and the single strongest number
- Print or large screen: decide the physical size and viewing distance first, then the type sizes
- Embedded in an article: follow the body text width, and text in the image is no smaller than body text

## Data is the protagonist, not decoration

- **Use only numbers the user gave or that can be verified**; illustrative diagrams must be labeled "illustrative" on the image. Inventing a number that looks like data is ten times worse than leaving it blank
- First ask what relationship this set of numbers is meant to show, then choose the form: proportion → a real object or area scaled proportionally; change → a curve or timeline; routes and space → a map; composition → a whole taken apart; scale → one oversized object and one familiar reference object
- One color stands for one meaning only, and the legend is written on the image
- For the hero asset, prefer real photos, public-domain scientific illustrations and maps (`references/materials.md`) over an icon platter

## Order of work

1. Three directions: 1 complete HTML per direction, with a full-page long screenshot at the target width (`references/directions.md`). The three versions need different skeletons (map, timeline, field guide, single giant object and narrative sequence are all possible structures), but don't force a metaphor just to be different.
2. After one is chosen, fill in all content and proofread every number and unit
3. Export: `npx playwright screenshot --full-page --viewport-size=1080,1350 file:///… out.png`; if it's going to a platform, cut it again to that platform's specs

## Design check

```bash
# $HD = this skill's root directory (the directory SKILL.md is in), not the user's project directory
python3 "$HD/scripts/design_lint.py" check info.html --viewport 1080x1350 --min-body 36 --min-label 28
```

Compute the minimum type size in the image from the final display size: a 1080-wide long image shrinks to about 390pt wide on a phone (about 2.8x), so body text ≥36px and labels ≥28px on the canvas give only 13–14pt on the phone screen. For print or large screens, calculate separately from the actual viewing distance.

## Related files

| What you're doing | Read |
|---|---|
| Style library and specimens (the infographic section of the seconds roulette, plus the cross-media Chinese & East Asian section) | `references/design-styles.md` |
| Quick spec reference for covers, in-article illustrations and long images | `references/scene-templates.md` |
| Fonts and Chinese typesetting | `references/typography.md` |
