---
title: QiAccess Server Runbook
status: active
updated: 2026-05-29
---

# QiAccess Server Runbook

## Confirmed Environment

- Host: `qiserver`
- Working account: `qiadmin`
- Operator home: `/home/qiadmin`
- Confirmed repo root: `/srv/qios/apps/_QiAccess_Start`
- Confirmed GitHub remote: `git@github.com-qidocs:qiallyme/_QiAccess_Start.git`
- Confirmed branch: `main`
- Confirmed runtime stack: Docker Compose project `qiaccess_start`
- Confirmed compose file: `/srv/qios/stacks/_qiaccess_start/docker-compose.yml`
- Confirmed runtime container: `homepage`
- Confirmed runtime image: `ghcr.io/gethomepage/homepage:latest`
- Confirmed local runtime URL: `http://127.0.0.1:3001`
- Confirmed public URL: `https://access.qially.com`
- Confirmed Tailscale URL: `https://qiserver-1.cerberus-sirius.ts.net`

There is also an older or alternate checkout at `/srv/qios/repos/_QiAccess_Start`. Do not deploy from it unless a fresh inspection proves it is the intended target.

## Runtime Model

QiAccess Start currently runs as a Homepage-powered dashboard. The live container does not serve the repo's `dist/` directory directly. The live stack bind-mounts:

- `/srv/qios/stacks/_qiaccess_start/config` to `/app/config`
- `/srv/qios/stacks/_qiaccess_start/public` to `/app/public`
- `/srv/qios/stacks/_qiaccess_start/config/images` to `/app/public/images`
- `/var/run/docker.sock` to `/var/run/docker.sock:ro`

The tracked repo contains the source versions under `qiaccess/config`, `qiaccess/docker-compose.yml`, and `public`. Treat the stack directory as the deployed runtime copy.

## Two-Codex Workflow

Local PC Codex:

1. Inspect and edit only the local repo.
2. Commit when the repo working tree is safe.
3. Push to GitHub.

Server Codex:

1. Inspect qiserver directly.
2. Confirm repo path, branch, remote, stack, ports, and working tree.
3. Pull from GitHub only after confirming the target branch and remote.
4. Compare live runtime state to repo intent.
5. Back up live config before overwriting it.
6. Deploy or restart only if needed.
7. Verify private and public routes after the server-side change.

GitHub:

- GitHub is the handoff layer between local repo changes and server deployment work.
- A push means "server can pull this," not "server already changed."

## Pull, Build, Restart, Verify

Inspect before every pull or deploy:

```bash
pwd
hostname
whoami
git -C /srv/qios/apps/_QiAccess_Start rev-parse --show-toplevel
git -C /srv/qios/apps/_QiAccess_Start remote -v
git -C /srv/qios/apps/_QiAccess_Start branch --show-current
git -C /srv/qios/apps/_QiAccess_Start status --short --branch
docker compose ls
docker compose -f /srv/qios/stacks/_qiaccess_start/docker-compose.yml ps
```

Fetch and pull only from the confirmed repo:

```bash
GIT_SSH_COMMAND='ssh -i /home/qiadmin/.ssh/qiserver_qiaccess_start -o IdentitiesOnly=yes' \
  git -C /srv/qios/apps/_QiAccess_Start fetch origin main

GIT_SSH_COMMAND='ssh -i /home/qiadmin/.ssh/qiserver_qiaccess_start -o IdentitiesOnly=yes' \
  git -C /srv/qios/apps/_QiAccess_Start pull --ff-only origin main
```

Build verification:

```bash
npm run build:all
```

Restart only when the live stack files or image require it:

```bash
docker compose -f /srv/qios/stacks/_qiaccess_start/docker-compose.yml up -d
docker compose -f /srv/qios/stacks/_qiaccess_start/docker-compose.yml restart homepage
```

Do not restart unrelated stacks. Do not deploy from `/srv/qios/repos/_QiAccess_Start` without re-confirming it is correct.

Live verification:

```bash
curl -fsS -I http://127.0.0.1:3001
curl -kfsS -I https://qiserver-1.cerberus-sirius.ts.net
curl -fsS -I https://access.qially.com
docker compose -f /srv/qios/stacks/_qiaccess_start/docker-compose.yml ps
```

Expected access behavior:

- `http://127.0.0.1:3001` returns `200 OK`.
- `https://qiserver-1.cerberus-sirius.ts.net` returns `200 OK` through Tailscale Serve.
- `https://access.qially.com` redirects to Cloudflare Access login when unauthenticated.

## Safety Rules

- Do not clone a second copy while a working repo exists.
- Do not overwrite `.env`, compose files, or runtime config without a backup and diff.
- Do not expose or copy Cloudflare tunnel tokens into docs or chat.
- Do not assume ports, public URLs, Tailscale URLs, remotes, branches, or deployment method.
