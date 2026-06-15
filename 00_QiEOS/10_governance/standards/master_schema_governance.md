# QiOS Master Schema Governance

## 1. Purpose

This document defines the canonical database schema strategy for the QiOS ecosystem.

The goal is to prevent database sprawl, duplicate tables, unclear ownership, and accidental coupling between modules.

The database should reflect **domain ownership**, not temporary folder placement.

A file’s current folder tells us where it lives.

A database schema tells us who owns its meaning.

---

# 2. Core Principle

## Schemas map to major system domains, not every folder.

Top-level Qi modules may become database schemas when they represent a real ownership boundary.

Subfolders should usually become:

* tables
* views
* enum groups
* metadata records
* file paths
* ingestion categories
* documentation sections

They should not automatically become schemas.

---

# 3. Canonical Schema Naming Rules

## 3.1 Schema names

All database schemas use:

* lowercase
* no spaces
* no hyphens
* `qi` prefix where the schema represents a canonical Qi module

Examples:

```text
qieos
qisystem
qinexus
qiaccess
qilife
qiconnect
qiserver
qivault
```

## 3.2 Table names

Tables use:

* lowercase
* snake_case
* plural nouns unless there is a strong reason otherwise

Examples:

```text
qieos.fields
qieos.field_usages
qinexus.files
qinexus.import_batches
qiserver.services
qilife.timeline_items
```

## 3.3 Column names

Columns use:

* lowercase
* snake_case
* clear semantic naming
* no ambiguous abbreviations unless standardized

Examples:

```text
created_at
updated_at
source_system
external_id
canonical_status
sensitivity_level
```

---

# 4. Required Core Schemas

## 4.1 `core`

The `core` schema contains global primitives used across the whole ecosystem.

It should stay boring, stable, and reusable.

### Owns

* people
* organizations
* locations
* entities
* identifiers
* relationships
* tags
* notes
* attachments
* audit metadata

### Example tables

```text
core.entities
core.people
core.organizations
core.locations
core.identifiers
core.relationships
core.tags
core.entity_tags
core.notes
core.attachments
core.audit_events
```

### Rule

If a concept is used everywhere and does not belong to one app, it probably belongs in `core`.

---

## 4.2 `qieos`

The `qieos` schema contains doctrine, standards, governance, canonical definitions, field registries, and system rules.

This is the database home for the “master fields table” concept.

### Owns

* canonical modules
* field registry
* field usages
* schema registry
* table registry
* status registry
* relationship type registry
* naming standards
* architectural decisions
* governance rules

### Example tables

```text
qieos.modules
qieos.schemas
qieos.tables
qieos.fields
qieos.field_usages
qieos.field_dependencies
qieos.statuses
qieos.relationship_types
qieos.naming_standards
qieos.rules
qieos.adr_records
```

### Rule

QiEOS defines what things mean.

It does not store operational runtime data unless that data is governance metadata.

---

## 4.3 `qisystem`

The `qisystem` schema contains the map of the operating system itself.

It describes the applications, modules, capabilities, surfaces, routes, and system boundaries.

### Owns

* app registry
* module registry
* feature registry
* route registry
* permission model
* capability model
* environment model
* system configuration metadata

### Example tables

```text
qisystem.apps
qisystem.modules
qisystem.features
qisystem.routes
qisystem.capabilities
qisystem.permissions
qisystem.environments
qisystem.config_items
```

### Rule

QiSystem maps the system.

QiEOS defines the doctrine.

QiServer runs the machine.

Do not merge those three.

---

## 4.4 `qinexus`

The `qinexus` schema contains file, source, archive, document, and ingestion metadata.

QiNexus owns the index of source material.

It does not necessarily store every raw file directly inside the database.

### Owns

* source systems
* files
* file versions
* import batches
* ingestion jobs
* extracted text references
* document metadata
* source-to-entity links
* migration intake tracking

### Example tables

