"""ElevenLabs integration (TTS provider + gen-audio) with a mocked HTTP layer.

Each test runs one scenario of el_harness.mjs, which replaces fetch, so no request leaves the box.
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
KEY = "sk_testSECRETkey0123456789abcdef"
pytestmark = pytest.mark.skipif(not (shutil.which("node") and shutil.which("ffmpeg")), reason="node/ffmpeg not installed")


def run(scenario):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("DSTACK_", "ELEVENLABS_"))}
    r = subprocess.run(["node", str(HERE / "el_harness.mjs"), scenario], capture_output=True, text=True, env=env, timeout=120)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip().splitlines()[-1]), r


def test_provider_selection_defaults_off():
    out, _ = run("selection")
    assert out["defaultTts"] == "silent"
    assert out["envTts"] == "elevenlabs"
    assert out["cliTts"] == "silent"  # --tts beats the env var
    assert out["unknown"] == "rejected"
    assert out["defaultAudio"] == "none"
    assert out["envAudio"] == "elevenlabs"
    assert out["host"] == "https://api.elevenlabs.io"
    assert out["defaults"] == {"voice": "JBFqnCBsd6RMkjVDRZzb", "model": "eleven_multilingual_v2", "format": "mp3_44100_128"}


def test_missing_key_falls_back_with_one_warning_and_no_request():
    out, r = run("missing-key")
    assert out["providers"] == ["silent", "silent"]
    assert out["fallback"] == "no API key"
    assert out["duration"] is True
    assert out["calls"] == 0 and out["genCalls"] == 0
    assert out["gen"] == "skipped"
    assert r.stderr.count("[tts] WARNING") == 1


def test_request_shape():
    out, _ = run("request-shape")
    assert out["tts"] == {"provider": "elevenlabs", "wordsEstimated": False, "words": ["Rain", "on", "the", "fields."]}
    tts, sfx, music = out["calls"]
    for c in out["calls"]:
        assert c["url"].startswith("https://api.elevenlabs.io/v1/")
        assert c["method"] == "POST" and c["key"] is True
        assert c["url"].endswith("?output_format=mp3_44100_128")
    assert "/v1/text-to-speech/AbCdEfGhIjKlMnOpQrSt/with-timestamps" in tts["url"]
    assert tts["body"] == {"text": "Rain on the fields.", "model_id": "eleven_flash_v2_5", "voice_settings": {"speed": 1.1}}
    assert "/v1/sound-generation" in sfx["url"]
    # prompt and length come from references/sfx-library.md
    assert sfx["body"] == {"text": "crisp modern interface click", "loop": False, "prompt_influence": 0.3,
                           "model_id": "eleven_text_to_sound_v2", "duration_seconds": 0.5}
    assert "/v1/music" in music["url"]
    assert music["body"]["music_length_ms"] == 30000
    assert music["body"]["force_instrumental"] is True
    assert music["body"]["model_id"] == "music_v1"
    assert out["sfxFile"] and out["bgmFile"]


def test_cache_hit_makes_no_second_request():
    out, _ = run("cache")
    # generated, --force same prompt -> cache, existing file kept, new prompt -> generated
    assert out["sfx"] == ["generated", "cached", "kept", "generated"]
    assert out["ttsSecondMeasured"] is True  # cached TTS keeps its alignment
    assert out["calls"] == 3  # 2 sfx + 1 tts


def test_key_never_in_output_logs_or_files():
    out, r = run("key-hygiene")
    assert out.pop("key") == KEY
    text = r.stderr + json.dumps(out)
    assert KEY not in text
    assert "****" in r.stderr  # the echoed key was masked, not dropped silently
    assert out["provider"] == "silent" and out["fallbackMasked"]
    assert out["gen"] == "error"
    assert out["maskSample"] == "key=**** xi-api-key: ****"
    assert out["keyOnDisk"] is False
    assert out["fileKey"] == "file"
    assert out["repoKey"] is None  # key files inside the repo are refused
    assert out["badEndpoint"] == "refused"


def test_no_other_elevenlabs_host_in_code():
    root = HERE.parents[1]
    import re
    hosts = set()
    for p in list((root / "scripts").rglob("*.mjs")) + list((root / "scripts").rglob("*.sh")):
        hosts.update(re.findall(r"\b(?:[\w-]+\.)+elevenlabs\.io", p.read_text(errors="ignore")))
    assert hosts == {"api.elevenlabs.io"}
