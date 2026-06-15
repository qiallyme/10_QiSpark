# QiAccess Homepage Conversion Report

Date: 2026-05-24

## Current Repo Classification

- Classification: mixed source + config workspace
- Reason:
  - Repo root contains a cloned `gethomepage/homepage` source tree and upstream docs.
  - Root also still contains local QiAccess-era wrapper files and duplicate artifacts from the pre-clone state.
  - Legacy material has started moving into `.legacy/`, but Git still shows tracked deletions from the older custom portal layout.

## Active Layout Decision

- Chosen layout: `qiaccess/`
- Reason:
  - Keeping the Homepage source clone intact at the repo root is less disruptive than moving upstream files.
  - The new `qiaccess/` directory cleanly separates active deployment config from both upstream source and legacy material.

## Files Created

- `qiaccess/README.md`
- `qiaccess/docker-compose.yml`
- `qiaccess/config/settings.yaml`
- `qiaccess/config/services.yaml`
- `qiaccess/config/bookmarks.yaml`
- `qiaccess/config/widgets.yaml`
- `qiaccess/config/docker.yaml`
- `qiaccess/config/custom.css`
- `qiaccess/config/custom.js`
- `qiaccess/config/images/README.md`
- `docs/notes/ADR-0011_homepage_powered_qiaccess.md`
- `_audit/2026-05-24_qiaccess_homepage_conversion_report.md`

## Files Modified

- `README.md`

## Legacy Folder Found

- `.legacy/_QiAccess_Start`

## Legacy Inspection Summary

- Present in `.legacy/_QiAccess_Start`:
  - `.npm-cache/`
  - `.runtime/`
  - `_audit/`
- Not found as physical moved directories inside `.legacy` during this pass:
  - `local/`
  - `web/`
  - prior Homepage config folders such as `local/config/`
- Those older paths are still visible in Git as tracked deletions from the pre-conversion tree, but they are not currently materialized inside `.legacy`.

## Salvage Candidates

| Current legacy path | Type | Salvage? | Destination | Notes |
| --- | --- | --- | --- | --- |
| `.legacy/_QiAccess_Start/_audit/2026-05-23_qiaccess_directory_intelligence_report.md` | old React QiAccess reference | Yes | `_audit/` reference only | Useful snapshot of the pre-conversion mixed workspace and prior portal sprawl. |
| `.legacy/_QiAccess_Start/.runtime/mkdocs/` | disposable generated output | No | N/A | Generated docs-site runtime output, not active deploy config. |
| `.legacy/_QiAccess_Start/.runtime/ci-test/` | disposable generated output | No | N/A | Build/test runtime cache only. |
| `.legacy/_QiAccess_Start/.npm-cache/` | disposable generated output | No | N/A | Package-manager cache only. |
| `Git-tracked deletions for local/, web/, run_copy.bat, and prior config files` | unknown | Pending | `.legacy/_QiAccess_Start/` if restored for reference | Not physically present in `.legacy` during this audit, so salvage remains unresolved. |

## Config Files Created or Updated

- Created:
  - `qiaccess/config/settings.yaml`
  - `qiaccess/config/services.yaml`
  - `qiaccess/config/bookmarks.yaml`
  - `qiaccess/config/widgets.yaml`
  - `qiaccess/config/docker.yaml`
  - `qiaccess/config/custom.css`
  - `qiaccess/config/custom.js`
- Updated:
  - `README.md`

## Deployment Assumptions

- Homepage should run from the official image `ghcr.io/gethomepage/homepage:latest`.
- Compose bind is local-only by default: `127.0.0.1:3001:3000`.
- Intended access modes:
  - Tailscale
  - Cloudflare Tunnel / `access.qially.com`
  - Local LAN only if the compose bind is intentionally widened later
- Docker socket is optional and remains commented out by default.

## Secrets and Env Warnings

- No secrets were printed.
- No real credentials were added to config.
- Widget-capable services were left with TODO comments rather than live keys.
- The only env-like file observed during inspection was `k3d/.envrc`; its contents were not printed or reused.

## Open Questions

- Should the host bind remain `127.0.0.1:3001`, or should QiServer expose a different local port for the canonical dashboard?
- Should the older `local/` and `web/` trees be explicitly restored into `.legacy/` so the archival state matches Git history?
- Which placeholder URLs should become Cloudflare-routed versus Tailscale-only?
- Which services should receive real Homepage widgets first once safe tokens are available?

## Next Manual Steps

1. Confirm the intended QiServer host port and reverse-proxy/tunnel target for the Homepage container.
2. Replace placeholder service URLs with verified runtime paths.
3. Add real widget tokens only through host-local secret handling, not by committing them here.
4. Decide whether to re-materialize the old `local/` and `web/` trees under `.legacy/` for a cleaner salvage archive.
5. Deploy later from `qiaccess/` only, leaving the upstream source tree untouched unless a future Homepage source patch is explicitly needed.
