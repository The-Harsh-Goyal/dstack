#!/bin/bash
# sfx-cues.sh: add SFX hits to a silent video from a cue table (distilled from hands-on work on the B00 step b-roll, 2026-07-17)
#
# Usage: bash sfx-cues.sh <silent-video.mp4> <cue-table.tsv> <output.mp4> [--dur=seconds]
#
# Cue table format (TSV, lines starting with # are comments):
#   seconds<TAB>sfx path (absolute, or relative to $DSTACK_SFX_DIR, default ~/.dstack/audio/sfx)<TAB>volume dB
#   dstack ships no SFX (the upstream ElevenLabs-generated set was removed; licence unverified).
#   Missing files are skipped with a warning; if no cue can be used the video is copied unchanged (exit 0).
#   Example: 63.0	impact/brand-stamp.mp3	-13
#
# Volume baseline (light SFX under voiceover): whoosh-type -16 / tick-type -15 / impact-type -12; finished pure animations can go +4dB overall
# For cue density, see the recipes in audio-design-rules.md (b-roll bed ≈ 1 per 9s, hit only structural beats)

set -e
SFX_DIR="${DSTACK_SFX_DIR:-${DSTACK_AUDIO_DIR:-${DSTACK_HOME:-$HOME/.dstack}/audio}/sfx}"
IN="${1:?Usage: bash sfx-cues.sh in.mp4 cues.tsv out.mp4 [--dur=210]}"
TABLE="${2:?missing cue table}"
OUT="${3:?missing output path}"
DUR=""
for a in "$@"; do case "$a" in --dur=*) DUR="${a#*=}";; esac; done
[ -z "$DUR" ] && DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN" | cut -d. -f1)

INPUTS=(-i "$IN")
FILTER=""; MIX=""; i=1
while IFS=$'\t' read -r t f db; do
  [ -z "$t" ] && continue
  case "$t" in \#*) continue;; esac
  case "$f" in /*) src="$f";; *) src="$SFX_DIR/$f";; esac
  [ ! -f "$src" ] && { echo "⚠ SFX not found, cue skipped: $src (supply it, or: DSTACK_AUDIO_PROVIDER=elevenlabs node scripts/gen-audio.mjs sfx <category>/<name>)" >&2; continue; }
  INPUTS+=(-i "$src")
  ms=$(python3 -c "print(int(float('$t')*1000))")
  FILTER+="[$i:a]adelay=${ms}:all=1,volume=${db}dB[s$i];"
  MIX+="[s$i]"
  i=$((i+1))
done < "$TABLE"
N=$((i-1))
[ "$N" = "0" ] && { echo "⚠ no usable SFX cues; video copied unchanged → $OUT" >&2; cp "$IN" "$OUT"; exit 0; }

ffmpeg -y -loglevel error "${INPUTS[@]}" \
  -filter_complex "${FILTER}${MIX}amix=inputs=${N}:normalize=0,apad=whole_dur=${DUR}[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest "$OUT"

echo "✓ ${N} cues → $OUT"
