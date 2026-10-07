// Assemble only public resources; source notes, reports and QA stay out of deployment.
import {mkdirSync,rmSync,readdirSync,copyFileSync,statSync} from 'node:fs';
import {resolve,join} from 'node:path';
const root=resolve(new URL('../..',import.meta.url).pathname);
const output=join(root,'_site');
rmSync(output,{recursive:true,force:true});mkdirSync(output);
const publicFiles=readdirSync(root).filter(name=>name.endsWith('.html')).concat(['CNAME','.nojekyll','LICENSE','robots.txt','sitemap.xml','sitemap-images.xml','sitemap-ai.xml','llms.txt','llms-full.txt','ai-profile.md','humans.txt']);
function copyTree(source,target){mkdirSync(target,{recursive:true});for(const item of readdirSync(source,{withFileTypes:true})){const from=join(source,item.name),to=join(target,item.name);if(item.isDirectory())copyTree(from,to);else if(item.isFile())copyFileSync(from,to);}}
for(const file of publicFiles)copyFileSync(join(root,file),join(output,file));
copyTree(join(root,'assets'),join(output,'assets'));
mkdirSync(join(output,'data'));copyFileSync(join(root,'data/entity-graph.json'),join(output,'data/entity-graph.json'));
const all=[];const walk=p=>{for(const f of readdirSync(p)){const full=join(p,f);statSync(full).isDirectory()?walk(full):all.push(full);}};walk(output);
console.log(`PASS — public artifact: ${all.length} files, ${all.reduce((s,f)=>s+statSync(f).size,0)} bytes; no docs, QA, README or install packs`);
