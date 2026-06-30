# Metadata

## Metadata Philosophy

Metadata is not decoration. Metadata is the **minimum structure required** for the system to understand what something is, where it belongs, how it relates, and whether it can be trusted.

Metadata must be:
* **Incremental** — builds up over the pipeline, not all at once
* **Auditable** — every change is traceable
* **Structured** — stored in canonical fields, not free-text blobs
* **Attached to canonical identity** — orphaned metadata is useless
* **Preserved through movement and transformation**

## Minimum Metadata Classes

### Identity Metadata
| Field | Description |
|---|---|
| `canonical_id` | UUID or ULID — the machine truth |
| `domain_prefix` | Namespace grouping (e.g. `BBR4821`) |
| `short_code` | Q + 6 hex — human-visible code |
| `checksum` | SHA-256 fingerprint |

### Source Metadata
| Field | Description |
|---|---|
| `source_type` | How it entered (watcher, upload, sync) |
| `source_path` | Where it came from |
| `origin_event` | What triggered ingest |
| `original_filename` | Pre-normalization name |
| `imported_by` | User or system that imported |
| `ingest_timestamp` | When registration occurred |

### Structural Metadata
| Field | Description |
|---|---|
| `mime_type` | Detected MIME type |
| `extension` | Lowercase file extension |
| `chunk_count` | Number of chunks generated |
| `page_count` | Pages if applicable |
| `parser_method` | Which parser was used |
| `extraction_method` | How text was obtained |

### Semantic Metadata
| Field | Description |
|---|---|
| `document_type` | Inferred type (tax return, contract, etc.) |
| `inferred_entities` | Extracted entities |
| `tax_year` | If applicable |
| `matter_or_case` | Associated case if applicable |
| `tags` | Classification tags |
| `confidence` | AI classification confidence score |

### Lifecycle Metadata
| Field | Description |
|---|---|
| `status` | Current pipeline state |
| `review_state` | Awaiting, reviewed, confirmed |
| `route_state` | Suggested, confirmed, overridden |
| `storage_path` | Current physical location |
| `created_at` | Creation timestamp |
| `updated_at` | Last modified timestamp |

## Automation Gate

> **Minimum metadata required before any automation proceeds**: canonical_id, domain_prefix, short_code, source_path, ingest_timestamp, mime_type, status.

If these fields are absent, the pipeline must halt and flag the record as incomplete.

## Content Metadata Profile (Front Matter)

For flat files, notes, and unstructured assets, an optional **front matter** block may be applied. The specification is strictly governed by `standards/content_metadata_profile.yaml`.

> **CRITICAL DOCTRINE**: Front matter is **Supportive Metadata**. It is NEVER the system of record.
> 
> * Canonical identity comes from QiArchive.
> * Schema placement comes from the Pipeline.
> * Node topology comes from the Graph.
> 
> A document cannot change its database relationships purely by altering its front matter tags.

Common supportive fields defined in the profile include:
* `status`: Content-level draft/review state.
* `sensitivity` / `classification`: Governed by `registry/sensitivity_classification.yaml`.
* `realm_label`: An optional UI/UX workspace filter (e.g., `personal`, `work`, `legal`) governed by `registry/workspace_realms.yaml`. Realms do not dictate physical placement, tenant isolation, or schema mapping.
