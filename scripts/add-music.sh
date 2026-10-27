#!/usr/bin/env bash
# Mix a user-supplied BGM track into an MP4 video.
#
# dstack ships NO music (the upstream Suno-generated tracks were removed because
# their licence couldn't be verified). Bring your own licensed track:
#   --music=<path>    any audio file you have the rights to (wins over --mood)
#   --mood=<name>     looks up bgm-<name>.mp3 in your own audio library:
#                     $DSTACK_AUDIO_DIR (default ~/.dstack/audio)
#   --out=<path>      output path (default: <input-basename>-bgm.mp4)
#
# If no music is found, the script does NOT fail: it copies the video unchanged
# to the output path, prints a notice and exits 0, so pipelines keep working.
#
# Legacy positional form still works: bash add-music.sh in.mp4 music.mp3 out.mp4
#
# Behavior:
#   - Music is trimmed to match video duration
#   - 0.3s fade in, 1.0s fade out (avoids hard cuts)
#   - Video stream copied (no re-encode), audio AAC 192k
#
# Examples:
#   bash add-music.sh my.mp4 --music=~/Music/licensed-track.mp3
#   bash add-music.sh my.mp4 --mood=tech      # needs ~/.dstack/audio/bgm-tech.mp3
#
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AUDIO_DIR="${DSTACK_AUDIO_DIR:-${DSTACK_HOME:-$HOME/.dstack}/audio}"

# ── Parse args ───────────────────────────────────────────────────────
INPUT=""
MOOD=""
CUSTOM_MUSIC=""
OUTPUT=""
POSITIONAL=()

for arg in "$@"; do
  case "$arg" in
    --mood=*)  MOOD="${arg#*=}" ;;
    --music=*) CUSTOM_MUSIC="${arg#*=}" ;;
    --out=*)   OUTPUT="${arg#*=}" ;;
    *)         POSITIONAL+=("$arg") ;;
  esac
done

# Legacy positional: <input> [music] [output]
INPUT="${POSITIONAL[0]}"
[ -z "$CUSTOM_MUSIC" ] && [ -n "${POSITIONAL[1]}" ] && CUSTOM_MUSIC="${POSITIONAL[1]}"
[ -z "$OUTPUT" ]       && [ -n "${POSITIONAL[2]}" ] && OUTPUT="${POSITIONAL[2]}"

if [ -z "$INPUT" ] || [ ! -f "$INPUT" ]; then
  echo "Usage: bash add-music.sh <input.mp4> [--mood=<name>] [--music=<path>] [--out=<path>]" >&2
  echo "Moods in your audio library ($AUDIO_DIR): $(ls "$AUDIO_DIR" 2>/dev/null | grep -E '^bgm-.*\.mp3$' | sed 's/^bgm-//;s/\.mp3$//' | tr '\n' ' ')" >&2
  exit 1
fi

# ── Resolve music source: --music wins, else --mood ─────────────────
if [ -n "$CUSTOM_MUSIC" ]; then
  MUSIC="$CUSTOM_MUSIC"
  SOURCE_LABEL="custom: $MUSIC"
elif [ -n "$MOOD" ]; then
  MUSIC="$AUDIO_DIR/bgm-${MOOD}.mp3"
  SOURCE_LABEL="mood: $MOOD"
else
  MUSIC=""
fi

# ── Resolve output path ─────────────────────────────────────────────
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
INPUT_NAME="$(basename "$INPUT" .mp4)"
[ -z "$OUTPUT" ] && OUTPUT="$INPUT_DIR/$INPUT_NAME-bgm.mp4"

if [ -z "$MUSIC" ] || [ ! -f "$MUSIC" ]; then
  echo "⚠ No music: ${MUSIC:-none given}. dstack ships no music; pass --music=<licensed file> or put bgm-<mood>.mp3 in $AUDIO_DIR." >&2
  if [ "$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")" != "$INPUT_DIR/$(basename "$INPUT")" ]; then
    cp "$INPUT" "$OUTPUT"
  fi
  echo "✓ Video left without music: $OUTPUT"
  exit 0
fi

# ── Measure video duration, compute fade-out start ──────────────────
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT")
if [ -z "$DURATION" ]; then
  echo "✗ Could not read video duration" >&2
  exit 1
fi
FADE_OUT_START=$(awk "BEGIN { d = $DURATION - 1; if (d < 0) d = 0; print d }")

echo "▸ Mixing BGM into video"
echo "  input:    $INPUT"
echo "  music:    $SOURCE_LABEL"
echo "  duration: ${DURATION}s"
echo "  output:   $OUTPUT"

ffmpeg -y -loglevel error \
  -i "$INPUT" \
  -i "$MUSIC" \
  -filter_complex "[1:a]atrim=0:${DURATION},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st=${FADE_OUT_START}:d=1[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  "$OUTPUT"

SIZE=$(du -h "$OUTPUT" | cut -f1)
echo "✓ Done: $OUTPUT ($SIZE)"
