# Workflow: from receiving a task to delivery

The more senior the designer, the earlier they align, because they know better what rework costs. This file is the main workflow after the three directions are chosen, plus how to ask questions before you start.

## Standard workflow (after the three directions are chosen)

1. **Understand the requirements**: when a specific product, technology or event is involved, the first action is a WebSearch to verify existence, release status, version and specs, written into the project's `product-facts.md`. This step comes before asking questions. Don't re-ask what three-direction Phase 1 already asked; for new tasks that didn't go through the three directions (for example after a direction exemption), ask one round; skip it for small fixes.
2. **Explore resources, extract core assets**: read the design system, links, screenshots, code. When a specific brand is involved, follow the brand asset protocol and produce `brand-spec.md`. Before starting, confirm the core assets are in place: physical products have product images, digital products have a logo and UI screenshots, and color values are extracted from real HTML/SVG. If something is missing, stop and fill it in.
3. **Answer the five form questions first, then plan the system** (before starting each page, screen or shot):
   - **Narrative role**: hero / transition / data / quote / ending?
   - **Viewing distance**: 10cm phone / 1m laptop / 10m projection? This decides font size and density
   - **Visual temperature**: quiet / excited / calm / authoritative / gentle / sad?
   - **Capacity estimate**: draw 3 five-second sketches and work out whether the content fits
   - **Visual motif**: what visual element, structure or metaphor is unique to this content, something no other subject would have? If you can't answer, you're still drawing lots from style labels

   Once answered, state the design system (color, typefaces, layout rhythm, component patterns); the system serves the answers. At delivery, write one sentence on "where in the content the form comes from".
   🛑 State the five answers + the system, and wait for the user to nod before writing code.
