# QiApp QiLife

## Overview

QiLife is the private life operating app. It turns life chaos into QiBits that can be captured, triaged, routed, acted on, documented, resolved, reflected on, and retrieved.

## Responsibilities

- QiBits.
- Timeline projection.
- Buckets.
- Threads.
- Actions and steps.
- People, money, documents, events, and knowledge items.
- Context Dock.
- Activity log.
- AI outputs and retrieval.

## Flows

```text
Capture
  -> Bucket
  -> Interpret
  -> Relate
  -> Slot
  -> Breakdown
  -> Enrich
  -> Act
  -> Resolve
  -> Reflect
  -> Retrieve
```

## Structure

Core v1 tables: `qibits`, `buckets`, `threads`, `actions`, `action_steps`, `people`, `transactions`, `obligations`, `knowledge_items`, `documents`, `events`, `links`, `activity_log`, `ai_outputs`, and `daily_summaries`.

## Folder Structure & Table of Contents

### Mirrored Subfolders

- [00 Overview](00_overview/): General overview of QiLife client.
- [10 Product](10_product/): Product specification and features.
- [20 Architecture](20_architecture/): System architecture and data flow maps.
- [30 Data Model](30_data_model/): Data structures and DB mappings.
- [40 UI Flows](40_ui_flows/): Frontend layouts and wireframes.
- [50 Modules](50_modules/): Application feature modules.
- [60 AI Layer](60_ai_layer/): Prompt engineering, copilot, and agent interactions.
- [70 Deployment](70_deployment/): Deploy steps and environments.
- [80 Prompts](80_prompts/): System prompts and behavior definitions.
- [90 Decisions](90_decisions/): Architectural decision records (ADRs) for QiLife.
- [Planning](planning/): Project planning and backlog.
