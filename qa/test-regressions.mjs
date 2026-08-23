// Unit-style offline coverage for the production-safety failure modes.
import { readFileSync } from 'node:fs';

const fixture = readFileSync(new URL('./fixtures/bad-placeholder.html', import.meta.url), 'utf8');
if (!/\bTODO\b/.test(fixture)) throw new Error('fixture must contain a TODO marker');
const form = fixture.match(/<form\b[^>]*>/)?.[0] || '';
const action = form.match(/\baction="([^"]*)"/)?.[1] || '';
if (!/example\.com|placeholder/i.test(action)) throw new Error('fixture must contain a placeholder action');
console.log('PASS — bad placeholder fixture exercises TODO and form-action guards');
