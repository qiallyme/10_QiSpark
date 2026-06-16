# Migration Notes

This document tracks known migration concerns, schema drift, and reconciliation items from the v0.4 canonicalization effort.

## v0.4 Reconciliation Items

### Resolved

| Item | Resolution |
|---|---|
| 50+ unindexed foreign keys across all schemas | ✅ Indexes added in v0.4 migration |
| `nods_page` / `nods_page_section` — RLS enabled, no policies | ✅ Public read policy added |
| `todos` RLS evaluating `auth.uid()` per row | ✅ Rewritten with `(SELECT auth.uid())` |
| `qione.update_modified_column` mutable search_path | ✅ Pinned to `search_path = ''` |
| Principles count inconsistency (10 vs 7) | ✅ v0.4 canonical — 7 principles |
| Blueprint scattered across working notes and README files | ✅ Consolidated into this repo |

### Outstanding

| Item | Priority | Notes |
|---|---|---|
| `vector` extension in `public` schema | Medium | Should be moved to `extensions` schema — requires Supabase dashboard action |
| Leaked password protection disabled | High | Enable in Supabase Auth dashboard → [remediation](https://supabase.com/docs/guides/auth/password-security#password-strength-and-leaked-password-protection) |
| `enforce_structure.py` not in CI as blocking check | Medium | Wire into GitHub Actions second job |
| "Railway" references in earlier docs superseded by Supabase | Low | Resolved in this blueprint — no action needed in DB |
| Products schema not yet defined | Low | ADR required before creation |
| Templates schema not yet defined | Low | ADR required before creation |
| `public.match_page_sections` mutable search_path | Medium | Function still has mutable search_path — pin in next migration |

## Schema Migration History

| Migration | Applied | Description |
|---|---|---|
| `add_missing_fk_indexes_all_schemas` | 2026-03-27 | Added 50+ FK indexes across all schemas |
| `fix_security_rls_policies_and_functions` | 2026-03-27 | RLS policies, search_path fixes, todos policy rewrite |

## Naming Contract Change Log

| Previous | Current | Reason |
|---|---|---|
| No standard | `{domain}_{name}_{QXXXXXX}.ext` | Canonicalized in v0.4 |
| Informal table naming | `qi{domain}` schema naming | Enforced via domain registry |
