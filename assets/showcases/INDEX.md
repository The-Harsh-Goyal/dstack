# Design Philosophy Showcases: Sample Asset Index

> 8 scenarios × 3 styles = 24 prebuilt design samples
> Used in Phase 3 when recommending design directions, to show directly "what this style looks like when it's built"

## Style Notes

| Code name | School | Style name | Visual character |
|------|------|---------|---------|
| **Pentagram** | Information architecture school | Pentagram / Michael Bierut | Restrained black and white, Swiss grid, strong type hierarchy, #E63946 red accent |
| **Build** | Minimalist school | Build Studio | Luxury-grade whitespace (70%+), subtle font weights (200-600), #D4A574 warm gold, refined |
| **Takram** | Eastern philosophy school | Takram | Soft tech feel, natural colors (beige/gray/green), rounded corners, charts as art |

## Scenario Quick Reference

### Content Design Scenarios

| # | Scenario | Spec | Pentagram | Build | Takram |
|---|------|------|-----------|-------|--------|
| 1 | WeChat Official Account cover | 1200×510 | `cover/cover-pentagram` | `cover/cover-build` | `cover/cover-takram` |
| 2 | PPT data slide | 1920×1080 | `ppt/ppt-pentagram` | `ppt/ppt-build` | `ppt/ppt-takram` |
| 3 | Vertical infographic | 1080×1920 | `infographic/infographic-pentagram` | `infographic/infographic-build` | `infographic/infographic-takram` |

### Website Design Scenarios

| # | Scenario | Spec | Pentagram | Build | Takram |
|---|------|------|-----------|-------|--------|
| 4 | Personal homepage | 1440×900 | `website-homepage/homepage-pentagram` | `website-homepage/homepage-build` | `website-homepage/homepage-takram` |
| 5 | AI tools directory site | 1440×900 | `website-ai-nav/ainav-pentagram` | `website-ai-nav/ainav-build` | `website-ai-nav/ainav-takram` |
| 6 | AI writing tool | 1440×900 | `website-ai-writing/aiwriting-pentagram` | `website-ai-writing/aiwriting-build` | `website-ai-writing/aiwriting-takram` |
| 7 | SaaS landing page | 1440×900 | `website-saas/saas-pentagram` | `website-saas/saas-build` | `website-saas/saas-takram` |
| 8 | Developer docs | 1440×900 | `website-devdocs/devdocs-pentagram` | `website-devdocs/devdocs-build` | `website-devdocs/devdocs-takram` |

> Each entry has two files: `.html` (source) and `.png` (screenshot)

## Usage

### Referencing in Phase 3 recommendations
After recommending a design direction, you can show the prebuilt screenshot for the matching scenario:
```
"This is what a WeChat Official Account cover looks like in the Pentagram style → [show cover/cover-pentagram.png]"
"This is how a PPT data slide feels in the Takram style → [show ppt/ppt-takram.png]"
```

### Scenario matching priority
1. The user's scenario has an exact match → show that scenario directly
2. No exact match but a similar type → show the closest scenario (e.g. "product website" → show the SaaS landing page)
3. No match at all → skip the prebuilt samples and go straight to Phase 3.5 for live generation

### Side-by-side comparison
The 3 styles for the same scenario work well side by side, helping the user compare them at a glance:
- "This is the same WeChat Official Account cover, built in each of the 3 styles"
- Display order: Pentagram (rational, restrained) → Build (luxurious minimalism) → Takram (soft, warm)

## Content Details

### WeChat Official Account cover (cover/)
- Content: Claude Code Agent workflow: an architecture of 8 parallel Agents
- Pentagram: a huge red "8" + Swiss grid lines + data bars
- Build: an ultra-thin-weight "Agent" floating in 70% whitespace + fine warm-gold lines
- Takram: an 8-node radial flowchart as an art piece + beige background

### PPT data slide (ppt/)
- Content: GLM-4.7 open-source model's breakthrough in coding ability (AIME 95.7 / SWE-bench 73.8% / τ²-Bench 87.4)
- Pentagram: a 260px "95.7" anchor + red/gray/light-gray comparison bar chart
- Build: three groups of 120px ultra-thin floating numbers + warm-gold gradient comparison bars
- Takram: SVG radar chart + three-color overlay + rounded data cards

### Vertical infographic (infographic/)
- Content: AI memory system, CLAUDE.md optimized from 93KB to 22KB
- Pentagram: huge "93→22" numbers + numbered blocks + CSS data bars
- Build: extreme whitespace + soft-shadow cards + warm-gold connecting lines
- Takram: SVG donut chart + organic curved flowchart + frosted-glass cards

### Personal homepage (website-homepage/)
- Content: portfolio homepage of indie developer Alex Chen
- Pentagram: 112px large name + Swiss grid columns + editorial numbers
- Build: glassmorphism navigation + floating stat cards + ultra-thin font weight
- Takram: paper texture + small round avatar + hairline dividers + asymmetric layout

### AI tools directory site (website-ai-nav/)
- Content: AI Compass: a directory of 500+ AI tools
- Pentagram: square-cornered search box + numbered tool list + uppercase category tags
- Build: rounded search box + refined white tool cards + pill tags
- Takram: organic staggered card layout + soft category tags + chart-style connections

### AI writing tool (website-ai-writing/)
- Content: Inkwell: AI writing assistant
- Pentagram: 86px large headline + wireframe editor mockup + grid feature columns
- Build: floating editor card + warm-gold CTA + luxurious writing experience
- Takram: poetic serif headline + organic editor + flowchart

### SaaS landing page (website-saas/)
- Content: Meridian: business intelligence analytics platform
- Pentagram: black-and-white columns + structured dashboard + 140px "3x" anchor
- Build: floating dashboard cards + SVG area chart + warm-gold gradient
- Takram: rounded bar chart + flow nodes + soft earth tones

### Developer docs (website-devdocs/)
- Content: Nexus API: unified AI model gateway
- Pentagram: left sidebar navigation + square-cornered code blocks + red string highlighting
- Build: centered floating code cards + soft shadows + warm-gold icons
- Takram: beige code blocks + flowchart connections + dashed-border feature cards

## File Stats

- HTML source files: 24
- PNG screenshots: 24
- Total assets: 48 files

---

**Version**: v1.0
**Created**: 2026-02-13
**For**: design-philosophy skill, Phase 3 recommendation step
