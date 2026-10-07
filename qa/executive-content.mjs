// A redesign must not silently rewrite identity, claims, sources or inquiry routes.
// Baseline was captured from main 1044094, before changing presentation.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const ROOT = resolve(new URL('..', import.meta.url).pathname);
const read = name => readFileSync(resolve(ROOT, name), 'utf8');
const hash = value => createHash('sha256').update(value).digest('hex');
export const normalize = html => html.replace(/<[^>]*>/g, ' ')
  .replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp|rarr);/gi, (all, code) => {
    if (code.startsWith('#x')) return String.fromCodePoint(parseInt(code.slice(2),16));
    if (code.startsWith('#')) return String.fromCodePoint(parseInt(code.slice(1),10));
    return {amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' ',rarr:'→'}[code] ?? all;
  }).replace(/\s+/g, ' ').trim();
const baseline = JSON.parse(read('qa/executive-content-baseline.json'));
for (const [file, expected] of Object.entries(baseline.unchanged)) {
  assert.equal(hash(readFileSync(resolve(ROOT, file))), expected, `${file}: protected content changed`);
}
const home = read('index.html');
assert.equal(hash(home.match(/<head>[\s\S]*?<\/head>/)[0]), baseline.home.head, 'Homepage metadata/preload changed');
const main = normalize(home.match(/<main\b[\s\S]*?<\/main>/)[0]);
for (const unit of baseline.home.text) assert.ok(main.includes(unit), `Homepage text lost: ${unit}`);
const hrefs = new Set([...home.matchAll(/\bhref="([^"]+)"/g)].map(m => normalize(m[1])));
for (const href of baseline.home.hrefs) assert.ok(hrefs.has(href), `Homepage destination lost: ${href}`);
const ids = new Set([...home.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]));
for (const id of baseline.home.ids) assert.ok(ids.has(id), `Homepage anchor lost: ${id}`);
assert.equal((home.match(/class="hero-photo\b/g)||[]).length, 1, 'Homepage must have only one portrait hero');
assert.ok(home.includes('Architecture overview · not a product screenshot'), 'Conceptual product visual needs its disclosure');
console.log(`PASS — content integrity: ${Object.keys(baseline.unchanged).length} protected files, ${baseline.home.text.length} homepage text blocks, links and anchors`);
