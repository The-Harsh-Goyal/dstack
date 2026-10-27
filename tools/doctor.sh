#!/usr/bin/env bash
# dstack doctor: is the local setup in place, and are the providers/hooks in an approved state?
# Approved: TTS silent (default) or elevenlabs; audio none (default) or elevenlabs; reviewer none.
# The ElevenLabs key is reported only as present/absent, never printed.
# Read-only: checks and prints, installs nothing, contacts no network.
#   bash /workspace/dstack/tools/doctor.sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ok=0
say() { printf '%-28s %s\n' "$1" "$2"; }
fail() { say "$1" "✗ $2"; ok=1; }

if [ -x "$ROOT/.venv/bin/python" ] && "$ROOT/.venv/bin/python" -c "import playwright, PIL, pptx" 2>/dev/null; then
  say "python venv" "✓ $ROOT/.venv ($("$ROOT/.venv/bin/python" -c 'from importlib.metadata import version as v; print("playwright", v("playwright"))'))"
else fail "python venv" "missing: run the one-time setup in INSTALL_BODY.md"; fi
if [ -d "$ROOT/node_modules/playwright" ]; then
  say "node_modules" "✓ playwright $(node -p "require('$ROOT/node_modules/playwright/package.json').version")"
else fail "node_modules" "missing: (cd $ROOT && npm ci)"; fi
if "$ROOT/.venv/bin/python" - <<'PY' 2>/dev/null
from playwright.sync_api import sync_playwright
import os, sys
with sync_playwright() as p:
    sys.exit(0 if os.path.exists(p.chromium.executable_path) else 1)
PY
then say "chromium" "✓ cached"; else fail "chromium" "missing: $ROOT/.venv/bin/python -m playwright install chromium (needs Harsh's OK)"; fi
command -v ffmpeg >/dev/null && say "ffmpeg" "✓ $(command -v ffmpeg)" || fail "ffmpeg" "not on PATH"

tts="${DSTACK_TTS_PROVIDER:-silent}"; aud="${DSTACK_AUDIO_PROVIDER:-none}"; rev="${DSTACK_REVIEWER:-none}"
key="absent"
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then key="present (env ELEVENLABS_API_KEY)"
elif [ -n "${DSTACK_ELEVENLABS_KEY_FILE:-}" ]; then
  kf="$(realpath -m "${DSTACK_ELEVENLABS_KEY_FILE/#\~/$HOME}")"
  case "$kf" in
    "$ROOT"|"$ROOT"/*) fail "ElevenLabs key file" "inside the dstack folder ($kf): move it outside the repo";;
    *) if [ -r "$kf" ] && [ -s "$kf" ]; then key="present (file DSTACK_ELEVENLABS_KEY_FILE)"
       else say "ElevenLabs key file" "! DSTACK_ELEVENLABS_KEY_FILE set but $kf is unreadable or empty"; fi;;
  esac
fi
el_note() { [ "$key" = absent ] && echo "(approved; no key, so it falls back to $1)" || echo "(approved; uses ElevenLabs credits, enable only for a task that asks)"; }
case "$tts" in
  silent) say "DSTACK_TTS_PROVIDER" "✓ silent (default, off)";;
  elevenlabs) say "DSTACK_TTS_PROVIDER" "✓ elevenlabs $(el_note silent)";;
  *) fail "DSTACK_TTS_PROVIDER" "$tts (approved: silent | elevenlabs)";;
esac
case "$aud" in
  none) say "DSTACK_AUDIO_PROVIDER" "✓ none (default, off)";;
  elevenlabs) say "DSTACK_AUDIO_PROVIDER" "✓ elevenlabs $(el_note none)";;
  *) fail "DSTACK_AUDIO_PROVIDER" "$aud (approved: none | elevenlabs)";;
esac
say "ElevenLabs key" "$key"
[ "$rev" = none ] && say "DSTACK_REVIEWER" "✓ none" || fail "DSTACK_REVIEWER" "$rev (must stay none unless Harsh approved a reviewer)"
[ -z "${DSTACK_TTS_COMMAND:-}" ] && say "DSTACK_TTS_COMMAND" "✓ unset" || say "DSTACK_TTS_COMMAND" "! set: $DSTACK_TTS_COMMAND"
[ -z "${DSTACK_REVIEW_COMMAND:-}" ] && say "DSTACK_REVIEW_COMMAND" "✓ unset" || say "DSTACK_REVIEW_COMMAND" "! set: $DSTACK_REVIEW_COMMAND"
say "data home (ledger, taste)" "${DSTACK_HOME:-${HUASHU_DESIGN_HOME:-$HOME/.dstack}}"
exit $ok
