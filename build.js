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
  '01_QiDNA/Architecture/Decisions/ADR-0018_supabase_qilife_data_authority.md',
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
  if (relativePath.startsWith('00_QiEOS/') || relativePath.startsWith('10_QiOS_Start/') ||
      relativePath.startsWith('60_QiApps/') || relativePath.startsWith('20_qinexus/') ||
      relativePath.startsWith('30_qiarchive/') || relativePath.startsWith('50_qiserver/') ||
      relativePath.startsWith('60_qiapps/') || relativePath.startsWith('70_qiconnect/')) return 'Legacy';
  if (relativePath.startsWith('20_QiSystem/50_Generated_Reports/') ||
      relativePath.startsWith('20_QiSystem/manifests/')) return 'Generated';
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

function buildTree(documents) {
  const rootNode = { name: 'Repository', path: '', children: new Map(), documents: [] };
  for (const doc of documents) {
    const directory = path.posix.dirname(doc.path);
    const parts = directory === '.' ? [] : directory.split('/');
    let node = rootNode;
    for (const part of parts) {
      if (!node.children.has(part)) {
        const nodePath = node.path ? `${node.path}/${part}` : part;
        node.children.set(part, { name: part, path: nodePath, children: new Map(), documents: [] });
      }
      node = node.children.get(part);
    }
    node.documents.push(doc);
  }
  return rootNode;
}

function renderDocumentLink(doc) {
  return `<li class="nav-item" data-status="${doc.status}" data-search="${escapeHtml(doc.search)}">
    <a class="nav-link" href="#${doc.id}"><span class="document-icon" aria-hidden="true"></span><span class="nav-label">${escapeHtml(doc.title)}</span><span class="nav-status status-${doc.status.toLowerCase()}">${doc.status}</span></a>
  </li>`;
}

function renderTreeNode(node, depth = 0) {
  const childNodes = [...node.children.values()]
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
  const documents = [...node.documents]
    .sort((a, b) => a.title.localeCompare(b.title, undefined, { numeric: true }));
  const contents = [
    ...documents.map(renderDocumentLink),
    ...childNodes.map((child) => renderTreeNode(child, depth + 1))
  ].join('');
  const label = node.name || 'Repository files';
  return `<li class="tree-node${depth === 0 ? ' tree-root-node' : ''}" data-path="${escapeHtml(node.path)}" data-depth="${depth}">
    <button class="folder-toggle" type="button" aria-expanded="${depth < 1 ? 'true' : 'false'}"><span class="tree-caret" aria-hidden="true"></span><span class="folder-icon" aria-hidden="true"></span><span class="folder-label">${escapeHtml(label)}</span></button>
    <ul class="tree-children">${contents}</ul>
  </li>`;
}

function render(documents) {
  const styles = fs.readFileSync(path.join(outputDir, 'style.css'), 'utf8');
  const clientScript = fs.readFileSync(path.join(outputDir, 'script.js'), 'utf8');
  const tree = buildTree(documents);
  const counts = Object.fromEntries(statuses.map((status) => [
    status, documents.filter((doc) => doc.status === status).length
  ]));

  const navigation = renderTreeNode(tree);

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
<style>${styles}</style>
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
  <div class="tree-heading">Folder mirror</div>
  <ul class="directory-tree">${navigation}</ul>
</nav>
<main><div class="content">
  <header class="intro"><h1>QiOS DNA</h1><p>${documents.length} source documents rendered. Active documentation is shown by default.</p><div class="status" aria-live="polite"></div></header>
  ${content}
</div></main>
<button class="top" type="button" aria-label="Back to top">&#8593;</button>
<script>${clientScript}</script>
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
