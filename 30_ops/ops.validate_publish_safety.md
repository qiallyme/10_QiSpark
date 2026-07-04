---
layout: page
title: Ops.validate Publish Safety
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

# Operations Runbook: Validate Publish Safety

Before executing git push on `10_QiSpark`, run an audit or inspect `dist/docs` to verify that no private information (keys, secure credentials, internal logs) was accidentally built.
