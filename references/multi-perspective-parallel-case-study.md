# Multi-perspective parallel experiment · Case Study

> md-html v2.0 launch film project · 2026-05-11
> Parallel director's notes + HTML + keyframe experiments from 6 artists' perspectives

---

## Background

When the user asked to "make a 30-second upgrade promo film for md-html v2.0", the main thread first produced a v5 baseline (Anthropic / Penguin Classics publisher taste). But the user felt it could be better and gave a critical instruction:

> "Call different subagents to each generate 6 completely different versions in expression and visual design. You can try bringing in different directors and artists. Then once they're all done, judge and review them."

This was the first systematic "multi-perspective parallel director's notes" experiment, and it validated a reusable workflow.

---

## How the 6 perspectives were chosen

Don't pick 6 designers at random: they must have **extremely high visual difference** to avoid converging.

The 6 perspectives finally chosen (with reasons):

| Perspective | School | Aesthetic anchor | Difference from the other perspectives |
|------|------|---------|----------------|
| **v5 baseline** | Modern publisher | Anthropic terracotta orange + Penguin Classics serif + Vignelli grid | The safe "taste" choice |
| **v5a Wes Anderson** | Cinematic chapter aesthetic | The French Dispatch magazine feel + 1960 Olivetti industrial catalogue | Symmetric composition + chapter cards + decorative borders |
| **v5b Saul Bass** | 60s film title art | cut-paper + Trajan caps + flowing geometry | Cut-paper silhouettes + big type + strong diagonals |
| **v5c Wong Kar-wai** | Hong Kong New Wave | *In the Mood for Love*, *2046* letterboxing + Chinese serif | Slow beats + hazy halation + Chinese-led |
| **v5d Massimo Vignelli** | 1970 modernism | Knoll identity manual + NYC Subway map | Strict grid + the 3-color iron rule + rejection of decoration |
| **v5e Kenya Hara** | Japanese minimalism | MUJI posters + *White* | Philosophy of whitespace + no chrome + ma (the space between) |
| **v5f Yayoi Kusama** | Installation art | Infinity Mirror Rooms + Polka Dot Obsession | Obsessive repetition + a single strong color + polka dots |

**Selection principles**:
1. **3 different geographic cultures** (Western film / Japanese design / Hong Kong Chinese)
2. **3 different eras** (1960s / 1970s / 2010s+)
3. **3 different media** (film / graphic design / installation art)
4. **Each has a visual signature that is "the complete opposite of the generic SaaS aesthetic in the training corpus"**

---

## Implementation workflow

### Step 1 · Write an independent brief for each perspective (about 15 minutes)

Each brief contains 8 fixed fields:

```
1. Project background (the same for all)
2. Required reading (the same v5-director-notes.md as the methodology template)
3. What you need to do (a 4-item delivery list)
4. The artist's DNA (6 core fields):
   - Palette (specific HEX)
   - Fonts (specific names + alternatives)
   - Visual language (a few core points)
   - Signature elements (identifiable signatures)
   - Rhythm (distinct from the other perspectives)
   - Reinforced anti-AI-slop (the no-go zones within this style's context)
5. 30-second structure reference (a draft of 4-6 shots)
6. Destination cards design requirements (keep them genuinely readable)
7. Key constraints (30s / 1920×1080 / file:// / Google Fonts CDN)
8. Output verification checklist + completion report format
```

**Key point**: every brief must stress "**don't repeat v5's aesthetic**"; otherwise the subagents get influenced by the v5 director-notes and converge.

### Step 2 · Launch 6 subagents in parallel (6 Agent tool calls in the same message)

```js
Agent({ subagent_type: "general-purpose", run_in_background: true, name: "v5a-anderson", ... })
Agent({ subagent_type: "general-purpose", run_in_background: true, name: "v5b-bass", ... })
// ... 6 of them
```

They run in the background; expect 30-60 minutes.

### Step 3 · Idle work while waiting

Don't poll agent status. Subagents send a task-notification automatically when they finish. While waiting:

