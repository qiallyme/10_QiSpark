# Decision 0008: Managed Document Vault (Dup-Allergic)

## Context
Ingesting the same documents multiple times creates noise and fragments context.

## Decision
QiLife will implement a managed document vault that hashes every incoming file. The system will be dup-allergic, preventing duplicate blobs and flagging near-duplicates.

## Consequences
- Meaningful documents are separated from raw file objects.
- Requires building hashing, duplicate candidate review, and versioning flows.
- Allows safe, restorable deletion before purging.
