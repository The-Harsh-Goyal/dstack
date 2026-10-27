"""INSTALL_BODY.md is generated from SKILL.md by tools/make_install_body.py: keep it current and absolute."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_install_body_is_up_to_date():
    r = subprocess.run([sys.executable, str(ROOT / 'tools/make_install_body.py'), '--root', '/workspace/dstack', '--check'],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_install_body_paths_are_absolute_and_rules_present():
    text = (ROOT / 'INSTALL_BODY.md').read_text(encoding='utf-8')
    assert text.startswith('Helper files for this skill are in /workspace/dstack/.')
    body = text.replace('still write `$HD`', '')
    assert '$HD' not in body
    assert not re.search(r'(?<![\w/.:-])(references|scripts|assets|demos)/\S', text.split('## Index')[0].replace(
        '("write it into\n   references/experience.md")', ''))
    for must in ('DRAFTS ONLY', 'NO DATA TO CHINA', 'DSTACK_TTS_PROVIDER=silent', 'DSTACK_REVIEWER=none',
                 "No installs without Harsh's OK", 'Cloudflare', 'alchaincyf/huashu-design', 'MIT',
                 'x-article` 2500×1000', 'x-infeed` 1600×900'):
        assert must in text, must
    for p in re.findall(r'/workspace/dstack/[\w./-]+\.(?:py|mjs|js|sh|md)\b', text):
        assert (ROOT / p[len('/workspace/dstack/'):]).exists(), p
