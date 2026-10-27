# Three Directions: Three Good Designs, Not Three Skins

For any new visual design, first produce real first drafts in three directions for the user to choose from. This gate itself doesn't change: it triggers 100% of the time, a specified style or brand doesn't exempt it, you stop once they're laid out, and the choice is recorded in `direction-approved.md` (for exemptions see SKILL.md "Core rules").

This file covers **how the three directions are generated**.

## Why it works this way (conclusions from three rounds of problems and blind picks)

**First-round problem: the three versions only changed skins.** The three versions were often the same skeleton with different colors and font weights. The differences need to land in the layout structure, not the color scheme.

**Second-round problem: metaphors pushed too hard.** Forcing each version to first settle on a "big-idea metaphor" turned whole pages into filing cabinets, library cards, and subway maps, and the user's blind picks lost 3 of 4 questions.

**Third-round problem: too many constraints, so it became boring.** To avoid the "AI default look", we once limited the three versions to at most one warm-paper serif, and listed look families like dark-background single-accent and hairline newspaper as yellow lights. The result: all three versions retreated together into light cool colors and orderly grids, the user said "too orderly, too boring", and it lost again to the old approach without these constraints. And the versions he approved under the old approach happened to be exactly dark-background single-accent and warm-paper serif.

So the current approach is **add options, not bans**: the three logics stay the same, each produces two candidates, six thumbnails are drawn first, and the strongest and most different three are picked to become full versions; styles are chosen from specimens you can see, and references are broken down from real screenshots. Look families are no longer a flaw; you only need to switch when all three versions crowd into the same family, or collide with a recently delivered project.

## Process

### Phase 1 · Clarify requirements + proactively ask for references

This is the only round of questions in the whole project (no re-asking once a direction is chosen; pick from the question bank in `references/workflow.md`), at most 3 questions at once: audience / core message / emotional tone / output format. At the same time, ask for all the reference material at once: what the project is called, whether there's a logo / brand colors / VI / type specs, whether there's a website or screenshot with "exactly that feeling"; if there's none, just one line saying "your call".

If the user doesn't respond, don't wait idly: fill in assumptions with your best judgment (labeled as assumptions), go straight ahead, and let "something you can see" replace further questions.

If they give a specific brand or product name (the kind where you can find a logo on the official site) → additionally run the Brand Asset Protocol (`references/brand-asset-protocol.md`); all three directions are based on the same set of real assets, and they differ in interpretation. A generic subject (coffee, history, fitness) isn't a brand; don't go looking for "the logo of coffee".

### Phase 2 · Advisor-style restatement

Restate in your own words the essential need, audience, scenario, emotional tone, and the expectations the user didn't voice. End with "I'll go ahead and make real versions in 3 different directions for you to look at", not with "which direction do you want to pick": a choice made before seeing visuals is meaningless.

### Phase 3 · Lock in the spec

Write a thorough design spec; it's the shared input for all three directions: what the project is, audience and scenario, core message in bullet points, emotional tone, **output format and dimensions (required, and identical across all three versions, otherwise they can't be compared side by side)**, known constraints, image needs. The spec only says "what to say", not "what it looks like": what it looks like is the direction card's job.

### Phase 3.5 · Assets first

Following `references/materials.md`, first determine the tier and gather the real images the content requires and the logos of named products, shared by all three directions.

### Phase 4 · Six candidates → six thumbnails → pick three

Before you start writing, look at three things:

```bash
# $HD = this skill's root directory (where SKILL.md lives), not the user's project directory
python3 "$HD/scripts/learn.py" direction color <subject-keywords>   # This user's preferences + past lessons
python3 "$HD/scripts/design_lint.py" ledger                     # What recent deliveries looked like and the references used: don't use them this time
```

Then use your image-viewing ability to open the style overview: `$HD/assets/style-specimens/sheet-<section>.jpg` (sections: web / ppt / info / app, plus the cross-media east section for Chinese & East Asian). One image holds the specimens of every style in that section, so you first know what each style looks like done right.

**4a · Three logics, two candidates each (six in total):**

