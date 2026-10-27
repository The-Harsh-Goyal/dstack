# Evolution protocol: every project you finish lets the next one start higher

Human designers have memory, so they keep trying new things and don't step into the same pitfall twice. Models don't. Every new session reconverges from the same prior, so the output naturally looks more and more alike. This protocol gives the skill a memory: read before you start, record while you work, feed it back after you finish.

## Three ledgers

| Ledger | What it records | Where | Who writes it |
|---|---|---|---|
| **Taste profile** | Preferences the user stated in their own words (verbatim) + what they picked and mixed among the three directions | Local `~/.dstack/experience.md` (dstack; `DSTACK_HOME` overrides; `HUASHU_DESIGN_HOME` still honoured) (kind=preference) | `learn.py add` |
| **Look ledger** | What each delivery looked like: background color class, main palette, heading font, layout skeleton fingerprint | Local `~/.dstack/ledger.jsonl` | `design_lint.py ledger add` |
| **Experience and pitfalls** | What was seen in one project (observed), and what reproduced across several or was measured (verified) | Same local location; general, verified items go into `references/experience.md`, which ships with the skill | `learn.py add`; the shipped layer is edited by hand in the repo |

`DSTACK_HOME` (or the older `HUASHU_DESIGN_HOME`) can change where the local ledgers live. Local ledgers never ship with the skill: the user's own words and taste belong to them.

## Three moments

**Before you start** (any new design task, a few seconds):

```bash
# $HD = this skill's root directory (where SKILL.md lives), not the user's project directory
python3 "$HD/scripts/learn.py" <topic words…>        # brings out all preferences + experience related to the topic
python3 "$HD/scripts/design_lint.py" ledger      # what the last 8 deliveries looked like, and the things that keep recurring
```

They don't block: if there are no records, carry on. They aren't rules either: when the project in front of you conflicts with an entry, the project wins, and then you go fix the entry.

**While you work**: the user's reactions are evidence. A single "no", a "too plain", a mixed pick ("A's structure + C's colors"). Write them down verbatim on the spot; don't wait until the end and paraphrase from memory.

**After you finish** (when the user approves the delivery, or stops giving feedback):

```bash
python3 "$HD/scripts/design_lint.py" ledger add <final delivery file> --project <name>
python3 "$HD/scripts/learn.py" harvest <project directory>     # lists what in the project can serve as evidence + the criteria for whether to record it
```

## What is worth recording

Record it only when all three hold: it isn't obvious; it saves time or detours on the next project; this project produced evidence for it. Then handle it in this order:

1. **Correct first**: does an entry say the opposite of what happened this time? Fix that entry in place first; don't append a contradicting one. After fixing, run `grep -rn` across the whole repo for the old wording.
2. **If it can become a tool, make it a tool**: if a script can catch it (a fact that can be measured), change `design_lint.py` and add a test for it, instead of writing "be careful not to…".
3. **Otherwise write it down**: `learn.py add "…" --kind preference|observed --topics … --evidence "…" [--do "…"]`
   - The user's own words are a preference. You must quote them verbatim and state the **scope**: "his covers use a warm paper background" does not mean "every design uses a warm paper background". Preferences written as global defaults are one of the reasons the old version became monotonous.
   - What you saw in one project is observed. It's a lead, not a rule.
