# Security & Data-Flow Statement

This document exhaustively declares every network destination, credential touchpoint, subprocess, and deletion this skill can perform, so that users and automated security reviewers can verify the claims against the code.

**TL;DR (dstack): the core pipeline (HTML design → render → MP4/GIF/PDF/PPTX export, narration, video review) runs locally with zero API keys. dstack contains no cloud client: the upstream ByteDance/Volcengine integrations (Doubao TTS, Ark video review) were removed, and so was the startup version check. There is no telemetry. The only outbound requests are the optional, user-triggered ones listed below. Policy for this fork: no data to China-based services, CDNs or mirrors.**

## Complete list of network destinations

| Host | Where | What is sent | When |
|---|---|---|---|
| `commons.wikimedia.org` (official Wikimedia API, US) | `scripts/fetch_images.py` | Image search keywords; downloads CC/public-domain images with license info printed for review | Only when the agent fetches stock imagery for a content design |
| Brand official websites, `simpleicons.org`, Google favicon service | `references/brand-asset-protocol.md` (instructions, no script) | Plain GET requests to download publicly served logos/brand assets | Only when you ask for a brand-specific design |
| Reference works the agent chose (any URL it passes; not filtered) | `scripts/ref_board.py` | Plain GET via headless Chromium to screenshot a reference page or image | Only when the agent builds a reference board |
| `fonts.googleapis.com` / `fonts.gstatic.com` (Google, US), `unpkg.com`, `cdn.jsdelivr.net` | Static `<link>`/`<script>` tags inside demo/output HTML and style specimens | Standard browser font/library fetches when a page is opened or rendered | Browser-side only |
| Whatever *you* configure in `DSTACK_TTS_COMMAND` / `DSTACK_REVIEW_COMMAND` | `scripts/tts/providers.mjs`, `scripts/review-video.py` | Narration text / video clips, only if your command sends them | Off by default; the command is printed before it runs |

`grep -rn "https://" --include="*.py" --include="*.mjs" --include="*.js" --include="*.sh" scripts/` to verify.

Full file:line inventory of every host named in the pack: `HOSTS.md` (regenerate with `python3 tools/host_inventory.py`; it exits 1 if any China-linked host or service name appears). No China-hosted host is named or contacted. Measured egress for a full check run can be reproduced with `tools/egress/` (Python audit hook, Node `--require` hook, Chromium net-log, socket poller).

## API keys

dstack itself reads no API keys. `.env.example` lists only optional local settings. `references/react-setup.md` option B (pasting a key into a demo page input) is local-demo-only and not recommended.

## Optional hooks instead of cloud scripts

Narration defaults to `--tts silent` (silent track, estimated timings, subtitle-only). Video review defaults to local ffmpeg checks plus contact sheets. Both have an off-by-default `command` hook that runs a local command you configure; asking for it without configuring it exits with a clear error.

## Local files written outside the skill directory

Three helper scripts keep a small local memory so the skill improves with use. None of them makes a network call; nothing is ever uploaded.

| File | Written by | Contents |
|---|---|---|
| `~/.dstack/experience.md` | `scripts/learn.py add` | Taste preferences and lessons, including short **verbatim quotes of what you said** about a design. The agent is instructed to tell you when it records one, and not to record if you decline |
| `~/.dstack/ledger.jsonl` | `scripts/design_lint.py ledger add` | A "look fingerprint" of each delivered design (background color class, palette, font names, a coarse layout vector), the project name and **the project's absolute path**, so new projects can avoid repeating old looks |

Set `DSTACK_HOME` (or the upstream `HUASHU_DESIGN_HOME`) to move them; delete the folder to forget everything. Both files stay on your machine and are not part of the skill.

## Environment and filesystem reads

`scripts/capabilities.py` checks **whether** `OPENAI_API_KEY` / `GEMINI_API_KEY` are set (it never reads or prints their values), lists folder names in common skill directories (`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, `~/.cursor/skills`, and the project's `.claude/skills` / `.agents/skills`) to see which companion skills are installed, and checks for `node`, `ffmpeg`, `npx` and Playwright's Chromium. It writes nothing.

## Subprocesses

All subprocess calls invoke local media tools only: `ffmpeg`, `ffprobe`, `ffplay`, Playwright/Chromium for HTML rendering and screenshots. No shell-to-network combinations, no curl-pipe-sh patterns.

## File deletion

`ref_board.py` and `build_specimens.py` write one temporary HTML page (`.board.html` / `.sheet.html`) next to their output and delete it after the screenshot; `ref_board.py` also removes its own previous board file when every source fails, so a stale board is not mistaken for a new one. Recursive deletion is limited to temp directories the scripts themselves create with unique timestamp+PID names (`.video-tmp-*`, `.seek-tmp-*`, `_narration/.tmp`, Python `tempfile.TemporaryDirectory`). No script ever deletes user data or anything outside its own scratch space.

## Dependencies

Mainstream registry packages only (`playwright`, `pillow`, `sharp`, `pptxgenjs`, `pdf-lib`, `requests`; lockfile resolves to `registry.npmjs.org` only), installed via standard `npm`/`pip`/`uv` — no binary downloads from arbitrary URLs. One documented exception to be aware of: `npx hyperframes init` (optional animation backend, see `references/hyperframes-backend.md`) installs 19 hyperframes documentation skills into `~/.claude/skills/`. This is called out with a warning in the docs before the command.

## Hooks

`scripts/design-gate-hook.sh` is **never installed automatically** — nothing in this skill writes to `settings.json`. If you manually opt in, its entire behavior is: block long-video render commands (exit 2) until a design-approval file exists. It makes no network calls, writes nothing, deletes nothing.

## Proxy handling note

`fetch_images.py` disables inheriting proxy environment variables (`trust_env = False` / clearing `ALL_PROXY` etc.) for their own requests. This exists to survive stale local proxy configurations that break TLS — not to evade monitoring. If you need these requests to go through your proxy, set it explicitly in the script invocation.

## Reporting

Found something that contradicts this document? Please open an issue — a mismatch between this file and the code is treated as a bug.
