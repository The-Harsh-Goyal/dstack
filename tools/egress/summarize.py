#!/usr/bin/env python3
"""Summarize an egress run: hostnames from Node/Python hooks and Chromium net-logs, raw remote IPs
from the socket poller, reverse DNS for each IP, and a China check. Exit 1 on any China hit."""
import glob, json, os, re, socket, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from host_inventory import CHINA_HOST  # noqa: E402
DIR = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('EGRESS_DIR', '/tmp/egress')
hosts = {}
for name in ('node.log', 'py.log'):
    p = os.path.join(DIR, name)
    if os.path.exists(p):
        for line in open(p):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == 'dns':
                hosts.setdefault(parts[3], set()).add(name)
            elif len(parts) >= 4 and parts[2] == 'connect':
                h = parts[3].rsplit(':', 1)[0]
                hosts.setdefault(h, set()).add(name)
chrome = sorted(glob.glob(os.path.join(DIR, 'chrome-*.json')))
for p in chrome:
    txt = open(p, errors='replace').read()
    for h in set(re.findall(r'(?:https?|wss?)://([a-z0-9.-]+\.[a-z]{2,})', txt, re.I)) | set(re.findall(r'"host":"([a-z0-9.-]+\.[a-z]{2,})(?::\d+)?"', txt, re.I)):
        hosts.setdefault(h.lower(), set()).add('chrome')
import ipaddress
ips, skipped = [], 0
base = set()
bp = os.path.join(DIR, 'baseline-sockets.log')
if os.path.exists(bp):
    base = {l.split()[1] for l in open(bp) if l.strip()}
sp = os.path.join(DIR, 'sockets.log')
if os.path.exists(sp):
    for line in open(sp):
        ep = line.split()[1]; ip = ep.rsplit(':', 1)[0]
        a = ipaddress.ip_address(ip.replace('::ffff:', ''))
        if ep in base or a.is_private or a in ipaddress.ip_network('198.18.0.0/15'):
            skipped += 1   # present before the run, or box-internal / gateway / egress-proxy range
            continue
        try:
            rdns = socket.gethostbyaddr(ip)[0]
        except OSError:
            rdns = '(no PTR)'
        ips.append((ep, rdns))
local = {'localhost', '127.0.0.1', '::1'}
china = [h for h in hosts if CHINA_HOST.search(h)] + [f'{e} {r}' for e, r in ips if CHINA_HOST.search(r)]
print(f'chrome net-logs: {len(chrome)}')
print('hostnames contacted:')
for h in sorted(hosts):
    if h not in local:
        print(f'  {h}  [{", ".join(sorted(hosts[h]))}]')
print(f'new public remote endpoints seen (socket poller; {skipped} baseline/private skipped):')
for e, r in ips:
    print(f'  {e}  {r}')
print(f'CHINA hits: {len(china)}', *china)
sys.exit(1 if china else 0)
