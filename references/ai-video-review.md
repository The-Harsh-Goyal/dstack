# Video Review Loop (scripts/review-video.py)

> dstack note: the upstream cloud review (Volcengine Ark, seed-2.0-lite) was removed. `review-video.py` runs fully locally by default:
> ffmpeg objective detection + one contact sheet (frame grid PNG) per segment + the checklist, written as a markdown report. Look at the
> sheets (or have the agent view them) against the checklist. An optional `--reviewer command` hook (`DSTACK_REVIEW_COMMAND`, off by default)
> can feed each segment to a reviewer you configure later. Nothing is sent anywhere unless you set that up.

## When to use it

- Once the final 60fps film is out, before delivery/mixing, run it once
- Run it again after the SFX mix is out (onset checking only works when there's an audio track)
- Recheck after re-rendering to fix major issues

## How to use it

```bash
python3 /workspace/dstack/scripts/review-video.py --video final-film.mp4 --context directors-script.md
# optional, off by default:
DSTACK_REVIEW_COMMAND='my-adapter --video {video} --prompt {prompt_file}' \
  python3 /workspace/dstack/scripts/review-video.py --video final-film.mp4 --reviewer command
```

- Report: `<video-name>-review.md` next to the video (`--output` to change); sheets in `<video-name>-review-sheets/`
- `--segment-len` defaults to 60 seconds per segment

> The section below describes the upstream model loop; with dstack it applies only when `--reviewer command` is used.

## Call chain (three-layer hybrid, not purely the model)

1. **ffmpeg objective detection** (deterministic, misses nothing):
   - `silencedetect` → timetable of sound-effect onsets (the model **cannot hear** the video's audio track, measured 2026-07-17)
   - `freezedetect` → list of segments that are completely still for ≥3 seconds
2. **Model reviews segments**: each 60s segment is compressed and sent for review (1280 wide/15fps/crf28, flat animation is about 0.5MB/minute);
   each segment's prompt includes the checklist + the director's script + that segment's onset/still-segment data, with timestamps converted to the original film's time
3. **Model's low-res full-film pass**: the whole film at 960 wide/10fps is sent separately for review, focusing only on cross-segment narrative continuity/hero continuity/overall pacing
4. A text summary call merges results by ①-⑧; the raw per-segment records + objective detection data are all kept in the report appendix

## Checklist and severity

①Black frames/incomplete rendering ②Clipped text/typos ③Overlapping or occluded elements ④Narrative continuity (transitions are identified using the three-layer vocabulary in camera-language.md §7: the six types [flash-wash/dip-to-dark/defocus-handoff/title-card/whip-pan/mask-wipe], hidden-cut, travel [shared-element homing/letter-counter fly-through]; bare cut = an unwrapped hard cut, marked ⚡)
⑤Hero continuity ⑥Dead pacing segments (objective list + model judgment of deliberate hold vs. truly dead segment) ⑦Sound-effect sync (onset + on-screen event check)
⑧Unbalanced composition/empty space

⚠️Critical = must fix before delivery | ⚡Important = noticeably hurts the viewing experience | 💡Suggestion = nice to have

## Limitations (read before using the report)

- **The model can't hear sound**: ⑦ is a one-way check of "whether there's an on-screen event at the audio onset moment";
  it can't judge whether the sound effect choice, volume, or BGM mood is right
- **It can't see frame-level detail**: 1-2 frame flickers, subtle jitter, precise color value deviations, and sub-pixel alignment slip through;
  these still rely on verify-video.sh frame captures and manual review
- **Transition type judgment runs strict**: after compression to 15fps, a fast crossfade may be reported as a "hard cut";
  when the segment pass and the full-film pass contradict each other, the summary marks it "uncertain"; pull frames yourself to confirm uncertain items before changing anything
- **"Deliberate hold vs. dead segment" is the model's opinion**: long freeze-frames where b-roll backs a voiceover are often let through; judge them again yourself when the film is watched on its own
- Call failures (network/key/quota) are written truthfully into the report header, and review results are never fabricated; the time ranges of failed segments are marked

## Measured baseline

First run target: B00-前三分钟主线-SFX.mp4 (210s). The model independently found the inter-act transition issues and the hero break points in the right direction,
but misreported fades as hard cuts; the model alone caught only 3/14 dead segments, and after adding freezedetect coverage was complete. Conclusion: the objective detection layer is
the floor guarantee of this loop, and the model is responsible for semantic judgment.
