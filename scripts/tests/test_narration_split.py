"""Subtitle line splitting in assets/narration_stage.jsx (English + Chinese).

The pure helpers between `function visualLen` and `function Subtitles(` are
evaluated in node (no React needed)."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

JSX = Path(__file__).resolve().parents[2] / "assets" / "narration_stage.jsx"
pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="node not installed")


def run(expr):
    src = JSX.read_text(encoding="utf-8")
    a = src.index("  function visualLen")
    b = src.index("  function Subtitles(")
    js = src[a:b] + f"\nprocess.stdout.write(JSON.stringify({expr}));"
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


EN = ("Hi everyone. Today we will explain, in plain English, what a design studio skill "
      "actually does for a busy team; it sketches three directions first!")


def test_english_splits_on_sentence_end():
    lines = run(f"splitChunkToLines({json.dumps('It sketches. Then it ships! Done?')})")
    assert lines == ["It sketches.", "Then it ships!", "Done?"]


def test_english_lines_respect_word_boundaries_and_length():
    lines = run(f"splitChunkToLines({json.dumps(EN)})")
    words = EN.split()
    assert " ".join(lines).split() == words           # nothing lost, no word cut in half
    assert all(len(l) <= 42 for l in lines), lines     # English default: ~42 chars per line
    assert lines[0] == "Hi everyone."


def test_english_prefers_clause_punctuation():
    lines = run(f"splitChunkToLines({json.dumps('First we sketch three directions, then we critique them; finally we ship one.')})")
    assert lines[0].endswith(",")
    assert any(l.endswith(";") for l in lines)


def test_decimal_points_do_not_split():
    lines = run(f"splitChunkToLines({json.dumps('Version 3.5 is out.')})")
    assert lines == ["Version 3.5 is out."]


def test_chinese_behaviour_unchanged():
    # pinned from the upstream implementation before the English path was added
    zh = "大家好，今天我们来聊一聊设计。这个技能会先给出三个方向！"
    assert run(f"splitChunkToLines({json.dumps(zh)})") == ["大家好，", "今天我们来聊一聊设计。", "这个技能会先给出三个方向！"]
    mixed = "我们用 Playwright 渲染 MP4，然后导出 GIF 和 PPTX 文件给团队。"
    assert run(f"splitChunkToLines({json.dumps(mixed)})") == ["我们用 Playwright 渲染 MP4，", "然后导出 GIF 和 PPTX 文件给", "团队。"]


def test_english_karaoke_words_break_after_sentence_and_fit():
    words = [{"text": w} for w in EN.split()]
    lines = run(f"splitWordsToLines({json.dumps(words)}).map(l => l.map(w => w.text).join(' '))")
    assert lines[0] == "Hi everyone."
    assert all(len(l) <= 42 for l in lines), lines
    assert " ".join(lines).split() == EN.split()


def test_join_tokens_adds_spaces_only_between_latin_words():
    assert run("joinTokens(['Hi','everyone.'])") == "Hi everyone."
    assert run("joinTokens(['大','家','好'])") == "大家好"
    assert run("joinTokens(['Hi',',','there'])") == "Hi, there"
