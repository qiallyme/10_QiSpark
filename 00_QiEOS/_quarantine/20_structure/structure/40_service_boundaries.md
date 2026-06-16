# Service Boundaries

## Public vs. Private Boundaries

- The public side is heavily locked down.
- The internal tailnet runs unauthenticated surfaces safely.
- Application frontends handle public-facing operations.

### The Two Launch Surfaces
To maintain this boundary, there are strictly two separate launch surfaces:
1. **`access.qially.com`**: The external/public static React app deployed through Cloudflare. Service links are maintained in the app's source code data files.
2. **`qiserver-1.cerberus-sirius.ts.net`**: The private Tailscale server utility (`gethomepage`). Its configuration lives at `/srv/qios/stacks/_qiaccess_start/config/services.yaml`. Editing this server file does *not* update the public landing page.

## Administrative Boundaries

- Admin/control services (e.g. Portainer, NocoDB, Ollama) must stay private/protected.

## System Subroutes

System owns:

- /system/access
- /system/server
- /system/storage
- /system/integrations
- /system/settings
- /system/blueprint
- /system/roadmap
- /system/security
- /system/diagnostics

## Legacy Boundaries (Quarantined)

*Note: Old tenant, RLS, and Supabase boundary doctrine is considered future/conditional or reference-only.*
