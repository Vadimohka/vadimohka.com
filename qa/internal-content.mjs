// Source snapshot: main@6be1903, before the internal-page layout changes.
// The older executive baseline is retained and anchors every source file hash.
import { approvedHash, restoredSource } from './health/approved-changes.mjs';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const ROOT=resolve(new URL('..',import.meta.url).pathname);
const read=f=>readFileSync(resolve(ROOT,f),'utf8');
const hash=s=>createHash('sha256').update(s).digest('hex');
const baseline=JSON.parse(read('qa/internal-content-baseline.json'));
const original=JSON.parse(read('qa/executive-content-baseline.json'));
const editorial=JSON.parse(read('qa/editorial-titles.json'));
export const internalPages=new Set(Object.keys(baseline.pages));
const normalize=html=>html.replace(/<[^>]*>/g,' ').replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp|rarr);/gi,(all,code)=>code.startsWith('#x')?String.fromCodePoint(parseInt(code.slice(2),16)):code.startsWith('#')?String.fromCodePoint(parseInt(code.slice(1),10)):({amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' ',rarr:'→'}[code]??all)).replace(/\s+/g,' ').trim();
for(const [file,expected] of Object.entries(baseline.locked))assert.equal(hash(read(file)),approvedHash('locked:'+file,expected),`${file}: homepage/shared production file changed`);
let blocks=0;
for(const [file,before] of Object.entries(baseline.pages)){
 assert.equal(before.sourceHash,original.unchanged[file],`${file}: baseline must describe original content`);
 const html=read(file);
 if(file==='expert.html'){
  const summaries=[...html.matchAll(/<summary>[\s\S]*?<\/summary>/g)].map(m=>normalize(m[0]).replace(/[+×]/g,'').trim());
  for(const label of ['25 words','50 words','100 words'])assert.ok(summaries.includes(label),`expert.html: biography summary lost: ${label}`);
 }
 const originalHead=html.match(/<head>[\s\S]*?<\/head>/)[0].replace('<link rel="stylesheet" href="assets/internal.css" />','');
 assert.equal(hash(originalHead),approvedHash('internal-head:'+file,before.head),`${file}: metadata/structured data changed`);
 for(const tag of ['header','footer'])assert.equal(hash(html.match(new RegExp(`<${tag}\\b[\\s\\S]*?<\\/${tag}>`))[0]),before[tag],`${file}: ${tag} changed`);
 const text=normalize(html.match(/<main\b[\s\S]*?<\/main>/)[0]);
 for(const [oldTitle,newTitle] of Object.entries(editorial[file]||{})){assert.ok(before.text.includes(oldTitle), `${file}: unknown editorial source heading`);assert.ok(text.includes(newTitle), `${file}: replacement heading missing: ${newTitle}`);}
 for(const unit of before.text){assert.ok(text.includes(editorial[file]?.[unit]||unit),`${file}: original content lost: ${unit}`);blocks++;}
 const hrefs=new Set([...html.matchAll(/\bhref="([^"]+)"/g)].map(m=>normalize(m[1])));
 for(const href of before.hrefs)assert.ok(hrefs.has(restoredSource(file,href)),`${file}: destination lost: ${href}`);
 const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
 for(const id of before.ids)assert.ok(ids.has(id),`${file}: anchor lost: ${id}`);
 assert.ok(html.includes('class="inner-page '),`${file}: missing page-specific layout`);
 assert.ok(html.includes('href="assets/internal.css"'),`${file}: missing isolated internal stylesheet`);
}
console.log(`PASS — internal content: ${blocks} original text blocks, 9 metadata/header/footer snapshots, all destinations/anchors; explicit SEO/performance changes authorized`);
