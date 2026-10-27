#!/bin/bash
# design-gate-hook.sh: PreToolUse(Bash) hook: checks the design process gate file before rendering long videos
#
# Iron rule background (set by Huashu on 2026-07-17): before designing, huashu-design must ① run the asset protocol (brand-spec.md)
# ② give the user three directions of real visuals to choose from (direction-approved.md records the choice or the reason for an exemption).
# B00 (210s) in practice: skipping direction confirmation and rendering the whole video → redoing the entire video. This hook turns the lesson into a machine constraint:
# **compositions ≥45 seconds long may not render without direction-approved.md**. Redoing a long video costs far more than pausing for a moment.
#
# Allowed through if (any of):
#   - the composition is <45s or its length can't be determined (shorts/experiments stay low-friction, governed by the SKILL.md gate protocol)
#   - direction-approved.md exists in the project directory (or up to two levels above)
#   - the command explicitly includes SKIP_DESIGN_GATE=1 (used when Huashu explicitly says to skip; auditable)
#
# Security statement: this hook **is not installed automatically by the skill**. SKILL.md/README contain no instruction to write into settings.json;
# it only takes effect after you manually configure it in settings.json. Maximum behavior: for matching long-video render commands, exit 2
# to block execution and print the reason; no network requests, no file writes, no deletions. See SECURITY.md in the repo root.
#
# settings.json configuration: PreToolUse / matcher "Bash" / command pointing to this script

INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | python3 -c "import json,sys;print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
CWD=$(printf '%s' "$INPUT" | python3 -c "import json,sys;print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null)

# Commands that talk about commands (echo/grep etc.) pass straight through, to avoid false hits on plain text (QA Bug1)
FIRST=$(echo "$CMD" | sed -E 's/^[[:space:]]*//' | cut -d' ' -f1)
case "$FIRST" in echo|printf|grep|cat|ls|head|tail|wc|sed|awk) exit 0;; esac
# Only handle render commands (including npm run render and long narrated video renders)
echo "$CMD" | grep -qE "hyperframes(@[0-9.]+)? +render|render-video(-seek)?\.js|render-narration\.sh|npm +run +render\b" || exit 0
# Explicit skip (an auditable escape hatch)
echo "$CMD" | grep -q "SKIP_DESIGN_GATE=1" && exit 0

# Locate the project directory: the target of a cd in the command > the hook cwd
DIR="$CWD"
CDDIR=$(echo "$CMD" | grep -oE 'cd +"[^"]+"|cd +[^ &;]+' | head -1 | sed -E 's/^cd +//; s/"//g')
[ -n "$CDDIR" ] && [ -d "$CDDIR" ] && DIR="$CDDIR"

# Get the composition length: hyperframes projects read data-duration from index.html; render-video-seek reads the --duration argument
DUR=""
D_ARG=$(echo "$CMD" | grep -oE '\-\-duration=[0-9]+' | head -1 | cut -d= -f2)
[ -n "$D_ARG" ] && DUR="$D_ARG"
if [ -z "$DUR" ] && [ -f "$DIR/index.html" ]; then
  DUR=$(grep -oE 'data-duration="[0-9.]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9.]+' | cut -d. -f1)
fi
# Length can't be determined, or it's a short → allow
[ -z "$DUR" ] && exit 0
[ "$DUR" -lt 45 ] 2>/dev/null && exit 0

# Long video: look for the gate file (project directory and up to two levels above)
for d in "$DIR" "$DIR/.." "$DIR/../.."; do
  if [ -f "$d/direction-approved.md" ]; then
    # dstack: an auto-default written by scripts/gate.py (no human present) does not block; it is logged and flagged
    grep -q "status: auto-default" "$d/direction-approved.md" && echo "ℹ️ direction-approved.md is an auto-default (no human choice yet); rendering as a draft, see gate-log.md" >&2
    exit 0
  fi
done

cat >&2 << EOF
🛑 Design process gate: this composition is ${DUR}s long (≥45s long video), but no direction-approved.md was found in the project.
dstack iron rule: before rendering a long video you must complete "give the user three directions of real visuals to choose from" (or have the user explicitly waive it), and write the choice/waiver record to direction-approved.md in the project directory (including: which versions were shown, screenshot paths, the user's choice in their own words).
Fill this in, then re-render; if the user explicitly says in person to skip, prefix the command with SKIP_DESIGN_GATE=1 to allow it explicitly.
(Basis: B00 in practice on 2026-07-17, skipping direction confirmation and rendering the full 210s video → redoing the visuals of the entire video)
EOF
exit 2
