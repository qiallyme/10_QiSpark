---
title: QiAccess Start QA Checklist
date: 2026-05-17
type: qa-checklist
app: QiAccess Start
status: draft
tags:
  - qiaccess
  - qios
  - qa
  - testing
  - checklist
  - obsidian
---

# QiAccess Start QA Checklist

**Date Tested:**  
**Tester:** Cody  
**App Version / Branch:**  
**Device:**  
**Browser / OS:**  
**Environment:** Local / Dev / Production  
**Server / Host:** QiServer / Localhost / Tailscale / Cloudflare  
**Repo / Path:**  

---

## 1. App Startup & Access

- [ ] QiAccess Start opens without crashing.
- [ ] Homepage loads without blank screen.
- [ ] No console errors appear on initial load.
- [ ] App loads within a reasonable time.
- [ ] App works from local URL.
- [ ] App works from Tailscale URL if applicable.
- [ ] App works from Cloudflare/public URL if applicable.
- [ ] Page refresh does not break routing.
- [ ] Direct navigation to internal pages works.
- [ ] Browser back/forward navigation works.
- [ ] Favicon/title display correctly.
- [ ] App gracefully handles unavailable backend services.

### Notes

---

## 2. Main Landing Page / Home Screen

- [ ] Home screen clearly communicates this is QiAccess Start.
- [ ] Primary system links are visible.
- [ ] Most important services are easy to reach.
- [ ] Layout does not feel cluttered.
- [ ] Sections are visually separated.
- [ ] Cards/buttons are readable at a glance.
- [ ] Mobile layout remains usable.
- [ ] Desktop layout uses space well.
- [ ] Important alerts/status items are visible.
- [ ] User can quickly tell what to click next.

### Notes

---

## 3. Navigation & Information Architecture

- [ ] Main navigation is visible and predictable.
- [ ] Navigation labels are clear.
- [ ] QiAccess / QiNexus / QiNote / QiTools naming is consistent.
- [ ] Internal pages follow the same layout pattern.
- [ ] User can return to the home screen easily.
- [ ] Dead links are not present.
- [ ] External links open correctly.
- [ ] Links to local services use correct ports/paths.
- [ ] Links to Tailscale services work if configured.
- [ ] Links to Cloudflare services work if configured.
- [ ] Broken or unavailable services show a helpful message.

### Notes

---

## 4. Service Directory

- [ ] Service directory displays all expected services.
- [ ] Each service has a clear name.
- [ ] Each service has a short description.
- [ ] Each service has the correct local URL.
- [ ] Each service has the correct remote/private URL if applicable.
- [ ] Each service shows category/domain.
- [ ] Each service shows status if supported.
- [ ] Each service shows whether it is local-only, Tailscale, Cloudflare, or public.
- [ ] Service cards are easy to scan.
- [ ] Service metadata is not duplicated or conflicting.
- [ ] Deprecated services are hidden or clearly marked.
- [ ] Experimental services are clearly marked.

### Notes

---

## 5. Core Service Links

- [ ] Paperless-ngx link works.
- [ ] NocoDB link works.
- [ ] Open WebUI link works.
- [ ] Portainer link works.
- [ ] Wiki.js link works.
- [ ] Qdrant link/status is represented correctly.
- [ ] Neo4j link works if enabled.
- [ ] Uptime Kuma link works if enabled.
- [ ] SolidTime link works if enabled.
- [ ] n8n link works if enabled.
- [ ] Homepage link works if separate from QiAccess Start.
- [ ] Cloudflare tunnel/service links are correct if applicable.

### Notes

---

## 6. System Status / Health Indicators

- [ ] App shows system status if supported.
- [ ] Online/offline states are accurate.
- [ ] Status indicators are not misleading.
- [ ] Status checks fail gracefully.
- [ ] Service unavailable state is clear.
- [ ] App does not hang while checking service status.
- [ ] Refresh/update status button works if present.
- [ ] Last checked timestamp appears if present.
- [ ] Critical services are visually distinguished from optional services.
- [ ] Local-only limitations are clear.

### Notes

---

## 7. QiAccess Knowledge System Links

