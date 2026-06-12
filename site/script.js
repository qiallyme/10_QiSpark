(() => {
  'use strict';
  const body = document.body;
  const root = document.documentElement;
  const nav = document.querySelector('nav');
  const overlay = document.querySelector('.overlay');
  const menu = document.querySelector('.menu');
  const search = document.querySelector('#search');
  const statusFilter = document.querySelector('#status-filter');
  const clearButton = document.querySelector('#clear');
  const focusButton = document.querySelector('#focus');
  const status = document.querySelector('.status');
  const topButton = document.querySelector('.top');
  const intro = document.querySelector('.intro');
  const docs = Array.from(document.querySelectorAll('.doc'));
  const links = Array.from(document.querySelectorAll('.nav-link'));
  const items = Array.from(document.querySelectorAll('.nav-item'));
  const treeNodes = Array.from(document.querySelectorAll('.tree-node'));
  const folderButtons = Array.from(document.querySelectorAll('.folder-toggle'));
  const docMap = new Map(docs.map((doc) => [doc.id, doc]));
  const index = docs.map((doc) => ({
    id: doc.id,
    title: doc.querySelector('h1')?.textContent.trim() || doc.id,
    path: doc.querySelector('.source-path')?.textContent.trim() || '',
    status: doc.dataset.status,
    search: doc.dataset.search || ''
  }));
  let activeId = location.hash.slice(1);
  let currentResults = [];
  let selectedResult = -1;
  let searchTimer;

  const brandBar = document.createElement('div');
  brandBar.className = 'brand-bar';
  nav.insertBefore(brandBar, nav.firstChild);
  brandBar.append(nav.querySelector('.brand'));
  const themeButton = document.createElement('button');
  themeButton.className = 'theme-toggle';
  themeButton.type = 'button';
  themeButton.title = 'Switch color theme';
  brandBar.append(themeButton);

  const searchShell = document.createElement('div');
  searchShell.className = 'search-shell';
  search.parentNode.insertBefore(searchShell, search);
  const searchIcon = document.createElement('span');
  searchIcon.setAttribute('aria-hidden', 'true');
  searchIcon.textContent = '⌕';
  const shortcut = document.createElement('kbd');
  shortcut.textContent = '/';
  searchShell.append(searchIcon, search, shortcut);
  search.placeholder = 'Search everything...';
  const help = document.createElement('p');
  help.className = 'search-help';
  help.innerHTML = '<kbd>Ctrl</kbd><kbd>K</kbd> search <span>·</span> <kbd>Esc</kbd> clear';
  document.querySelector('.tools').append(help);

  const results = document.createElement('section');
  results.className = 'search-results hidden';
  results.setAttribute('aria-label', 'Search results');
  intro.insertAdjacentElement('afterend', results);

  function closeNav() {
    nav.classList.remove('open');
    overlay.classList.remove('open');
  }
  function openNav() {
    nav.classList.add('open');
    overlay.classList.add('open');
  }
  function setTheme(theme) {
    root.dataset.theme = theme;
    themeButton.textContent = theme === 'dark' ? '☾' : '☀';
    themeButton.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    localStorage.setItem('qios-docs-theme', theme);
  }
  function termsFor(value) {
    return value.toLowerCase().match(/[a-z0-9_./-]+/g) || [];
  }
  function rank(doc, terms) {
    const title = doc.title.toLowerCase();
    const path = doc.path.toLowerCase();
    let score = 0;
    for (const term of terms) {
      if (!doc.search.includes(term)) return -1;
      if (title === term) score += 30;
      else if (title.startsWith(term)) score += 18;
      else if (title.includes(term)) score += 12;
      if (path.includes(term)) score += 6;
      score += Math.min(doc.search.split(term).length - 1, 8);
    }
    return score + (doc.status === 'Active' ? 2 : 0);
  }
  function snippet(doc, terms) {
    const text = doc.search.replace(/[#*|>[\]]/g, ' ').replace(/\s+/g, ' ').trim();
    const positions = terms.map((term) => text.indexOf(term)).filter((position) => position >= 0);
    const start = Math.max(0, (positions.length ? Math.min(...positions) : 0) - 65);
    const end = Math.min(text.length, start + 220);
    return (start ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }
  function highlight(value, terms) {
    const fragment = document.createDocumentFragment();
    const escaped = terms.map((term) => term.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&'));
    const matcher = new RegExp('(' + escaped.join('|') + ')', 'ig');
    value.split(matcher).forEach((part) => {
      if (terms.some((term) => part.toLowerCase() === term)) {
        const mark = document.createElement('mark');
        mark.textContent = part;
        fragment.append(mark);
      } else {
        fragment.append(document.createTextNode(part));
      }
    });
    return fragment;
  }
  function resultCard(doc, terms, position) {
    const card = document.createElement('button');
    card.className = 'result-card';
    card.type = 'button';
    card.dataset.id = doc.id;
    if (position === selectedResult) card.classList.add('selected');
    const head = document.createElement('div');
    head.className = 'result-head';
    const title = document.createElement('span');
    title.className = 'result-title';
    title.append(highlight(doc.title, terms));
    const badge = document.createElement('span');
    badge.className = 'status-badge status-' + doc.status.toLowerCase();
    badge.textContent = doc.status;
    head.append(title, badge);
    const path = document.createElement('div');
    path.className = 'result-path';
    path.append(highlight(doc.path, terms));
    const summary = document.createElement('p');
    summary.className = 'result-snippet';
    summary.append(highlight(snippet(doc, terms), terms));
    card.append(head, path, summary);
    return card;
  }
  function updateUrl() {
    const params = new URLSearchParams();
    if (search.value.trim()) params.set('q', search.value.trim());
    if (statusFilter.value !== 'Active') params.set('status', statusFilter.value);
    const query = params.toString();
    history.replaceState(null, '', (query ? '?' + query : '') + (activeId ? '#' + activeId : ''));
  }
  function setFocus(id, scroll) {
    if (!docMap.has(id)) return;
    activeId = id;
    docs.forEach((doc) => doc.classList.toggle('focused', doc.id === id));
    links.forEach((link) => link.classList.toggle('active', link.hash === '#' + id));
    const activeLink = links.find((link) => link.hash === '#' + id);
    let ancestor = activeLink?.closest('.tree-node');
    while (ancestor) {
      ancestor.classList.remove('collapsed');
      ancestor.querySelector(':scope > .folder-toggle')?.setAttribute('aria-expanded', 'true');
      ancestor = ancestor.parentElement?.closest('.tree-node');
    }
    updateUrl();
    if (scroll) docMap.get(id).scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function filter() {
    const query = search.value.trim();
    const terms = termsFor(query);
    const selectedStatus = statusFilter.value;
    const allowed = index.filter((doc) => selectedStatus === 'All' || doc.status === selectedStatus);
    items.forEach((item) => item.classList.toggle('hidden', selectedStatus !== 'All' && item.dataset.status !== selectedStatus));
    [...treeNodes].reverse().forEach((node) => {
      if (node.classList.contains('tree-root-node')) return;
      const hasVisibleDocument = Boolean(node.querySelector(':scope > .tree-children > .nav-item:not(.hidden)'));
      const hasVisibleFolder = Boolean(node.querySelector(':scope > .tree-children > .tree-node:not(.hidden)'));
      node.classList.toggle('hidden', !hasVisibleDocument && !hasVisibleFolder);
    });

    if (terms.length) {
      currentResults = allowed.map((doc) => ({ doc, score: rank(doc, terms) }))
        .filter((entry) => entry.score >= 0)
        .sort((a, b) => b.score - a.score || a.doc.title.localeCompare(b.doc.title))
        .slice(0, 75)
        .map((entry) => entry.doc);
      selectedResult = currentResults.length ? 0 : -1;
      results.replaceChildren();
      if (currentResults.length) {
        currentResults.forEach((doc, position) => results.append(resultCard(doc, terms, position)));
      } else {
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        empty.innerHTML = '<strong>No matching documents</strong>Try fewer words, a path fragment, or switch the status filter to All.';
        results.append(empty);
      }
      results.classList.remove('hidden');
      docs.forEach((doc) => doc.classList.add('hidden'));
      status.textContent = currentResults.length + ' result' + (currentResults.length === 1 ? '' : 's') + ' for “' + query + '”';
    } else {
      currentResults = [];
      selectedResult = -1;
      results.classList.add('hidden');
      docs.forEach((doc) => doc.classList.toggle('hidden', selectedStatus !== 'All' && doc.dataset.status !== selectedStatus));
      status.textContent = allowed.length + ' ' + selectedStatus.toLowerCase() + ' document' + (allowed.length === 1 ? '' : 's');
    }
    updateUrl();
  }
  function moveResult(direction) {
    if (!currentResults.length) return;
    selectedResult = (selectedResult + direction + currentResults.length) % currentResults.length;
    document.querySelectorAll('.result-card').forEach((card, position) => card.classList.toggle('selected', position === selectedResult));
    document.querySelector('.result-card.selected')?.scrollIntoView({ block: 'nearest' });
  }
  function openResult(id) {
    search.value = '';
    body.classList.add('focus');
    focusButton.classList.add('active');
    focusButton.setAttribute('aria-pressed', 'true');
    focusButton.textContent = 'Show all';
    filter();
    setFocus(id, true);
    closeNav();
  }

  const mindMapButton = document.createElement('button');
  mindMapButton.id = 'mind-map-toggle';
  mindMapButton.className = 'tool';
  mindMapButton.type = 'button';
  mindMapButton.textContent = 'Mind map';
  mindMapButton.setAttribute('aria-pressed', 'false');
  document.querySelector('.tool-row').prepend(mindMapButton);

  const mindMapView = document.createElement('section');
  mindMapView.className = 'mind-map-view hidden';
  mindMapView.innerHTML = '<header class="mind-map-header"><div><h2 class="mind-map-title">QiDNA Mind Map</h2><p class="mind-map-subtitle">Select a folder to expand it. Select a document to open its page.</p></div><div class="mind-map-actions"><button class="map-action" id="map-collapse" type="button">Collapse</button><button class="map-action" id="map-fit" type="button">Fit</button><button class="map-action" id="map-close" type="button">Document view</button></div></header><div class="mind-map-viewport"><svg class="mind-map-svg" role="img" aria-label="Interactive QiDNA folder and document mind map"></svg></div>';
  intro.insertAdjacentElement('afterend', mindMapView);
  const mindMapSvg = mindMapView.querySelector('.mind-map-svg');
  const mindMapViewport = mindMapView.querySelector('.mind-map-viewport');
  const mapExpanded = new Set();
  let mapScale = 1;

  function mindTree() {
    const selectedStatus = statusFilter.value;
    const rootNode = { key: 'root', name: 'QiDNA', type: 'root', children: [] };
    const folderMap = new Map([['', rootNode]]);
    index.filter((doc) => selectedStatus === 'All' || doc.status === selectedStatus).forEach((doc) => {
      const parts = doc.path.split('/');
      parts.pop();
      let parentPath = '';
      let parent = rootNode;
      parts.forEach((part) => {
        const folderPath = parentPath ? parentPath + '/' + part : part;
        if (!folderMap.has(folderPath)) {
          const folder = { key: 'folder:' + folderPath, name: part, path: folderPath, type: 'folder', children: [] };
          folderMap.set(folderPath, folder);
          parent.children.push(folder);
        }
        parent = folderMap.get(folderPath);
        parentPath = folderPath;
      });
      parent.children.push({ key: 'doc:' + doc.id, name: doc.title, type: 'document', id: doc.id, status: doc.status, path: doc.path, children: [] });
    });
    const sortNode = (node) => {
      node.children.sort((a, b) => {
        if (a.type !== b.type) return a.type === 'folder' ? -1 : 1;
        return a.name.localeCompare(b.name, undefined, { numeric: true });
      });
      node.children.forEach(sortNode);
    };
    sortNode(rootNode);
    return rootNode;
  }

  function visibleMapChildren(node) {
    if (node.type === 'root') return node.children;
    return node.type === 'folder' && mapExpanded.has(node.key) ? node.children : [];
  }

  function mapWords(value, limit) {
    const words = value.replace(/_/g, ' ').split(/\s+/);
    const lines = [''];
    words.forEach((word) => {
      const current = lines[lines.length - 1];
      if (!current || (current + ' ' + word).length <= limit) lines[lines.length - 1] = current ? current + ' ' + word : word;
      else if (lines.length < 2) lines.push(word);
      else lines[1] = (lines[1] + ' ' + word).slice(0, limit - 1) + '…';
    });
    return lines;
  }

  function renderMindMap() {
    const tree = mindTree();
    const left = tree.children.filter((_, index) => index % 2);
    const right = tree.children.filter((_, index) => index % 2 === 0);
    const positions = new Map([[tree.key, { node: tree, x: 0, y: 0, side: 0, parent: null }]]);
    const edges = [];

    function layoutSide(nodes, side) {
      let cursor = 0;
      const placed = [];
      function place(node, depth, parent) {
        const children = visibleMapChildren(node);
        let y;
        if (children.length) {
          const childPositions = children.map((child) => place(child, depth + 1, node));
          y = childPositions.reduce((sum, child) => sum + child.y, 0) / childPositions.length;
        } else {
          y = cursor * 92;
          cursor += 1;
        }
        const position = { node, x: side * (235 + (depth - 1) * 235), y, side, parent };
        positions.set(node.key, position);
        placed.push(position);
        if (parent) edges.push([parent.key, node.key]);
        return position;
      }
      nodes.forEach((node) => place(node, 1, tree));
      if (!placed.length) return;
      const ys = placed.map((position) => position.y);
      const offset = (Math.min(...ys) + Math.max(...ys)) / 2;
      placed.forEach((position) => { position.y -= offset; });
    }

    layoutSide(left, -1);
    layoutSide(right, 1);

    const all = [...positions.values()];
    const minX = Math.min(...all.map((p) => p.x)) - 150;
    const maxX = Math.max(...all.map((p) => p.x)) + 150;
    const minY = Math.min(...all.map((p) => p.y)) - 85;
    const maxY = Math.max(...all.map((p) => p.y)) + 85;
    const width = Math.max(900, maxX - minX);
    const height = Math.max(620, maxY - minY);
    mindMapSvg.setAttribute('viewBox', [minX, minY, width, height].join(' '));
    mindMapSvg.setAttribute('width', width * mapScale);
    mindMapSvg.setAttribute('height', height * mapScale);
    mindMapSvg.replaceChildren();

    const ns = 'http://www.w3.org/2000/svg';
    const edgeLayer = document.createElementNS(ns, 'g');
    edgeLayer.setAttribute('class', 'map-edges');
    edges.forEach(([fromKey, toKey]) => {
      const from = positions.get(fromKey);
      const to = positions.get(toKey);
      if (!from || !to) return;
      const path = document.createElementNS(ns, 'path');
      const startX = from.x + (to.side < 0 ? -82 : 82);
      const endX = to.x + (to.side < 0 ? 96 : -96);
      const bend = (startX + endX) / 2;
      path.setAttribute('d', `M ${startX} ${from.y} C ${bend} ${from.y}, ${bend} ${to.y}, ${endX} ${to.y}`);
      path.setAttribute('class', 'map-connector');
      edgeLayer.append(path);
    });
    mindMapSvg.append(edgeLayer);

    all.forEach(({ node, x, y }) => {
      const group = document.createElementNS(ns, 'g');
      const nodeClass = node.type === 'document' ? 'map-node map-node-document status-' + node.status.toLowerCase() : 'map-node map-node-' + node.type;
      group.setAttribute('class', nodeClass);
      group.setAttribute('transform', `translate(${x} ${y})`);
      group.setAttribute('tabindex', '0');
      group.setAttribute('role', 'button');
      group.setAttribute('aria-label', node.type === 'document' ? 'Open ' + node.name : 'Toggle ' + node.name);
      const rect = document.createElementNS(ns, 'rect');
      const nodeWidth = node.type === 'root' ? 170 : node.type === 'folder' ? 190 : 210;
      const nodeHeight = node.type === 'root' ? 58 : 66;
      rect.setAttribute('x', -nodeWidth / 2);
      rect.setAttribute('y', -nodeHeight / 2);
      rect.setAttribute('width', nodeWidth);
      rect.setAttribute('height', nodeHeight);
      rect.setAttribute('rx', node.type === 'root' ? 22 : 13);
      const text = document.createElementNS(ns, 'text');
      text.setAttribute('text-anchor', 'middle');
      const lines = mapWords(node.name, node.type === 'document' ? 27 : 23);
      lines.forEach((line, lineIndex) => {
        const tspan = document.createElementNS(ns, 'tspan');
        tspan.setAttribute('x', 0);
        tspan.setAttribute('dy', lineIndex ? 15 : (lines.length === 1 ? 4 : -2));
        tspan.textContent = line;
        text.append(tspan);
      });
      group.append(rect, text);
      if (node.type === 'folder' && node.children.length) {
        const dot = document.createElementNS(ns, 'circle');
        dot.setAttribute('class', 'map-expand-dot');
        dot.setAttribute('cx', x < 0 ? -95 : 95);
        dot.setAttribute('cy', 0);
        dot.setAttribute('r', 7);
        group.append(dot);
      }
      const activate = () => {
        if (node.type === 'folder') {
          if (mapExpanded.has(node.key)) mapExpanded.delete(node.key);
          else mapExpanded.add(node.key);
          renderMindMap();
        } else if (node.type === 'document') {
          const doc = index.find((entry) => entry.id === node.id);
          if (doc && statusFilter.value !== 'All' && statusFilter.value !== doc.status) statusFilter.value = doc.status;
          closeMindMap();
          filter();
          body.classList.add('focus');
          focusButton.classList.add('active');
          focusButton.setAttribute('aria-pressed', 'true');
          focusButton.textContent = 'Show all';
          setFocus(node.id, true);
        }
      };
      group.addEventListener('click', activate);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          activate();
        }
      });
      mindMapSvg.append(group);
    });
    requestAnimationFrame(() => {
      mindMapViewport.scrollLeft = Math.max(0, (mindMapViewport.scrollWidth - mindMapViewport.clientWidth) / 2);
      mindMapViewport.scrollTop = Math.max(0, (mindMapViewport.scrollHeight - mindMapViewport.clientHeight) / 2);
    });
  }

  function openMindMap() {
    body.classList.add('mind-map-mode');
    mindMapView.classList.remove('hidden');
    mindMapButton.classList.add('active');
    mindMapButton.setAttribute('aria-pressed', 'true');
    mindMapButton.textContent = 'Document view';
    renderMindMap();
    closeNav();
  }

  function closeMindMap() {
    body.classList.remove('mind-map-mode');
    mindMapView.classList.add('hidden');
    mindMapButton.classList.remove('active');
    mindMapButton.setAttribute('aria-pressed', 'false');
    mindMapButton.textContent = 'Mind map';
  }

  mindMapButton.addEventListener('click', () => body.classList.contains('mind-map-mode') ? closeMindMap() : openMindMap());
  mindMapView.querySelector('#map-close').addEventListener('click', closeMindMap);
  mindMapView.querySelector('#map-collapse').addEventListener('click', () => {
    mapExpanded.clear();
    renderMindMap();
  });
  mindMapView.querySelector('#map-fit').addEventListener('click', () => {
    mapScale = 1;
    renderMindMap();
    mindMapViewport.scrollTo({ left: 0, top: 0, behavior: 'smooth' });
  });

  menu.addEventListener('click', () => nav.classList.contains('open') ? closeNav() : openNav());
  overlay.addEventListener('click', closeNav);
  themeButton.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  statusFilter.addEventListener('change', () => { filter(); if (body.classList.contains('mind-map-mode')) renderMindMap(); });
  search.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(filter, 70);
  });
  search.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      moveResult(1);
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      moveResult(-1);
    } else if (event.key === 'Enter' && selectedResult >= 0) {
      event.preventDefault();
      openResult(currentResults[selectedResult].id);
    }
  });
  results.addEventListener('click', (event) => {
    const card = event.target.closest('.result-card');
    if (card) openResult(card.dataset.id);
  });
  clearButton.addEventListener('click', () => {
    search.value = '';
    statusFilter.value = 'Active';
    filter();
    search.focus();
  });
  focusButton.addEventListener('click', () => {
    const enabled = body.classList.toggle('focus');
    focusButton.classList.toggle('active', enabled);
    focusButton.setAttribute('aria-pressed', String(enabled));
    focusButton.textContent = enabled ? 'Show all' : 'Focus mode';
    setFocus(activeId || docs.find((doc) => !doc.classList.contains('hidden'))?.id, false);
  });
  folderButtons.forEach((button) => {
    const node = button.closest('.tree-node');
    const depth = Number(node.dataset.depth);
    const open = depth <= 1;
    button.setAttribute('aria-expanded', String(open));
    if (!open) node.classList.add('collapsed');
    button.addEventListener('click', () => {
      const collapsed = node.classList.toggle('collapsed');
      button.setAttribute('aria-expanded', String(!collapsed));
    });
  });
  links.forEach((link) => link.addEventListener('click', () => {
    setFocus(link.hash.slice(1), false);
    closeNav();
  }));
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('scroll', () => topButton.classList.toggle('visible', window.scrollY > 500), { passive: true });
  document.addEventListener('keydown', (event) => {
    const typing = /input|textarea|select/i.test(document.activeElement.tagName);
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      if (innerWidth <= 800) openNav();
      search.focus();
    } else if (event.key === '/' && !typing) {
      event.preventDefault();
      if (innerWidth <= 800) openNav();
      search.focus();
    } else if (event.key === 'Escape') {
      if (search.value) {
        search.value = '';
        filter();
        search.focus();
      } else {
        closeNav();
      }
    }
  });

  const observer = new IntersectionObserver((entries) => {
    if (body.classList.contains('focus') || search.value.trim()) return;
    const visible = entries.filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) setFocus(visible.target.id, false);
  }, { rootMargin: '-12% 0px -68% 0px', threshold: [0, .2, .6] });
  docs.forEach((doc) => observer.observe(doc));

  const params = new URLSearchParams(location.search);
  const requestedStatus = params.get('status');
  if (requestedStatus && Array.from(statusFilter.options).some((option) => option.value === requestedStatus)) {
    statusFilter.value = requestedStatus;
  }
  search.value = params.get('q') || '';
  setTheme(localStorage.getItem('qios-docs-theme')
    || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  setFocus(docMap.has(activeId) ? activeId : docs[0]?.id, false);
  filter();
})();
