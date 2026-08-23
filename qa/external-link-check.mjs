// Optional network check for the public proof links. The offline QA remains
// authoritative; inaccessible links are reported, not silently removed.
import { readFileSync } from 'node:fs';

const {sources} = JSON.parse(readFileSync('qa/brand/sources.json', 'utf8'));
const selected = new Set(['S001','S002','S003','S005','S007','S010','S013','S021']);
for (const source of sources.filter(item => selected.has(item.source_id))) {
  let result;
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    let response = await fetch(source.url, {method:'HEAD', redirect:'follow', signal:controller.signal});
    if (response.status === 405 || response.status === 403) response = await fetch(source.url, {redirect:'follow', signal:controller.signal});
    clearTimeout(timeout);
    result = `${response.status} ${response.url}`;
  } catch (error) {
    result = `ERROR ${error.name}`;
  }
  console.log(`${source.source_id}\t${result}`);
}