- [ ] Link to core documentation works.
- [ ] Link to governance documentation works.
- [ ] Link to architecture documentation works.
- [ ] Link to data documentation works.
- [ ] Link to compute/integrations documentation works.
- [ ] Link to services/apps documentation works.
- [ ] Link to operations/templates documentation works.
- [ ] Link to appendices/changelog works.
- [ ] Documentation links follow the numbered folder structure.
- [ ] App does not duplicate the knowledge base unnecessarily.
- [ ] App points users to the source of truth.

### Notes

---

## 8. QiNexus / Storage Map

- [ ] QiNexus root folders are represented correctly.
- [ ] Folder order follows the intended numbered hierarchy.
- [ ] Root categories include inbox.
- [ ] Root categories include workbench.
- [ ] Root categories include timeline.
- [ ] Root categories include life.
- [ ] Root categories include people.
- [ ] Root categories include business.
- [ ] Root categories include finance.
- [ ] Root categories include legal.
- [ ] Root categories include tech.
- [ ] Root categories include assets.
- [ ] Root categories include data.
- [ ] Root categories include reference.
- [ ] Root categories include archive.
- [ ] Root categories include system.
- [ ] Display names are clean and human-friendly.
- [ ] Numeric codes are visible only where helpful.
- [ ] Folder map does not force alphabetical order.

### Notes

---

## 9. Tools / Toolbox Integration

- [ ] QiOne / local toolbox entry point is visible.
- [ ] Tool categories are clear.
- [ ] Proven tools are separated from beta/experimental tools.
- [ ] Tool links or launch instructions are accurate.
- [ ] Tool descriptions explain the job in plain language.
- [ ] Standalone scripts are represented with README/manifest expectations.
- [ ] App does not present broken tools as production-ready.
- [ ] Directory Markmind Mapper is listed correctly if included.
- [ ] PDF splitter/compiler tools are listed correctly if included.
- [ ] Text extractor tools are listed correctly if included.
- [ ] Video/audio tools are listed correctly if included.
- [ ] Remote SSH/sys tools are listed correctly if included.

### Notes

---

## 10. Local-First / Network Mode Clarity

- [ ] User can tell whether they are using local, Tailscale, or public access.
- [ ] Local-only links are clearly labeled.
- [ ] Private remote links are clearly labeled.
- [ ] Public links are clearly labeled.
- [ ] App does not expose sensitive local URLs in public contexts unless intended.
- [ ] Cloudflare links do not accidentally point to localhost.
- [ ] Tailscale links are not shown as public links.
- [ ] App warns when a service requires VPN/private access.
- [ ] App avoids confusing duplicate links.
- [ ] Access mode is understandable at a glance.

### Notes

---

## 11. Authentication / Permissions

- [ ] Protected areas require login if applicable.
- [ ] Public areas do not expose sensitive data.
- [ ] Admin-only links are clearly marked.
- [ ] App avoids displaying passwords, keys, tokens, or secrets.
- [ ] Service links do not embed credentials.
- [ ] Environment variables are not exposed in frontend output.
- [ ] Console logs do not expose sensitive data.
- [ ] Error pages do not expose secrets.
- [ ] Permission boundaries are documented if applicable.
- [ ] Family/user-facing areas are separate from admin/dev areas if applicable.

### Notes

---

## 12. Search / Quick Find

- [ ] Search input appears if supported.
- [ ] Search can find services by name.
- [ ] Search can find services by category.
- [ ] Search can find documentation links.
- [ ] Search can find tools.
- [ ] Search handles partial terms.
- [ ] Search handles no results gracefully.
- [ ] Search is fast enough to use.
- [ ] Search works on mobile.
- [ ] Search does not break keyboard navigation.

### Notes

---

## 13. Mobile / Low-Friction Use

- [ ] App is usable on a phone.
- [ ] Tap targets are large enough.
- [ ] Text is readable without zooming.
- [ ] Cards do not become too cramped.
- [ ] Important actions are reachable quickly.
- [ ] App does not require precision clicking.
- [ ] User can quickly open a service while busy.
- [ ] Navigation does not bury critical links.
- [ ] Mobile view feels like a control panel, not a squeezed desktop page.
- [ ] App supports low-energy use.

### Notes

---

## 14. UI / UX Sanity Check

