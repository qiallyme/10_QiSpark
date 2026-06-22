# Firefly

Firefly is the planned finance-management application for the QiAccess personal system.

Its job is to make money activity visible, reviewable, and reportable without turning daily life into accounting overhead.

## Purpose

Firefly should become the finance command layer for:

- account tracking
- transaction review
- category and context cleanup
- household and caregiver spending visibility
- exportable reporting

## Relationship To QiAccess

QiAccess should remain the front door.

Firefly should be a dedicated linked app that opens from QiAccess when the task is:

- reviewing spending
- tracking money movement
- preparing finance reports
- clarifying household, legal, business, or caregiver-related expenses

## Working Scope

Firefly is intended to cover:

- personal finance review
- household expense tracking
- caregiver-related costs
- business and legal expense visibility where needed
- reporting and export support

It should not try to become a bloated general-purpose accounting suite in the first version.

## MVP Direction

The first version should focus on:

1. accounts
2. transactions
3. import or manual entry
4. review inbox
5. categorization
6. reporting
7. exports

## Starting Workflows

### Daily use

1. Open Firefly from QiAccess.
2. Review new or uncategorized transactions.
3. Assign category, context, or person where needed.
4. Check current balances, spending, or recent activity.
5. Export or report when needed.

### Key reporting uses

- household spending
- caregiver support costs
- business or legal-related expenses
- uncategorized money that still needs cleanup

## Existing Reference

The earlier [QiLedger Blueprint](../80_productivity/qiledger.md) already contains a much deeper finance architecture draft.

Treat that page as source material for Firefly rather than the final product name.

## Initial Build Rule

Build Firefly as a dedicated app with a narrow finance mission.

Do not overload QiAccess Start with ledger screens that belong inside the finance app itself.