- **Best designer ×2**: take a deep breath and think hard: if the budget were unlimited, which studio or designer in the world is best suited to design for "this user, this subject"? Come up with two of different temperaments (one bold, one restrained; or one Western, one East Asian). Adopt their design thinking and build from scratch; don't imitate the look of one of their works. Don't always reach for the same few names: beyond Pentagram, Kenya Hara, and Vignelli, there are Lü Jingren, Kohei Sugiura, Ikko Tanaka, Kazunari Hattori, Irma Boom, Experimental Jetset, Collins, Studio Dumbar…
- **Real-world reference ×2**: pick two real works **in the same medium** as the need, which you're sure are superbly designed: for an App, find Apps (Apple Design Awards); for a website, find websites (Awwwards annuals, brand sites); for a deck, find publications and pitches; for an infographic, find newspaper graphics (SND, Malofiej award winners). Same-medium references transfer their layouts directly; cross-media ones (making a deck into a Penguin cover, making an App into a specimen mount) proved in testing to be either overdone or boring. Verify that it exists with WebSearch, then **screenshot it and look**:

  ```bash
  python3 "$HD/scripts/ref_board.py" <work-url-or-image-url> [<second-one>] --out refs/board.jpg
  ```

  Use your image-viewing ability to open the reference board, and write what you borrow as concrete rules: how many grid columns, the heading-to-body size ratio, the share of the main color, the image-text relationship. If you can't capture it (anti-scraping, WebGL black screen), switch to a press page or images of the same work, or ask the user for screenshots; if none of that works, write "not seen firsthand" on the card, and don't pretend you've seen it.
- **Seconds roulette ×2**: take the current seconds S (`date +%S`; on Windows PowerShell use `(Get-Date).Second`), draw number `S % number-of-styles-in-section + 1` from the matching section of `references/design-styles.md`, then draw number `S % 12 + 1` from the east section. The number is the order in which the entry appears in its section, matching the numbers in the specimen file names and on the overview grid cells. First open the specimen image of the drawn style (the "Specimen" line in the entry) and see clearly what it looks like done right before writing the card. If you draw something of the same kind as the last 3 deliveries in the look ledger, move on to the next number; do the same when the draw clashes with the topic or brand (dstack: e.g. an East-section style that would add a national or cultural cue to a geopolitical theme, or a style the brand spec excludes), and log one line in directions.md saying why; if fidelity is <70%, note which part is downgraded. The roulette's job is to take you somewhere you wouldn't choose yourself.

**When the user has specified a style or brand**: the six candidates each give one interpretation within that context, and the colors may all be constrained by the brand (add `--brand` to compare, comparing skeletons only); the roulette only draws from styles compatible with the context. "Apple style" is a context, not a design.

**4b · Write six direction cards** into `directions.md` in the project directory, one paragraph each:

| Field | What to write |
|---|---|
| Logic and source | Which designer / which work (with citation and reference board path) / which number and style was drawn |
| What's borrowed | The concrete rules broken out of the source to apply to this design: grid, type relationships, color proportions, image-text relationship |
| Hero asset | What the picture's protagonist is: real image, generated image, procedural texture, data image, giant type… (for tiers see `references/materials.md`) |
| Skeleton | The layout structure in one sentence |
| Where the boldness goes | The single boldest place; everything else serves the content |
| Where in the content the form comes from | One sentence: which thing in this design only this subject would have |

**4c · Draw six thumbnails.** One `design-demos/thumbs.html`, six cells, each the candidate's most crucial screen (web first screen, deck cover, infographic opening, App main screen), about 480×300: real fonts, real colors, real skeleton, real headline (dstack: the headline is optional for text-free covers, thumbnails or a brand whose covers carry no text; then the cell shows the real image composition instead); details can be skipped. After screenshotting, look with your image-viewing ability. Thumbnails are cheap; this step exists to try more styles. If a thumbnail looks wrong, switch the source and redraw that cell, instead of finding out only after building the full version.

**4d · Pick three to make full versions**, by these criteria in order:

1. **Good enough on its own**: you wouldn't be embarrassed to show it. If it can't hold up as a thumbnail, the full version can't save it.
2. **The three differ from each other**: different skeletons, different temperaments (bold / neutral / quiet needn't all be present, but don't make all three the same temperature), not crowded into the same look family.
3. **No collision with recent projects**: looks and references just used in the look ledger aren't picked this time.
4. **Not overdone**: turning the whole page into a prop or replica of a physical object, applying a one-size-fits-all metaphor (subway map, terminal command line, newspaper front page, dashboard), maxing out saturation and type size across the board: at most one of the three can be like this, and only when the content truly needs it. How to judge: **remove this technique; does the information get clearer or muddier?** If removing it makes things clearer, it's overdone.

The three don't need one from each logic: two best designers plus one roulette is fine too; pick the strongest. Keep the three that weren't picked and show them to the user alongside.