```text
qinexus.sources
qinexus.files
qinexus.file_versions
qinexus.import_batches
qinexus.import_files
qinexus.ingestion_jobs
qinexus.extracted_text
qinexus.document_links
qinexus.source_entity_links
```

### Rule

Raw CSVs, PDFs, scans, exports, and evidence belong under QiNexus ownership.

The database tracks them, classifies them, and links them.

The database should not casually absorb raw messy exports as final tables.

---

## 4.5 `qiaccess`

The `qiaccess` schema contains front-door capture, intake, and access-layer events.

QiAccess is where information enters the system.

It does not own all data that passes through it.

### Owns

* capture events
* quick entries
* intake sessions
* user surfaces
* entry routes
* temporary intake payloads
* classification handoff records

### Example tables

```text
qiaccess.capture_events
qiaccess.quick_entries
qiaccess.intake_sessions
qiaccess.entry_routes
qiaccess.user_surfaces
qiaccess.classification_queue
qiaccess.handoff_events
```

### Rule

QiAccess captures.

Other schemas own the final meaning.

A medical note captured through QiAccess does not become `qiaccess.medical_notes`.

It should become a care, life, document, or entity record depending on meaning.

---

## 4.6 `qilife`

The `qilife` schema contains personal operating data, daily life events, care logs, tasks, timelines, and lived records.

### Owns

* timeline items
* tasks
* appointments
* care logs
* medications
* symptoms
* financial life events
* projects
* routines
* personal events

### Example tables

```text
qilife.timeline_items
qilife.tasks
qilife.appointments
qilife.care_logs
qilife.medications
qilife.symptoms
qilife.financial_events
qilife.projects
qilife.routines
```

### Rule

QiLife owns lived operational data.

It should not own server infrastructure, doctrine, raw document storage, or external sync mechanics.

---

## 4.7 `qiconnect`

The `qiconnect` schema contains integrations, external accounts, provider connections, sync jobs, webhooks, and external IDs.

### Owns

* providers
* connected accounts
* sync jobs
* webhook events
* external IDs
* API connection metadata
* integration health

### Example tables

```text
qiconnect.providers
qiconnect.connected_accounts
qiconnect.sync_jobs
qiconnect.webhook_events
qiconnect.external_ids
qiconnect.integration_health
qiconnect.api_token_refs
```

### Rule

QiConnect stores connection metadata and external system mapping.

It should not store plaintext secrets.

Secrets belong in secure storage, with references tracked by `qivault`.

---

## 4.8 `qiserver`

The `qiserver` schema contains infrastructure and runtime metadata.

It represents the server, services, containers, tunnels, ports, backup runs, and health checks.

### Owns

* hosts
* services
* containers
* ports
* tunnels
* backup runs
* health checks
* incidents
* runtime jobs
* deployment metadata

### Example tables

```text
qiserver.hosts
qiserver.services
qiserver.containers
qiserver.ports
qiserver.tunnels
qiserver.backup_runs
qiserver.health_checks
qiserver.incidents
qiserver.runtime_jobs
qiserver.deployments
```

### Rule

QiServer owns the machine and runtime.

It does not own random CSV exports, client data, website content, app source code, or doctrine.

---

## 4.9 `qivault`

The `qivault` schema contains sensitive-data metadata, secret references, access logs, redaction rules, and security classifications.

It should not become a plaintext password database.

### Owns

* secret references
* sensitive record metadata
* access events
* encryption key metadata
* redaction rules
* sensitivity classifications

### Example tables

```text
qivault.secret_refs
qivault.sensitive_records
qivault.access_events
qivault.encryption_key_metadata
qivault.redaction_rules
qivault.sensitivity_levels
```

### Rule

QiVault tracks sensitive data safely.

Actual secrets should live in a proper secret manager or encrypted storage.

The database may store references, hashes, labels, and access metadata.

---

# 5. Optional Future Schemas

Optional schemas should only be created when the domain has enough gravity to justify its own boundary.

Do not create optional schemas just because a folder exists.

## 5.1 Possible future schemas

