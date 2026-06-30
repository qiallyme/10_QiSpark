# Legacy CSV Migration Plan & Audit

## 1. Executive Summary
The legacy CSV corpus contains immense operational value spanning CRM, accounting, and proprietary knowledge extraction. However, it is heavily polluted with duplicate subsets, deprecated structural matrixes, and extremely sensitive plaintext credential exports.

Importing this data directly into the canonical `qione` or `qiarchive` schemas is prohibited. It would violate single-source-of-truth principles and expose the system to dirty, non-normalized types.

Instead, all imported files must pass through `staging` isolated tables before mapped normalization.

## 2. Sensitive / Quarantine List 🚨
**IMMEDIATE ACTION**: The following files must be relocated to an offline encrypted store (e.g., 1Password or physical vault) and permanently shredded from the migration workspace. They must **never** touch Supabase or any web-facing database schema.

* `Chrome Passwords.csv` - Contains clear text browser credentials.
* `API Recovery Keys ... .csv` - Contains unencrypted infrastructure break-glass keys.

## 3. Migration Families
Files have been bucketed into 6 structural families to allow incremental, logical migration.

### Family 1: Contacts & CRM (The Entry Point)
* `contacts_cleaned.csv`, `contact_merged.csv`, `vendors_merged.csv`

### Family 2: Knowledge & Blueprint Memory
* `20251116_biz_ai_kb_full.csv`, `20251116_biz_blueprints_workflows_list.csv`
* `Notes_001.csv`, `gina_memory_rows.csv`

### Family 3: Communications & Timeline
* `raw_emails_combined.csv`, `db_RawEmails_KB ... .csv`, `Emails_001.csv`
* `conversations.csv`, `Meetings_001.csv`, `qimessages_C_001.csv`

### Family 4: Catalog & Services
* `master_services_catalog__all.csv`, `service_matrix.csv`, `Products_001.csv`

### Family 5: Finance & Accounting
* `Internal COA (OS)...csv`, `QiCode_Chart_of_Accounts_Mapping.csv`
* `Sales Orders_001.csv`, `Ordered Items_001.csv`, `Quoted Items_001.csv`, `Invoices_001.csv`

### Family 6: Governance & System Metadata (Archive/Preserve Only)
* `qios_rules_v1_1.csv`, `qios_matrix.csv`, `front_matter_schema_v1.csv`
* `realms_registry.csv`, `sensitivity_classification_*.csv`
* `Roles_001.csv`, `Modules_001.csv`, `file_system_nodes.csv`

---

## 4. Staging Schema Proposal
A dedicated `staging` schema is required inside Supabase. This acts as Zone B.

**Zone A** - Immutable Raw files (Stored on S3/Disk)
**Zone B** - `staging.raw_*` (Supabase: direct 1:1 CSV column dumps, text types only)
**Zone C** - `staging.norm_*` (Supabase: SQL views/tables converting dates, mapping UUIDs)
**Zone D** - Canonical Domains (e.g., `qione.contact`, `qicase.event`, `qihome.invoice`)

### Expected Staging Tables:
* `staging.csv_import_batches` (Tracks migration jobs)
* `staging.raw_contacts`
* `staging.raw_companies`
* `staging.raw_notes`
* `staging.raw_emails`
* `staging.raw_messages`
* `staging.raw_transactions`
* `staging.raw_products`
* `staging.raw_services`
* `staging.raw_blueprints`
* `staging.raw_agent_memory`

---

## 5. Canonical Destination Mapping
Once Zone C (normalized views) establishes clean relationships and valid types, data will be piped to canonical tables owned by specific downstream domains:

| Family | Staging Norm View | Canonical Target |
|--------|-------------------|------------------|
| **Contacts** | `staging.norm_contacts` | `qione.contact`, `qione.organization` |
| **Knowledge** | `staging.norm_notes` | `qiknowledge.note`, `qiarchive.file_record` |
| **Emails/Comms** | `staging.norm_messages` | `qicase.communication`, `qivault.raw_extract` |
| **Finance** | `staging.norm_transactions` | `qihome.transaction`, `qihome.invoice` |
| **Catalog** | `staging.norm_services` | `qihome.service_tier`, `qione.product` |

---

## 6. Matrix & Disposition

Every file maps to one of four rules:
1. **Quarantine**: Shred from disk. Never import. (Passwords, Keys)
2. **Archive**: Superseded by current blueprint. Do not import. Keep for reference. (Legacy governance matrixes)
3. **Preserve Only**: Keep raw but do not import. System irrelevant. (Roles, file system nodes)
4. **Migrate**: Send to staging. (Contacts, KBs, Emails, Finance)

## 7. Action Plan: First 10 Steps

To prevent contamination, we will prove the pipeline with the **Contacts** family first.

1. **Delete & Shred** `Chrome Passwords.csv` and `API Recovery Keys` from the staging directory to prevent accidental upload.
2. Initialize `staging` schema via a new standard Supabase migration file.
3. Create generic `staging.csv_import_batches` to track what file was ingested when.
4. Create empty table `staging.raw_contacts` with `TEXT` column types matching the header of `contacts_cleaned.csv`.
5. Write a small Python ingestion script using `supabase-py` or `psycopg2` to upload `contacts_cleaned.csv` into `raw_contacts`.
6. Query `staging.raw_contacts` to find distinct states, nulls, and duplicate email addresses.
7. Create `staging.norm_contacts` view casting text to timestamps, booleans, and generating deterministic UUIDs (e.g., using `uuid_generate_v5` against the email).
8. Verify the `norm_contacts` entity shape against the blueprint's `qione.contact` requirements.
9. Execute a bulk `INSERT INTO qione.contact SELECT * FROM staging.norm_contacts`.
10. Once CRM data is verified live in the Admin portal, repeat steps 4-9 for **Knowledge** (using `Notes_001.csv`).
