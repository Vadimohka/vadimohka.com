// Package the ready-to-publish static files. No generators or QA commands run here.
import {mkdirSync, rmSync, readdirSync, copyFileSync} from 'node:fs';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const output = join(root, '_site');
const publicFiles = readdirSync(root).filter(name => name.endsWith('.html')).concat([
  'CNAME', '.nojekyll', 'LICENSE', 'robots.txt',
  'sitemap.xml', 'sitemap-images.xml', 'sitemap-ai.xml',
  'llms.txt', 'llms-full.txt', 'ai-profile.md', 'humans.txt',
]);

function copyTree(source, target) {
  mkdirSync(target, {recursive: true});
  for (const item of readdirSync(source, {withFileTypes: true})) {
    const from = join(source, item.name);
    const to = join(target, item.name);
    if (item.isDirectory()) copyTree(from, to);
    else if (item.isFile()) copyFileSync(from, to);
  }
}

rmSync(output, {recursive: true, force: true});
mkdirSync(output);
for (const file of publicFiles) copyFileSync(join(root, file), join(output, file));
copyTree(join(root, 'assets'), join(output, 'assets'));
mkdirSync(join(output, 'data'));
copyFileSync(join(root, 'data/entity-graph.json'), join(output, 'data/entity-graph.json'));
