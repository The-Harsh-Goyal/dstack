#!/usr/bin/env bash
# dstack doctor: is the local setup in place, and are the providers/hooks in an approved state?
# Approved: TTS silent (default) or elevenlabs; audio none (default), local (offline music library) or
# elevenlabs; reviewer none. The local music library's manifest.json is validated (offline).
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
    *) # same forms as loadKey() (scripts/audio/keyfile.mjs): a dotenv line ELEVENLABS_API_KEY=...
       # (optional export/quotes, comments ignored) or the bare key on line 1. Tests the file; never prints it.
       if [ ! -r "$kf" ]; then say "ElevenLabs key file" "! DSTACK_ELEVENLABS_KEY_FILE set but $kf is unreadable"
       elif grep -Eq '^[[:space:]]*(export[[:space:]]+)?ELEVENLABS_API_KEY[[:space:]]*=' "$kf"; then
         if grep -Eq '^[[:space:]]*(export[[:space:]]+)?ELEVENLABS_API_KEY[[:space:]]*=[[:space:]]*(["'"'"'][^"'"'"'[:space:]]|[^"'"'"'#[:space:]])' "$kf"
         then key="present (file DSTACK_ELEVENLABS_KEY_FILE, dotenv)"
         else say "ElevenLabs key file" "! $kf has ELEVENLABS_API_KEY= but no value"; fi
       elif head -n1 "$kf" | grep -Eq '^[[:space:]]*[^#=[:space:]][^=]*$'; then key="present (file DSTACK_ELEVENLABS_KEY_FILE, bare key)"
       else say "ElevenLabs key file" "! $kf has no key (expected ELEVENLABS_API_KEY=... or the bare key on line 1)"; fi;;
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
  local) say "DSTACK_AUDIO_PROVIDER" "✓ local (offline music library, no network)";;
  elevenlabs) say "DSTACK_AUDIO_PROVIDER" "✓ elevenlabs $(el_note none) (bgm falls back to the local library)";;
  *) fail "DSTACK_AUDIO_PROVIDER" "$aud (approved: none | local | elevenlabs)";;
esac
# Local music library: validate manifest.json (fields, files, licence, commercial flag). Offline.
if command -v node >/dev/null; then
  mlib_out="$(node "$ROOT/scripts/audio/music-library.mjs" validate 2>&1)"; mlib_rc=$?
  mlib_head="$(printf '%s\n' "$mlib_out" | head -1)"
  if [ $mlib_rc -eq 0 ]; then say "local music library" "✓ $mlib_head"
  else fail "local music library" "$mlib_head"; fi
  printf '%s\n' "$mlib_out" | tail -n +2 | while IFS= read -r l; do say "" "$l"; done
  [ "${DSTACK_MUSIC_ALLOW_NONCOMMERCIAL:-}" = 1 ] && say "DSTACK_MUSIC_ALLOW_NONCOMMERCIAL" "! 1: non-commercial tracks may be used (personal / non-commercial work only)"
fi
say "ElevenLabs key" "$key"
[ "$rev" = none ] && say "DSTACK_REVIEWER" "✓ none" || fail "DSTACK_REVIEWER" "$rev (must stay none unless Harsh approved a reviewer)"
[ -z "${DSTACK_TTS_COMMAND:-}" ] && say "DSTACK_TTS_COMMAND" "✓ unset" || say "DSTACK_TTS_COMMAND" "! set: $DSTACK_TTS_COMMAND"
[ -z "${DSTACK_REVIEW_COMMAND:-}" ] && say "DSTACK_REVIEW_COMMAND" "✓ unset" || say "DSTACK_REVIEW_COMMAND" "! set: $DSTACK_REVIEW_COMMAND"
say "data home (ledger, taste)" "${DSTACK_HOME:-${HUASHU_DESIGN_HOME:-$HOME/.dstack}}"
exit $ok
