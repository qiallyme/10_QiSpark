# QiDNA Documentation Site

## Status

Active.

## Overview

`site/` contains the generated single-page reader for the QiDNA master blueprint. Source Markdown and MDX remain canonical according to their document status; `site/index.html` is a derived reading surface.

## Responsibilities

- Render all repository Markdown and MDX source documents.
- Default to Active documents while preserving access to Legacy, Proposed, Generated, and Evidence material.
- Mirror the physical repository hierarchy in a cascading, collapsible left-side directory tree.
- Provide an optional center-screen mind map using the same folder and document hierarchy.
- Open the selected source document section from either navigation mode.
- Preserve search, focus mode, theme selection, responsive behavior, and status filtering.

## Navigation Modes

### Directory Tree

The primary left navigation mirrors folders recursively rather than grouping documents by full path.

```text
01_QiDNA
  -> Architecture
     -> Decisions
        -> ADR document
```

Folder rows expand or collapse. Selecting a document opens its rendered page and expands its ancestor folders.

### Mind Map

The Mind Map button opens a separate center-screen visual navigator. It supplements the directory tree and does not replace it.

- The QiDNA root is centered.
- Top-level folders branch to both sides.
- Selecting a folder expands or collapses that branch.
- Selecting a document exits the map and opens that document page.
- The active status filter controls which documents appear.
- Collapse and Fit controls reset the view.

## Build Flow

```text
Markdown and MDX sources
  -> build.js discovers and classifies documents
  -> folder paths become tree and mind-map data
  -> site/style.css and site/script.js are embedded
  -> site/index.html is generated
```

Run:

```text
npm run build
```

## File Roles

```text
site/
├── _site.md     active documentation for the reader
├── script.js    source behavior for search, tree, and mind map
├── style.css    source presentation for the reader
└── index.html   generated single-page output
```

## Authority Rules

- `_site.md`, `script.js`, `style.css`, and `build.js` define the reader behavior.
- `index.html` is generated and must not be edited directly.
- Navigation visibility does not change a document's authority.
- Legacy evidence remains available but does not appear as Active.
