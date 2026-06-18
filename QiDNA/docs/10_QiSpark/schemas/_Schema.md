# Schema

## Overview

`Schema/` describes QiOS domains, entities, relationships, flows, and boundaries while distinguishing intent from verified implementation.

## Responsibilities

- Define shared system concepts.
- Link detailed schemas from their owning domain.
- Mark proposed structures as proposed.
- Avoid duplicating migrations or runtime configuration.

## Current Model

```text
QiAccess -> QiLife -> (QiSystem + QiNexus + QiCapture + QiConnect)
                         |
                      QiServer
```
