// Node egress logger for dstack checks: node --require tools/egress/egress.cjs …
// Logs every DNS lookup / outbound socket to $EGRESS_DIR/node.log and makes Playwright's
// Chromium write a net-log (all hosts the browser contacts) to $EGRESS_DIR/chrome-*.json.
const fs = require('fs'), path = require('path'), net = require('net'), dns = require('dns'), Module = require('module');
const DIR = process.env.EGRESS_DIR || '/tmp/egress'; fs.mkdirSync(DIR, { recursive: true });
const log = (k, v) => fs.appendFileSync(path.join(DIR, 'node.log'), `${new Date().toISOString()} ${process.pid} ${k} ${v}\n`);
const origLookup = dns.lookup;
dns.lookup = function (host, ...a) { log('dns', host); return origLookup.call(this, host, ...a); };
const origConnect = net.Socket.prototype.connect;
net.Socket.prototype.connect = function (...a) {
  const o = a[0] && typeof a[0] === 'object' ? a[0] : { port: a[0], host: a[1] };
  if (!o.path) log('connect', `${o.host || 'localhost'}:${o.port}`);
  return origConnect.apply(this, a);
};
let n = 0;
const wrap = (bt) => {
  if (!bt || bt.__egress) return; bt.__egress = true;
  const orig = bt.launch.bind(bt);
  bt.launch = (opts = {}) => orig({ ...opts, args: [...(opts.args || []), `--log-net-log=${path.join(DIR, `chrome-node-${process.pid}-${n++}.json`)}`] });
};
const origLoad = Module._load;
Module._load = function (req, ...a) {
  const m = origLoad.call(this, req, ...a);
  if (/^playwright(-core)?$/.test(req) && m && m.chromium) wrap(m.chromium);
  return m;
};
