#!/usr/bin/env bash
# Pull later upstream .md edits from huashu-design-en into dstack, keeping dstack's edits.
# Three-way merge per file: base = snapshot commit, ours = dstack working tree, theirs = en.
# Reads the en folder only; never writes there. Conflicts are left marked in the dstack file.
#   tools/resync.sh [EN_DIR] [BASE_COMMIT]
set -euo pipefail
EN="${1:-/workspace/design/skills/huashu-design-en}"
BASE="${2:-1f70a6c}"
cd "$(dirname "$0")/.."
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
changed=0; conflicts=0
while IFS= read -r f; do
  rel="${f#"$EN"/}"
  [ -f "$rel" ] || continue
  git show "$BASE:$rel" > "$tmp/base" 2>/dev/null || continue
  cmp -s "$tmp/base" "$f" && continue           # upstream unchanged since snapshot
  changed=$((changed+1))
  if git merge-file -L dstack -L snapshot -L en "$rel" "$tmp/base" "$f"; then echo "merged   $rel"
  else conflicts=$((conflicts+1)); echo "CONFLICT $rel"; fi
done < <(find "$EN" -name '*.md' -not -path '*/node_modules/*')
echo "upstream-changed: $changed, conflicts: $conflicts"
