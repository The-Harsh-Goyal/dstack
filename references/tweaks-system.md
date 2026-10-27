# Tweaks: live parameter tuning for design variations

Tweaks is a core capability of this skill: it lets the user switch variations / adjust parameters live without touching code.

**Cross-agent-environment compatibility**: some native design-agent environments (such as Claude.ai Artifacts) rely on the host's postMessage to write tweak values back into the source for persistence. This skill uses a **pure front-end localStorage approach**. The effect is the same (state survives a refresh), but persistence happens in the browser's localStorage rather than the source file. This approach works in any agent environment (Claude Code / Codex / Cursor / Trae / etc.).

## When to add Tweaks

- The user explicitly asks for "adjustable parameters" / "switching between multiple versions"
- When the design has multiple variations that need comparing
- The user didn't say so, but you judge that **adding a few illuminating tweaks would help the user see the possibilities**

Default recommendation: **add 2-3 tweaks to every design** (color theme / font size / layout variant) even if the user didn't ask. Showing the user the space of possibilities is part of the design service.

## Implementation (pure front-end version)

### Basic structure

```jsx
const TWEAK_DEFAULTS = {
  "primaryColor": "#2F6F5E",
  "fontSize": 16,
  "density": "comfortable",
  "dark": false
};

function useTweaks() {
  const [tweaks, setTweaks] = React.useState(() => {
    try {
      const stored = localStorage.getItem('design-tweaks');
      return stored ? { ...TWEAK_DEFAULTS, ...JSON.parse(stored) } : TWEAK_DEFAULTS;
    } catch {
      return TWEAK_DEFAULTS;
    }
  });

  const update = (patch) => {
    const next = { ...tweaks, ...patch };
    setTweaks(next);
    try {
      localStorage.setItem('design-tweaks', JSON.stringify(next));
    } catch {}
  };

  const reset = () => {
    setTweaks(TWEAK_DEFAULTS);
    try {
      localStorage.removeItem('design-tweaks');
    } catch {}
  };

  return { tweaks, update, reset };
}
```

### Tweaks panel UI

A floating panel in the bottom-right corner. Collapsible:

```jsx
function TweaksPanel() {
  const { tweaks, update, reset } = useTweaks();
  const [open, setOpen] = React.useState(false);

  return (
    <div style={{
      position: 'fixed',
      bottom: 20,
      right: 20,
      zIndex: 9999,
    }}>
      {open ? (
        <div style={{
          background: 'white',
          border: '1px solid #e5e5e5',
          borderRadius: 12,
          padding: 20,
          boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
          width: 280,
          fontFamily: 'system-ui',
          fontSize: 13,
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: 16,
          }}>
            <strong>Tweaks</strong>
            <button onClick={() => setOpen(false)} style={{
              border: 'none', background: 'none', cursor: 'pointer', fontSize: 16,
            }}>×</button>
          </div>

          {/* Color */}
          <label style={{ display: 'block', marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: '#666' }}>Primary color</div>
            <input 
              type="color" 
              value={tweaks.primaryColor} 
              onChange={e => update({ primaryColor: e.target.value })}
              style={{ width: '100%', height: 32 }}
            />
          </label>

          {/* Font size slider */}
          <label style={{ display: 'block', marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: '#666' }}>Font size ({tweaks.fontSize}px)</div>
            <input 
              type="range" 
              min={12} max={24} step={1}
              value={tweaks.fontSize}
              onChange={e => update({ fontSize: +e.target.value })}
              style={{ width: '100%' }}
            />
          </label>

          {/* Density options */}
          <label style={{ display: 'block', marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: '#666' }}>Density</div>
            <select 
              value={tweaks.density}
              onChange={e => update({ density: e.target.value })}
              style={{ width: '100%', padding: 6 }}
            >
              <option value="compact">Compact</option>
              <option value="comfortable">Comfortable</option>
              <option value="spacious">Spacious</option>
            </select>
          </label>

          {/* Dark mode toggle */}
          <label style={{ 
            display: 'flex', 
            alignItems: 'center',
            gap: 8,
            marginBottom: 16,
          }}>
            <input 
              type="checkbox" 
              checked={tweaks.dark}
              onChange={e => update({ dark: e.target.checked })}
            />
            <span>Dark mode</span>
          </label>

          <button onClick={reset} style={{
            width: '100%',
            padding: '8px 12px',
            background: '#f5f5f5',
            border: 'none',
            borderRadius: 6,
            cursor: 'pointer',
            fontSize: 12,
          }}>Reset</button>
        </div>
      ) : (
        <button 
          onClick={() => setOpen(true)}
          style={{
            background: '#1A1A1A',
            color: 'white',
            border: 'none',
            borderRadius: 999,
            padding: '10px 16px',
            fontSize: 12,
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >⚙ Tweaks</button>
      )}
    </div>
  );
}
```

