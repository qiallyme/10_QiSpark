# QiLife Schema Source Report

## Status

The missing-repository blocker was resolved on 2026-06-12. ADR-0018 reclassified the inspected SQLite system as legacy implementation and migration evidence on 2026-06-14.

## Verified Legacy Source

- Repository: `/home/qiadmin/qi_workspace/qilife`
- Inspected commit: `c589e1e`
- Models: `backend/app/db/models.py`
- Database: `data/db/qilife.sqlite`
- ORM metadata: `SQLModel.metadata`
- Migration integration: `backend/alembic/env.py`

The implementation contains 15 tables. It proves existing data shapes and workflows but is no longer canonical authority.

## Canonical Source

- Decision: `01_QiDNA/Architecture/Decisions/ADR-0018_supabase_qilife_data_authority.md`
- Field contract: `20_QiSystem/schemas/QiLife_Data_Spine.mdx`
- Catalog: `20_QiSystem/schemas/SCHEMA_CATALOG.md`
- Migration: `supabase/migrations/20260614162319_establish_qilife_entity_qibit_spine.sql`

## Transition Rule

No automatic conversion or deletion is authorized. Legacy tables must be mapped, validated, backed up, and cut over through a separate approved transition plan.
