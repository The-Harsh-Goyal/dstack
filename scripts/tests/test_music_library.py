"""Local background-music library (scripts/audio/music-library.mjs + gen-audio `local` provider).

Fixture audio is tiny ffmpeg sine tones generated in tmp; no real tracks are in the repo.
Every node call runs with a throwing fetch under tools/egress/egress.cjs, and the tests assert
that no DNS lookup or socket connect happened (render-time music selection is offline).
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KEY = "sk_testSECRETkey0123456789abcdef"
pytestmark = pytest.mark.skipif(not (shutil.which("node") and shutil.which("ffmpeg")), reason="node/ffmpeg not installed")


def sine(path, freq=440, seconds=2):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={seconds}",
                    "-ac", "2", "-q:a", "9", str(path)], check=True)


def entry(file, moods, commercial=True, attribution="", **kw):
    e = {"file": file, "moods": moods, "duration": 2.0, "title": file.split(".")[0], "artist": "Test Tone",
         "source_url": f"https://example.org/{file}", "licence": {"name": "CC0 1.0", "url": "https://creativecommons.org/publicdomain/zero/1.0/"},
         "attribution": attribution, "commercial": commercial, "fetched": "2026-10-28"}
    e.update(kw)
    return e


@pytest.fixture
def library(tmp_path):
    lib = tmp_path / "music"
    lib.mkdir()
    for i, name in enumerate(["a-tech.mp3", "b-tech.mp3", "c-tech.wav", "calm.mp3", "nc.mp3", "stray.mp3"]):
        sine(lib / name, 220 + 110 * i)
    tracks = [entry("a-tech.mp3", ["tech"]), entry("b-tech.mp3", ["Tech", "ad"], attribution='"B" by Test Tone, CC BY 4.0'),
              entry("c-tech.wav", ["tech"]), entry("calm.mp3", ["calm", "tutorial"]), entry("nc.mp3", ["lofi"], commercial=False)]
    (lib / "manifest.json").write_text(json.dumps({"version": 1, "tracks": tracks}))
    return lib


def node(tmp_path, mode, *args, **env_over):
    egress = tmp_path / "egress"
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DSTACK_", "ELEVENLABS_", "HUASHU_"))}
    env.update(DSTACK_HOME=str(tmp_path / "home"), DSTACK_AUDIO_DIR=str(tmp_path / "audio"), EGRESS_DIR=str(egress))
    env.update({k: v for k, v in env_over.items() if v is not None})
    r = subprocess.run(["node", "--require", str(ROOT / "tools/egress/egress.cjs"), str(HERE / "music_harness.mjs"), mode, *args],
                       capture_output=True, text=True, env=env, timeout=60)
    assert r.returncode == 0, r.stderr
    log = (egress / "node.log").read_text() if (egress / "node.log").exists() else ""
    assert " dns " not in log and " connect " not in log, log
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_validation_lists_only_complete_entries(tmp_path, library):
    m = json.loads((library / "manifest.json").read_text())
    m["tracks"] += [entry("missing.mp3", ["tech"]), {"file": "calm.mp3", "moods": []},
                    entry("../escape.mp3", ["tech"]), entry("calm.mp3", ["x"], commercial="yes", fetched="today")]
    (library / "manifest.json").write_text(json.dumps(m))
    out = node(tmp_path, "load", DSTACK_MUSIC_DIR=str(library))
    assert out["tracks"] == ["a-tech.mp3", "b-tech.mp3", "c-tech.wav", "calm.mp3", "nc.mp3"]
    errs = " | ".join(out["errors"])
    assert "missing.mp3): file not found" in errs
    assert "moods must be a non-empty list" in errs and "source_url missing" in errs and "licence.name missing" in errs
    assert "inside the library folder" in errs
    assert "commercial must be true or false" in errs and "fetched must be YYYY-MM-DD" in errs
    assert out["unlisted"] == ["stray.mp3"]


def test_pick_is_deterministic_and_seedable(tmp_path, library):
    picks = {node(tmp_path, "pick", "tech", "", DSTACK_MUSIC_DIR=str(library))["file"] for _ in range(3)}
    assert len(picks) == 1
    seeded = {s: node(tmp_path, "pick", "TECH", s, DSTACK_MUSIC_DIR=str(library))["file"] for s in ["1", "2", "3", "4", "5", "6"]}
    assert set(seeded.values()) <= {"a-tech.mp3", "b-tech.mp3", "c-tech.wav"}
    assert len(set(seeded.values())) > 1  # the seed changes the pick
    assert node(tmp_path, "pick", "tech", "4", DSTACK_MUSIC_DIR=str(library))["file"] == seeded["4"]


def test_unlisted_and_noncommercial_tracks_are_refused(tmp_path, library):
    out = node(tmp_path, "pick", "lofi", "", DSTACK_MUSIC_DIR=str(library))
    assert out["file"] is None and "DSTACK_MUSIC_ALLOW_NONCOMMERCIAL=1" in out["reason"]
    assert node(tmp_path, "pick", "lofi", "", DSTACK_MUSIC_DIR=str(library), DSTACK_MUSIC_ALLOW_NONCOMMERCIAL="1")["file"] == "nc.mp3"
    (library / "manifest.json").unlink()  # files without manifest entries are never used
    out = node(tmp_path, "pick", "tech", "", DSTACK_MUSIC_DIR=str(library))
    assert out["file"] is None and 'no valid track tagged "tech"' in out["reason"]


def test_local_provider_copies_track_and_records_licence(tmp_path, library):
    out = node(tmp_path, "gen", "bgm", "ad", DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="local")
    assert out["status"] == "local" and out["track"] == "b-tech.mp3" and out["fetchCalls"] == 0
    target = tmp_path / "audio" / "bgm-ad.mp3"
    assert target.read_bytes() == (library / "b-tech.mp3").read_bytes()
    prov = json.loads(Path(str(target) + ".provenance.json").read_text())
    assert prov["provider"] == "local" and prov["licence"]["name"] == "CC0 1.0" and prov["source_url"].startswith("https://")
    assert prov["credit"] == 'Attribution required: "B" by Test Tone, CC BY 4.0'
    assert any(l.startswith("Attribution required:") for l in out["logs"])
    # a non-mp3 track is transcoded locally; no-attribution licences say so
    out = node(tmp_path, "gen", "bgm", "calm", DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="local")
    assert out["status"] == "local" and any(l.startswith("No attribution required (CC0 1.0") for l in out["logs"])
    out = node(tmp_path, "gen", "bgm", "tech", "--seed", "x", "--force", DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="local")
    assert out["status"] == "local"
    assert subprocess.run(["ffprobe", "-v", "error", str(tmp_path / "audio" / "bgm-tech.mp3")]).returncode == 0
    # SFX and unknown moods: nothing written, no error
    assert node(tmp_path, "gen", "sfx", "ui/click", DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="local")["status"] == "skipped"
    assert node(tmp_path, "gen", "bgm", "jazz", DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="local")["status"] == "skipped"


@pytest.mark.parametrize("why,env", [
    ("no key", {}),
    ("network error", {"ELEVENLABS_API_KEY": KEY}),
    ("free plan 402", {"ELEVENLABS_API_KEY": KEY, "HARNESS_FETCH": "402"}),
])
def test_elevenlabs_bgm_falls_back_to_local(tmp_path, library, why, env):
    out = node(tmp_path, "gen", "bgm", "tutorial", DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="elevenlabs", **env)
    assert out["status"] == "local" and out["track"] == "calm.mp3", out
    assert out["fallback"]
    assert KEY not in json.dumps(out)
    assert (tmp_path / "audio" / "bgm-tutorial.mp3").exists()


def test_elevenlabs_bgm_without_library_stays_silent(tmp_path):
    out = node(tmp_path, "gen", "bgm", "tutorial", DSTACK_MUSIC_DIR=str(tmp_path / "nolib"), DSTACK_AUDIO_PROVIDER="elevenlabs")
    assert out["status"] == "skipped" and not (tmp_path / "audio" / "bgm-tutorial.mp3").exists()
    out = node(tmp_path, "gen", "bgm", "tutorial", DSTACK_MUSIC_DIR=str(tmp_path / "nolib"), DSTACK_AUDIO_PROVIDER="elevenlabs", ELEVENLABS_API_KEY=KEY)
    assert out["status"] == "error" and not (tmp_path / "audio" / "bgm-tutorial.mp3").exists()


def test_add_music_uses_local_library_and_writes_credits(tmp_path, library):
    video = tmp_path / "v.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=64x64:d=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video)], check=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DSTACK_", "ELEVENLABS_", "HUASHU_"))}
    env.update(DSTACK_HOME=str(tmp_path / "home"), DSTACK_AUDIO_DIR=str(tmp_path / "audio"), DSTACK_MUSIC_DIR=str(library), DSTACK_AUDIO_PROVIDER="local")
    r = subprocess.run(["bash", str(ROOT / "scripts/add-music.sh"), str(video), "--mood=ad"], capture_output=True, text=True, env=env, timeout=60)
    assert r.returncode == 0, r.stderr
    out = tmp_path / "v-bgm.mp4"
    streams = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.split()
    assert streams == ["video", "audio"]
    assert (tmp_path / "v-bgm.credits.txt").read_text().strip() == 'Attribution required: "B" by Test Tone, CC BY 4.0'
    assert "♪ Attribution required" in r.stdout


def test_library_inside_repo_is_refused(tmp_path):
    out = node(tmp_path, "load", DSTACK_MUSIC_DIR=str(ROOT / "music"))
    assert out["tracks"] == [] and "inside the dstack folder" in out["errors"][0]


@pytest.mark.parametrize("case,expect,rc", [
    ("empty", "empty: no library", 0),
    ("good", "5 track(s), 4 commercial-ok", 0),
    ("broken", "✗ 0 track(s), 0 commercial-ok", 1),
])
def test_doctor_validates_manifest(tmp_path, library, case, expect, rc):
    if case == "empty":
        d = tmp_path / "none"
    else:
        d = library
        if case == "broken":
            (library / "manifest.json").write_text("{not json")
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DSTACK_", "ELEVENLABS_", "HUASHU_"))}
    env.update(DSTACK_HOME=str(tmp_path / "home"), DSTACK_MUSIC_DIR=str(d))
    r = subprocess.run(["bash", str(ROOT / "tools/doctor.sh")], capture_output=True, text=True, env=env, timeout=120)
    assert expect in r.stdout, r.stdout
    if rc:
        assert r.returncode == 1 and "not valid JSON" in r.stdout


def test_no_audio_files_tracked_and_gitignore_guards_them():
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n")
    assert not [f for f in tracked if f.lower().endswith((".mp3", ".wav", ".ogg", ".oga", ".opus", ".flac", ".m4a", ".aac"))]
    r = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "x.mp3", "a/b.wav", "music/manifest.json", "y.flac"], capture_output=True, text=True)
    assert len(r.stdout.split()) == 4
