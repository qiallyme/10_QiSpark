# QiAccess

## Overview

QiAccess is the portal and navigation shell for the system. It is the daily entry point for opening tools, seeing what needs attention, capturing quickly, and reaching system services.

## Role & Cockpit Boundary

QiAccess Start answers the core question:
```text
Where do I go next, and how do I safely get there?
```
It surfaces tools, docs, service links, server entry points, current priorities, and operating dashboards. QiAccess is the interface layer for QiOS and is not the whole operating system itself.

- Runtime belongs to [QiServer](../30_QiServer/_30_QiServer.md).
- Doctrine belongs to [QiEOS / QiOS DNA](../00_QiEOS/_QiEOS.md).
- Rules and schemas belong to [QiSystem](../20_QiSystem/_20_QiSystem.md).
- Storage belongs to [QiNexus](../50_QiNexus/_50_QiNexus.md).

## Responsibilities

- Provide the main portal and dashboard.
- Open real tools and services quickly.
- Present the seven-root navigation contract.
- Surface Capture as a fast path.
- Point Knowledge to canonical docs and references.
- Show System visibility without becoming the system layer itself.

## Flows

```text
Open QiAccess
  -> see Home for attention items
  -> use Start to open tools
  -> use Capture for immediate input
  -> use Knowledge for references
  -> use System for runtime visibility
```

## Structure

QiAccess active navigation has seven roots: Home, Start, Capture, Knowledge, Memory, Insights, and System. System subroutes stay nested under System.

### Folder Documents
- [Bookmark Administration Plan](qilinks_bookmark_admin_plan.md): Project plan and details for bookmark/link management.
