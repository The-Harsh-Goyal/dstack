# Module · Web / Landing Pages / Official Sites / UI Prototypes

Clickable sites, landing pages, official sites, dashboards and desktop UI prototypes go through here (mobile Apps go through `references/app-prototype.md`). First pass through the core rules in SKILL.md, then follow this manual.

## First screen: lead with the most distinctive thing in the subject's world

The first screen is what the viewer sees first. Open with the most distinctive thing in this subject's world, in whichever form fits best: a headline, an image, an animation, a playable demo, an interactive moment.

"Big number + small label + a row of supporting data + gradient accent" is the default answer for a first screen; use it only when it really fits best. The same goes for the landing page template of "big hero + three feature columns + testimonials + CTA".

## Order of work

1. Three directions: 1 complete HTML per direction + first-screen screenshot + full-page long screenshot (`references/directions.md`)
2. After one is chosen, first write assumptions + placeholder structure for the user to look at, then fill in the components (the standard flow in `references/workflow.md`)
3. Once structure and rhythm are settled, add Tweaks (`references/tweaks-system.md`) so the user can adjust colors, type sizes and copy themselves

## Hard rules

- Body text ≥14px (16px on mobile), clickable elements ≥44×44px, body text contrast ≥4.5:1
- Responsive: verify at least two widths, 1440 and 375 (`python3 "$HD/scripts/verify.py" page.html --viewports 1440x900,375x812`)
- Interactions must really be clickable: build out the navigation, tabs, expand/collapse and form states, with zero console errors
- Don't invent data, reviews or logo walls; if you don't have them, leave an honest placeholder or ask the user for them
- Motion: one choreographed page load beats a fade-up on every section; motion that responds to user actions (expanding, confirming) is good motion

## Starter components

| File | Use |
|---|---|
| `assets/browser_window.jsx` | Show a web page inside a browser window (URL bar + tab bar) |
| `assets/macos_window.jsx` | Desktop App window shell |
| `assets/design_canvas.jsx` | Side-by-side comparison of several static variants |

How to write React + Babel and the three technical red lines (style objects must have unique names, share between multiple babel scripts with `Object.assign(window, …)`, don't use `scrollIntoView`): `references/react-setup.md`.

## Related files

| What you're doing | Read |
|---|---|
| Style library and specimens (the web section of the seconds roulette, plus the cross-media Chinese & East Asian section) | `references/design-styles.md` |
| Font pairing and Chinese typesetting | `references/typography.md` |
| The user has a codebase / design system | `references/design-context.md` |
| Verification before delivery | `references/verification.md` |
