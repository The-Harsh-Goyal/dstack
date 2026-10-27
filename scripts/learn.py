#!/usr/bin/env python3
"""
learn.py: help dstack understand this user a little better with every project.

Experience has two layers:
  shipped with the skill  references/experience.md: general findings (reproduced in two projects or measured), true for everyone;
                 edited by hand in the repo, this command never writes it.
  private to this machine  ~/.dstack/experience.md (location changeable via DSTACK_HOME; HUASHU_DESIGN_HOME is still honoured): this machine's user:
                 their own words, their taste, observations seen in only one project. Never shipped.

Usage:
  python3 scripts/learn.py [topic…]            before starting: read this user's preferences + experience related to the topics
  python3 scripts/learn.py add "…" --kind preference|observed|verified|superseded \
          --topics deck,color --evidence "own words/project/file/measurement" [--do "what to do next time"] [--project name]
  python3 scripts/learn.py harvest <project-dir>   after finishing: list what in the project can serve as evidence, and the criteria for whether to record it
  python3 scripts/learn.py status
  python3 scripts/learn.py -- status            when a topic word happens to be add/harvest/status, separate it with --

Ported from huashu-motion's `om learn` (same author, MIT), with the dependency on studio comments removed.
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

KINDS = {
    'preference': 'said by the user in person; must quote their own words; holds for this user until they change their mind',
    'observed': 'seen in only one project; a lead, not a rule',
    'verified': 'reproduced in two or more projects, or measured; the general ones eventually go into references/experience.md',
    'superseded': 'no longer holds; keep the entry and state clearly what replaced it',
}

SKILL_ROOT = Path(__file__).resolve().parent.parent
SHIPPED = SKILL_ROOT / 'references' / 'experience.md'

HEAD = """# Local experience (dstack)

