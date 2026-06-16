const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const root = __dirname;
const siteDir = path.join(root, '1000_QiApps', 'site');
const outputFile = path.join(siteDir, 'index.html');
const excluded = new Set(['.git', '.github', 'node_modules', '_staging_write_test']);
const duplicateFilePattern = /\s\(\d+\)\.(mdx?|json|bat|mmd)$/i;
const explicitlySkippedFilePatterns = [
  /^_markmind_export(?:_with_content)?\.md$/i,
  /^\.aider\./i
];
const required = [
  'README.md',
  '00_QiEOS/_QiEOS.md',
  '00_QiEOS/QiOS_Core_Doctrine.mdx',
  '05_Decisions/ADR-0017_canonical_vocabulary_and_v1_direction.md',
  '05_Decisions/ADR-0018_supabase_qilife_data_authority.md',
  '20_QiSystem/schemas/QiLife_Data_Spine.mdx',
  '1000_QiApps/site/_site.md'
];
const statuses = ['Active', 'Legacy', 'Proposed', 'Generated', 'Evidence'];

function posix(value) {
  return value.split(path.sep).join('/');
}

function readText(file) {
  const buffer = fs.readFileSync(file);
  if (buffer.length >= 2) {
    if (buffer[0] === 0xff && buffer[1] === 0xfe) {
      return buffer.slice(2).toString('utf16le').replace(/^\uFEFF/, '');
    }
    if (buffer[0] === 0xfe && buffer[1] === 0xff) {
      return Buffer.from(buffer.slice(2)).swap16().toString('utf16le').replace(/^\uFEFF/, '');
    }
  }
  const text = buffer.toString('utf8').replace(/^\uFEFF/, '');
  return text.includes('\u0000') ? buffer.toString('utf16le').replace(/^\uFEFF/, '') : text;
}

function shouldSkipDirectory(fullPath, entryName) {
  return excluded.has(entryName) || entryName.startsWith('.');
}

function shouldSkipFile(fileName) {
  return duplicateFilePattern.test(fileName) ||
    explicitlySkippedFilePatterns.some((pattern) => pattern.test(fileName));
}

function discover(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !shouldSkipDirectory(fullPath, entry.name)) {
      discover(fullPath, files);
    } else if (entry.isFile() && /\.mdx?$/i.test(entry.name) && !shouldSkipFile(entry.name)) {
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
  const lp = relativePath.toLowerCase();

  // Generated: exported or auto-generated content
  if (lp.includes('/exports/') || lp.includes('generated_reports') ||
      lp.includes('generated_indexes')) return 'Generated';

  // Legacy: superseded or quarantined content
  if (lp.includes('/90_superseded_sources/') || lp.includes('legacy_quarantine') ||
      lp.endsWith('readme_drop_this_in.md')) return 'Legacy';

  // Evidence: operational records, logs, audits, reconciliation
  if (lp.includes('/reconciliation/') || lp.includes('/receipts/') ||
      lp.includes('/logs/') || lp.includes('/audits/') ||
      lp.includes('/backups/') || lp.includes('/health_checks/') ||
      lp.includes('/maintenance/')) return 'Evidence';

  return 'Active';
}

function stripFrontmatter(markdown) {
  return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
}

function makeDocument(file) {
  const relativePath = posix(path.relative(root, file));
  const markdown = stripFrontmatter(readText(file));
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
  const styles = fs.readFileSync(path.join(siteDir, 'style.css'), 'utf8');
  const clientScript = fs.readFileSync(path.join(siteDir, 'script.js'), 'utf8')
    .replace("searchIcon.textContent = 'âŒ•';", "searchIcon.textContent = 'S';")
    .replace("help.innerHTML = '<kbd>Ctrl</kbd><kbd>K</kbd> search <span>Â·</span> <kbd>Esc</kbd> clear';", "help.innerHTML = '<kbd>Ctrl</kbd><kbd>K</kbd> search <span>|</span> <kbd>Esc</kbd> clear';")
    .replace("themeButton.textContent = theme === 'dark' ? 'â˜¾' : 'â˜€';", "themeButton.textContent = theme === 'dark' ? 'DK' : 'LT';")
    .replaceAll("â€¦", "...")
    .replace("status.textContent = currentResults.length + ' result' + (currentResults.length === 1 ? '' : 's') + ' for â€œ' + query + 'â€ ';", "status.textContent = currentResults.length + ' result' + (currentResults.length === 1 ? '' : 's') + ' for \"' + query + '\"';");
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
fs.mkdirSync(siteDir, { recursive: true });
fs.writeFileSync(outputFile, html.replace(/[ \t]+$/gm, ""));
console.log(`Built ${documents.length} documents into ${posix(path.relative(root, outputFile))}.`);
