// Exact exceptions for owner-requested maintenance and editorial releases.
// Historical baselines remain intact; an exception can only bridge a known old hash
// to one audited replacement. Semantic content and search-specific guards still run.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const manifest=JSON.parse(readFileSync(new URL('./approved-changes.json',import.meta.url),'utf8'));
export function approvedHash(key, historicalHash){
  const entry=manifest.hashes[key];
  if(!entry)return historicalHash;
  assert.equal(entry.before,historicalHash,`${key}: unauthorized historical baseline`);
  return entry.after;
}
export function restoredSource(file,href){
  const changes=manifest.destinationChanges?.[file] || {};
  if(Object.hasOwn(changes,href))return changes[href];
  return file==='sources.html' ? manifest.sourceRepairs[href] || href : href;
}
export function removedText(file,text){
  return manifest.contentRevisions?.[file]?.removedText.includes(text) || false;
}
export function removedId(file,id){
  return manifest.contentRevisions?.[file]?.removedIds.includes(id) || false;
}
export function checkContentRevision(file,historicalText,currentText){
  const revision=manifest.contentRevisions?.[file];
  if(!revision)return;
  const hash=s=>createHash('sha256').update(s).digest('hex');
  assert.equal(revision.before,hash(JSON.stringify(historicalText)),`${file}: revision must name the historical text`);
  assert.equal(revision.after,hash(currentText),`${file}: editorial text changed outside the approved revision`);
}
