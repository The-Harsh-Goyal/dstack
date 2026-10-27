# Design Context: Start from Existing Context

**This is the most important one thing in this skill.**

Good hi-fi design always grows out of existing design context. **Building hi-fi from nothing is a last resort, and it will always produce generic work**. So at the start of every design task, first ask: is there anything to reference?

## What counts as design context

From highest to lowest priority:

### 1. The user's design system/UI kit
The component library, color tokens, type specs, and icon system the user's own product already has. **The ideal case**.

### 2. The user's codebase
If the user gives you a codebase, it contains living component implementations. Read those component files:
- `theme.ts` / `colors.ts` / `tokens.css` / `_variables.scss`
- Specific components (Button.tsx, Card.tsx)
- Layout scaffold (App.tsx, MainLayout.tsx)
- Global stylesheets

**Read the code and copy exact values**: hex codes, spacing scale, font stack, border radius. Don't redraw from memory.

### 3. The user's shipped product
If the user has a live product but didn't give you the code, use Playwright or ask the user for screenshots.

```bash
# Screenshot a public URL with Playwright
npx playwright screenshot https://example.com screenshot.png --viewport-size=1920,1080
```

This lets you see the real visual vocabulary.

### 4. Brand guidelines/logo/existing assets
The user may have: logo files, brand color specs, marketing materials, slide templates. All of these are context.

### 5. Competitor references
The user says "like the XX website": ask them for the URL or screenshots. **Don't** work from vague impressions in your training data.

### 6. A well-known design system (fallback)
If none of the above exist, use a recognized design system as the base:
- Apple HIG
- Material Design 3
- Radix Colors (color)
- shadcn/ui (components)
- Tailwind's default palette

Tell the user clearly what you're using, so they know it's a starting point, not the final version.

## Process for gathering context

### Step 1: Ask the user

The must-ask checklist at the start of a task (from `workflow.md`):

```markdown
1. Do you have an existing design system/UI kit/component library? Where is it?
2. Do you have brand guidelines, or color/type specs?
3. Can you give me screenshots or the URL of your existing product?
4. Is there a codebase I can read?
```

### Step 2: When the user says "no", help them find something

Don't just give up. Try:

```markdown
Let me see if there are any leads:
- Did your previous projects have related designs?
- What colors/type does the company's marketing website use?
- What style is your product's logo? Can you send me a copy?
- Are there products you admire that could serve as references?
```

### Step 3: Read all the context you can find

If the user gives you a codebase path, read:
1. **First list the file structure**: find the files related to style/theme/components
2. **Read the theme/token files**: lift the specific hex/px values
3. **Read 2-3 representative components**: look at the visual vocabulary (hover states, shadows, borders, padding node patterns)
4. **Read the global stylesheet**: base resets, font loading
5. **If there's a Figma link/screenshots**: look at the images, but **trust the code more**

**Important**: **don't** glance once and work from impressions. You've only really lifted it when you've read out 30+ specific values.

### Step 4: Vocalize the system you'll use

After reviewing the context, tell the user the system you'll use:

```markdown
Based on your codebase and product screenshots, here's the design system I've distilled:

**Color**
- Primary: #C27558 (from tokens.css)
- Background: #FDF9F0
- Text: #1A1A1A
- Muted: #6B6B6B

**Type**
- Display: Instrument Serif (from the @font-face in global.css)
- Body: Geist Sans
- Mono: JetBrains Mono

**Spacing** (from your scale system)
- 4, 8, 12, 16, 24, 32, 48, 64

**Shadow pattern**
- `0 1px 2px rgba(0,0,0,0.04)` (subtle card)
- `0 10px 40px rgba(0,0,0,0.1)` (elevated modal)

**Border-radius**
- Small components 4px, cards 12px, buttons 8px

**Component vocabulary**
- Button: filled primary, outlined secondary, ghost tertiary, all with 8px radius
- Card: white background, subtle shadow, no border

I'll start building with this system. Does it look right?
```

Start only after the user confirms.

## Designing from nothing (fallback when there's no context)

**Strong warning**: output quality drops significantly in this situation. Tell the user clearly.

```markdown
You don't have any design context, so I can only work from general intuition.
The output will be something that "looks OK but lacks distinctiveness".
Do you want to continue, or add some reference material first?
```

If the user insists you go ahead, make decisions in this order:

### 1. Pick an aesthetic direction
Don't give a generic result. Pick a clear direction:
- brutally minimal
- editorial/magazine
- brutalist/raw
- organic/natural
- luxury/refined
- playful/toy
- retro-futuristic
- soft/pastel

Tell the user which one you chose.

### 2. Pick a known design system as the skeleton
- Use Radix Colors for the palette (https://www.radix-ui.com/colors)
- Use shadcn/ui for the component vocabulary (https://ui.shadcn.com)
- Use the Tailwind spacing scale (multiples of 4)

### 3. Pick a distinctive font pairing

Don't use Inter/Roboto. Suggested pairings (free from Google Fonts):
- Instrument Serif + Geist Sans
- Cormorant Garamond + Inter Tight
- Bricolage Grotesque + Söhne (paid)
- Fraunces + Work Sans (note that AI has already worn out Fraunces)
- JetBrains Mono + Geist Sans (technical feel)

### 4. Every key decision has reasoning

Don't choose silently. Write it in an HTML comment:

```html
<!--
Design decisions:
- Primary color: warm terracotta (oklch 0.65 0.18 25) — fits the "editorial" direction  
- Display: Instrument Serif for humanist, literary feel
- Body: Geist Sans for cleanness contrast
- No gradients — committed to minimal, no AI slop
- Spacing: 8px base, golden ratio friendly (8/13/21/34)
-->
```

## Import strategy (when the user gives you a codebase)

If the user says "import this codebase as a reference":

### Small (<50 files)
Read all of it and internalize the context.

### Medium (50-500 files)
Focus on:
- `src/components/` or `components/`
- All files related to styles/tokens/theme
- 2-3 representative full-page components (Home.tsx, Dashboard.tsx)

### Large (>500 files)
Have the user specify the focus:
- "I'm building the settings page" → read the existing settings-related files
- "I'm building a new feature" → read the overall shell + the closest reference
- Aim for precision, not completeness

## Working with Figma/design files

If the user gives you a Figma link:

- **Don't** expect to "convert Figma to HTML" directly: that needs extra tools
- Figma links usually aren't publicly accessible
- Ask the user to: export **screenshots** and send them to you + tell you the specific color/spacing values

If they only give you Figma screenshots, tell the user:
- I can see the visuals, but I can't get exact values
- Please tell me the key numbers (hex, px), or export as code (Figma supports this)

## Final reminder

**The ceiling on a project's design quality is set by the quality of the context you get**.

Spending 10 minutes gathering context is worth more than spending 1 hour drawing hi-fi from nothing.

**When there's no context, prefer asking the user for it over forcing your way through**.