4. **Create the folder**: put the main HTML and the assets you need under `project-name/` (don't bulk-copy >20 files).
5. **Alignment pass**: at the top of the HTML, write assumptions + placeholders + reasoning comments. 🛑 Show the user as early as possible (even if it's just gray boxes with labels), and wait for feedback before writing components.
6. **Full pass**: fill placeholders, make variants, add Tweaks. Show the user once more halfway through.
7. **Verify**: Playwright screenshots, check for console errors, `python3 "$HD/scripts/design_lint.py" check` (red lights must be fixed). 🛑 Before delivery, look through it in the browser with your own eyes; interactions written by AI often have bugs.
8. **Deliver and feed back**: the summary only covers caveats and next steps; `design_lint.py ledger add` records the look ledger; `learn.py harvest` shows what's worth recording (`references/evolution.md`).

**Checkpoint principle**: when you hit 🛑, stop and say clearly "I did X, next I plan to do Y, do you confirm?", then actually wait. "Continue" authorizes moving to the next step, not skipping the gate within this step.

## Exception handling

| Scenario | Handling |
|---|---|
| Requirements too vague to start | List 3 possible directions (e.g. "landing page / Dashboard / product detail page") for the user to choose; don't fire off 10 questions directly |
| User says "stop asking, just do it" | You can skip the questions (fill in assumptions yourself), but still go through the three directions; only when the user explicitly says "don't make three versions / one is enough" do you drop to 1 main + 1 variant, and record their exact words in `direction-approved.md` |
| Reference images clash with the brand guidelines | Stop, point out the specific contradiction ("the screenshot uses a serif, the guidelines say sans-serif"), and let the user choose |
| Starter components fail to load | First check the error table in `references/react-setup.md`; if that doesn't work, downgrade to plain HTML+CSS |
| Tight on time, "need it within 30 minutes" | Skip the alignment pass and go straight to the full pass, make only 1 option, and mark it "not confirmed early" at delivery |
| A single HTML >1000 lines | Split it into multiple jsx files per `references/react-setup.md`, sharing via `Object.assign(window, …)` at the end |
| The restraint principle conflicts with the information density the product needs | When the product's selling point is AI, data or context awareness (Dashboard, Tracker, Copilot, health, bookkeeping), go high density: ≥3 places per screen with differentiated, contentful information; decorative icons are still out |

When an exception happens, first tell the user in one sentence what happened, then handle it per the table; don't make silent decisions.

## The art of asking questions

Ask only one round for the whole project: tasks that go through the three directions ask in Phase 1 (at most 3 questions + ask for all reference material at once). The list below is a question bank; pick the ones that most affect the result, not every question. This isn't a formality; you really do need to understand the requirements. But don't ask just to fill a quota: decide what you can infer yourself and note the basis. If the user doesn't respond, fill in assumptions with your best judgment and keep going, replacing follow-up questions with something they can see.

**When you must ask**: new tasks, vague tasks, no design context, the user said only one vague sentence.

**When you can skip asking**: small fixes, follow-up tasks, the user has already given a clear PRD + screenshots + context.

**How to ask**: most agent environments have no structured question UI, so ask with a markdown list in the conversation. **List all the questions at once and let the user answer in a batch**; don't go back and forth one at a time, which wastes the user's time and breaks their train of thought.

## Must-ask checklist

Every design task must clarify these 5 kinds of questions:

### 1. Design Context (most important)

- Is there an existing design system, UI kit or component library? Where?
- Are there brand guidelines, color specs, type specs?
- Are there screenshots of existing products/pages to reference?
- Is there a codebase to read?

**If the user says "no"**:
- Help them find it: go through the project directory, see whether there's a reference brand
- Still nothing? Say clearly: "I'll work from general intuition, but that usually doesn't produce work that fits your brand. Would you consider providing some references first?"
- If you really have to go ahead, follow the fallback strategy in `references/design-context.md`

### 2. Variations dimensions

- Beyond the three directions, which dimensions does the user want to see variants on? (The three directions themselves are fixed; no need to ask how many)

### 3. Fidelity and Scope

- How high fidelity? Wireframe / half-finished / full hi-fi with real data?
- How many flows to cover? One screen / one flow / the whole product?
- Are there specific "must include" elements?

### 4. Tweaks

- Which parameters do they want to adjust live? (color / font size / spacing / layout / copy / feature flag)
- Will the user want to keep adjusting it themselves after it's done?

### 5. Task-specific (at least 4)

Ask 4+ detailed questions about the specific task. For example:

**Making a landing page**:
- What's the target conversion action?
- Main audience?
- Competitor references?
- Who provides the copy?

**Making iOS App onboarding**:
- How many steps?
- What does the user need to do?
- Skip path?
- Target retention rate?

**Making an animation**:
- Duration?
- Final use (video asset / website / social)?
- Pacing (fast / slow / sectioned)?
- Key frames that must appear?

## Question template example

For a new task, you can copy this structure and ask in the conversation:

```markdown
Before I start, I'd like to align on a few questions. They're all listed here, so you can answer them in one go:

**Design Context**
1. Is there a design system / UI kit / brand guidelines? If so, where?
2. Are there screenshots of existing products or competitors to reference?
3. Is there a codebase in the project I can read?

**Variations**
4. Beyond the three directions, which dimensions do you want variants on (color / layout / copy / interaction)?
5. Any elements that must be included?

**Fidelity**
6. Fidelity: wireframe / half-finished / full hi-fi with real data?
7. Scope: one screen / one whole flow / the whole product?

**Tweaks**
8. Which parameters do you want to adjust live after it's done?

**Specific task**
9. [Task-specific question 1]
10. [Task-specific question 2]
...
```

## Early alignment mode

This is the most important part of the whole workflow. **Don't charge ahead blindly the moment you get a task**. Steps:

### Pass 1: Assumptions + Placeholders (5-15 minutes)

At the top of the HTML file, first write your **assumptions + reasoning comments**, like a junior reporting to a manager:

```html
<!--
My assumptions:
- This is for an XX audience
- I read the overall tone as XX (based on the user saying "professional but not stiff")
- The main flow is A→B→C
- For color I'd like brand blue + warm gray; not sure whether you want an accent color

Open questions:
- Where does the data in step 3 come from? Using a placeholder for now
- Abstract geometry or real photos for the background image? Placeholder for now

If you see this and feel the direction is wrong, now is the cheapest time to change it.
-->

<!-- then the structure with placeholders -->
<section class="hero">
  <h1>[Main title slot - waiting for the user]</h1>
  <p>[Subtitle slot]</p>
  <div class="cta-placeholder">[CTA button]</div>
</section>
```

**Save → show the user → wait for feedback before the next step**.

### Pass 2: Real components + Variations (the bulk of the work)

Once the user approves the direction, start filling it in. At this point:
- Write React components to replace the placeholders
- Make variations (with design_canvas or Tweaks)
- For slides/animations, start from the starter components

**Show it once more halfway through**; don't wait until everything is done. If the design direction is wrong, showing it late means the work is wasted.

### Pass 3: Detail polish

Once the user is happy with the whole, polish:
- Fine-tune font size / spacing / contrast
- Animation timing
- Edge cases
- Finish the Tweaks panel

### Pass 4: Verify + deliver

- Take Playwright screenshots (see `references/verification.md`)
- Open the browser and confirm by eye
- Keep the summary **minimal**: only caveats and next steps

## The deeper logic of Variations

Giving variations isn't about creating decision paralysis for the user; it's about **exploring the space of possibilities**. Let the user mix and match their way to the final version.

### What good variations look like

- **Clear dimensions**: each variation changes along a different dimension (A vs B only swap the palette, C vs D only swap the layout)
- **A gradient**: stepping up from a "by-the-book conservative version" to a "bold novel version"
- **Labeled**: each variation has a short label saying what it explores

### How to implement

**Pure visual comparison** (static):
→ Use `assets/design_canvas.jsx` to show them side by side in a grid layout. Each cell has a label.

**Multiple options / interaction differences**:
→ Build a complete prototype and switch with Tweaks. For example, for a login page, "layout" is one tweak option:
- Copy on the left, form on the right
- Logo at the top + form in the center
- Full-screen background image + floating form

The user can switch by toggling Tweaks, without opening multiple HTML files.

### Thinking in an exploration matrix

For every design, run through these dimensions in your head and pick 2-3 to give variations on:

- Visual: minimal / editorial / brutalist / organic / futuristic / retro
- Color: monochrome / dual-tone / vibrant / pastel / high-contrast
- Typefaces: sans-only / sans+serif contrast / all serif / monospace
- Layout: symmetric / asymmetric / irregular grid / full-bleed / narrow column
- Density: sparse and airy / medium / information-dense
- Interaction: minimal hover / rich micro-interactions / dramatic large animations
- Material: flat / layered shadows / texture / noise / gradients

## When you hit uncertainty

- **Don't know how to do it**: say honestly that you're not sure, ask the user, or make a placeholder and keep going. **Don't make things up**.
- **The user's description contradicts itself**: point out the contradiction and let the user choose one direction.
- **The task is too big to take in one go**: break it into steps, do the first step for the user to see, then push forward.
- **The effect the user asks for is technically hard**: explain the technical limits clearly and offer alternatives.

## Summary rules

At delivery, the summary is **extremely short**:

```markdown
✅ Slides done (10 slides), with Tweaks to switch between "night/day mode".

Notes:
- The data on slide 4 is fake; I'll replace it once you provide the real data
- The animation uses CSS transitions, no JS needed

Suggested next step: open it in your browser and look through it first; if anything's wrong, tell me which slide and where.
```

Don't:
- List the contents of every slide
- Repeat what technology you used
- Praise how good your design is

Caveats + next steps, done.
