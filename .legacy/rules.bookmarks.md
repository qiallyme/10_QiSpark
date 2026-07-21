---
layout: page
title: Rules.bookmarks
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

# Rules: Bookmarks Integration

The homepage launcher loads bookmarks dynamically from the toolbox bookmarks database.

- **Source CSV**: `C:\QiLabs\00_QiLabs.workspace\toolbox\tools\access\qiaccess_bookmarks\bookmarks.csv`
- **Filtering**: Only bookmarks with `enabled = true` are imported.
- **Grouping**: Bookmarks are rendered in separate cards grouped by the `group` column.
