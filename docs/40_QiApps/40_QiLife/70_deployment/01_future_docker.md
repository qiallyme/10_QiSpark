# Future Docker Deployment Plan

## Services

1. Frontend
2. Backend
3. SQLite-backed data volume for v1

## Canonical Database Path

Use `sqlite:////app/data/db/qilife.sqlite` inside the backend container.

## Compose Direction

- Mount `/app/data` as a persistent volume.
- Keep the repo docs mounted or baked into the image so the importer can read `docs/`.
- Preserve the same database path convention used in local development.

Postgres remains a later migration target, not a v1 dependency.
