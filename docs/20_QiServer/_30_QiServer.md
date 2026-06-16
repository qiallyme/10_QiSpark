# QiServer

## Overview

QiServer is the protected runtime host for internal services. It contains live Docker Compose stacks, system services, private access routes, public restricted routes, and runtime configuration paths.

Verified runtime facts win over repo planning notes.

## Responsibilities

- Host protected runtime services.
- Keep runtime stack paths and service facts clear.
- Separate public restricted access from private-only access.
- Run Docker Compose stacks and systemd services.
- Verify local, tailnet, and public routes after changes.

## Flows

```text
Inspect qiserver
  -> confirm repo, branch, remote, stack, ports, and working tree
  -> pull only from the confirmed repo
  -> back up runtime config before overwriting
  -> deploy or restart only the needed stack
  -> verify routes
```

## Folder Structure & Table of Contents

### Primary Documents
- [Service Map](Service_Map.md): Configuration mappings, ports, and route definitions for services.
- [QiServer Runbook](qiserver_runbook.md): Manual procedures, commands, and backup/restore steps.
- [Runtime Environment](runtime.md): Paths, locations, and setup details for runtime containers.
- [Runtime Profile](runtime_profile.md): Hardware, specs, and environment facts of host servers.
