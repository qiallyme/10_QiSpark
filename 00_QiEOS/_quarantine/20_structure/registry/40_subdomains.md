# Subdomains

Subdomains are sub-groupings within a domain. They allow finer-grained namespace resolution without requiring a new Postgres schema.

## Namespace Pattern

```
{band}.{domain}.{subdomain}.{object}
```

Example: `b_domain.qicase.civil.case_record`

## Known Subdomains (v0.4)

| Domain | Subdomain | Description |
|---|---|---|
| `qicase` | `civil` | Civil litigation and dispute cases |
| `qicase` | `administrative` | Administrative and regulatory cases |
| `qitax` | `personal` | Individual tax returns |
| `qitax` | `business` | Business / entity tax returns |
| `qihome` | `expenses` | Household expense tracking |
| `qihome` | `chores` | Household task management |
| `qivault` | `contracts` | Contracts and agreements |
| `qivault` | `filings` | Court and regulatory filings |

## Subdomain Rules

* Subdomains are a **namespace convention**, not a separate database schema
* They are recorded in `registry/subdomain_registry.yaml`
* An object may belong to only one subdomain
* Subdomains do not create new FK relationships — they annotate existing ones via metadata
