# dstack

dstack is an English-translated fork of [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design), used under the MIT License. See [NOTICE](NOTICE) for what changed and [LICENSE](LICENSE) for the original copyright.

## What it does

dstack is a design-studio skill for coding agents. It makes high-fidelity work in HTML and renders it locally with Playwright Chromium and ffmpeg:

- covers and single social images at exact sizes (for example X `x-infeed` 1600×900, `x-article` 2500×1000)
- slide decks (HTML, PDF, editable PPTX), web and app prototypes, infographics
- animation exported to MP4 or GIF, and design reviews

For every new design it first drafts three directions and waits for a choice. Everything it makes is a draft; it never posts or publishes.

## Quick start

1. Read [INSTALL_BODY.md](INSTALL_BODY.md). It is the agent instruction file, with absolute paths and the hard rules.
2. Run `bash tools/doctor.sh` to check Python, Node, Playwright, ffmpeg and which providers are on.

Dependencies install locally only (`.venv`, `node_modules`); nothing is installed globally.

## What was removed, and the optional ElevenLabs provider

The upstream pack's China-linked parts were removed: Doubao text-to-speech, Volcengine video review, and the bundled Suno/ElevenLabs music and sound-effect files (their licence could not be verified).

In their place there is one optional provider, ElevenLabs:

- Calls the ElevenLabs REST API at the US host `api.elevenlabs.io` from local scripts (`scripts/audio/elevenlabs.mjs`, `scripts/gen-audio.mjs`). No MCP connector or plugin is used.
- Off by default (`DSTACK_TTS_PROVIDER=silent`, `DSTACK_AUDIO_PROVIDER=none`). Turn it on per run for narration, sound effects or music.
- Needs `ELEVENLABS_API_KEY` in the environment. The key is never written to disk or logged.
- Plans and licensing: free-plan output is non-commercial and needs attribution, and the Music API is paid-only. Details and sources are in [references/audio-design-rules.md](references/audio-design-rules.md#licensing-dstack-elevenlabs-output).

Free background music: `DSTACK_AUDIO_PROVIDER=local` picks tracks from your own offline library (`~/.dstack/music` + `manifest.json` with licence and attribution), and ElevenLabs music falls back to it; see [Local music library](references/audio-design-rules.md#local-music-library).

Every outside host the pack touches is listed in [HOSTS.md](HOSTS.md).

## Licence

MIT. Original work © 2026 alchaincyf; dstack's changes are released under the same licence.
