Here you go — save this as:

`docs/05_operations/qiaccess_static_docs_site_runbook.md`

---

# QiAccess Static Docs Site Runbook

## Purpose

QiAccess Start has two documentation layers:

1. **Wiki.js** — living self-hosted knowledge base and operating manual.
2. **Static Docs Site** — backup/published documentation site deployed with QiAccess Start through Cloudflare Pages.

The static docs site exists so the documentation remains reachable even if Wiki.js import/sync becomes messy, broken, or unavailable.

The goal is:

* `/` → QiAccess Start app
* `/docs/` → static documentation site

## Operating Doctrine

The repo remains the source of truth.

The static docs site is a published view of the repo documentation.

Wiki.js is still useful for live editing, readable manuals, and internal operating pages, but it should not become the only place the documentation exists.

## Final Architecture

```text
C:\QiLabs\_QiAccess_Start
├── docs/                 source Markdown documentation
├── docs-site/            VitePress configuration
├── scripts/              build/copy helper scripts
├── src/                  QiAccess React/Vite app
├── dist/                 final Cloudflare output
│   ├── index.html        QiAccess Start
│   └── docs/             static docs site
```

## URL Structure

Production:

```text
https://access.qially.com/
```

opens QiAccess Start.

```text
https://access.qially.com/docs/
```

opens the static docs site.

The QiAccess Start app should include a navigation card or menu item that links to:

```text
/docs/
```

This should be a normal anchor link, not a React Router route.

Correct:

```tsx
<a href="/docs/">Open Docs</a>
```

Avoid:

```tsx
<Link to="/docs">Open Docs</Link>
```

unless `/docs` is intentionally handled inside React.

## Build Model

Cloudflare Pages should build both the app and the docs site in one build.

Cloudflare build command:

```bash
npm run build:all
```

Cloudflare output directory:

```text
dist
```

The build process should:

1. Type-check and build the QiAccess React/Vite app.
2. Build the VitePress documentation site from `/docs`.
3. Copy the VitePress output into `dist/docs`.
4. Deploy the entire `dist` folder to Cloudflare Pages.

## Package Scripts

Recommended `package.json` scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -p tsconfig.app.json --noEmit && tsc -p tsconfig.node.json --noEmit && vite build",
    "build:app": "tsc -p tsconfig.app.json --noEmit && tsc -p tsconfig.node.json --noEmit && vite build",
    "preview": "vite preview",

    "docs:sync": "python scripts/sync_docs_site.py sync",
    "docs:build:legacy": "python scripts/sync_docs_site.py build",
    "docs:serve:legacy": "python scripts/sync_docs_site.py serve",

    "docs:dev": "vitepress dev docs --config docs-site/config.mts",
    "docs:build": "vitepress build docs --config docs-site/config.mts",
    "docs:copy": "node scripts/copy-vitepress-docs.mjs",
    "build:all": "npm run build:app && npm run docs:build && npm run docs:copy"
  }
}
```

## VitePress Role

VitePress is the static docs renderer.

It does not replace QiAccess Start.

It does not replace Wiki.js.

It simply turns the Markdown files in `/docs` into a static website.

Recommended config location:

```text
docs-site/config.mts
```

Recommended content source:

```text
docs/
```

Recommended base path:

```text
/docs/
```

Recommended temporary output:

```text
.vitepress-dist/
```

Recommended deployed output:

```text
dist/docs/
```

## Source of Truth Rules

The source Markdown files live in:

```text
C:\QiLabs\_QiAccess_Start\docs
```

Do not treat `dist/docs` as editable.

Do not edit generated HTML.

Do not treat Wiki.js as the only source of truth.

Correct flow:

```text
Edit docs in repo
→ commit changes
→ push to GitHub
→ Cloudflare builds QiAccess + docs
→ docs become available at /docs/
```

## Wiki.js Relationship

Wiki.js remains the living knowledge base.

The static docs site is the backup/published docs layer.

Recommended usage:

| System               | Job                                   |
| -------------------- | ------------------------------------- |
| Repo `/docs`         | Canonical source documentation        |
| Static `/docs/` site | Published backup/read-only docs       |
| Wiki.js              | Living KB, manuals, operational pages |
| QiAccess Start       | Front door and launcher               |

## Cloudflare Pages Settings

Set Cloudflare Pages to:

```text
Build command:
npm run build:all
```

```text
Output directory:
dist
```

If Cloudflare previously used:

```text
npm run build
```

change it to:

```text
npm run build:all
```

## QiAccess App Link

Add a card or navigation item in QiAccess Start.

Title:

```text
Docs
```

Description:

```text
Open the static QiAccess documentation site.
```

URL:

```text
/docs/
```

Access class:

```text
Public Restricted or Internal, depending on the deployment protection.
```

The link should open the static documentation site generated by VitePress.

## Why This Exists

Wiki.js import/sync can be useful but fragile.

The static docs backup solves this problem:

```text
If the repo builds, the docs build.
If Cloudflare deploys QiAccess, Cloudflare deploys the docs.
If Wiki.js is down, docs are still available.
```

This reduces operational friction and keeps the system recoverable.

## What Not To Do

Do not manually copy random docs into Wiki.js as the normal workflow.

Do not let the app repo, Wiki.js import folder, and static docs output all become separate competing truths.

Do not point the docs site at generated files.

Do not edit `dist/docs`.

Do not overbuild a custom React Markdown docs system unless VitePress fails the actual need.

Do not remove the existing Wiki.js workflow.

Do not remove the current MDX dependencies until the existing docs pipeline has been inspected and confirmed unused.

## Recommended Codex Task

Add a VitePress static documentation site to QiAccess Start.

Requirements:

1. Keep the existing QiAccess app at `/`.
2. Add a static documentation site at `/docs/`.
3. Keep source Markdown in `/docs`.
4. Add VitePress config under `/docs-site`.
5. Build the app and docs together with `npm run build:all`.
6. Copy the VitePress output into `dist/docs`.
7. Update Cloudflare Pages build documentation.
8. Add a QiAccess Start card/link to `/docs/`.
9. Do not remove the existing Wiki.js workflow.
10. Do not remove current MDX dependencies yet.
11. Do not convert the entire app to VitePress.
12. Inspect `scripts/sync_docs_site.py` before replacing or removing any existing docs pipeline.

## Local Testing

From Windows:

```powershell
cd C:\QiLabs\_QiAccess_Start
npm install
npm run build:all
```

Confirm output exists:

```text
dist/index.html
dist/docs/index.html
```

Preview the app:

```powershell
npm run preview
```

Then check:

```text
http://localhost:4173/
http://localhost:4173/docs/
```

## Deployment Check

After Cloudflare deploys, verify:

```text
https://access.qially.com/
https://access.qially.com/docs/
```

If `/` works but `/docs/` does not, check:

1. Did `npm run build:all` run in Cloudflare?
2. Does `dist/docs/index.html` exist after build?
3. Is the VitePress base set to `/docs/`?
4. Is QiAccess linking with `<a href="/docs/">` instead of React Router?
5. Is Cloudflare output directory set to `dist`?

## Final Rule

QiAccess Start is the front door.

Wiki.js is the living knowledge base.

The static docs site is the reliable published backup.

The repo remains the source of truth.