```text
finance
legal
care
content
qially
lumara
clients
```

## 5.2 Creation test

A new schema is allowed only if at least three of the following are true:

* It has its own lifecycle.
* It has its own permissions model.
* It has many tables.
* It has independent business logic.
* It integrates with external systems.
* It has sensitive boundaries.
* It has a separate product/app identity.
* It would become messy if forced into another schema.

---

# 6. Folder-to-Schema Interpretation Rules

## 6.1 Physical folder does not equal database schema

Example:

```text
30_QiServer/data/csv/Fields_001.csv
```

This file physically sits under QiServer, but its meaning may belong to:

```text
qieos.fields
qieos.field_usages
qinexus.import_batches
qinexus.files
```

It should not become:

```text
qiserver.csv_fields
```

unless the CSV specifically describes server infrastructure fields.

## 6.2 Ownership beats location

When deciding schema placement, ask:

1. What does this record mean?
2. Which module owns that meaning?
3. Which module governs its lifecycle?
4. Which module would be damaged if this data were wrong?
5. Which module needs permission/control over this data?

The answer determines the schema.

---

# 7. Master Registry Tables

QiOS should maintain registry tables to prevent duplicate definitions.

## 7.1 Field registry

Canonical home:

```text
qieos.fields
```

Purpose:

Track every canonical field used across the system.

Example fields:

```text
id
field_key
display_name
description
data_type
canonical_format
sensitivity_level
allowed_values
created_at
updated_at
deprecated_at
```

## 7.2 Field usage registry

Canonical home:

```text
qieos.field_usages
```

Purpose:

Track where each field appears.

Example fields:

```text
id
field_id
schema_name
table_name
column_name
required
unique
indexed
default_value
usage_notes
```

## 7.3 Schema registry

Canonical home:

```text
qieos.schemas
```

Purpose:

Track approved schemas and ownership.

Example fields:

```text
id
schema_name
owning_module
purpose
status
created_at
updated_at
deprecated_at
```

## 7.4 Table registry

Canonical home:

```text
qieos.tables
```

Purpose:

Track approved tables and their meaning.

Example fields:

```text
id
schema_id
table_name
purpose
owner
status
sensitivity_level
source_of_truth_policy
created_at
updated_at
deprecated_at
```

---

# 8. Source-of-Truth Rules

Every table should declare its source-of-truth policy.

Allowed values:

```text
canonical
derived
imported
cached
runtime
staging
archived
external_reference
```

## Definitions

### `canonical`

The table is the official source of truth inside QiOS.

### `derived`

The table is generated from other canonical data.

### `imported`

The table stores imported data from an external source.

### `cached`

The table stores replaceable cache data.

### `runtime`

The table stores operational runtime state.

### `staging`

The table stores temporary pre-review data.

### `archived`

The table stores historical or inactive data.

### `external_reference`

The table points to an external source but does not own the full record.

---

# 9. Sensitivity Rules

Every schema and table should support sensitivity classification.

Suggested levels:

```text
public
internal
private
sensitive
restricted
secret
```

## Default sensitivity by schema

```text
core: private
qieos: internal
qisystem: internal
qinexus: private
qiaccess: private
qilife: sensitive
qiconnect: sensitive
qiserver: internal
qivault: restricted
```

## Rule

No table should silently accept sensitive data without classification.

If a table can contain medical, legal, financial, identity, passwords, API keys, or private relationship data, it must be classified.

---

# 10. Ingestion Flow

Raw data should move through a controlled pipeline.

## Standard flow

```text
Raw file
→ qinexus.files
→ qinexus.import_batches
→ staging table or extracted payload
→ review/classification
→ canonical target schema
→ source link retained
```

## Example

A Zoho contacts CSV should flow as:

```text
CSV file in QiNexus
→ qinexus.files
→ qinexus.import_batches
→ staging.zoho_contacts
→ review/dedupe
→ core.people / core.organizations
→ qiconnect.external_ids
```

