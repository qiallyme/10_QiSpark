# QiAccess

## Status and Authority

**Active.** QiAccess is the Homepage-powered front door and operational launcher for the Qi ecosystem.

Verified on 2026-06-12:

- Live stack: `/srv/qios/stacks/_qiaccess_start`
- Live service: `homepage`, healthy when inspected
- Runtime bind: `127.0.0.1:3001 -> 3000`
- Implementation repository: `/srv/qios/repos/_QiAccess_Start`
- Inspected repository commit: `07268d4`
- Live deployed configuration is authoritative for working routes and current grouping.
- Repository configuration is the maintained deployment source but may lag the live stack until synchronized.

## Role & Cockpit Boundary

QiAccess answers:

```text
Where do I go next, and how do I safely reach the correct system surface?
```

It surfaces tools, docs, service links, server entry points, current priorities, and operating dashboards. QiAccess is the interface layer for QiOS and is not the whole operating system itself:

- Runtime belongs to [QiServer](../30_QiServer/_30_QiServer.md).
- Doctrine belongs to [QiEOS / QiOS DNA](../00_QiEOS/_QiEOS.md).
- Rules and schemas belong to [QiSystem](../20_QiSystem/_20_QiSystem.md).
- Storage belongs to [QiNexus](../50_QiNexus/_50_QiNexus.md).

## Ownership Boundaries

- Homepage owns the dashboard UI and grouping.
- QiServer owns container runtime and service execution.
- Cloudflare owns the protected public edge route and offline/recovery edge behavior.
- Tailscale owns private network reachability.
- Terminal, Cockpit, Portainer, and linked applications own real control actions.
- QiDNA owns canonical system documentation.
- QiAccess must not become a duplicate database, documentation authority, or runtime control plane.

### Folder Documents
- [Bookmark Administration Plan](qilinks_bookmark_admin_plan.md): Project plan and details for bookmark/link management.

## Active Dashboard Groups

The live configuration currently defines:

1. QiAccess
2. Core Services
3. Knowledge + Archive
4. Data + Workflows
5. Finance
6. Server Control
7. Attention + Recovery
8. External / Mobile Functions
9. Admin Bookmarks
10. Docs & References

These are dashboard presentation groups, not new QiOS architecture roots.

## Configuration

Canonical live files:

```text
/srv/qios/stacks/_qiaccess_start/
├── docker-compose.yml
└── config/
    ├── settings.yaml
    ├── services.yaml
    ├── bookmarks.yaml
    ├── widgets.yaml
    ├── docker.yaml
    ├── custom.css
    └── custom.js
```

Maintained repository source:

```text
/srv/qios/repos/_QiAccess_Start/qiaccess/
```

## Deployment Rules

- Runtime facts and deployed config beat planning notes and stale repo URLs.
- Repository changes do not become live until deliberately synchronized to the stack.
- Never commit service tokens, widget credentials, passwords, or other secrets.
- Public, tailnet-only, and recovery routes must remain visibly distinct.
- A launcher link is navigation, not proof that the target service is healthy.
- Legacy custom React portal material must not be redeployed unless explicitly salvaged and documented.

## Documentation Boundary

Chronicle QiDNA remains the canonical documentation reader under ADR-0015. Wiki.js and BookStack may provide operational knowledge surfaces, but automated publication plans do not override source Markdown/MDX or create a second doctrine authority.
