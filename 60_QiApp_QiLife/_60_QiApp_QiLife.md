# QiApp QiLife

## Overview

QiLife is the private operational app and data spine. It captures reality as QiBits and relates those QiBits to persistent Entities.

## Canonical Concepts

- **Entity:** who or what.
- **QiBit:** event or unit of reality.
- Every canonical structured record is represented as an Entity or QiBit.
- QiBits may reference Entities.
- Files remain in QiNexus; Paperless may process documents without replacing file authority.

## Data Authority

Supabase Postgres is canonical under ADR-0018. SQLite is deprecated and limited to legacy, local, or transitional use.

## Baseline Structure

- `qi_entities.entities`
- `qi_entities.relationships`
- `qi_events.qibits`

The field contract is maintained in `20_QiSystem/schemas/QiLife_Data_Spine.mdx`. Additional tables require proven constraints or query needs and an accepted reconciliation decision.