It should not be directly dumped into final production tables.

---

# 11. Staging Strategy

A dedicated staging schema may be used during migration.

Recommended staging schema:

```text
staging
```

### Example tables

```text
staging.notion_tasks_raw
staging.zoho_contacts_raw
staging.zoho_invoices_raw
staging.mmex_transactions_raw
staging.chrome_passwords_quarantine
```

## Rule

Staging tables are temporary.

They are not canonical.

Every staging table must have:

```text
import_batch_id
source_file_id
row_number
raw_payload
review_status
created_at
```

---

# 12. Relationship Strategy

Relationships should be explicit.

Do not rely only on scattered foreign keys when the system needs flexible graph behavior.

## Recommended approach

Use normal foreign keys for strong structural relationships.

Use `core.relationships` for flexible cross-domain relationships.

### Example

A person can be related to:

* an organization
* a document
* a task
* a care event
* a legal matter
* a project
* an external account

Canonical flexible relationship table:

```text
core.relationships
```

Suggested fields:

```text
id
source_entity_id
target_entity_id
relationship_type
relationship_strength
start_date
end_date
status
notes
created_at
updated_at
```

---

# 13. Required Metadata Columns

Most canonical tables should include:

```text
id
created_at
updated_at
created_by
updated_by
status
source_system
source_file_id
import_batch_id
sensitivity_level
notes
```

Not every table needs every column, but missing metadata should be intentional.

---

# 14. Anti-Patterns

Avoid these.

## 14.1 Schema confetti

Do not make every folder a database schema.

Bad:

```text
docker
cloudflare
csv
docs
posts
json
yaml
sheets
```

Better:

```text
qiserver.services
qiserver.tunnels
qinexus.files
qieos.rules
content.posts
```

## 14.2 Location-based ownership

Bad:

```text
qiserver.csv_contacts
```

Better:

```text
qinexus.files
staging.zoho_contacts_raw
core.people
core.organizations
qiconnect.external_ids
```

## 14.3 Plaintext secrets in normal tables

Bad:

```text
qiconnect.api_keys
```

Better:

```text
qivault.secret_refs
qiconnect.api_token_refs
```

## 14.4 Duplicate fields everywhere

Bad:

```text
client_email
contact_email
person_email
primary_email_address
email_1
```

Better:

```text
qieos.fields
qieos.field_usages
core.identifiers
```

## 14.5 Raw imports pretending to be final data

Bad:

```text
core.zoho_contacts_import
```

Better:

```text
staging.zoho_contacts_raw
core.people
core.organizations
qiconnect.external_ids
```

---

# 15. First Approved Schema Set

The initial database should begin with:

```text
core
qieos
qisystem
qinexus
qiaccess
qilife
qiconnect
qiserver
qivault
staging
```

Optional schemas may be added later only after the creation test is passed.

---

# 16. Immediate Build Order

## Phase 1: Governance foundation

Create:

```text
qieos.schemas
qieos.tables
qieos.fields
qieos.field_usages
qieos.relationship_types
qieos.statuses
```

## Phase 2: Core primitives

Create:

```text
core.entities
core.people
core.organizations
core.identifiers
core.relationships
core.tags
```

## Phase 3: Source tracking

Create:

```text
qinexus.sources
qinexus.files
qinexus.import_batches
qinexus.import_files
```

## Phase 4: Intake and staging

Create:

```text
qiaccess.capture_events
staging.import_rows
```

## Phase 5: Runtime/system metadata

Create:

```text
qisystem.modules
qisystem.apps
qiserver.hosts
qiserver.services
qiserver.health_checks
```

---

# 17. Final Rule

The database should make QiOS easier to reason about.

If a schema, table, or field makes ownership less clear, it is probably wrong.

When in doubt:

```text
QiEOS defines.
QiSystem maps.
QiNexus stores/indexes.
QiAccess captures.
QiLife operates.
QiConnect syncs.
QiServer runs.
QiVault protects.
Core connects.
Staging cleans.
```
