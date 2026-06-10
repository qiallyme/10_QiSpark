const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const root = __dirname;
const outputDir = path.join(root, 'site');
const outputFile = path.join(outputDir, 'index.html');
const excluded = new Set(['.git', '.github', 'node_modules']);
const required = [
  '_..md',
  '01_QiDNA/_01_QiDNA.md',
  '01_QiDNA/Architecture/Decisions/ADR-0017_canonical_vocabulary_and_v1_direction.md',
  '20_QiSystem/schemas/QiLife_Data_Spine.mdx',
  '60_QiApp_QiLife/_60_QiApp_QiLife.md'
];
const statuses = ['Active', 'Legacy', 'Proposed', 'Generated', 'Evidence'];

function posix(value) {
  return value.split(path.sep).join('/');
}

function discover(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !excluded.has(entry.name) && !entry.name.startsWith('.')) {
      discover(fullPath, files);
    } else if (entry.isFile() && /\.mdx?$/i.test(entry.name)) {
      files.push(fullPath);
    }
  }
  return files;
}

function escapeHtml(value) {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function slug(value) {
  return value.toLowerCase().replace(/\.mdx?$/, '').replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'repository-root';
}

function documentStatus(relativePath) {
  if (relativePath.startsWith('00_QiEOS/exports/')) return 'Generated';
  if (relativePath.startsWith('00_QiEOS/reconciliation/')) return 'Evidence';
  if (relativePath === 'README.md' || relativePath.startsWith('00_QiEOS/') || relativePath.startsWith('10_QiOS_Start/') ||
      relativePath.startsWith('60_QiApps/') || relativePath.startsWith('20_qinexus/') ||
      relativePath.startsWith('30_qiarchive/') || relativePath.startsWith('50_qiserver/') ||
      relativePath.startsWith('60_qiapps/') || relativePath.startsWith('70_qiconnect/')) return 'Legacy';
  if (relativePath.startsWith('20_QiSystem/50_Generated_Reports/') ||
      relativePath.startsWith('20_QiSystem/manifests/') || relativePath === 'site/_site.md') return 'Generated';
  if (relativePath.startsWith('01_QiDNA/Reconciliation/') && !relativePath.endsWith('_Reconciliation.md')) return 'Evidence';
  if (relativePath.startsWith('50_modules/') || relativePath.startsWith('60_ai_layer/') ||
      relativePath.startsWith('70_deployment/') || relativePath.startsWith('80_prompts/')) return 'Proposed';
  if (relativePath.startsWith('90_decisions/') || relativePath.startsWith('99_project_receipts/') ||
      relativePath === 'ADR-0011_homepage_powered_qiaccess.md' || relativePath === 'README 2.md' ||
      relativePath === 'codex.md' || relativePath === 'qilinks_bookmark_admin_plan.md') return 'Evidence';
  return 'Active';
}

function stripFrontmatter(markdown) {
  return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
}

function makeDocument(file) {
  const relativePath = posix(path.relative(root, file));
  const markdown = stripFrontmatter(fs.readFileSync(file, 'utf8'));
  const heading = markdown.match(/^#\s+(.+)$/m);
  const fallback = path.basename(file).replace(/\.mdx?$/i, '').replace(/^_+/, '').replace(/_/g, ' ');
  const directory = path.posix.dirname(relativePath);
  const status = documentStatus(relativePath);
  return {
    id: slug(relativePath),
    path: relativePath,
    group: directory === '.' ? 'Repository' : directory,
    title: heading ? heading[1].trim() : (fallback === '..' ? 'Repository Root' : fallback),
    status,
    search: `${status} ${relativePath} ${markdown}`.toLowerCase(),
    html: marked.parse(markdown)
  };
}

function render(documents) {
  const groups = new Map();
  for (const doc of documents) {
    if (!groups.has(doc.group)) groups.set(doc.group, []);
    groups.get(doc.group).push(doc);
  }
  const counts = Object.fromEntries(statuses.map((status) => [
    status, documents.filter((doc) => doc.status === status).length
  ]));

  const navigation = [...groups.entries()].map(([group, docs]) => `
    <li class="nav-group">
      <div class="group-title">${escapeHtml(group)}</div>
      <ul>${docs.map((doc) => `
        <li class="nav-item" data-status="${doc.status}" data-search="${escapeHtml(doc.search)}">
          <a class="nav-link" href="#${doc.id}"><span class="nav-status status-${doc.status.toLowerCase()}">${doc.status}</span>${escapeHtml(doc.title)}</a>
        </li>`).join('')}
      </ul>
    </li>`).join('');

  const content = documents.map((doc) => `
    <article id="${doc.id}" class="doc" data-status="${doc.status}" data-search="${escapeHtml(doc.search)}">
      <div class="doc-meta"><span class="status-badge status-${doc.status.toLowerCase()}">${doc.status}</span><span class="source-path">${escapeHtml(doc.path)}</span></div>
      ${doc.html}
    </article>`).join('');

  const options = statuses.filter((status) => status !== 'Active')
    .map((status) => `<option value="${status}">${status} (${counts[status]})</option>`).join('');

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="QiOS DNA governance, architecture, system, and QiLife documentation.">
<title>QiOS DNA</title>
<style>
:root{--bg:#f7f5fb;--surface:#fff;--sidebar:#18112b;--muted:#b9add1;--border:#e6e0ef;--text:#342e3e;--heading:#17121f;--accent:#7c3aed;--code:#f2eff6;--header:62px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--text);background:var(--bg);font:16px/1.68 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,input,select{font:inherit}
.mobile-header{display:none;position:fixed;inset:0 0 auto;height:var(--header);padding:0 1rem;align-items:center;gap:.8rem;color:#fff;background:var(--sidebar);z-index:20}.menu{border:0;color:#fff;background:transparent;font-size:1.5rem;cursor:pointer}.overlay{display:none}
nav{position:fixed;inset:0 auto 0 0;width:330px;padding:1.4rem 1.05rem;overflow-y:auto;color:#fff;background:var(--sidebar);z-index:30}.brand{margin:0;font-size:1.45rem}.tagline{margin:.1rem 0 1rem;color:var(--muted);font-size:.83rem}.tools{position:sticky;top:-1.4rem;padding:1.4rem 0 .8rem;background:var(--sidebar);z-index:2}
.search,.status-filter{width:100%;padding:.7rem .8rem;border:1px solid #4d3f66;border-radius:8px;color:#fff;background:#251b38;outline:none}.status-filter{margin-top:.55rem}.search:focus,.status-filter:focus{border-color:#a78bfa;box-shadow:0 0 0 3px rgba(167,139,250,.2)}.tool-row{display:flex;gap:.5rem;margin-top:.55rem}.tool{flex:1;padding:.5rem;border:1px solid #4d3f66;border-radius:7px;color:#eee9f8;background:#251b38;cursor:pointer}.tool:hover,.tool.active{border-color:#a78bfa;background:#392554}
nav ul{margin:0;padding:0;list-style:none}.nav-group{margin:0 0 1rem}.group-title{margin:.5rem 0 .3rem;color:var(--muted);font-size:.7rem;font-weight:750;letter-spacing:.08em;text-transform:uppercase;overflow-wrap:anywhere}.nav-link{display:block;padding:.42rem .62rem;border-radius:6px;color:#f5f3ff;font-size:.88rem;text-decoration:none}.nav-link:hover,.nav-link.active{color:#fff;background:rgba(124,58,237,.52)}.nav-status{display:inline-block;min-width:4.8rem;margin-right:.35rem;font-size:.61rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase}
.hidden{display:none!important}main{margin-left:330px;padding:2.3rem}.content{width:min(940px,100%);margin:0 auto}.intro{margin-bottom:1.35rem}.intro h1{margin:0;border:0}.intro p{margin:.2rem 0 0;color:#655b72}.status{min-height:1.5rem;margin:.5rem 0 0;color:#655b72;font-size:.9rem}
.doc{margin:0 0 1.6rem;padding:2.5rem 3rem;border:1px solid var(--border);border-radius:14px;background:var(--surface);box-shadow:0 8px 30px rgba(38,24,56,.06);scroll-margin-top:1.5rem}body.focus .doc{display:none}body.focus .doc.focused{display:block}.doc-meta{display:flex;align-items:center;gap:.55rem;margin:0 0 1.4rem}.source-path{padding:.42rem .65rem;border-radius:6px;color:#665c72;background:var(--code);font:.78rem/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}.status-badge{padding:.35rem .55rem;border-radius:999px;font-size:.7rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase}.status-active{color:#166534}.status-legacy{color:#c2410c}.status-proposed{color:#9333ea}.status-generated{color:#64748b}.status-evidence{color:#3b82f6}.status-badge.status-active{background:#dcfce7}.status-badge.status-legacy{background:#ffedd5}.status-badge.status-proposed{background:#f3e8ff}.status-badge.status-generated{background:#e2e8f0}.status-badge.status-evidence{background:#dbeafe}
h1,h2,h3,h4{color:var(--heading);line-height:1.25}h1{padding-bottom:.55rem;border-bottom:2px solid var(--border);font-size:2rem}h2{margin-top:2rem;font-size:1.45rem}a{color:var(--accent)}code{padding:.15em .35em;border-radius:4px;background:var(--code)}pre{padding:1.1rem;border-radius:8px;color:#f8f7fa;background:#211a2d;overflow-x:auto}pre code{padding:0;color:inherit;background:transparent}table{display:block;width:100%;border-collapse:collapse;overflow-x:auto}th,td{padding:.65rem;border:1px solid var(--border);text-align:left;vertical-align:top}blockquote{margin-left:0;padding-left:1rem;border-left:4px solid var(--accent)}
.top{position:fixed;right:1.4rem;bottom:1.4rem;display:none;width:44px;height:44px;border:0;border-radius:50%;color:#fff;background:var(--accent);cursor:pointer}.top.visible{display:block}
@media(max-width:800px){.mobile-header{display:flex}nav{width:min(90vw,350px);padding-top:calc(var(--header) + .75rem);transform:translateX(-100%);transition:transform .2s ease}nav.open{transform:translateX(0)}.overlay.open{display:block;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:25}nav .brand,nav .tagline{display:none}.tools{top:calc(-1 * (var(--header) + .75rem));padding-top:calc(var(--header) + .75rem)}main{margin-left:0;padding:calc(var(--header) + 1rem) 1rem 1rem}.doc{padding:1.3rem;border-radius:10px;scroll-margin-top:calc(var(--header) + .75rem)}.doc-meta{align-items:flex-start;flex-direction:column}h1{font-size:1.65rem}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
</style>
</head>
<body>
<header class="mobile-header"><button class="menu" type="button" aria-label="Open navigation">&#9776;</button><strong>QiOS DNA</strong></header>
<div class="overlay"></div>
<nav aria-label="Documentation navigation">
  <h1 class="brand">QiOS DNA</h1><p class="tagline">Canonical blueprint with status-labeled evidence</p>
  <div class="tools">
    <label class="group-title" for="search">Find a document</label>
    <input id="search" class="search" type="search" placeholder="Search titles and content" autocomplete="off">
    <label class="group-title" for="status-filter">Document status</label>
    <select id="status-filter" class="status-filter"><option value="Active">Active (${counts.Active})</option><option value="All">All statuses (${documents.length})</option>${options}</select>
    <div class="tool-row"><button id="focus" class="tool" type="button" aria-pressed="false">Focus mode</button><button id="clear" class="tool" type="button">Clear</button></div>
  </div>
  <ul>${navigation}</ul>
</nav>
<main><div class="content">
  <header class="intro"><h1>QiOS DNA</h1><p>${documents.length} source documents rendered. Active documentation is shown by default.</p><div class="status" aria-live="polite"></div></header>
  ${content}
</div></main>
<button class="top" type="button" aria-label="Back to top">&#8593;</button>
<script>
const body=document.body,nav=document.querySelector('nav'),overlay=document.querySelector('.overlay'),menu=document.querySelector('.menu'),search=document.querySelector('#search'),statusFilter=document.querySelector('#status-filter'),clear=document.querySelector('#clear'),focus=document.querySelector('#focus'),status=document.querySelector('.status'),topButton=document.querySelector('.top');
const links=[...document.querySelectorAll('.nav-link')],items=[...document.querySelectorAll('.nav-item')],groups=[...document.querySelectorAll('.nav-group')],docs=[...document.querySelectorAll('.doc')];let activeId=docs[0]?.id||'';
function closeNav(){nav.classList.remove('open');overlay.classList.remove('open')}function setFocus(id){activeId=id||activeId;docs.forEach(doc=>doc.classList.toggle('focused',doc.id===activeId))}
function filter(){const term=search.value.trim().toLowerCase(),selected=statusFilter.value;let count=0;items.forEach(item=>{const matchStatus=selected==='All'||item.dataset.status===selected,matchText=!term||item.dataset.search.includes(term),match=matchStatus&&matchText;item.classList.toggle('hidden',!match);if(match)count++});groups.forEach(group=>group.classList.toggle('hidden',![...group.querySelectorAll('.nav-item')].some(item=>!item.classList.contains('hidden'))));docs.forEach(doc=>{const matchStatus=selected==='All'||doc.dataset.status===selected,matchText=!term||doc.dataset.search.includes(term);doc.classList.toggle('hidden',!(matchStatus&&matchText))});status.textContent=count+' '+selected.toLowerCase()+' document'+(count===1?'':'s')+(term?' matching search':'')}
menu.addEventListener('click',()=>{nav.classList.toggle('open');overlay.classList.toggle('open')});overlay.addEventListener('click',closeNav);links.forEach(link=>link.addEventListener('click',()=>{setFocus(link.hash.slice(1));closeNav()}));search.addEventListener('input',filter);statusFilter.addEventListener('change',filter);clear.addEventListener('click',()=>{search.value='';statusFilter.value='Active';filter();search.focus()});focus.addEventListener('click',()=>{const enabled=body.classList.toggle('focus');focus.classList.toggle('active',enabled);focus.setAttribute('aria-pressed',String(enabled));focus.textContent=enabled?'Show all':'Focus mode';setFocus(activeId)});topButton.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));window.addEventListener('scroll',()=>topButton.classList.toggle('visible',window.scrollY>500),{passive:true});
const observer=new IntersectionObserver(entries=>{const visible=entries.find(entry=>entry.isIntersecting);if(!visible)return;activeId=visible.target.id;links.forEach(link=>link.classList.toggle('active',link.hash==='#'+activeId))},{rootMargin:'-15% 0px -70% 0px'});docs.forEach(doc=>observer.observe(doc));setFocus(activeId);filter();
</script>
</body>
</html>`;
}

const files = discover(root);
const documents = files.map(makeDocument);
const found = new Set(documents.map((doc) => doc.path));
const missing = required.filter((file) => !found.has(file));
if (missing.length) throw new Error(`Required documentation missing: ${missing.join(', ')}`);
if (!documents.length) throw new Error('No Markdown or MDX documents were discovered.');
const html = render(documents);
for (const doc of documents) {
  if (!html.includes(`id="${doc.id}"`)) throw new Error(`Generated output missing ${doc.path}`);
}
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(outputFile, html.replace(/[ \t]+$/gm, ""));
console.log(`Built ${documents.length} documents into ${posix(path.relative(root, outputFile))}.`);
