# ADR-0009: Backup Server Control Plane & Internet Access Layer

## Context

QiOS requires a pattern for deploying user-controlled, internet-accessible backup servers on secondary hardware. These nodes provide infrastructure services like local AI runtimes, data storage, and public application hosting. Historically, exposing such services often involved insecure port forwarding or mixing administrative and public traffic.

## Decision

QiOS adopts a dual-path access model for self-hosted infrastructure nodes:

1.  **Private Control Plane**: Administrative access (SSH, Docker Management, DB Admin) must occur exclusively over a secure private network overlay (e.g., Tailscale/WireGuard).
2.  **Public Edge Exposure**: Intentionally public services (portals, webhooks) must be exposed via an outbound tunnel (e.g., Cloudflare Tunnels) and routed through a local reverse proxy.

The node shall be organized into four conceptual runtime zones:
* **Zone A (Private Admin)**: No public routing.
* **Zone B (Public App)**: Governed tunnel/proxy path.
* **Zone C (Data Services)**: Internal-only state services.
* **Zone D (AI Execution)**: Internal-only model runtimes.

## Rationale

This approach:
* Minimizes the attack surface for administrative tools.
* Eliminates the need for inbound port forwarding on local networks.
* Separates internal data and AI concerns from public application exposure.
* Aligns with the QiOS doctrine of modular, governed device nodes.

## Consequences

* Increased security for self-hosted infrastructure.
* Requirement for a private network overlay and tunnel provider.
* Clearer operational boundaries for service deployment on infrastructure nodes.
