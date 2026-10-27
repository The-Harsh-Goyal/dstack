// Key-file reader for the ElevenLabs provider (DSTACK_ELEVENLABS_KEY_FILE).
// A key file holds either the bare key on line 1, or dotenv lines such as
//   ELEVENLABS_API_KEY=...   or   export ELEVENLABS_API_KEY="..."
// (optional `export `, optional single/double quotes, `#` comments and blank lines ignored).
// The key is returned to the caller only; nothing here prints or stores it.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const PACK_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

export function expandHome(file) { return path.resolve(String(file).replace(/^~(?=\/|$)/, os.homedir())); }

export function insideRepo(abs) {
  const rel = path.relative(PACK_ROOT, abs);
  return !rel.startsWith('..') && !path.isAbsolute(rel);
}

/** Parse key-file text. `varName` is the dotenv variable (e.g. ELEVENLABS_API_KEY). Returns the key or null. */
export function parseKeyFile(text, varName) {
  const lines = String(text).replace(/^\uFEFF/, '').split(/\r?\n/);
  const re = new RegExp(`^(?:export\\s+)?${varName}\\s*=\\s*(.*)$`);
  let assigned = false;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const m = line.match(re);
    if (!m) continue;
    assigned = true;
    let v = m[1].trim();
    const q = v[0];
    if ((q === '"' || q === "'") && v.indexOf(q, 1) > 0) v = v.slice(1, v.indexOf(q, 1));
    else v = v.replace(/\s+#.*$/, '').trim();
    if (v) return v;
  }
  if (assigned) return null;
  // bare form: the key alone on line 1 (not a comment, not an assignment)
  const first = (lines[0] || '').trim();
  return first && !first.startsWith('#') && !first.includes('=') ? first : null;
}

/** Read a key file (no repo check). Returns the key or null; throws if unreadable. */
export function readKeyFile(file, varName) {
  return parseKeyFile(fs.readFileSync(expandHome(file), 'utf8'), varName);
}