### Applying Tweaks

Use Tweaks in the main component:

```jsx
function App() {
  const { tweaks } = useTweaks();

  return (
    <div style={{
      '--primary': tweaks.primaryColor,
      '--font-size': `${tweaks.fontSize}px`,
      background: tweaks.dark ? '#0A0A0A' : '#FAFAFA',
      color: tweaks.dark ? '#FAFAFA' : '#1A1A1A',
    }}>
      {/* Your content */}
      <TweaksPanel />
    </div>
  );
}
```

Use the variables in CSS:

```css
button.cta {
  background: var(--primary);
  color: white;
  font-size: var(--font-size);
}
```

## Typical Tweak options

What tweaks to add to different kinds of design:

### General
- Primary color (color picker)
- Font size (slider 12-24px)
- Typeface (select: display font vs body font)
- Dark mode (toggle)

### Slide deck
- Theme (light/dark/brand)
- Background style (solid/gradient/image)
- Type contrast (more decorative vs more restrained)
- Information density (minimal/standard/dense)

### Product prototype
- Layout variant (layout A / B / C)
- Interaction speed (animation speed 0.5x-2x)
- Data volume (number of mock data items 5/20/100)
- State (empty/loading/success/error)

### Animation
- Speed (0.5x-2x)
- Looping (once/loop/ping-pong)
- Easing (linear/easeOut/spring)

### Landing page
- Hero style (image/gradient/pattern/solid)
- CTA copy (several variants)
- Structure (single column / two column / sidebar)

## Tweaks design principles

### 1. Meaningful options, not busywork

Every tweak must expose a **real design choice**. Don't add tweaks nobody would actually switch (like a border-radius 0-50px slider, where the user finds every value in between is ugly).

A good tweak exposes **discrete, considered variations**:
- "Corner style": no rounding / slight rounding / large rounding (three options)
- Not: "Corner radius": 0-50px slider

### 2. Less is more

A design's Tweaks panel has **at most 5-6** options. Any more and it becomes a "settings page", losing the point of quickly exploring variations.

### 3. The defaults are the finished design

Tweaks are **icing on the cake**. The defaults must be a complete, shippable design on their own. What the user sees after closing the Tweaks panel is the deliverable.

### 4. Sensible grouping

When there are many options, show them in groups:

```
---- Visual ----
Primary color | Font size | Dark mode

---- Layout ----
Density | Sidebar position

---- Content ----
Data volume shown | State
```

## Forward compatibility with source-level persistence hosts

If you might later want the design to also run when uploaded to an environment that supports source-level tweaks (such as Claude.ai Artifacts), keep the **EDITMODE marker block**:

```jsx
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#2F6F5E",
  "fontSize": 16,
  "density": "comfortable",
  "dark": false
}/*EDITMODE-END*/;
```

The marker block **does nothing** in the localStorage approach (it's just an ordinary comment), but hosts that support writing back to the source will read it and get source-level persistence. Adding it is harmless in the current environment and keeps you forward compatible.

## Common issues

**The Tweaks panel covers the design content**
→ Make it closable. Closed by default, showing a small button that expands it only when the user clicks.

**The user has to set tweaks again after switching**
→ localStorage is already in use. If settings don't persist after a refresh, check whether localStorage is available (it fails in private browsing mode, so catch it).

**Multiple HTML pages want to share tweaks**
→ Add the project name to the localStorage key: `design-tweaks-[projectName]`.

**I want tweaks to be linked to each other**
→ Add logic in `update`:

```jsx
const update = (patch) => {
  let next = { ...tweaks, ...patch };
  // Linked: automatically switch the text color when dark mode is chosen
  if (patch.dark === true && !patch.textColor) {
    next.textColor = '#F0EEE6';
  }
  setTweaks(next);
  localStorage.setItem(...);
};
```
