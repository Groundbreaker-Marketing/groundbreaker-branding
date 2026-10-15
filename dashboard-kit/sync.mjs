// Copies dist/ files into every dashboard listed in kit.json.
//   node dashboard-kit/sync.mjs            copy, then list what changed
//   node dashboard-kit/sync.mjs --check    exit 1 if any consumer is behind (copies nothing)
// Paths in kit.json are relative to the folder that holds groundbreaker-branding (~/apps).
// Each consumer still needs its own branch, PR, and deploy; this only writes the files.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import './build.mjs'; // dist/ is not committed: always build first

const here = dirname(fileURLToPath(import.meta.url));
const apps = resolve(here, '../..');
const kit = JSON.parse(readFileSync(join(here, 'kit.json'), 'utf8'));
const check = process.argv.includes('--check');
const only = process.argv.find((a) => a.startsWith('--only='))?.slice(7);
let behind = 0;
for (const c of kit.consumers) {
  if (only && c.repo !== only) continue;
  const root = join(apps, c.repo);
  if (!existsSync(root)) { console.log(`skip ${c.repo}: not cloned here`); continue; }
  for (const [src, dest] of Object.entries(c.files)) {
    const want = readFileSync(join(here, 'dist', src), 'utf8');
    const target = join(root, dest);
    const have = existsSync(target) ? readFileSync(target, 'utf8') : null;
    if (have === want) continue;
    behind++;
    console.log(`${check ? 'behind' : 'wrote '} ${c.repo}/${dest}`);
    if (!check) { mkdirSync(dirname(target), { recursive: true }); writeFileSync(target, want); }
  }
}
if (!behind) console.log('every consumer is current');
if (check && behind) process.exit(1);
