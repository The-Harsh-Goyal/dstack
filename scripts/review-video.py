#!/usr/bin/env python3
"""
review-video.py: QC review of a rendered animation MP4.

dstack runs this fully locally by default and sends nothing anywhere:
  1. ffprobe: duration / audio track
  2. ffmpeg silencedetect: sound-effect onset table (if there is audio)
  3. ffmpeg freezedetect: static segments >= 3 s
  4. ffmpeg: one contact sheet per segment (PNG grid of frames) for the agent
     or a person to look at against the checklist (1)-(8)
  5. a markdown report with the objective data, the checklist and the sheets

Optional model review (OFF by default): --reviewer command runs a LOCAL command
you configure in DSTACK_REVIEW_COMMAND, once per segment, the whole-film pass and
the synthesis. Placeholders: {video} (compressed clip, or empty for the synthesis
call), {prompt_file} (UTF-8 prompt). The command prints the review markdown on
stdout. This is the plug-in point for a vetted provider adapter added later;
dstack contains no cloud video reviewer (the upstream Volcengine Ark integration was removed).

Usage:
    python3 scripts/review-video.py --video final.mp4
    python3 scripts/review-video.py --video final.mp4 --context director-notes.md --segment-len 30
    DSTACK_REVIEW_COMMAND='my-adapter --video {video} --prompt {prompt_file}' \
        python3 scripts/review-video.py --video final.mp4 --reviewer command
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


MAX_SEGMENT_MB = 8  # if a compressed segment exceeds this, compress it one more notch

CHECKLIST = """\
① Black frames/blank gaps/incomplete rendering: whole-frame or large black or white screens, elements not rendered, obviously broken images
② Text problems: title cards/labels clipped, overflowing their container, typos, garbled text, text overlapping text
③ Elements overlapping/occluding: elements that shouldn't overlap covering each other, wrong layering, clipping through each other
④ Narrative continuity: scene transitions come in three kinds: hard cut (the whole frame changes abruptly between frames, with no connection at all),
   crossfade (the old scene's opacity fades out), morph (elements continuously deform/move into the new scene).
   Your report must state which kind you saw; don't misreport a crossfade as a hard cut;
   hard cut = ⚡, crossfade when the director's script calls for morph = 💡 "lazy transition"
⑤ hero/subject continuity: if a subject element runs through the whole film, does it break, disappear or jump position at scene changes
⑥ Dead stretches in pacing: see the "objective static-segment table" below (ffmpeg frame-by-frame detection, intervals of ≥3 seconds completely still).
   Your job isn't to find dead stretches but to judge each interval in the table: is it a deliberate hold (reading a title card/a bullet-comment lingering/a closing freeze)
   or a real dead stretch (nothing on screen to read and it's still sitting there). Deliberate hold = don't report or 💡, real dead stretch = ⚡
⑦ Sound-effect hits (see the onset table below): check whether the picture has a matching event at each sound-effect time
⑧ Composition: obvious imbalance, large meaningless empty areas, important elements hugging the edge or squeezed into a corner"""

SEVERITY_RULE = """\
Severity has three levels:
- ⚠️ Critical: must be fixed before delivery (black frames, typos, clipped text, elements stuck on top of each other, obviously broken images)
- ⚡ Important: viewing experience clearly damaged (hard-cut feel, hero breaks, dead stretches over 3 seconds, obviously unbalanced composition)
- 💡 Suggestion: nice-to-have improvements"""


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r


def probe(video: Path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-show_entries", "stream=codec_type", "-of", "json", str(video)])
    info = json.loads(r.stdout)
    duration = float(info["format"]["duration"])
    has_audio = any(s.get("codec_type") == "audio" for s in info.get("streams", []))
    return duration, has_audio


def detect_audio_onsets(video: Path, noise_db=-45, min_silence=0.3):
    """Infer sound-effect onsets from silencedetect. Returns a list of seconds in the original."""
    r = subprocess.run(
        ["ffmpeg", "-i", str(video), "-af",
         f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-"],
        capture_output=True, text=True)
    onsets = [round(float(m), 1) for m in
              re.findall(r"silence_end:\s*([\d.]+)", r.stderr)]
    # pad with 0 when the opening isn't silent (sound from the very start)
    starts = re.findall(r"silence_start:\s*([\d.-]+)", r.stderr)
    if starts and float(starts[0]) > min_silence:
        onsets.insert(0, 0.0)
    return onsets


def detect_static_segments(video: Path, noise=0.001, min_dur=3.0):
    """freezedetect finds intervals of ≥min_dur seconds completely still. Returns [(start,end)] in original seconds."""
    r = subprocess.run(
        ["ffmpeg", "-i", str(video), "-vf",
         f"freezedetect=n={noise}:d={min_dur}", "-f", "null", "-"],
        capture_output=True, text=True)
    starts = re.findall(r"freeze_start:\s*([\d.]+)", r.stderr)
    durs = re.findall(r"freeze_duration:\s*([\d.]+)", r.stderr)
    return [(round(float(s), 1), round(float(s) + float(d), 1))
            for s, d in zip(starts, durs)]


def compress(src: Path, dst: Path, ss=None, t=None, width=1280, fps=15, crf=28):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    if t is not None:
        cmd += ["-t", str(t)]
    cmd += ["-i", str(src), "-vf", f"scale={width}:-2,fps={fps}",
            "-c:v", "libx264", "-crf", str(crf), "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-an", str(dst)]
    run(cmd)


def fmt_ts(sec: float) -> str:
    return f"{int(sec) // 60}:{int(sec) % 60:02d}"


def ask_reviewer(prompt, video_path: Path | None = None):
    """Run the user-configured local review command (DSTACK_REVIEW_COMMAND)."""
    import shlex
    tpl = os.environ.get("DSTACK_REVIEW_COMMAND")
    if not tpl:
        raise RuntimeError("DSTACK_REVIEW_COMMAND is not set")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        pf = f.name
    cmd = tpl.replace("{prompt_file}", shlex.quote(pf)).replace("{video}", shlex.quote(str(video_path)) if video_path else "''")
    try:
        r = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=900)
    finally:
        os.unlink(pf)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"review command failed (exit {r.returncode}): {r.stderr[-500:]}")
    return r.stdout.strip(), {}


def contact_sheet(src: Path, dst: Path, ss: float, t: float, cols=4, rows=3):
    """A grid of evenly spaced frames from [ss, ss+t] as one PNG, for looking at by eye."""
    n = cols * rows
    fps = max(n / max(t, 0.1), 0.01)
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", str(src),
         "-vf", f"fps={fps:.4f},scale=480:-2,tile={cols}x{rows}:padding=4:color=white",
         "-frames:v", "1", str(dst)])


def segment_prompt(seg_start, seg_end, duration, context_text, onsets_in_seg,
                   statics_in_seg):
    p = [f"You are a QC reviewer for finished animations. Your job is to find faults strictly, not to praise the film.",
         f"This video is one clip of a finished animation {fmt_ts(duration)} long in total, "
         f"corresponding to {fmt_ts(seg_start)}–{fmt_ts(seg_end)} in the original. "
         f"Second t within the clip = second {fmt_ts(seg_start)}+t of the original; always use original times (min:sec) in the report."]
    if context_text:
        p.append("Below is the director's script for the whole film (review context, for judging narrative intent and what should appear):\n"
                 "<director_script>\n" + context_text + "\n</director_script>")
    p.append("Check the following checklist item by item, reporting only findings within this clip:\n" + CHECKLIST)
    if statics_in_seg:
        ts = ", ".join(f"{fmt_ts(a)}–{fmt_ts(b)} ({b - a:.1f}s)" for a, b in statics_in_seg)
        p.append(f"Objective static-segment table for ⑥ (within this segment, original time): {ts}. Judge each one: deliberate hold or real dead stretch.")
    else:
        p.append("No static segments of ≥3 seconds in this clip; for ⑥ just write \"none found\".")
    if onsets_in_seg:
        ts = ", ".join(f"{fmt_ts(t)}({t}s)" for t in onsets_in_seg)
        p.append(f"Onset table for ⑦ (original times at which sound effects actually occur in this segment): {ts}. "
                 f"You can't hear the sound; just check whether the picture at each of these times has an event worth a sound effect "
                 f"(transition/title card landing/impact/element appearing). A time with no matching event = a sound effect hitting nothing, which must be reported.")
    else:
        p.append("No sound-effect onsets detected in this clip, so skip ⑦; but if this segment has a strong visual event "
                 "(impact/title card/transition) with no sound effect covering it, you can raise it under ⑦ with 💡.")
    p.append(SEVERITY_RULE)
    p.append("Output format: markdown. Go item by item through ①-⑧, with a list under each item:\n"
             "- [original min:sec] severity emoji, specific description\n"
             "If an item has no problems, write \"none found\". Report only what you actually saw; mark anything uncertain as \"uncertain\"; don't make things up.")
    return "\n\n".join(p)


def global_prompt(duration, context_text):
    p = ["You are a QC reviewer for finished animations. This is a low-res version of a whole finished animation (compressed for review; low image quality is normal, "
         "don't report image quality/sharpness problems), " + fmt_ts(duration) + " long in total."]
    if context_text:
        p.append("Director's script:\n<director_script>\n" + context_text + "\n</director_script>")
    p.append("Do only three things (detail problems are handled by the segment reviews; you don't need to worry about them):\n"
             "A. Narrative continuity: watching from start to finish, at which times are there PowerPoint-style hard cuts (the whole frame changes abruptly with no transition)?\n"
             "B. hero/subject continuity: at which changes does the subject element that runs through the whole film break, disappear or jump?\n"
             "C. Overall pacing: which intervals drag (no new information for a long time), and which are rushed?\n\n"
             + SEVERITY_RULE +
             "\n\nOutput markdown, with three sections A/B/C, findings carrying [min:sec] times. If there are no problems, write \"none found\". Don't make things up.")
    return "\n\n".join(p)


def synthesis_prompt(duration, seg_reports, global_report):
    parts = ["You are the editor-in-chief of review reports. Below are the raw records of the segment reviews + the whole-film review of the same " + fmt_ts(duration) +
             " finished animation; merge them into the body of one final report.",
             "Requirements:\n"
             "1. Organize item by item along checklist ①-⑧, listing findings under each item in time order: - [min:sec] severity description\n"
             "2. Merge the same problem reported repeatedly by several segments into one entry; where segment and whole-film reviews contradict each other, keep both views and mark it \"uncertain\"\n"
             "3. Keep each finding's time and severity emoji (⚠️/⚡/💡); don't add findings that aren't in the raw records\n"
             "4. Start with a stats line \"Total problems: ⚠️x ⚡y 💡z\" and an overall verdict of no more than three sentences\n"
             "5. Output only the markdown body of the report, no pleasantries",
             "<whole_film_review>\n" + global_report + "\n</whole_film_review>"]
    for (s, e, text) in seg_reports:
        parts.append(f"<segment_review original {fmt_ts(s)}–{fmt_ts(e)}>\n{text}\n</segment_review>")
    return "\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Video QC review: objective local checks + contact sheets; optional local review-command hook")
    ap.add_argument("--video", required=True, help="path to the finished film (mp4)")
    ap.add_argument("--context", help="path to the director's script/scene notes md (optional, used as review context)")
    ap.add_argument("--segment-len", type=int, default=60, help="segment length in seconds (default 60)")
    ap.add_argument("--reviewer", choices=["none", "command"], default=os.environ.get("DSTACK_REVIEWER", "none"),
                    help="none (default, fully local) | command (run DSTACK_REVIEW_COMMAND)")
    ap.add_argument("--output", "-o", help="report path (default: <video-name>-review.md in the video's folder)")
    args = ap.parse_args()

    video = Path(args.video).resolve()
    if not video.exists():
        sys.exit(f"Error: video does not exist {video}")
    if args.reviewer == "command" and not os.environ.get("DSTACK_REVIEW_COMMAND"):
        sys.exit("Error: --reviewer command needs DSTACK_REVIEW_COMMAND (see the header of this script). "
                 "dstack ships no cloud reviewer; run without --reviewer for the local report.")
    out_path = Path(args.output) if args.output else video.parent / f"{video.stem}-review.md"
    sheet_dir = out_path.parent / f"{video.stem}-review-sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)

    context_text = ""
    if args.context:
        ctx = Path(args.context)
        if not ctx.exists():
            sys.exit(f"Error: context file does not exist {ctx}")
        context_text = ctx.read_text(encoding="utf-8")[:12000]

    duration, has_audio = probe(video)
    log(f"Video {fmt_ts(duration)}, audio track={'yes' if has_audio else 'no'}")
    onsets = detect_audio_onsets(video) if has_audio else []
    raw_statics = detect_static_segments(video)
    statics = []
    for a, b in raw_statics:
        if statics and a - statics[-1][1] < 0.2:
            statics[-1] = (statics[-1][0], b)
        else:
            statics.append((a, b))
    log(f"Onsets: {len(onsets)}; static segments (>=3s): {len(statics)}")

    bounds, t0 = [], 0.0
    while t0 < duration - 0.05:
        bounds.append((t0, min(t0 + args.segment_len, duration)))
        t0 += args.segment_len

    sheets, seg_reports, failures, global_report = [], [], [], ""
    with tempfile.TemporaryDirectory(prefix="dstack-review-") as tmp:
        tmp = Path(tmp)
        for i, (s, e) in enumerate(bounds, 1):
            sheet = sheet_dir / f"seg{i:02d}-{int(s)}-{int(e)}s.png"
            contact_sheet(video, sheet, s, e - s)
            sheets.append((s, e, sheet))
            if args.reviewer == "command":
                seg = tmp / f"seg{i}.mp4"
                compress(video, seg, ss=s, t=e - s)
                try:
                    text, _ = ask_reviewer(segment_prompt(s, e, duration, context_text,
                                                          [t for t in onsets if s <= t < e],
                                                          [(a, b) for a, b in statics if a < e and b > s]), seg)
                    seg_reports.append((s, e, text))
                except RuntimeError as err:
                    failures.append((s, e, str(err)))
        if args.reviewer == "command":
            full = tmp / "full.mp4"
            compress(video, full, width=960, fps=10, crf=30)
            try:
                global_report, _ = ask_reviewer(global_prompt(duration, context_text), full)
            except RuntimeError as err:
                failures.append((0, duration, f"whole-film pass: {err}"))

    lines = [f"# {video.name} · review report", "",
             f"> Reviewed at {time.strftime('%Y-%m-%d %H:%M')} | length {fmt_ts(duration)} | reviewer: "
             f"{'local command' if args.reviewer == 'command' else 'none (local checks + contact sheets only; nothing was sent anywhere)'}", ""]
    if args.reviewer == "command" and (seg_reports or global_report):
        try:
            body, _ = ask_reviewer(synthesis_prompt(duration, seg_reports, global_report or "(no whole-film pass)"))
        except RuntimeError as err:
            body = f"> Synthesis failed ({err}); raw records follow.\n\n" + (global_report or "") + "\n\n" + \
                "\n\n".join(f"## Segment {fmt_ts(s)}–{fmt_ts(e)}\n{t}" for s, e, t in seg_reports)
        lines.append(body)
    else:
        lines.append("## Look at the contact sheets against this checklist\n\n" + CHECKLIST + "\n\n" + SEVERITY_RULE)
    if failures:
        lines.append("\n> ⚠️ Not covered by the reviewer: " + "; ".join(f"{fmt_ts(s)}–{fmt_ts(e)} ({m[:100]})" for s, e, m in failures))
    lines.append("\n## Contact sheets\n")
    for s, e, sheet in sheets:
        lines.append(f"- {fmt_ts(s)}–{fmt_ts(e)}: {sheet}")
    lines.append("\n## Objective detection data (ffmpeg, not model judgment)\n")
    lines.append("Static segments ≥3s: " + (", ".join(f"{fmt_ts(a)}–{fmt_ts(b)} ({b - a:.1f}s)" for a, b in statics) or "none"))
    lines.append("\nSound-effect onsets: " + (", ".join(fmt_ts(t) for t in onsets) or "none/no audio track"))
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"Report written to: {out_path}")
    print(out_path)


if __name__ == "__main__":
    main()
