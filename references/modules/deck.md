# Module · Slides / PPT / Presentations

Slides, PPT, pitch decks, course slides and report materials all go through here. First pass through the core rules in SKILL.md (the three-direction gate, etc.), then follow this manual.

## Delivery chain (don't ask about format when starting)

HTML deck (the base output, always made first) → when finished, **automatically** produce a PDF → produce an editable PPTX only if the user asks.

- PDF: for the multi-file architecture use `scripts/export_deck_pdf.mjs`; for a single-file deck-stage use `scripts/export_deck_stage_pdf.mjs`. Text stays vector and searchable; deliver it without asking.
- There are two routes to PPTX. Choose by the state of the HTML, and don't mix them:
  - HTML not written yet → write it under the 4 hard constraints, then go through `scripts/export_deck_pptx.mjs` (calls `html2pptx.js` internally) → `references/editable-pptx.md`
  - HTML already written and visually driven, or the client requires inheriting their template → `scripts/pptx_from_rendered.py`, which reads rendered coordinates with zero rework → `references/pptx-from-rendered-html.md`. After export it automatically compares against the page innerText and reports whether any text was lost
  - Never downgrade an already-written design to accommodate html2pptx's constraints. That is exactly why the second route exists

## Architecture (decide it first; get it wrong and you'll keep hitting CSS scope pitfalls)

- **Default: multi-file + overview wall** (almost every deck). Each slide is a standalone HTML file (a 1920×1080 `<section>`), assembled with `assets/deck_index.html`: copy it directly as `index.html` and edit the MANIFEST to use it. **Don't rewrite the overview logic** (the three pitfalls of tilt, click hit-testing and clipping are already solved in it). It comes with two adaptive overviews (grid iframe / infinite gallery; the gallery needs `scripts/gen_deck_thumbs.mjs` run first to generate thumbnails), keyboard paging, scaling, unified page numbers and print merging.
- **Single file**: use `assets/deck_stage.js` only for a minimal pitch of ≤5 slides, when an overview wall is explicitly not needed, or when JS state must be shared across slides. The script must come after `</deck-stage>`, and the section's `display: flex` must be written on `.active`.
- Before choosing single file, confirm "really ≤5 slides and no overview wall needed". Choosing single file for a 13-slide deck and losing the overview wall is a pitfall that was actually hit in testing.

Details, directory structure, slide skeleton, what goes in tokens: the "Decide the architecture first" section of `references/slide-decks.md`.

## Order of work

1. Three directions: each direction produces **2 representative slides** (the two with the biggest difference in visual structure, e.g. cover + data slide), which double as a showcase. All three deck versions share the same shell and change only the visuals.
2. After the user chooses, for decks of ≥5 slides, first set the 2 showcase slides as the grammar of the chosen direction, then do the remaining slides in batches. Skipping this step = reworking N slides instead of 2 when the direction is wrong.
3. Answer the five form questions for each slide first (see `references/workflow.md`), especially "narrative role": cover, transition, data, quote, ending. One role per slide, and the layout changes with it.
4. When everything is done, assemble `index.html` and produce the PDF.

## Hard rules

- **Slide content never carries its own page number or progress marker**; page numbers are carried only by the shell (testing produced two clashing sets of page numbers, "02/03" and "6/16")
- Body text ≥24px, labels and annotations ≥16px, headings 60–120px (full type-size table in the "Scale guidelines" section of `references/content-guidelines.md`)
- Fixed-size content implements its own scaling + letterbox (the shell already does this)
- Store the playback position in localStorage so it survives a refresh
- Use the deck type-size floors when running the design check: `python3 "$HD/scripts/design_lint.py" check slides/*.html --viewport 1920x1080 --min-body 24 --min-label 16`. A single-file deck-stage can only check the slide currently displayed, which is one of the reasons multi-file is the default

## Don't default data slides to "three big numbers + a bar chart"

That's the template answer for deck data slides, and it looks the same whatever the style. First ask what relationship this set of numbers is meant to show: proportion (a real object scaled proportionally), change (one narrative curve), composition (a whole taken apart), comparison (side-by-side contrast), scale (one oversized object). The data itself can be the hero asset of the slide (`references/materials.md`).

## Related files

| What you're doing | Read |
|---|---|
| Architecture, directories, single-slide skeleton, common pitfalls | `references/slide-decks.md` |
| Editable PPTX · route A | `references/editable-pptx.md` + `scripts/html2pptx.js` |
| Editable PPTX · route B (already-written visual drafts / client templates) | `references/pptx-from-rendered-html.md` + `scripts/pptx_from_rendered.py` |
| Speaker notes, Tweaks parameter tuning | `references/slide-decks.md`, `references/tweaks-system.md` |
| Style library and specimens (the PPT section of the seconds roulette, plus the cross-media Chinese & East Asian section) | `references/design-styles.md` |
