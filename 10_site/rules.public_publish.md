# Rules: Public Publishing

This document defines the strict filtering guidelines that prevent private content leakage during site builds.

## 1. Inclusion Filter (White-list)
A file is only compiled if its front-matter `status` property matches one of:
- `publish`
- `published`
- `public`

## 2. Exclusion Filter (Black-list)
Any file matching any of the following is immediately skipped:
- `sensitivity` contains `private`, `sensitive`, or `confidential`.
- `classification` contains `private`, `sensitive`, or `confidential`.
- Explicit boolean flags like `private`, `sensitive`, or `private_theory_flag` are set to `true` or `"yes"`.
