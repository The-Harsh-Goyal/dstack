# Python egress logger for dstack checks: PYTHONPATH=tools/egress python3 …
# Logs DNS lookups / socket connects to $EGRESS_DIR/py.log and makes Playwright's Chromium
# write a net-log to $EGRESS_DIR/chrome-py-*.json.
import importlib.abc, importlib.machinery, itertools, os, sys, time
DIR = os.environ.get('EGRESS_DIR', '/tmp/egress'); os.makedirs(DIR, exist_ok=True)
def _log(k, v):
    with open(os.path.join(DIR, 'py.log'), 'a') as f:
        f.write(f'{time.strftime("%H:%M:%S")} {os.getpid()} {k} {v}\n')
def _hook(event, args):
    if event == 'socket.getaddrinfo':
        _log('dns', args[0])
    elif event == 'socket.connect':
        addr = args[1]
        if isinstance(addr, tuple):
            _log('connect', f'{addr[0]}:{addr[1]}')
sys.addaudithook(_hook)
_n = itertools.count()
def _patch(mod):
    bt = getattr(mod, 'BrowserType', None)
    if bt is None or getattr(bt, '_egress', False):
        return
    orig = bt.launch
    def launch(self, *a, **k):
        k['args'] = list(k.get('args') or []) + [f'--log-net-log={DIR}/chrome-py-{os.getpid()}-{next(_n)}.json']
        return orig(self, *a, **k)
    bt.launch = launch; bt._egress = True
class _Finder(importlib.abc.MetaPathFinder):
    targets = {'playwright.sync_api._generated', 'playwright.async_api._generated'}
    def find_spec(self, name, path, target=None):
        if name not in self.targets:
            return None
        spec = importlib.machinery.PathFinder.find_spec(name, path)
        if spec and spec.loader:
            orig = spec.loader.exec_module
            def exec_module(module, _o=orig):
                _o(module); _patch(module)
            spec.loader.exec_module = exec_module
        return spec
sys.meta_path.insert(0, _Finder())
