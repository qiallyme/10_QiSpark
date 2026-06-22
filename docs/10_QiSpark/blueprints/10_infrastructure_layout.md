# Infrastructure Layout (Node-Local)

Infrastructure nodes (e.g., `infra.backup_server`) must follow a standardized persistent path pattern to ensure reproducibility, backup compatibility, and operational clarity.

## Recommended Persistence Pattern

The following pattern is the approved baseline for local persistence under the `C:/QiLabs/` root.

```text
/QiLabs/
  QiData/
    infra/
      backup_server/
        configs/     # Service-specific configuration files
        compose/     # Docker Compose / manifest files
        env/         # Access-controlled environment files (NOT in repo)
        exports/     # Temporary exports or reports
        logs/        # Rotated system and container logs
        backups/     # Scheduled local snapshots
        restore/     # Workspace for testing restore procedures
    services/
      postgres/      # Relational storage volumes
      vector/        # Vector database indices
      automation/    # Flow data and configs (e.g., n8n, Prefect)
      ai/            # Model weights and cache
      proxy/         # SSL certs and routing configs
```

## Persistence Rules

1.  **Separation of Concerns**: Service configurations must be separable from raw data volumes.
2.  **Backup Accessibility**: Local snapshots in `QiData/infra/backups/` must be accessible to off-node backup jobs.
3.  **Secret Management**: `.env` files and secret keys must reside in `QiData/infra/env/`, be access-controlled at the host level, and be strictly excluded from version control.
4.  **Logging**: Container logs should be directed to `QiData/infra/logs/` or managed by a host-level rotated logging service.
5.  **Restore Validation**: Every infrastructure node must maintain a `restore/` directory for periodic verification of data integrity.
