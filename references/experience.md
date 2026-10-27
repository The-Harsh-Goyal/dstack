# Shipped experience (dstack)

Findings that have reproduced across projects, or been measured, and hold for any user. Before work starts, `learn.py` brings out the entries that match the topic.

Maintenance rules are in `references/evolution.md`: edit only by hand in the repo; once a reference absorbs an entry, delete it; one user's taste doesn't go in here.

## S1 · verified · topics: direction, color, typography

- Finding: without constraints, all three directions slide together toward a warm cream background + high-contrast serif headings + terracotta accents. This is the model's own default aesthetic (Anthropic's interface palette), and Anthropic's official frontend-design skill (2026) lists it as the first clustering trait of AI-generated pages. But the family itself isn't ugly; the problem is the three versions crowding together and it recurring from project to project (see S6).
- Next time: don't let the three versions crowd into the same look family; `design_lint.py compare` will report "three versions land in the same look family", and `ledger check` will report a collision with recent projects.
- Evidence: internal self-tests during skill development and three-direction screenshots from several projects (2026-10 review, unpublished); official source text https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md

## S2 · verified · topics: direction, layout

- Finding: if the three versions only change colors and fonts and share one layout skeleton, reviewers and users will spot it as a reskin at a glance. The differences have to land in how the information is organized.
- Next time: the skeletons of the three direction cards must differ from one another; if `compare` shows skeleton correlation is too high, go back to the cards and change the skeleton or the source. Be careful not to overcorrect: forcing every version into a metaphor makes pages try too hard (see S5).
- Evidence: internal blind tests during skill development and the 2026-10 review (unpublished).

## S3 · verified · topics: readability, quiet, whitespace

- Finding: a quiet, lavish-whitespace style taken too far turns into large areas of dead white with tiny font sizes. At first glance it looks like the page didn't finish rendering, and it loses to an ordinary baseline version.
- Next time: the font size and contrast floors (web body text ≥14px, deck ≥24px, long mobile image ≥36px canvas pixels, contrast ≥4.5:1) are not waived for any style; `design_lint.py check` will show a red light.
- Evidence: internal blind-test reviews during skill development (unpublished).

## S4 · verified · topics: assets, logo, single-file

- Finding: in a single-file HTML meant to be opened by double-clicking, referencing images and the logo with relative paths means every image breaks when the directory moves.
- Next time: single-file deliveries always embed as base64; `design_lint.py check` shows a yellow light for relative-path images and a red light for images that are already broken.
- Evidence: in a blind test, all six product buttons had broken images and the version lost the review outright.

## S5 · verified · topics: direction, metaphor, intensity

- Finding: forcing every version to settle a "big idea metaphor" first, to push the three directions apart, turns whole pages into props (filing cabinets, library cards, prescription slips) or slaps on all-purpose metaphors (subway route maps, terminals, newspaper front pages). The three directions did spread apart, but the blind pick lost to the version without this constraint, and the same subway map appeared once each in two unrelated topics, which is just a new kind of sameness.
- Next time: among the three full versions, at most one turns the whole page into a prop or uses an all-purpose metaphor; to judge, remove the device and see whether the information gets clearer or muddier.
- Evidence: before/after blind picks for the 2026-10 revision (the new approach won only 1 of 4 rounds), and the new approach used a subway route map twice in those 4 rounds (internal benchmark during skill development, unpublished).

## S6 · verified · topics: direction, constraint, boring

- Finding: constraints added to avoid the default AI look (at most one of three versions in warm paper and serif, a yellow light for the look family, a quota on trying too hard) made all three versions retreat together to light, cool colors and tidy grids. The user rated them "too tidy, too boring", and the blind pick lost again to the old approach without those constraints. The versions that were approved under the old approach happened to be a dark background with a single accent, and warm paper with serif. Constraints can only reduce options; they can't reduce their way to good design.
- Next time: add options, not bans. Each logic produces two candidates, draw thumbnails first and then pick; see styles in the specimens, and break down references from screenshots. Use the look family only to compare the three versions and to compare against the ledger.
- Evidence: second round of before/after blind picks, 2026-10 (2 rounds, the revision lost both), internal benchmark during skill development, unpublished.

## S7 · observed · topics: direction, reference, medium

- Finding: directions whose real-world reference was an award-winning work in the same medium (an App referencing an Apple Design Award winning App, a bookstore deck referencing Stripe Press) were approved; cross-medium references (a deck referencing a 1935 Penguin paperback cover, an App referencing herbarium mounting sheets) came out one trying too hard and one boring.
- Next time: prefer same-medium real-world references; from cross-medium ones, borrow only color or type relationships, not layout.
- Evidence: 4 real-world reference directions across the second and third rounds of blind picks, 2026-10. Small sample, awaiting validation from more projects.

## S8 · verified · topics: direction, style, reference

- Finding: "add options, not bans" won in the blind pick. Three logics, two candidates each, thumbnails first and then pick three; styles seen in specimens, references broken down from screenshots, and the look family no longer shows a yellow light. On the same two rounds that lost last time, the revision was picked in both, and the user's verdict was "this is clearly better this time".
- Next time: when you hit "too monotonous" or "too AI-looking", add candidates and references first, don't add bans first; any new ban must pass a round of blind picks first.
- Evidence: third round of before/after blind picks, 2026-10 (2 rounds, the revision won both), internal benchmark during skill development, unpublished.
