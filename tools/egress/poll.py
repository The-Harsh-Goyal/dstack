#!/usr/bin/env python3
"""Poll /proc/net/tcp{,6} every 20 ms and record every non-loopback remote endpoint (catches all
processes, including Chromium). Runs until killed. Output: $EGRESS_DIR/sockets.log"""
import os, socket, struct, time
DIR = os.environ.get('EGRESS_DIR', '/tmp/egress'); os.makedirs(DIR, exist_ok=True)
seen = set()
def ip4(h): return socket.inet_ntop(socket.AF_INET, struct.pack('<I', int(h, 16)))
def ip6(h): return socket.inet_ntop(socket.AF_INET6, b''.join(struct.pack('<I', int(h[i:i + 8], 16)) for i in range(0, 32, 8)))
with open(os.path.join(DIR, 'sockets.log'), 'a', buffering=1) as out:
    while True:
        for f, conv in (('/proc/net/tcp', ip4), ('/proc/net/tcp6', ip6)):
            try:
                rows = open(f).read().splitlines()[1:]
            except OSError:
                continue
            for r in rows:
                rem = r.split()[2]; h, p = rem.split(':'); ip = conv(h); port = int(p, 16)
                if port == 0 or ip.startswith(('127.', '::ffff:127.', '0.0.0.0')) or ip in ('::1', '::'):
                    continue
                if (ip, port) not in seen:
                    seen.add((ip, port)); out.write(f'{time.strftime("%H:%M:%S")} {ip}:{port}\n')
        time.sleep(0.02)