What the projects on this machine have taught. Written by `learn.py add`, and can also be edited by hand: if an entry is wrong, fix it in place;
if it no longer holds, change kind to superseded and state the reason. Not shipped with the skill.
"""


def home() -> Path:
    return Path(os.environ.get('DSTACK_HOME') or os.environ.get('HUASHU_DESIGN_HOME') or Path.home() / '.dstack')


def local_file() -> Path:
    return home() / 'experience.md'


class LearnError(Exception):
    pass


def entries(path: Path, layer: str):
    """Each "## …" heading in the markdown file plus its body is one entry."""
    if not path.exists():
        return []
    out = []
    for block in re.split(r'\n(?=## )', path.read_text(encoding='utf-8')):
        if not block.startswith('## '):
            continue
        head = block.split('\n', 1)[0][3:].strip()
        m = re.search(r'·\s*(preference|observed|verified|superseded)\b', head)   # also accepted when a hand edit drops the trailing "·"
        kind = m.group(1) if m else ('shipped' if layer == 'shipped' else 'observed')
        t = re.search(r'topics?:\s*([^\n·]+)', head, re.I)
        tags = [x for x in re.split(r'[,，\s]+', t.group(1) if t else '') if x]
        idm = re.match(r'(L\d+)', head)
        out.append({'layer': layer, 'head': head, 'kind': kind, 'tags': tags,
                    'body': block.strip(), 'id': idm.group(1) if idm else None})
    return out


def recall(topics):
    want = [t.lower() for t in topics]

    def match(e):
        return not want or any(t in [x.lower() for x in e['tags']] or t in e['body'].lower() for t in want)

    local = entries(local_file(), 'local')
    shipped = entries(SHIPPED, 'shipped')
    prefs = [e for e in local if e['kind'] == 'preference']
    rest = [e for e in local if e['kind'] not in ('preference', 'superseded') and match(e)] + \
           [e for e in shipped if match(e)]
    on = f' ({", ".join(want)})' if want else ''
    parts = []
    if prefs:
        parts.append(f'## This user\'s preferences ({len(prefs)} entries): their own words, valid until they change their mind. '
                     f'Note: preferences have a scope; one written as only for a certain kind of material must not spill over into a default for every design\n\n'
                     + '\n\n'.join(e['body'] for e in prefs))
    else:
        parts.append(f'## This user\'s preferences: nothing recorded yet ({local_file()})')
    if rest:
        parts.append(f'## Lessons from past projects{on} ({len(rest)} entries): if the current project conflicts with an entry, the project wins; then fix the entry\n\n'
                     + '\n\n'.join(('[local] ' if e['layer'] == 'local' else '') + e['body'] for e in rest))
    else:
        parts.append(f'## Lessons from past projects{on}: none matching')
    return '\n\n'.join(parts)


def add_entry(kind, topics, text, evidence, todo=None, project=None):
    if kind not in KINDS:
        raise LearnError('learn.py add needs --kind ' + '|'.join(KINDS) + '\n' +
                         '\n'.join(f'  {k:<11} {v}' for k, v in KINDS.items()))
    tags = [x for x in re.split(r'[,，\s]+', topics or '') if x]
    if not tags:
        raise LearnError('learn.py add needs --topics (e.g. deck,color,direction), otherwise it can\'t be found next time')
    if not (text or '').strip():
        raise LearnError('learn.py add needs the finding written as text: learn.py add "…" --kind … --topics … --evidence …')
    if not (evidence or '').strip():
        raise LearnError('learn.py add needs --evidence: own words, project and file, measurement results; an entry nobody can check is just hearsay')
    if kind == 'preference' and not re.search(r'[「“"]', text):
        raise LearnError('preference must quote the user\'s own words: wrap them in 「…」 or "…"')
    f = local_file()
    f.parent.mkdir(parents=True, exist_ok=True)
    prev = f.read_text(encoding='utf-8') if f.exists() else HEAD
    n = 1 + max([0] + [int(e['id'][1:]) for e in entries(f, 'local') if e['id']])
    block = [f'## L{n} · {date.today().isoformat()} · {kind} · topics: {", ".join(tags)}', '',
             f'- {"Own words" if kind == "preference" else "Finding"}: {text.strip()}']
    if todo:
        block.append(f'- Next time: {todo.strip()}')
    block.append(f'- Evidence: {evidence.strip()}' + (f' ({project})' if project else ''))
    f.write_text(prev.rstrip() + '\n\n' + '\n'.join(block) + '\n', encoding='utf-8')
    return f'Recorded  L{n} → {f}'


def harvest(project: Path):
    if not project.is_dir():
        raise LearnError(f'Not a directory: {project}')
    lines = [f'Harvest  {project}']
    approved = project / 'direction-approved.md'
    if approved.exists():
        lines += ['', 'direction-approved.md (what they chose among the three directions and how they said it; the most direct evidence of taste):',
                  approved.read_text(encoding='utf-8').strip()[:3000]]
    directions = project / 'directions.md'
    if directions.exists():
        lines += ['', f'directions.md is at: {directions} (direction cards; compare against their choice to see which logic and which intensity they lean toward, not just which color)']
    demos = sorted((project / 'design-demos').glob('dir-*.html')) if (project / 'design-demos').is_dir() else []
    if demos:
        lines.append(f'design-demos: {len(demos)} full directions' + (' (plus thumbnails in thumbs.html)' if (project / 'design-demos' / 'thumbs.html').exists() else ''))
    ledger = home() / 'ledger.jsonl'
    if ledger.exists():
        root = project.resolve()

        def inside(x):
            try:
                return bool(x) and Path(x).resolve().is_relative_to(root)
            except (OSError, ValueError):
                return False
        # a row belongs to this project if its project_dir or its file is inside the project folder
        # (older rows stored the delivered file's own folder, e.g. <project>/out)
        mine = [r for r in (json.loads(l) for l in ledger.read_text(encoding='utf-8').splitlines() if l.strip())
                if inside(r.get('project_dir')) or inside(r.get('file'))]
        lines.append(f'Look ledger: {len(mine)} entries for this project' + ('' if mine else '. Delivered but not logged? Run design_lint.py ledger add'))
    lines += ['', 'Now find what they said in the conversation and quote it word for word.', '',
              'Only record it when all three hold: it isn\'t obvious; it saves time or a detour on the next project; this project produced evidence for it. Then, in order:',
              '  1. Does an entry say the opposite? Fix that one first (learn.py lists them; edit the file directly).',
              '  2. Can a tool catch it (a check in design_lint.py)? Change the tool and its tests instead of writing it down.',
              '  3. Otherwise: learn.py add "…" --kind preference|observed --topics … --evidence "…" [--do "…"].',
              '     Their own words are a preference, with the scope stated ("only for their own covers"); what you saw in one project is observed.',
              '  4. Seen in two projects, or measured, and true for anyone (not this user\'s taste)? On the dev machine,',
              '     write it into references/experience.md, which ships with the skill, and merge the stable parts into the reference they belong to.',
              f'Local experience: {local_file()}']
    return '\n'.join(lines)


def status():
    f = local_file()
    local = entries(f, 'local')
    shipped = entries(SHIPPED, 'shipped')
    by = {k: sum(1 for e in local if e['kind'] == k) for k in KINDS}
    s = (f'Local {f}' + (f' ({len(local)} entries: preference {by["preference"]}, observed {by["observed"]}, '
                        f'verified {by["verified"]}, superseded {by["superseded"]})' if f.exists() else ' (none yet)'))
    return s + f'\nShipped with the skill: {len(shipped)} entries, in references/experience.md'


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):   # the Windows console isn't UTF-8 by default
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if argv and argv[0] == '--':
            print(recall(argv[1:]))
        elif argv and argv[0] == 'add':
            p = argparse.ArgumentParser(prog='learn.py add')
            p.add_argument('text')
            p.add_argument('--kind', required=True)
            p.add_argument('--topics', required=True)
            p.add_argument('--evidence', default='')
            p.add_argument('--do', dest='todo')
            p.add_argument('--project')
            a = p.parse_args(argv[1:])
            print(add_entry(a.kind, a.topics, a.text, a.evidence, a.todo, a.project))
        elif argv and argv[0] == 'harvest':
            if len(argv) < 2:
                raise LearnError('Usage: learn.py harvest <project-dir>')
            print(harvest(Path(argv[1])))
        elif argv and argv[0] == 'status':
            print(status())
        else:
            print(recall(argv))
    except LearnError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
