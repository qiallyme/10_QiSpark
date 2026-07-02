# Source Map: QiVault to QiSpark

This document outlines the pipeline flow between the source database and the published static layout.

- **QiVault** (`C:\QiLabs\40_QiVault`) is the canonical source content layer.
- **QiSpark** (`C:\QiLabs\10_QiSpark`) is the static site/publisher layer.
- **QiSpark/dist** (`C:\QiLabs\10_QiSpark\dist`) is the generated output.

## Safety Rules & Core Boundaries

1. **Only publish-approved QiVault markdown enters the site**: Any file compiled must have status set to `publish`, `published`, or `public`.
2. **Private/sensitive/confidential content must not publish**: Any file marked with sensitive classification or private flags must be ignored by the compiler.
3. **Read-Only Source**: The build script treats the source directory as strictly read-only to prevent editing or deleting files in the primary vault.
