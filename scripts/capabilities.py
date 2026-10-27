#!/usr/bin/env python3
"""
capabilities.py: check what the user actually has, to decide which tier the materials go to (see references/materials.md).

Read-only: checks the skill directory, whether keys exist in the environment variables (only whether they exist, values are never printed), and whether a few commands are present.
Not detecting something doesn't mean it isn't there; if the user says they have it, the user wins.

dstack: a script can't see tools built into the agent runtime (GenerateImage, image_gen, ...), so the agent
declares them: --image-tool NAME (repeatable) or DSTACK_IMAGE_TOOL=NAME[,NAME]. Extra skill folders can be
listed in DSTACK_SKILL_DIRS (os.pathsep-separated); the folder dstack itself sits in is always searched.

Usage: python3 scripts/capabilities.py [--json] [--image-tool GenerateImage]
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

SKILL_DIRS = ['~/.claude/skills', '~/.agents/skills', '~/.codex/skills', '~/.cursor/skills',
              '.claude/skills', '.agents/skills']
IMAGE_SKILLS = ['huashu-gpt-image', 'nano-banana-pro']   # detection only; dstack never installs or calls these
SIBLINGS = {
    'huashu-gpt-image': None,
    'huashu-art-motion': None,
    'huashu-md-html': None,
    'huashu-3djs': None,
    'huashu-flow-diagram': None,
    'huashu-motion': None,
}
IMAGE_SKILL_RE = re.compile(r'(^|[-_])(image|images|img|imagen|nano-banana|dall-?e|flux|midjourney|sdxl|stable-diffusion)([-_]|$)', re.I)
IMAGE_KEYS = ['OPENAI_API_KEY', 'GEMINI_API_KEY']   # only reports presence; this skill has no script that calls an image generation API directly, so having a key doesn't mean image generation works


def skill_dirs(extra=None):
    dirs = list(SKILL_DIRS)
    dirs += [d for d in os.environ.get('DSTACK_SKILL_DIRS', '').split(os.pathsep) if d]
    dirs += [str(d) for d in (extra if extra is not None else [Path(__file__).resolve().parents[2]])]
    return dirs


def is_image_skill(name):
    return name in IMAGE_SKILLS or bool(IMAGE_SKILL_RE.search(name))


def installed_skills(extra=None):
    found = {}
    for d in skill_dirs(extra):
        p = Path(d).expanduser()
        if p.is_dir():
            for s in p.iterdir():
                if (s / 'SKILL.md').exists():
                    found.setdefault(s.name, str(s))
    return found


def detect(image_tools=None, skill_dirs_extra=None, check_playwright=True):
    skills = installed_skills(skill_dirs_extra)
    keys = [k for k in IMAGE_KEYS if os.environ.get(k)]
    image = sorted(s for s in skills if is_image_skill(s))
    declared = list(image_tools or []) + [t.strip() for t in os.environ.get('DSTACK_IMAGE_TOOL', '').split(',') if t.strip()]
    tools = {t: bool(shutil.which(t)) for t in ('node', 'ffmpeg', 'npx')}
    tools['playwright(py)'] = False
    try:
        if not check_playwright:
            raise RuntimeError('skipped')   # having the package isn't enough, chromium must be there too
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            tools['playwright(py)'] = Path(p.chromium.executable_path).exists()
    except Exception:
        pass
    siblings = {s: skills.get(s) for s in SIBLINGS}
    # Tiers aren't a ladder: T0 is always there; image generation (an image generation skill installed) adds T1; sibling skills installed adds T2
    tier = ['T0'] + (['T1'] if image or declared else []) + (['T2'] if any(siblings.values()) else [])
    return {'tier': '+'.join(tier), 'image_skills': image, 'image_tools': declared, 'image_keys': keys,
            'siblings': siblings, 'tools': tools}


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    argv = sys.argv[1:]
    tools_arg = [argv[i + 1] for i, a in enumerate(argv) if a == '--image-tool' and i + 1 < len(argv)]
    r = detect(image_tools=tools_arg)
    if '--json' in argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f'Material tier: {r["tier"]} (T0 everyone has; T1 can generate images; T2 has sibling skills installed. See references/materials.md)')
    found = r['image_skills'] + [f'{t} (runtime tool, declared)' for t in r['image_tools']]
    print('Image generation: ' + (', '.join(found) if found else 'none detected')
          + ('' if found else '. A script can\'t see tools built into your runtime: if you have one (e.g. GenerateImage, image_gen), '
             'rerun with --image-tool <name> (or set DSTACK_IMAGE_TOOL) and you are T1'))
    if r['image_keys'] and not found:
        print(f'  The environment has {", ".join(r["image_keys"])}, but this skill doesn\'t call image generation APIs directly; an image generation skill or a tool built into the runtime is needed')
    have = [s for s, p in r['siblings'].items() if p]
    print('Sibling skills: ' + (', '.join(have) if have else 'none'))
    print('Tools: ' + '  '.join(f'{k} {"✓" if v else "✗"}' for k, v in r['tools'].items()))
    missing = [(s, cmd) for s, cmd in SIBLINGS.items() if cmd and not r['siblings'][s]]
    if missing:
        print('Missing ones don\'t block anything; when relevant to the current task, recommend just one at delivery:')
        for s, cmd in missing:
            print(f'  {s}: {cmd}')
    if not r['tools']['playwright(py)']:
        print('Screenshots and the design check need: pip install playwright pillow && playwright install chromium')
    return 0


if __name__ == '__main__':
    sys.exit(main())