- Fix bugs in the main thread's v5 baseline
- Write the review framework (the scoring dimensions / Q&A each version gets)
- Distill the methodology into the skill (which is exactly where this case study came from)
- Prepare the skeleton of the final summary document

### Step 4 · Failure handling (about a 16% failure rate, acceptable)

Observed in practice: about 1 in 6 subagents fails due to network issues or token limits (Bass hit a socket error in the first round). Handling:

1. When a completion notification arrives, **check that agent's output folder immediately**
2. Key deliverables missing → restart that agent (same brief; you can mark it "failed last time, please run again")
3. Partially complete (e.g. html but no screenshots) → the main thread adds Playwright screenshots; don't restart the agent

### Step 5 · Systematic review once all 6 versions are done

Review framework (5 dimensions + 3 top-level questions + use case allocation):

```
5-dimension scoring (1-10 per dimension):
- Distinctiveness: visual differentiation
- Coherence: aesthetic consistency
- Anti-slop: anti-AI-slop execution
- Story arc: pacing and story arc
- Pause-and-look: detail density

3 top-level questions:
- Q1 Screenshot-shareable? (can make people stop scrolling on social platforms)
- Q2 One line remembered? (leaves a thesis-level memory)
- Q3 Timeless? (won't look cheap when viewed again in 5 years)

Use case allocation (by platform and audience):
- WeChat Official Account / X / Bilibili / WeChat Moments / Dribbble / client demos / private community / ...
```

See REVIEW.md in the same directory as `assets/director-notes-samples/launch-film-30s-sample.md`.

---

## Experiment output (facts)

### Document volume

- v5 baseline director-notes: 11,500 characters
- 6 perspective director-notes: 4,000-12,000 characters each
- Total document volume: about 55,000-70,000 characters
- Full 5-part structure: 6/6 versions

### HTML implementation

- Each version is an independent animation.html, 30 seconds, 1920×1080
- File sizes 28-74KB
- All open via file:// (no server dependency)

### Keyframes

- 10-18 PNGs per version, covering the full 30-second story arc
- Total screenshots: 80+
- Average PNG size: 100-200KB

### Duration

- 6 subagents running in parallel: about 12-15 minutes (as shown by duration_ms)
- Main thread's parallel idle work (fixing v5 + writing the methodology): finished in the same period
- Overall "from launching the 6 perspectives to every deliverable in place": about 60 minutes

---

## Key insights (for future users of this skill)

### Insight 1 · The "write ten thousand characters of director's notes first" methodology is **fully reproducible**

All 6 subagents produced complete 4,000-12,000 character specs following the 5-part structure, and all reached marketing-ready quality when implementing the HTML. This shows the methodology itself doesn't depend on one executor's talent: **as long as the brief is clear, multiple independent executors can produce consistently high-quality results**.

### Insight 2 · A "perspective" must be as specific as "work + year"

Each brief lists specific works to converse with:
- Anderson → *The French Dispatch* (2021) + *Moonrise Kingdom* (2012) + Penguin Classics dust jackets + 1960s Olivetti catalogues
- WKW → *In the Mood for Love* (2000) + *2046* (2004)
- Vignelli → 1972 NYC Subway map + Knoll identity manual + *The Vignelli Canon*
- Hara → MUJI brand 1995-2023 + *White* + Junya Ishigami transparency
- Kusama → Infinity Mirrored Rooms (2013-2023) + Polka Dot Obsession installations

**Result in practice**: every subagent accurately captured the core visual DNA of those works, rather than the "average" of the school.

### Insight 3 · A "style-reinforced version" of anti-AI-slop is key

Generic anti-slop (purple gradients / emoji / SVG people) applies to every version. But **each style also needs its own "dedicated anti-slop"**:

- Bass: no Helvetica (too clean; Bass is rugged)
- Vignelli: no rounded corners (every corner 90°)
- Hara: no gradients of any kind + no sans display
- Kusama: no modern SaaS look
- Anderson: no cyber palettes
- WKW: no Inter (WKW uses serifs)

With these added, the 6 versions had extremely high stylistic purity, and none converged with another.

### Insight 4 · The real value of multiple perspectives isn't "picking a winner"

