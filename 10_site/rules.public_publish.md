---
layout: page
title: Rules.public Publish
slug: ""
summary: ""
status: active
created_at: ""
updated_at: ""
author: ""
owner: ""
tags: []
keywords: []
aliases: []
context: ""
sensitivity: internal
classification: business_internal
realm_label: ""
uid: ""
canonical_ref: ""
source_type: manual
template_key: master-template
---

# Rules: Public Publishing

This document defines the frontmatter contract and strict filtering rules that prevent private content leakage during site builds.

## 1. Publish States

Allowed general lifecycle values:
```yaml
status: active
status: draft
status: archived
status: deprecated
status: publish
status: published
status: public
```

Builder-published values:
```yaml
status: publish
status: published
status: public
```

*Note: `status: active` will not publish unless the builder is run with `--allow-active`.*

## 2. Visibility
```yaml
visibility: internal
visibility: private
visibility: public
```

## 3. Publish Target
```yaml
publish_target: none
publish_target: qispark
publish_target: qsaysit
publish_target: qially
```

For static docs compiled by the QiSpark compiler, set:
```yaml
publish_target: qispark
```

## 4. Public Page Minimum (Required to Publish)
To appear on the static QiSpark site, a document must use:
```yaml
status: publish
visibility: public
publish_target: qispark
sensitivity: public
classification: public
```

## 5. Internal Default (Safe Defaults)
All normal notes and templates must default to:
```yaml
status: active
visibility: internal
publish_target: none
sensitivity: internal
classification: business_internal
```
