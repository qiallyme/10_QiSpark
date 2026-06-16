# Legacy Data Bridge
QiLife should not inherit old Supabase schema chaos.

## Doctrine
- QiLife uses a clean canonical schema.
- Existing Supabase tables are legacy sources.
- Preserve/export Supabase data.
- Inventory tables, stage legacy rows.
- Selectively migrate useful records.
- Import messy useful rows as legacy QiBits.
- Supabase is not the runtime source of truth.

## Planned Legacy Bridge Tables
- `legacy_sources`
- `legacy_tables`
- `legacy_records`
- `legacy_mappings`
- `legacy_import_runs`
