# QiDNA Site Coverage Report

## Scope

Assessment date: 2026-06-10.

## Previous State

The site builder discovered only `.md` files. Fourteen `.mdx` documents were omitted, including the historical master map, source-of-truth rules, QiLife data spine, and module pages. Current and legacy documents appeared together without authority labels.

## Implemented Coverage

The builder now:

- discovers both `.md` and `.mdx`
- strips MDX frontmatter before Markdown rendering
- assigns every source document a status
- displays status in navigation and document headers
- defaults to Active documents
- provides Active, Legacy, Proposed, Generated, Evidence, and All filters
- retains search and focus mode
- provides a cascading folder-mirror directory tree
- provides a separate center-screen expandable mind map
- validates required canonical documents during the build

## Authority Behavior

Legacy and Evidence documents remain accessible but are hidden from the default Active view. Generated documents are visibly non-canonical. Proposed documents are not presented as accepted implementation contracts.

## Remaining Limitations

- MDX React components are not supported; current MDX files are Markdown-compatible and render after frontmatter removal.
- Status is path-derived rather than embedded in every source file.
- A future promotion changes the source location or classifier rule and requires review.
- The site is a reader, not the canonical source. Markdown and MDX files remain authoritative according to their status.

## Acceptance Test

The site is acceptable for blueprint review when:

- all Markdown and MDX source documents build
- every document has a visible status
- Active is the default view
- required canonical documents are present
- legacy evidence remains available without appearing current
- directory-tree and mind-map document nodes open the same rendered source page
