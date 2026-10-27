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

Voice and sound effects come from ElevenLabs. dstack's own scripts (`scripts/audio/elevenlabs.mjs`, `scripts/gen-audio.mjs`) call the ElevenLabs API directly at the US host `api.elevenlabs.io` with your API key.

- Off by default (`DSTACK_TTS_PROVIDER=silent`, `DSTACK_AUDIO_PROVIDER=none`). Turn it on per run for narration or sound effects.
- The key comes from `ELEVENLABS_API_KEY` or a key file outside the repo (`DSTACK_ELEVENLABS_KEY_FILE`). It is masked in logs and never committed.
- The free ElevenLabs plan is enough for voice and sound effects; its output is non-commercial and needs attribution. Details and sources are in [references/audio-design-rules.md](references/audio-design-rules.md#licensing-dstack-elevenlabs-output).

Background music comes from a local royalty-free library: `DSTACK_AUDIO_PROVIDER=local` picks tracks by mood from `~/.dstack/music`, whose `manifest.json` records each track's source, licence and attribution, and makes no network calls at render time. See [Local music library](references/audio-design-rules.md#local-music-library).

Every outside host the pack touches is listed in [HOSTS.md](HOSTS.md).

## Licence

MIT. Original work © 2026 alchaincyf; dstack's changes are released under the same licence.
