# Current Project State

This receipt is the live verification record. The repo-side configuration snapshot lives in `50_generated_reports/current_project_state.md`.

Last inspected: 2026-05-29 on `qiserver`.

## Confirmed State

- QiAccess Start is deployed and working.
- The actual deployed runtime path is `/srv/qios/stacks/_qiaccess_start`.
- The tracked repo used for pull/build handoff is `/srv/qios/apps/_QiAccess_Start`.
- The confirmed repo remote is `git@github.com-qidocs:qiallyme/_QiAccess_Start.git`.
- The confirmed branch is `main`.
- The confirmed deployment method is Docker Compose running Homepage:
  - project: `qiaccess_start`
  - compose file: `/srv/qios/stacks/_qiaccess_start/docker-compose.yml`
  - container: `homepage`
  - image: `ghcr.io/gethomepage/homepage:latest`
  - local port: `127.0.0.1:3001 -> 3000`

## Codebase Structure Summary

- App framework: Homepage/gethomepage-derived Next.js dashboard branded as QiAccess.
- `src/`: React views, routing, layout, and registry states.
- `qiaccess/`: Homepage deployment config tracked in Git.
- `worker/`: Cloudflare edge worker configs for static/offline paths and CRUD bookmark planning.
- `docs/`: Canonical documentation tree and operational receipts.

## Config Merge And Deployment Receipt

The repo config files under `/srv/qios/apps/_QiAccess_Start/qiaccess/config` were merged using:

- live config as the source of truth for real working service URLs
- repo config as the source of truth for future-state grouping, layout, and styling

Updated repo files:

- `qiaccess/config/services.yaml`
- `qiaccess/config/bookmarks.yaml`
- `qiaccess/config/settings.yaml`
- `qiaccess/config/widgets.yaml`

The reviewed repo config was synced into the live stack config:

- `/srv/qios/stacks/_qiaccess_start/config/services.yaml`
- `/srv/qios/stacks/_qiaccess_start/config/bookmarks.yaml`
- `/srv/qios/stacks/_qiaccess_start/config/settings.yaml`
- `/srv/qios/stacks/_qiaccess_start/config/widgets.yaml`

Backup created before sync:

- `/srv/qios/stacks/_qiaccess_start/backups/config_20260528_232052/`

After sync, `homepage` was restarted through the confirmed `qiaccess_start` compose stack.

## Live Verification Receipt

Verified after sync:

- `homepage` was healthy.
- `http://127.0.0.1:3001` returned `200 OK`.
- `https://qiserver-1.cerberus-sirius.ts.net` returned `200 OK`.
- `https://access.qially.com` returned a Cloudflare Access login redirect for unauthenticated access.
- `/api/services` returned the merged groups: `QiAccess`, `Core Services`, `Knowledge + Archive`, `Data + Workflows`, `Finance`, `Server Control`, `Attention + Recovery`.

## Handoff Notes

- `/srv/qios/repos/_QiAccess_Start` also exists, but it is not the confirmed deployment checkout.
- `/srv/qios/stacks/_qiaccess_start/docker-compose.yml` contains sensitive Cloudflare tunnel material in the cloudflared stack area. Do not copy secrets into docs or chat.
- Server-side docs and config changes should be committed and pushed back to GitHub to avoid divergence from the local PC checkout.
- Older repo notes about placeholder URLs are superseded by the merged config and server verification receipts.

## Server Codex Follow-Ups

1. Keep `/srv/qios/apps/_QiAccess_Start` as the pull/build handoff checkout unless Cody decides otherwise.
2. Do not deploy from `/srv/qios/repos/_QiAccess_Start` without reinspection.
3. For future config changes, back up `/srv/qios/stacks/_qiaccess_start/config`, show the diff, sync only reviewed files, restart only `homepage`, and verify routes.
