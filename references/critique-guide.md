# Design Critique In-Depth Guide

> Detailed reference for Phase 7. Provides scoring criteria, per-scenario emphasis, and a list of common problems.

---

## Scoring criteria in detail

### 0. Concept / core idea (Concept) · highest weight

First ask "does this design have an idea", then look at whether it's done well. Why it's in position 0: execution is an amplifier, and amplifying a hollow concept only makes it hollower.

| Score | Criteria |
|------|------|
| 9-10 | Has a unique idea grown from the user's content; the visual motif is irreplaceable |
| 7-8 | Has a clear core idea; the motif relates to the content but would just about work for a similar subject |
| 5-6 | Style only, no concept: good-looking, but says nothing |
| 3-4 | A generic template reskinned; zero at the concept level |
| 1-2 | Didn't even pick the right style; pure piled-up decoration |

**Core question list**:
- What does this design say? Can you state its idea in one sentence? If you can't, it doesn't have one
- Cover all text and logos: can you still recognize the subject? If not, the visuals aren't carrying the expression (except for typographic designs where the text is the motif; ask instead: would this text treatment still hold up for a different subject?)
- Would it still hold up with a different client name/product name? **If it would = template; this dimension is capped at ≤5**
- Does the form have a unique visual motif drawn from the content? (echoes SKILL.md's form derivation: form should be derived from the content, not drawn from the style library)

**Veto rule**: when Concept is ≤5, the overall score is capped at 6.0 (the floor of the Good tier). The 5 dimensions after it are all execution, and no amount of polished execution can rescue a design with no idea: that just polishes the template shinier.

### 1. Philosophy Alignment

| Score | Criteria |
|------|------|
| 9-10 | The design perfectly embodies the core spirit of the chosen philosophy; every detail has a philosophical basis |
| 7-8 | The overall direction is right and the core traits are in place; a few details deviate |
| 5-6 | The intent is visible, but execution mixes in elements of other styles; not pure enough |
| 3-4 | Only surface imitation; doesn't understand the philosophy's core |
| 1-2 | Basically unrelated to the chosen philosophy |

**Review points**:
- Does it use that designer's/studio's signature techniques?
- Do color, type, and layout fit that philosophical system?
- Are there "self-contradictory" elements? (e.g. choosing Kenya Hara but cramming it with content)

### 2. Visual Hierarchy

| Score | Criteria |
|------|------|
| 9-10 | The user's eye flows naturally along the designer's intent; zero friction in getting the information |
| 7-8 | Clear primary/secondary relationships; occasionally 1-2 spots where the hierarchy blurs |
| 5-6 | Headings and body can be told apart, but the middle levels are muddled |
| 3-4 | Information laid out flat, with no clear visual entry point |
| 1-2 | Chaotic; the user doesn't know where to look first |

**Review points**:
- Is the size contrast between headings and body sufficient? (at least 2.5×)
- Do color/weight/size establish 3-4 clear levels?
- Is the white space guiding the eye?
- "Squint test": squint at it; is the hierarchy still clear?

### 3. Craft Quality

| Score | Criteria |
|------|------|
| 9-10 | Pixel-precise; no flaws in alignment, spacing, or color at all |
| 7-8 | Refined overall, with 1-2 tiny alignment/spacing issues |
| 5-6 | Basically aligned, but spacing is inconsistent and color use isn't systematic enough |
| 3-4 | Obvious alignment errors, chaotic spacing, too many colors |
| 1-2 | Rough; looks like a draft |

**Review points**:
- Does it use a consistent spacing system (e.g. an 8pt grid)?
- Is spacing between similar elements consistent?
- Is the number of colors under control? (usually no more than 3-4)
- Are the font families unified? (usually no more than 2)
- Is edge alignment precise?

### 4. Functionality

| Score | Criteria |
|------|------|
| 9-10 | Every design element serves the goal; zero redundancy |
| 7-8 | Clearly function-driven, with a little decoration that could be cut |
| 5-6 | Basically usable, but has obviously decorative elements that distract |
| 3-4 | Form over function; the user has to work to find information |
| 1-2 | Completely drowned in decoration; has lost the ability to communicate information |

**Review points**:
- Would deleting any one element make the design worse? (if not, it should be deleted)
- Is the CTA/key information in the most prominent position?
- Are there elements "added because they look nice"?
- Does the information density match the medium? (PPT shouldn't be too dense; PDF can be denser)

### 5. Originality

| Score | Criteria |
|------|------|
| 9-10 | Refreshing; finds a unique expression within the philosophy's framework |
| 7-8 | Has its own ideas; not a simple template application |
| 5-6 | Middle of the road; looks like a template |
| 3-4 | Heavy use of clichés (e.g. gradient orbs to represent AI) |
| 1-2 | Entirely a template or a patchwork of stock assets |

**Review points**:
- Does it avoid common clichés? (see "Common problem list" below)
- Is there personal expression while following the design philosophy?
- Are there "unexpected but very reasonable" design decisions?

---

## Review emphasis by scenario

Different output types have different review priorities (the Concept dimension isn't in the table: it's the first gate for every scenario and isn't part of the trade-offs):

| Scenario | Most important dimensions | Second | Can be relaxed |
|------|-----------|--------|--------|
| WeChat Official Account cover/illustrations | Originality, Visual Hierarchy | Philosophy Alignment | Functionality (a single image involves no interaction) |
| Infographic | Functionality, Visual Hierarchy | Craft Quality | Originality (accuracy first) |
| PPT/Keynote | Visual Hierarchy, Functionality | Craft Quality | Originality (clarity first) |
| PDF/white paper | Craft Quality, Functionality | Visual Hierarchy | Originality (professionalism first) |
| Landing page/official site | Functionality, Visual Hierarchy | Originality | — (full requirements) |
| App UI | Functionality, Craft Quality | Visual Hierarchy | Philosophy Alignment (usability first) |
| Xiaohongshu illustrations | Originality, Visual Hierarchy | Philosophy Alignment | Craft Quality (atmosphere first) |

---

## Top 10 common design problems

### 1. AI tech clichés
**Problem**: gradient orbs, digital rain, blue circuit boards, robot faces
**Why it's a problem**: users are visually fatigued by these and can't tell you apart from everyone else
**Fix**: replace literal symbols with abstract metaphors (e.g. a metaphor of "conversation" rather than a chat bubble icon)

### 2. Insufficient type size hierarchy
**Problem**: the gap between headings and body is too small (<2.5×)
**Why it's a problem**: users can't quickly locate the key information
**Fix**: headings at least 3× the body (e.g. body 16px → headings 48-64px)

### 3. Too many colors
**Problem**: 5+ colors with no primary/secondary order
**Why it's a problem**: visual chaos, weak brand feel
**Fix**: limit to 1 primary + 1 secondary + 1 accent + grayscale

### 4. Inconsistent spacing
**Problem**: arbitrary spacing between elements, no system
**Why it's a problem**: looks unprofessional; the visual rhythm is chaotic
**Fix**: set up an 8pt grid system (spacing only in 8/16/24/32/48/64px)

### 5. Not enough white space
**Problem**: every bit of space is filled with content
**Why it's a problem**: crowded information causes reading fatigue and actually lowers communication efficiency
**Fix**: white space at least 40% of the total area (60%+ for minimalist styles)

### 6. Too many fonts
**Problem**: 3+ fonts
**Why it's a problem**: visual noise, weakens cohesion
**Fix**: at most 2 fonts (1 for headings + 1 for body); create variation with weight and size

### 7. Inconsistent alignment
**Problem**: some left-aligned, some centered, some right-aligned
**Why it's a problem**: breaks the sense of visual order
**Fix**: pick one alignment (left-aligned recommended) and apply it globally

### 8. Decoration over content
**Problem**: background patterns/gradients/shadows steal the spotlight from the main content
**Why it's a problem**: puts the cart before the horse; users come for information, not decoration
**Fix**: "If I delete this decoration, does the design get worse?" If not, delete it

### 9. Overused cyber neon
**Problem**: dark blue background (#0D1117) + neon glow effects
**Why it's a problem**: a default aesthetic no-go zone (this skill's taste baseline), and it has become one of the biggest clichés. Users can override it with their own brand
**Fix**: choose a more distinctive color scheme (see the color systems of the 20 styles)

### 10. Information density doesn't match the medium
**Problem**: a whole page of text in a PPT / 10 elements crammed into a cover image
**Why it's a problem**: different media have different optimal information densities
**Fix**:
- PPT: 1 core point per slide
- Cover image: 1 visual focal point
- Infographic: layered presentation
- PDF: can be denser, but needs clear navigation

---

## Review output template

```
## Design Review Report

**Overall score**: X.X/10 [Excellent (8+)/Good (6-7.9)/Needs improvement (4-5.9)/Failing (<4)]
(When Concept ≤5, the overall score is capped at 6; fix the concept before discussing execution)

**Scores by dimension**:
- Concept / core idea: X/10 [What is this design's idea? State it in one sentence]
- Philosophy Alignment: X/10 [one-sentence explanation]
- Visual Hierarchy: X/10 [one-sentence explanation]
- Craft Quality: X/10 [one-sentence explanation]
- Functionality: X/10 [one-sentence explanation]
- Originality: X/10 [one-sentence explanation]

### Strengths (Keep)
- [Point out specifically what was done well, described in design language]

### Issues (Fix)
[Sorted by severity]

**1. [Issue name]**: ⚠️Critical / ⚡Important / 💡Polish
- Current: [describe the current state]
- Problem: [why this is a problem]
- Fix: [concrete action, with values]

### Quick fix checklist (Quick Wins)
If you only have 5 minutes, do these 3 things first:
- [ ] [The most impactful fix]
- [ ] [The second most important fix]
- [ ] [The third most important fix]
```

---

**Version**: v1.0
**Updated**: 2026-02-13