- [ ] Visual hierarchy is clear.
- [ ] Most important items are visually prioritized.
- [ ] Labels are plain language.
- [ ] Icons support meaning but do not replace labels.
- [ ] Cards/buttons have consistent styling.
- [ ] Spacing is clean.
- [ ] Page does not feel chaotic.
- [ ] Status colors are understandable.
- [ ] Color is not the only status indicator.
- [ ] User can understand the page without remembering the backend architecture.
- [ ] The app feels like a command center, not a link dump.

### Notes

---

## 15. Data / Config Integrity

- [ ] Service config loads correctly.
- [ ] Missing config does not crash the app.
- [ ] Invalid URL config shows a clear error.
- [ ] Duplicate service records are not shown unless intentional.
- [ ] Categories sort in intended order.
- [ ] Services sort in intended order.
- [ ] Deprecated records are handled correctly.
- [ ] App does not hardcode values that should live in config.
- [ ] Environment-specific settings are separated.
- [ ] Config changes are easy to review.

### Notes

---

## 16. Error Handling

- [ ] Broken service link gives useful feedback.
- [ ] Failed status check gives useful feedback.
- [ ] Missing config gives useful feedback.
- [ ] Failed API/backend call gives useful feedback.
- [ ] App does not show raw stack traces to normal users.
- [ ] Dev errors are available in dev mode.
- [ ] User knows what to do when something fails.
- [ ] App avoids silent failure.
- [ ] Failed state does not destroy the rest of the page.
- [ ] Retry/refresh behavior works if present.

### Notes

---

## 17. Documentation / README Alignment

- [ ] README explains what QiAccess Start is.
- [ ] README explains how to run it locally.
- [ ] README explains how to configure service links.
- [ ] README explains local/Tailscale/Cloudflare access modes.
- [ ] README explains where source config lives.
- [ ] README explains how to add a new service.
- [ ] README explains how to mark services as experimental/deprecated.
- [ ] README includes testing instructions.
- [ ] README includes troubleshooting notes.
- [ ] README matches the current app behavior.

### Notes

---

## 18. Build / Deployment

- [ ] Local dev server starts cleanly.
- [ ] Production build completes without error.
- [ ] Build output works when served.
- [ ] Environment variables are documented.
- [ ] Missing env vars produce clear errors.
- [ ] Static deployment works if applicable.
- [ ] Cloudflare Pages deployment works if applicable.
- [ ] Docker deployment works if applicable.
- [ ] App does not assume a single hardcoded machine path.
- [ ] Build does not include unnecessary files/secrets.

### Notes

---

## 19. Regression / Retest Checklist

Use this after Gemini, Codex, Aider, or another AI tool changes the app.

- [ ] App still starts.
- [ ] Home screen still loads.
- [ ] Main navigation still works.
- [ ] Service directory still displays.
- [ ] Core service links still work.
- [ ] Mobile layout still works.
- [ ] No new console errors.
- [ ] Existing fixed issue remains fixed.
- [ ] No obvious new bug was introduced.
- [ ] Documentation was updated if behavior changed.
- [ ] Config examples still match the app.
- [ ] Production build still succeeds.

### Notes

---

## 20. Final Acceptance Checklist

- [ ] QiAccess Start works as the system front door.
- [ ] User can reach key services quickly.
- [ ] User can understand local/private/public access mode.
- [ ] Service directory is accurate.
- [ ] Documentation links point to the right source of truth.
- [ ] Tool links are accurate and not misleading.
- [ ] Sensitive information is not exposed.
- [ ] App is usable on mobile.
- [ ] App feels calm, clear, and operational.
- [ ] Known issues are documented.
- [ ] AI work queue is clear for remaining fixes.

### Notes

---

# 2026-05-18 Initial Smoke Pass

**Environment:** Local preview  
**URL:** `http://127.0.0.1:4173`  
**Build:** Passed via `npm run build`  
**Direct route probe:** `/`, `/system`, `/knowledge`, and `/quick` all returned HTTP 200 in local preview  
**Rendered browser validation:** Blocked in this session because sandboxed Chromium/Edge headless runs failed with Windows access-denied profile/lock errors

## Initial Findings

### ISSUE-001 - Seven-root doctrine is not actually implemented

