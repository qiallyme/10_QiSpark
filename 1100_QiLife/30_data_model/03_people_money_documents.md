# People, Money, Documents Data Model

## People

People records are lightweight private records for individuals and entities involved in QiLife.

Canonical fields:

- `id`: ULID
- `display_name`
- `legal_name`
- `type`
- `relationship`
- `email`
- `phone`
- `address`
- `notes`
- `tags_json`
- `metadata_json`
- `created_at`
- `updated_at`
- `archived_at`
- `deleted_at`

## Transactions

Transactions log actual money movement.

Canonical fields:

- `id`: ULID
- `date`
- `amount_cents`
- `currency`
- `direction`
- `from_label`
- `to_label`
- `category`
- `bucket_code`
- `thread_id`
- `status`
- `notes`
- `evidence_document_id`
- `source_qibit_id`
- `created_at`
- `updated_at`
- `archived_at`
- `deleted_at`

Monetary values use integer cents, not floats.

## Obligations

Obligations track who owes what.

Canonical fields:

- `id`: ULID
- `owed_by_label`
- `owed_to_label`
- `obligation_type`
- `amount_cents`
- `currency`
- `reason`
- `status`
- `due_date`
- `related_transaction_id`
- `source_qibit_id`
- `created_at`
- `updated_at`
- `resolved_at`
- `archived_at`
- `deleted_at`

Canonical statuses:

```text
open
partial
waiting_on
resolved
disputed
archived
```

## Documents

Documents store file metadata only. Files remain on disk.

Canonical fields:

- `id`: ULID
- `title`
- `file_path`
- `source`
- `document_type`
- `bucket_code`
- `thread_id`
- `file_hash`
- `mime_type`
- `size_bytes`
- `notes`
- `created_at`
- `updated_at`
- `archived_at`
- `deleted_at`

## Relationship Rule

People, transactions, obligations, and documents can relate to QiBits, threads, and one another through a mix of direct foreign keys and `links`. Tags support retrieval, but links remain the canonical way to express known structure.
