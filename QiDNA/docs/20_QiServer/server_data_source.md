# QiSystem

## Overview

QiSystem is the operational integrity layer. It tracks evidence that the system is running correctly and keeps generated operational material separate from product, portal, and doctrine docs.

## Responsibilities

- Logs and operational records.
- Audits and validation outputs.
- Backup and restore references.
- Health checks and verification results.
- Generated reports.
- Generated indexes and inventories.
- Maintenance notes and cleanup tasks.

## Flows

```text
Runtime or service check
  -> health result
  -> audit or generated report
  -> maintenance action if needed
  -> retained QiSystem record
```

## Folder Structure & Table of Contents

### Mirrored Subfolders
- [10 Logs](10_logs/): Runtime and operational logs.
- [20 Audits](20_audits/): Validation and audit outputs.
- [30 Backups](30_backups/): Backup and restore references.
- [40 Health Checks](40_health_checks/): Verification and health inspection results.
- [50 Generated Reports](50_generated_reports/): Generated summaries and report artifacts.
- [60 Generated Indexes](60_generated_indexes/): Machine-readable indexes and inventories.
- [70 Maintenance](70_maintenance/): Maintenance notes and cleanup tasks.

### Core Documentation
- [Cloudflare Map](cloudflare.md): Cloudflare networking config and configuration details.
- [Docker Compose Stack Map](docker_compose.md): Mirror reference of Docker Compose configurations.
- [GetHomepage dashboard](gethomepage.md): Configurations for the homepage cockpit service.
- [Portainer manager](portainer.md): Portainer stack and container manager references.
- [Public Interfaces Contract](public_interfaces.md): Public domain mapping and certificates.
- [Tailscale mesh network](tailscale.md): Tailnet and private machine configuration.
- [Uptime Kuma dashboard](uptime_kuma.md): Configuration for monitor heartbeat status.
