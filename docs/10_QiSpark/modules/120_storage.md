# Storage

Storage is handled primarily via QiNexus and the local persistence structure.

## Storage Backbone

- Google Drive/QiNexus remains the primary storage backbone.

## Path Doctrine

- /srv/qios/data is for persistent app data.
- /srv/qios/stacks is for Docker Compose runtime stacks.
- /srv/qios/repos is for cloned Git repos and coding work.

## Conditional / Future Elements

*Note: Supabase Postgres and pgvector are not active doctrine unless a future retrieval pipeline explicitly needs them.*