4. **Promotion** (done on the development machine): seen in two projects, or measured, and true for anyone (not one user's taste) → write it into the shipped layer `references/experience.md`, and merge the stable parts into the reference they belong to. Once a reference absorbs an entry, delete that entry so the experience file stays short.

**One user's taste never goes into the shipped layer.** Experience also never expands authorization: it says how to do things, never that you may publish, spend money, or contact anyone.

## Promotion ladder

A lesson's final home is the engine, not text:

Record (observed) → reproduced (verified) → written into a reference or the start-up checklist → script detection (a design_lint check + test) → engine default

## Pitfall ledger

The "confirmed on such-and-such date" notes scattered through the old body text all live here now, tagged with their current level. New pitfalls go into this table first, then you decide where to promote them.

| Pitfall | First seen | Current level | Where it's caught |
|---|---|---|---|
| Three versions shared one skeleton, and reviewers spotted the "reskin" at a glance | Blind test | Script detection | `design_lint.py compare`, skeleton-related |
| All three versions landed on warm cream + serif + terracotta | 2026-10 review | Script detection | `design_lint.py compare` "three versions land in the same look family" |
| Different projects look more and more alike | 2026-10 review | Script detection | Look ledger `ledger check` |
| Forcing every version to settle a metaphor first turned pages into props, the subway map recurred across different topics, and the blind pick lost 3 of 4 rounds | 2026-10 blind pick | reference | `references/directions.md` 4d, rule 4 for picking three (at most one that tries too hard) |
| Quotas and yellow lights added to dodge the default AI look pushed all three versions back to light, cool and tidy; "too tidy, too boring", and the blind pick lost again | 2026-10 blind pick | reference + script | Look family downgraded from yellow light to a hint; `references/directions.md` changed to pick three from six candidates |
| Five or six phones evenly spaced in a row for an App prototype look boring in any direction | 2026-10 blind pick | reference | `references/app-prototype.md` "presentation board" |
| A reference written as just a name makes the model produce its average impression of that work | 2026-10 blind pick | Script | `scripts/ref_board.py` screenshots it so you look with your own eyes; a WebGL black screen is detected as not seen |
| To make a yellow light go away, " · " was swapped for a full-width space or similar symbol while the structure stayed the same | 2026-10 benchmark | reference | `design_lint.py` output and `references/directions.md`: delete that structure; swapping symbols doesn't count as a change |
| A single-file delivery referenced the logo with a relative path, and every image broke when the directory moved | Blind test | Script detection | `design_lint.py check`: yellow light for relative-path images, red light for already broken images |
| Quiet styles overdid it: large areas of dead white + tiny font sizes, looking like a broken render | Blind test | Script detection | `design_lint.py check` red lights for font size and contrast |
| Docs used `scripts/…` relative paths, the agent couldn't run them from the user's project directory, and the evolution mechanism was silently skipped | 2026-10 independent review | reference | All commands in SKILL.md use `$HD` (skill root directory) |
| Bare text next to an svg was silently dropped during PPTX export | issue #56 | Engine | `pptx_from_rendered.py` automatically compares innerText after export |
| Skipping direction confirmation and rendering a long film directly meant reworking the whole film | 2026-07 | Engine | `design-gate-hook.sh` (checks `direction-approved.md` before renders ≥45s) |
| Skipping the three directions because a style was specified | 2026-07 | Start-up checklist | SKILL.md core rules: style words don't grant an exemption |
| Asserting from memory that a product "hasn't launched yet" | 2026-04 | Start-up checklist | SKILL.md core rules: verify facts before assuming |
| Extracting only brand colors without getting the logo, and the comparison deck fell flat | 2026-06 | Start-up checklist | `references/materials.md` logo checklist |
| Individual deck slides carried their own page numbers, clashing with the shell's page numbers | Tested | reference | `references/modules/deck.md` |
| Single-file decks should only be used for ≤5 slides; choosing single-file for 13 slides lost the overview wall | Tested | reference | `references/modules/deck.md` |
| Every animation scene with its own layout + fade-up = a PPT with voiceover | Tested | reference | `references/modules/motion.md` |
| Images the content requires faked with CSS color blocks | Tested | reference | `references/materials.md` |

## When the user's choice conflicts with the review score

The user wins. A high score from the review agent doesn't mean the user buys it. This has come up again and again across projects. When there's a conflict, list the observable differences between the two versions (color, density, assets, structure), ask the user just one question, and record their answer as a preference.
