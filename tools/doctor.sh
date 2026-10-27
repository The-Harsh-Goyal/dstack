#!/usr/bin/env bash
# dstack doctor: is the local setup in place, and are the hooks still off?
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

tts="${DSTACK_TTS_PROVIDER:-silent}"; rev="${DSTACK_REVIEWER:-none}"
[ "$tts" = silent ] && say "DSTACK_TTS_PROVIDER" "✓ silent" || fail "DSTACK_TTS_PROVIDER" "$tts (must stay silent unless Harsh approved a provider)"
[ "$rev" = none ] && say "DSTACK_REVIEWER" "✓ none" || fail "DSTACK_REVIEWER" "$rev (must stay none unless Harsh approved a reviewer)"
[ -z "${DSTACK_TTS_COMMAND:-}" ] && say "DSTACK_TTS_COMMAND" "✓ unset" || say "DSTACK_TTS_COMMAND" "! set: $DSTACK_TTS_COMMAND"
[ -z "${DSTACK_REVIEW_COMMAND:-}" ] && say "DSTACK_REVIEW_COMMAND" "✓ unset" || say "DSTACK_REVIEW_COMMAND" "! set: $DSTACK_REVIEW_COMMAND"
say "data home (ledger, taste)" "${DSTACK_HOME:-${HUASHU_DESIGN_HOME:-$HOME/.dstack}}"
exit $ok