An example (subject: the official website of a handmade soy sauce brewery run for three generations):

- Best designer | Kenya Hara | borrowed: lots of white space, the material itself as the protagonist, very little text | hero asset: real photos of the clay vats and the drying yard | skeleton: one image and one sentence per screen, a slow vertical rhythm | boldness: a full first screen of a salt-frost close-up | form: soy sauce sun-dries for 180 days, so the rhythm slows down
- Real-world reference | an award-winning website of an old Japanese food brand (screenshot attached) | borrowed: the relationship between vertical headings and horizontal captions, the ratio of two colors, thin-framed sections | hero asset: real photos of the bottle + vertical headings | skeleton: vertical heading on the left, three columns of content on the right | boldness: only two colors | form: the "recipe" temperament of an old brand
- Seconds roulette | drew "Editorial Brutalism" | borrowed: huge type-size contrast and a modular grid | hero asset: an oversized Chinese character 「酱」 ("sauce") cutting into the first screen | skeleton: modular grid, alternating images and text | boldness: the type-size contrast on the first screen | form: one character tells the whole story of a sauce brewery

### Phase 5 · Build in parallel, self-check each version

Each subagent gets only the spec + its own single direction card (including the reference board or specimen image) + the shared assets, with independent context and no reference to the others. On runtimes that don't support subagents, build serially: before starting each version, read only the spec and its own card, without referring to versions already made.

Build rules (shared by all three versions):

- Real user content, no Lorem; all three versions have the same content and change only the design
- Hard readability floor: web body ≥14px, labels ≥12px; deck body ≥24px, labels ≥16px; 1080-wide long images viewed on phones body ≥36px, labels ≥28px; body contrast ≥4.5:1; white space must be composition, not missing content
- Single-file HTML; for single-file delivery, images and logos are embedded as base64
- Decks use the deck shell, with 2 representative pages per direction (`references/modules/deck.md`)
- For multi-screen App prototypes, don't just line up a row of phones; for presentation board composition see "Presentation board" in `references/app-prototype.md`
- Save thumbnails to `design-demos/thumbs.html` and the three full versions to `design-demos/dir-1.html`, `dir-2.html`, `dir-3.html` (decks are subdirectories like `dir-1/`); screenshot with `npx playwright screenshot file:///… out.png --viewport-size=1440,900` (1920,1080 for decks)

After all three versions are done, run:

```bash
python3 "$HD/scripts/design_lint.py" check design-demos/dir-*.html       # Red lights must be fixed; yellow lights are habitual template chrome, delete them; look families are only notes
python3 "$HD/scripts/design_lint.py" compare design-demos/dir-*.html     # Two versions collide → swap in another one from the alternates, or change the skeleton, not the colors
#   Add --brand when the brand constrains colors and fonts; add --ignore-layout for App prototypes with several phones side by side; for decks add --viewport 1920x1080 --min-body 24 --min-label 16
python3 "$HD/scripts/design_lint.py" ledger check design-demos/dir-*.html # Collides with a recent project → swap in another one from the alternates
```

Name the full versions `design-demos/dir-1.html` through `dir-3.html`, and confirm there really are 3 before moving on. For a yellow light, just delete that structure; swapping in a different symbol to dodge the check doesn't count as a fix. Look families don't need changing; they only matter when the three versions crowd together or collide with the ledger. If the Python version of playwright isn't installed, the script skips and prompts you to install it; in that case, compare the three versions by eye from screenshots, and note this in the delivery notes.

### Phase 6 · Present, then stop

Lay out the screenshots of the three full versions together, each with a summary of its direction card (logic and source, what's borrowed, hero asset) and one sentence on "where in the content the form comes from"; then attach the thumbnail overview with one line: "The other three are alternates; if one catches your eye, I'll make it into a full version." Once they're laid out, end this turn and wait for the user to choose, including in unattended sessions.

### Phase 7 · After the user chooses

- Write "which versions were shown, the screenshot paths, and the user's exact words" into `direction-approved.md`
- If the user's words include a clear statement of taste ("this doesn't feel AI at all", "too plain", "make it more like a magazine"), record it verbatim with `learn.py add --kind preference`, and state where it applies
- Follow mixed choices ("A's layout + C's colors") as given, and note which two fields they mixed: that's more useful than remembering which color they picked; if they say a version is "overdone" or "too plain", record that verbatim too
- Move into execution; after delivery, log a look ledger entry with `design_lint.py ledger add <final-file> --project <name> --note "<source: designer/work/style>"`, so next time the references get avoided too
