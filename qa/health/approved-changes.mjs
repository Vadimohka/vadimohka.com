// Exact exceptions for the owner-requested SEO/performance maintenance release.
// Historical baselines remain intact; an exception can only bridge a known old hash
// to one audited replacement. Semantic content and search-specific guards still run.
import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const manifest=JSON.parse(readFileSync(new URL('./approved-changes.json',import.meta.url),'utf8'));
export function approvedHash(key, historicalHash){
  const entry=manifest.hashes[key];
  if(!entry)return historicalHash;
  assert.equal(entry.before,historicalHash,`${key}: unauthorized historical baseline`);
  return entry.after;
}
export function restoredSource(file,href){
  return file==='sources.html' ? manifest.sourceRepairs[href] || href : href;
}