The original idea was an A/B test to pick the best version. During the actual review we found: **each of the 6 versions has a clear use case**:
- v5 baseline → product page / WeChat Read (high information density)
- Anderson → header image for long Official Account articles (strong magazine page-turning feel)
- WKW → Bilibili / Chinese-culture-oriented audiences (nostalgic warmth)
- Vignelli → design community / Dribbble (every frame is a print poster)
- Hara → client demos / static screenshots (minimalist philosophy)
- Kusama → short X videos / viral spread (visual impact)

**Conclusion**: marketing isn't single-shot, it's a platform-specific multiplex. The real value of running 6 perspectives in parallel is **giving one project 6 differentiated weapons**, not leaving 5 versions unfit to show.

### Insight 5 · A subagent failure rate of ~16% is acceptable

1 of 6 failed (Bass hit a socket error in the first round). The cost of handling it: a restart + a simplified brief in 5 minutes, then another 12-15 minute wait. **Compared with having 1 agent run 6 versions sequentially (90+ minutes)**, parallel + retry is clearly more economical.

### Insight 6 · The main thread must do substantive idle work while waiting

Subagents take 12-15 minutes to finish. The main thread should never sit idle during that time:

- **Fix bugs in the main version** (ones the user already reported)
- **Write the review framework** (to fill in during review)
- **Distill the methodology into the skill** (like this case study)
- **Prepare the final summary** (so the user sees everything at a glance when they come back)

This is the "main thread's responsibility" in a parallel multi-agent workflow: not a PM waiting for results, but an orchestrator pushing forward in sync.

---

## When to use "multi-perspective parallel"

| Scenario | Use it? | Reason |
|------|---------|------|
| The user explicitly says "I want to see different directions" or "make a few more versions" | ✅ Use it right away | Direct request |
| The user isn't happy with the first version but can't say what they want | ✅ Use it | An A/B pick beats "guessing what you want" |
| The project is going out on multiple platforms (X / Official Account / Bilibili / WeChat Moments) | ✅ Use it | One version per platform |
| The client hasn't settled on a style but has budget (time + tokens) | ✅ Use it | Repeated revisions = 5x the cost |
| The user already gave a clear style reference and wants only 1 version | ❌ Don't use it | Wasteful |
| The task is a simple motion graphic / icon animation | ❌ Don't use it | Over-engineering |
| Tight on time, < 30 minutes | ❌ Don't use it | The subagents won't finish |

---

## Complete methodology flowchart

```
User brief (including quality expectations)
       ↓
[Main thread] write the v5 baseline director's notes (ten-thousand-character level, 5 parts)
       ↓
[Main thread] implement the v5 HTML + capture keyframes (marketing baseline)
       ↓
[Decision point] use multiple perspectives?
       ↓ YES
[Main thread] pick 6 differentiated perspectives + write 6 independent briefs (8 fields each)
       ↓
[6 subagents in parallel]
   ├── v5a brief → director-notes + html + keyframes + README
   ├── v5b brief → ...
   ├── v5c brief → ...
   ├── v5d brief → ...
   ├── v5e brief → ...
   └── v5f brief → ...
       ↓
[Main thread in sync] fix v5 bugs · write the review framework · distill the methodology
       ↓
[All 6 notifications arrive]
       ↓
[Main thread] failure detection + retry / add screenshots
       ↓
[Main thread] 5-dimension scoring + 3 top-level questions + use case allocation
       ↓
[Main thread] write the final REVIEW.md
       ↓
[Delivery] 6 complete versions + review + platform distribution recommendations
```

---

## Related documents

- Full methodology: `references/launch-film-director-notes.md`
- Single-perspective sample: `assets/director-notes-samples/launch-film-30s-sample.md` (v5 baseline)
- Real project location: the author's local demos directory (with the full set of files for all 6 + 1 perspectives; not shipped with the repo)
- Review: the author's local REVIEW.md (not shipped with the repo)

---

*Last updated: 2026-05-11*
*Real case study: md-html v2.0 launch film 6-perspective parallel experiment*
