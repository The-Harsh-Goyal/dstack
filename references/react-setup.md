# React + Babel project conventions

Technical conventions you must follow when building prototypes with HTML+React+Babel. Ignore them and things blow up.

## Pinned Script Tags (you must use these versions)

Put these three script tags in the HTML `<head>`, with **pinned versions + integrity hashes**:

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

**Don't** use unpinned versions like `react@18` or `react@latest`; you'll get version drift / caching problems.

**Don't** omit `integrity`; if the CDN is ever hijacked or tampered with, this is your line of defense.

## File structure

```
project-name/
├── index.html               # main HTML
├── components.jsx           # component file (loaded with type="text/babel")
├── data.js                  # data file
└── styles.css               # extra CSS (optional)
```

How to load them in the HTML:

```html
<!-- React+Babel first -->
<script src="https://unpkg.com/react@18.3.1/..."></script>
<script src="https://unpkg.com/react-dom@18.3.1/..."></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/..."></script>

<!-- then your component files -->
<script type="text/babel" src="components.jsx"></script>
<script type="text/babel" src="pages.jsx"></script>

<!-- main entry last -->
<script type="text/babel">
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<App />);
</script>
```

**Don't** use `type="module"`; it conflicts with Babel.

## Three rules you must never break

### Rule 1: styles objects must have unique names

**Wrong** (guaranteed to blow up with multiple components):
```jsx
// components.jsx
const styles = { button: {...}, card: {...} };

// pages.jsx  ← same name, overwritten!
const styles = { container: {...}, header: {...} };
```

**Right**: give each component file's styles a unique prefix.

```jsx
// terminal.jsx
const terminalStyles = { 
  screen: {...}, 
  line: {...} 
};

// sidebar.jsx
const sidebarStyles = { 
  container: {...}, 
  item: {...} 
};
```

**Or use inline styles** (recommended for small components):
```jsx
<div style={{ padding: 16, background: '#111' }}>...</div>
```

This one is **non-negotiable**. Every time you write `const styles = {...}` you must replace it with a specific name, or loading multiple components throws errors across the whole stack.

### Rule 2: scope isn't shared, so export manually

**Key insight**: Babel compiles each `<script type="text/babel">` independently, and **scope doesn't carry over** between them. A `Terminal` component defined in `components.jsx` is **undefined by default** in `pages.jsx`.

**Fix**: at the end of each component file, export the components/utilities you want to share onto `window`:

```jsx
// end of components.jsx
function Terminal(props) { ... }
function Line(props) { ... }
const colors = { green: '#...', red: '#...' };

Object.assign(window, {
  Terminal, Line, colors,
  // list everything you want to use elsewhere here
});
```

Then `pages.jsx` can use `<Terminal />` directly, because JSX will look it up on `window.Terminal`.

### Rule 3: don't use scrollIntoView

`scrollIntoView` pushes the whole HTML container up and breaks the web harness layout. **Never use it**.

Alternatives:
```js
// scroll to a position inside the container
container.scrollTop = targetElement.offsetTop;

// or use element.scrollTo
container.scrollTo({
  top: targetElement.offsetTop - 100,
  behavior: 'smooth'
});
```

## Calling the Claude API (inside HTML)

Some native design-agent environments (such as Claude.ai Artifacts) have a zero-config `window.claude.complete`, but most agent environments (Claude Code / Codex / Cursor / Trae / etc.) **don't** have it locally.

If your HTML prototype needs to call an LLM for a demo (say, a chat interface), here are two options:

### Option A: don't really call it, use a mock

Recommended for demos. Write a fake helper that returns a preset response:
```jsx
window.claude = {
  async complete(prompt) {
    await new Promise(r => setTimeout(r, 800)); // simulate latency
    return "This is a mock response. Replace it with the real API when you actually deploy.";
  }
};
```

### Option B: really call the Anthropic API (not recommended, local demos only)

This needs an API key, and the user has to enter their own key in the HTML for it to run. **Never hard-code the key in the HTML**.

⚠️ Security boundary: this approach only suits demos opened locally via `file://` and closed right after use. The key stays in the DOM/memory.
**Don't deploy this page, and don't share screenshots/screen recordings of the page with the key filled in**. Production always goes through a local proxy backend,
and the browser side never touches the key. Prefer options A/C by default (no key needed at all).

```html
<input id="api-key" placeholder="Paste your Anthropic API key" />
<script>
window.claude = {
  async complete(prompt) {
    const key = document.getElementById('api-key').value;
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5',
        max_tokens: 1024,
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await res.json();
    return data.content[0].text;
  }
};
</script>
```

**Note**: calling the Anthropic API directly from the browser runs into CORS problems. If the preview environment the user gives you doesn't support a CORS bypass, this route won't work. In that case use the option A mock, or tell the user they need a proxy backend.

### Option C: generate mock data with the agent's own LLM capability

If it's only for a local demo, you can use the current agent session's own LLM capability (or a multi-model skill the user has installed) to generate mock response data first, then hard-code it into the HTML. That way the HTML doesn't depend on any API at runtime.

## Typical HTML starter template

Copy this template as the skeleton of a React prototype:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Prototype Name</title>

  <!-- React + Babel pinned -->
  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; width: 100%; }
    body { 
      font-family: -apple-system, 'SF Pro Text', sans-serif;
      background: #FAFAFA;
      color: #1A1A1A;
    }
    #root { min-height: 100vh; }
  </style>
</head>
<body>
  <div id="root"></div>

  <!-- your component files -->
  <script type="text/babel" src="components.jsx"></script>

  <!-- main entry -->
  <script type="text/babel">
    const { useState, useEffect } = React;

    function App() {
      return (
        <div style={{padding: 40}}>
          <h1>Hello</h1>
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
```

## Common errors and fixes

**`styles is not defined` or `Cannot read property 'button' of undefined`**
→ You defined `const styles` in one file and another file overwrote it. Give each one a specific name.

**`Terminal is not defined`**
→ Scope doesn't carry over for cross-file references. Add `Object.assign(window, {Terminal})` at the end of the file that defines Terminal.

**The whole page is blank, no errors in the console**
→ Most likely a JSX syntax error that Babel didn't report in the console. Temporarily swap `babel.min.js` for the unminified `babel.js`; the error messages are clearer.

**ReactDOM.createRoot is not a function**
→ Wrong version. Make sure you're using react-dom@18.3.1 (not 17 or anything else).

**`Objects are not valid as a React child`**
→ You rendered an object instead of JSX/a string. Usually `{someObj}` should have been written as `{someObj.name}`.

## How to split files in a large project

**A single file >1000 lines** is hard to maintain. How to split it:

```
project/
├── index.html
├── src/
│   ├── primitives.jsx      # primitives: Button, Card, Badge...
│   ├── components.jsx      # business components: UserCard, PostList...
│   ├── pages/
│   │   ├── home.jsx        # home page
│   │   ├── detail.jsx      # detail page
│   │   └── settings.jsx    # settings page
│   ├── router.jsx          # simple routing (switching React state)
│   └── app.jsx             # entry component
└── data.js                 # mock data
```

Load them in order in the HTML:
```html
<script type="text/babel" src="src/primitives.jsx"></script>
<script type="text/babel" src="src/components.jsx"></script>
<script type="text/babel" src="src/pages/home.jsx"></script>
<script type="text/babel" src="src/pages/detail.jsx"></script>
<script type="text/babel" src="src/pages/settings.jsx"></script>
<script type="text/babel" src="src/router.jsx"></script>
<script type="text/babel" src="src/app.jsx"></script>
```

**At the end of every file**, use `Object.assign(window, {...})` to export what needs to be shared.