**Priority:** P1  
**Type:** UX / Navigation / Architecture  
**Area:** Navigation  
**Status:** Open

**Expected**  
QiAccess Start should reflect the declared seven roots: Home, Start, Capture, Knowledge, Memory, Insights, and System.

**Actual**  
`/start` redirects to `/`, and the visible nav tree exposes only `Home`, `Capture`, `Knowledge`, and `System`. `Memory` and `Insights` exist only as hidden route metadata rather than first-class navigation roots.

**Evidence**  
- `src/components/app/routes.tsx` defines `path: "start"` as a redirect to `/`
- `src/lib/navigation.ts` only exports four visible top-level nav items

**Impact**  
The app does not match its documented information architecture, which makes the QA checklist and the portal doctrine diverge.

### ISSUE-002 - Blueprint quick link points to a route that does not exist

**Priority:** P1  
**Type:** Bug / Docs / Navigation  
**Area:** Docs  
**Status:** Open

**Expected**  
Quick links and doctrine docs should only point to implemented app routes.

**Actual**  
`DocLayout.tsx` links to `/system/blueprint`, but the router does not define `/system/blueprint`, `/system/roadmap`, or `/system/security`.

**Evidence**  
- `src/components/docs/DocLayout.tsx` links to `/system/blueprint`
- `src/components/app/routes.tsx` only defines `access`, `server`, `storage`, `integrations`, `settings`, and `diagnostics` under `/system`

**Impact**  
This creates a docs-to-app mismatch and likely dead links for users following the documented system structure.

### ISSUE-003 - README coverage is missing for the app root

**Priority:** P2  
**Type:** Docs  
**Area:** Documentation / README Alignment  
**Status:** Open

**Expected**  
The repo should have a README that explains what QiAccess Start is, how to run it, and how local/private/public access modes work.

**Actual**  
There is no `README.md` at the QiAccess Start repo root, so checklist items in section 17 cannot currently pass.

**Impact**  
Run/config/access behavior is only inferable from source and docs fragments instead of one canonical operator entrypoint.

# Issue Capture Template

## ISSUE-000 — Short Title

**Priority:** P0 / P1 / P2 / P3  
**Type:** Bug / UI / UX / Data / Config / Security / Performance / Docs / Deployment  
**Area:** Startup / Home / Navigation / Services / Status / Docs / Tools / Config / Build / Other  
**Status:** Open / Sent to AI / Fixed / Retest Needed / Closed / Deferred  

### Expected

What should have happened?

### Actual

What happened instead?

### Steps to Reproduce

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

### Evidence

Screenshot, traceback, console error, broken link, wrong URL, failed build output, etc.

### Impact

Why does this matter?

### AI Instruction

Tell the AI exactly what to fix.

Example:

Fix the QiAccess Start service directory so Paperless-ngx, NocoDB, Open WebUI, Portainer, Wiki.js, SolidTime, n8n, and Uptime Kuma display with correct labels, categories, and access mode tags. Do not redesign the entire layout. Preserve the existing component structure unless required. Add a short README note explaining how to update service links.

---

# AI Work Order Template

## QiAccess Start Work Order

**Goal:**  
Fix the highest-priority QiAccess Start issues without redesigning unrelated architecture.

## Rules

- [ ] Fix P0 and P1 issues first.
- [ ] Do not refactor unrelated systems.
- [ ] Do not rename QiAccess / QiNexus / QiNote / QiTools concepts without approval.
- [ ] Preserve the intended numbered hierarchy and source-of-truth structure.
- [ ] Keep the app local-first and access-mode aware.
- [ ] Do not expose secrets, tokens, passwords, or private credentials.
- [ ] Update README or dev notes if behavior/config changes.
- [ ] Summarize files changed, fixes made, and how to retest.

## Issues to Fix

- [ ] ISSUE-001:
- [ ] ISSUE-002:
- [ ] ISSUE-003:

## Done Criteria

- [ ] App launches.
- [ ] Home screen loads.
- [ ] Core service links work.
- [ ] Service directory is accurate.
- [ ] Mobile layout is usable.
- [ ] No new obvious console errors.
- [ ] Production build succeeds.
- [ ] Retest checklist passes.
