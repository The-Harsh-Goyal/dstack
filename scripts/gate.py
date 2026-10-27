#!/usr/bin/env python3
"""gate.py: the three-direction gate when no human is there to choose (dstack).

The gate normally stops and waits for the user's choice. In an unattended run, or when the
brief explicitly asks for finished output, don't block: pick the strongest direction as a
DRAFT default, record it, carry on, and flag it at delivery so the user can still choose.

  python3 scripts/gate.py default <project> --pick dir-1 --reason "unattended; brief asks for finals" [--shown a.png,b.png]
  python3 scripts/gate.py status  <project>

`default` writes <project>/direction-approved.md (status: auto-default) and appends a line to
<project>/gate-log.md. It never overwrites a direction-approved.md that holds a real user choice.
"""
import argparse
import sys
import time
from pathlib import Path

AUTO = 'status: auto-default (no human present)'


def status(project: Path):
    f = project / 'direction-approved.md'
    if not f.exists():
        return 'missing'
    return 'auto-default' if AUTO in f.read_text(encoding='utf-8') else 'approved'


def cmd_default(a):
    project = Path(a.project).resolve()
    if not project.is_dir():
        sys.exit(f'Not a directory: {project}')
    st = status(project)
    if st == 'approved':
        print(f'direction-approved.md already holds a user choice; not touched ({project / "direction-approved.md"})')
        return 1
    shown = [s for s in (a.shown or '').split(',') if s] or \
        sorted(str(p.relative_to(project)) for p in project.glob('design-demos/*.png'))
    stamp = time.strftime('%Y-%m-%d %H:%M %Z')
    body = '\n'.join([
        '# Direction approval', '', AUTO, f'- When: {stamp}', f'- Picked by the agent as a draft default: {a.pick}',
        f'- Why no human choice: {a.reason}', '- Shown / produced:', *[f'  - {s}' for s in shown or ['(none listed)']], '',
        "User's verbatim choice: PENDING. Deliver the result as a draft and ask which direction they want;",
        'if they pick another, rebuild from that direction card. Replace this file with their words when they answer.', ''])
    (project / 'direction-approved.md').write_text(body, encoding='utf-8')
    with (project / 'gate-log.md').open('a', encoding='utf-8') as fh:
        fh.write(f'- {stamp}: auto-default → {a.pick} ({a.reason})\n')
    print(f'Gate auto-default logged: {a.pick} → {project / "direction-approved.md"} (+ gate-log.md). Flag it as a draft at delivery.')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Three-direction gate helper')
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('default')
    d.add_argument('project')
    d.add_argument('--pick', required=True)
    d.add_argument('--reason', required=True)
    d.add_argument('--shown')
    s = sub.add_parser('status')
    s.add_argument('project')
    a = ap.parse_args(argv)
    if a.cmd == 'status':
        print(status(Path(a.project)))
        return 0
    return cmd_default(a)


if __name__ == '__main__':
    sys.exit(main())
