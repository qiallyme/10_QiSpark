# QiLedger Blueprint

## 1. Project Name

**QiLedger**
Working title: **FinanceOS Ledger**

A custom web-based money activity system for tracking, reviewing, categorizing, and reporting all financial activity across personal, household, business, legal, and caregiver-related money flows.

---

# 2. Core Goal

Build a centralized, web-based general ledger that captures **all money activity** across accounts and contexts, then turns that activity into clear, filterable, reportable records.

The system should answer:

> Who was money for?
> What was it spent on?
> When did it happen?
> Where did it come from?
> Which account touched it?
> Was it personal, household, business, legal, caregiver, or tax-related?
> Has it been reviewed?
> Can it support a report, reimbursement, tax record, legal record, or budget decision?

---

# 3. Problem Statement

Existing finance tools do not fit the actual use case.

## Current tool issues

### Money Manager Ex

Good local ledger, but:

* not web-based
* difficult to access across devices
* limited automation
* not ideal for household/business/legal blended reporting
* not built around modern API workflows

### Google Sheets / Excel

Flexible, but:

* messy over time
* weak relational structure
* poor audit trail
* hard to normalize vendors/categories/accounts
* not ideal for long-term automation

### QuickBooks

Rejected.

Reasons:

* too rigid
* too expensive
* too accountant-centric
* overbuilt for this blended personal/household/business/legal use case
* painful UI
* bad fit for fast personal operations

### Zoho Books / Quicken / Other Apps

Problems:

* freemium limits
* subscription traps
* too consumer-focused or too enterprise-focused
* weak custom reporting
* not designed around caregiver/household/legal/business overlap

---

# 4. Strategic Diagnosis

This project sits between categories:

## Not just personal budgeting

Because the system must handle:

* household contributions
* caregiver-related spending
* shared bills
* reimbursable items
* account transfers
* legal case expenses
* business expenses
* tax support
* recurring bills
* receipts and statements
* multiple people/entities

## Not full business accounting

Because the goal is not traditional bookkeeping first.

The goal is:

> Money intelligence first, formal accounting second.

## Not enterprise finance ops

Because it must remain lightweight, fast, and usable by one person under real-life pressure.

---

# 5. Product Philosophy

QiLedger is not trying to replace full accounting software immediately.

It is a **ledger intelligence layer**.

The system should prioritize:

1. Fast capture
2. Clean review
3. Unified transaction history
4. Easy categorization
5. Relationship tracking
6. Reporting by context
7. Audit support
8. Exportability
9. Automation readiness

The system should avoid:

* overbuilding
* full double-entry accounting in v1
* complex invoicing
* payroll
* tax filing
* bloated dashboards
* enterprise permissions
* unnecessary accounting jargon
* trying to become QuickBooks

---

# 6. Core Doctrine

## Doctrine 1: Postgres is the source of truth

The database is the real system.

The UI is replaceable.

No app builder, no-code platform, spreadsheet, or dashboard tool should become the foundation.

## Doctrine 2: Every money event becomes a normalized record

Raw bank data can be messy.

The system must normalize it into consistent transaction records.

## Doctrine 3: Imported data and reviewed data are separate

Never destroy the original import.

Use a staging/inbox model:

**Raw import → reviewed transaction → unified ledger**

## Doctrine 4: Reports are views, not separate spreadsheets

Once the ledger is clean, reports should come from filters and views.

Do not manually rebuild reports in separate files unless exporting for outside use.

## Doctrine 5: Build for real life, not perfect accounting theory

The first priority is operational clarity.

Formal accounting can be layered in later.

---

# 7. System Overview

## High-Level Flow

1. User imports or enters money activity.
2. Activity lands in a review inbox.
3. System normalizes vendor, category, account, person, project, and context.
4. User reviews and approves transaction.
5. Approved transaction becomes part of the unified ledger.
6. Reports and dashboards pull from the unified ledger.
7. Rules improve future categorization.

## Data Flow

**Bank / Card / Cash / Manual Entry**
→ **Import Batch**
→ **Raw Transactions**
→ **Money Inbox**
→ **Reviewed Ledger Transactions**
→ **Reports / Views / Exports**

---

# 8. Main User Experience

The daily experience should be fast.

The user should not feel like they are “doing accounting.”

They should feel like they are clearing an inbox.

## Primary workflow

1. Open QiLedger.
2. See unreviewed transactions.
3. Approve obvious items.
4. Fix unclear items.
5. Assign category/person/project.
6. Mark transfers.
7. Add notes or receipts where needed.
8. View reports when needed.

---

# 9. Core Screens

## 9.1 Money Inbox

The most important screen.

Purpose:

> Show transactions that need review.

### Key features

* list of unreviewed transactions
* quick approve button
* category dropdown
* person dropdown
* project/context dropdown
* vendor normalization
* transfer matching
* split transaction option
* notes field
* receipt attachment
* confidence indicator
* rule suggestion

### Filters

* account
* date range
* amount range
* vendor
* imported batch
* possible transfer
* needs category
* needs person
* needs project
* low confidence

---

## 9.2 Unified Ledger

The master transaction view.

Purpose:

> Show all reviewed money activity in one normalized table.

### Must support filtering by

* date
* account
* person
* category
* vendor
* project
* context
* amount
* direction
* reviewed status
* tax relevance
* legal relevance
* household relevance
* business relevance

### Transaction fields displayed

* transaction date
* account
* vendor/payee
* description
* amount
* direction
* category
* person
* project
* context
* reviewed status
* notes

---

## 9.3 Accounts

Tracks every place money can exist or move through.

Examples:

* Chase Checking
* Cash App
* PayPal
* Venmo
* Mom Clearing
* Zai Clearing
* Household Bills
* Business Income
* Legal Costs
* Cash on Hand
* Credit Card
* Prepaid Card

### Account types

* checking
* savings
* credit card
* cash
* digital wallet
* clearing account
* loan
* liability
* income source
* external account

---

## 9.4 Categories

The chart of accounts / reporting categories.

This does not need to be overly formal in v1.

Examples:

* Income
* Household Bills
* Groceries
* Medical
* Transportation
* Legal
* Business Expense
* Caregiver Expense
* Debt Payment
* Transfer
* Reimbursement
* Personal
* Emergency
* Subscriptions
* Taxes

---

## 9.5 Vendors / Payees

Normalizes messy bank descriptions.

Examples:

Raw:

* `WM SUPERCENTER #1341`
* `WALMART.COM 8009666546`
* `WAL-MART STORE`

Normalized:

* Walmart

Raw:

* `ASTOUND BROADBAND`
* `WOW INTERNET`
* `RCN ASTOUND`

Normalized:

* Astound Internet

---

## 9.6 People / Entities

Tracks who the transaction relates to.

Examples:

* Cody
* Mom
* Zai
* Household
* Client
* Court
* Vendor
* Business
* Legal Case
* Unknown

This is critical because normal apps do not understand blended household operations.

---

## 9.7 Projects / Contexts

Tracks why the money matters.

Examples:

* Household Operations
* Caregiver Support
* Legal Case
* Business Operations
* Tax Prep
* Vehicle Repair
* Mom Medical Support
* Home Repair
* QiLabs
* Personal Spending
* Emergency Reset

---

## 9.8 Reports

MVP reports should be simple and useful.

### Required reports

1. Cashflow report
   Money in vs money out.

2. Spending by category
   Where money went.

3. Spending by person/entity
   Who money was for.

4. Spending by account
   Which accounts were used.

5. Vendor report
   Who got paid.

6. Household report
   Shared household expenses.

7. Mom contribution report
   Contributions, expenses, balance, and usage.

8. Legal expense report
   Court, filing, document, transport, case-related costs.

9. Business expense report
   Tax/business-related expenses.

10. Uncategorized report
    Items needing cleanup.

11. Transfer report
    Movement between accounts.

12. Reimbursement report
    Items paid by one person/context that belong to another.

---

# 10. MVP Scope

## MVP must include

* web-based login
* accounts table
* categories table
* vendors table
* people/entities table
* projects/contexts table
* manual transaction entry
* CSV import
* raw transaction staging
* money inbox review screen
* unified ledger screen
* basic reports
* export to CSV
* mobile-friendly layout

## MVP should not include yet

* full double-entry accounting
* bank API integrations
* automatic Plaid sync
* invoice generation
* payroll
* inventory
* full tax filing
* OCR receipt processing
* AI categorization
* advanced permissions
* complex dashboards

Those come later.

Do not let v1 become a productivity swamp.

---

# 11. Recommended Tech Stack

## Frontend

**React + TypeScript + Vite**

Reason:

* fast
* familiar
* flexible
* works well with Supabase
* easy to make mobile-first
* supports future PWA use

## Backend / Database

**Supabase Postgres**

Reason:

* hosted Postgres
* auth included
* row-level security available
* APIs generated automatically
* can export/migrate
* works well with custom React apps

## Auth

**Supabase Auth**

MVP:

* single-user first
* later add household/support users if needed

## Storage

**Supabase Storage or Google Drive link references**

For:

* statement files
* receipts
* exported reports
* supporting documents

MVP can store file metadata first, then add actual upload later.

## Automation Layer

Later:

* n8n
* Python import scripts
* AI categorization worker
* statement parser
* Drive sync

---

# 12. Architecture

## Core architecture

**Frontend Web App**
→ Supabase client
→ Postgres tables
→ Views / RPC functions
→ Reports

## Optional later architecture

**Statement Upload**
→ Storage
→ Parser Worker
→ Raw Transactions
→ Rules Engine
→ Review Inbox
→ Unified Ledger

## Principle

The frontend should not contain the financial logic.

The database should enforce:

* required fields
* account relationships
* category relationships
* transaction integrity
* duplicate prevention
* review state

---

# 13. Core Data Model

## 13.1 `accounts`

Stores financial accounts and clearing accounts.

Important fields:

* `id`
* `name`
* `institution`
* `account_type`
* `owner_entity_id`
* `last_four`
* `currency`
* `is_active`
* `opening_balance`
* `notes`
* `created_at`
* `updated_at`

---

## 13.2 `entities`

People, household members, businesses, vendors, institutions, courts, etc.

Important fields:

* `id`
* `name`
* `entity_type`
* `default_context`
* `notes`
* `created_at`
* `updated_at`

Entity types:

* person
* household
* business
* vendor
* institution
* court
* client
* other

---

## 13.3 `categories`

Stores reporting categories.

Important fields:

* `id`
* `name`
* `parent_category_id`
* `category_type`
* `tax_relevant`
* `business_relevant`
* `household_relevant`
* `legal_relevant`
* `is_active`
* `notes`

Category types:

* income
* expense
* transfer
* liability
* asset
* adjustment

---

## 13.4 `vendors`

Normalized payees.

Important fields:

* `id`
* `name`
* `default_category_id`
* `default_entity_id`
* `default_context_id`
* `notes`
* `created_at`
* `updated_at`

---

## 13.5 `contexts`

Projects, purposes, or operational buckets.

Important fields:

* `id`
* `name`
* `context_type`
* `description`
* `is_active`
* `created_at`
* `updated_at`

Context examples:

* household
* personal
* business
* legal
* caregiver
* tax
* vehicle
* medical
* emergency

---

## 13.6 `statements`

Represents imported bank/card statements.

Important fields:

* `id`
* `account_id`
* `statement_start_date`
* `statement_end_date`
* `statement_date`
* `beginning_balance`
* `ending_balance`
* `source_file_name`
* `source_file_url`
* `import_status`
* `notes`
* `created_at`

---

## 13.7 `import_batches`

Tracks each import event.

Important fields:

* `id`
* `account_id`
* `statement_id`
* `source_type`
* `source_file_name`
* `imported_at`
* `row_count`
* `duplicate_count`
* `status`
* `notes`

Source types:

* csv
* manual
* pdf
* api
* migration

---

## 13.8 `raw_transactions`

Stores untouched imported transaction data.

Important fields:

* `id`
* `import_batch_id`
* `statement_id`
* `account_id`
* `raw_date`
* `raw_posted_date`
* `raw_description`
* `raw_amount`
* `raw_balance`
* `raw_category`
* `raw_reference`
* `source_row_hash`
* `matched_transaction_id`
* `created_at`

This table preserves source truth.

---

## 13.9 `ledger_transactions`

The normalized unified ledger.

Important fields:

* `id`
* `transaction_date`
* `posted_date`
* `account_id`
* `vendor_id`
* `payee_text`
* `description`
* `amount`
* `direction`
* `category_id`
* `entity_id`
* `context_id`
* `source_raw_transaction_id`
* `source_statement_id`
* `transfer_group_id`
* `review_status`
* `confidence_score`
* `tax_relevant`
* `business_relevant`
* `household_relevant`
* `legal_relevant`
* `receipt_url`
* `notes`
* `created_at`
* `updated_at`

Direction values:

* income
* expense
* transfer_in
* transfer_out
* adjustment

Review statuses:

* inbox
* reviewed
* needs_info
* ignored
* duplicate

---

## 13.10 `transaction_splits`

Allows one transaction to be split across multiple categories/entities/contexts.

Example:

A $60 Walmart purchase:

* $30 groceries
* $15 medical supplies
* $15 household supplies

Important fields:

* `id`
* `ledger_transaction_id`
* `amount`
* `category_id`
* `entity_id`
* `context_id`
* `notes`

---

## 13.11 `rules`

Auto-categorization rules.

Important fields:

* `id`
* `rule_name`
* `match_field`
* `match_operator`
* `match_value`
* `account_id`
* `vendor_id`
* `category_id`
* `entity_id`
* `context_id`
* `direction`
* `confidence_score`
* `is_active`
* `created_at`

Example:

If description contains `ASTOUND`, set:

* vendor = Astound
* category = Internet
* entity = Household
* context = Household Operations

---

## 13.12 `reconciliation_runs`

Tracks statement reconciliation.

Important fields:

* `id`
* `account_id`
* `statement_id`
* `period_start`
* `period_end`
* `expected_start_balance`
* `expected_end_balance`
* `calculated_end_balance`
* `difference`
* `status`
* `notes`
* `created_at`

---

# 14. Key Views

Database views should power reports.

## `v_unreviewed_transactions`

Shows all transactions needing review.

## `v_unified_ledger`

Clean ledger with joined names:

* account name
* vendor name
* category name
* entity name
* context name

## `v_cashflow_monthly`

Monthly income, expenses, and net.

## `v_spending_by_category`

Category totals by date range.

## `v_spending_by_entity`

Totals by person/entity.

## `v_spending_by_context`

Totals by project/context.

## `v_legal_expenses`

All legal-relevant transactions.

## `v_household_expenses`

All household-relevant transactions.

## `v_business_expenses`

All business-relevant transactions.

## `v_possible_duplicates`

Potential duplicate imports.

## `v_transfers`

Transfer groups and matched internal movement.

---

# 15. UI Design Principles

## Fast before fancy

The app should feel like clearing messages, not doing bookkeeping.

## Mobile-first

The user may need to enter or review transactions from phone.

## Big tap targets

Do not make tiny spreadsheet controls.

## Default to inbox

The first screen after login should be:

**Money Inbox**

## Filters must be obvious

Every major ledger view needs quick filters.

## Review should be one-click when possible

If the system guesses correctly, user should approve quickly.

## Manual editing must be easy

No hidden modals for every tiny edit.

## Keep visual clutter low

Use:

* left navigation on desktop
* bottom nav or drawer on mobile
* clean table/list hybrid
* badges for status/context
* persistent search
* quick action buttons

---

# 16. Suggested Navigation

## Primary nav

* Inbox
* Ledger
* Accounts
* Reports
* Rules
* Imports
* Settings

## Secondary admin nav

* Categories
* Vendors
* People / Entities
* Contexts
* Reconciliation
* Exports

---

# 17. MVP Roadmap

## Phase 0 — Blueprint and schema

Goal:
Define the system before building.

Tasks:

* finalize table list
* finalize category structure
* finalize context structure
* define account list
* define import CSV requirements
* define review workflow
* create Supabase schema

Deliverable:
Working database schema.

---

## Phase 1 — Core app shell

Goal:
Create the web app foundation.

Tasks:

* create React + TypeScript + Vite app
* connect Supabase
* set up auth
* create layout
* add navigation
* create protected routes
* create basic styling system

Deliverable:
Logged-in app shell with navigation.

---

## Phase 2 — Admin data setup

Goal:
Create the supporting tables.

Screens:

* Accounts
* Categories
* Vendors
* People / Entities
* Contexts

Tasks:

* list records
* create records
* edit records
* deactivate records
* search/filter records

Deliverable:
Usable admin foundation.

---

## Phase 3 — Manual transaction entry

Goal:
Allow quick manual logging.

Tasks:

* add transaction form
* date/account/vendor/amount/category/entity/context
* notes
* review status
* save to ledger

Deliverable:
Manual ledger works.

---

## Phase 4 — CSV import

Goal:
Import statement transactions.

Tasks:

* upload CSV
* map columns
* create import batch
* create raw transaction rows
* generate row hashes
* prevent duplicate rows
* display import summary

Deliverable:
CSV statement import works.

---

## Phase 5 — Money Inbox

Goal:
Create the main workflow.

Tasks:

* show raw/unreviewed transactions
* suggest vendor/category/context
* quick approve
* edit transaction
* mark duplicate
* mark transfer
* push to reviewed ledger

Deliverable:
User can clean imported transactions.

---

## Phase 6 — Unified Ledger

Goal:
Create master ledger view.

Tasks:

* searchable ledger
* filters
* edit transaction
* split transaction
* attach notes
* export CSV

Deliverable:
Central money history works.

---

## Phase 7 — Reports

Goal:
Turn ledger into useful views.

Reports:

* cashflow
* by category
* by person/entity
* by context/project
* by account
* household
* business
* legal
* uncategorized
* transfers

Deliverable:
Basic financial intelligence.

---

## Phase 8 — Rules engine

Goal:
Reduce repetitive categorization.

Tasks:

* create rules table
* apply rules on import
* suggest categories
* let user create rule from transaction
* confidence score

Deliverable:
System starts learning patterns.

---

## Phase 9 — Reconciliation

Goal:
Verify statements against ledger.

Tasks:

* compare statement ending balance
* compare ledger-calculated balance
* show differences
* mark reconciled

Deliverable:
Ledger becomes audit-friendly.

---

## Phase 10 — Automation and AI

Goal:
Speed up imports and classification.

Possible features:

* n8n import workflows
* receipt OCR
* AI vendor cleanup
* AI category suggestions
* recurring bill detection
* anomaly detection
* natural language search

Deliverable:
Semi-automated finance assistant.

---

# 18. Initial Category Framework

## Income

* Caregiver Income
* Rideshare Income
* Business Income
* Family Contribution
* Refund
* Reimbursement
* Legal Disbursement
* Other Income

## Household

* Rent / Housing
* Utilities
* Internet
* Phone
* Groceries
* Household Supplies
* Repairs
* Furniture
* Appliances
* Shared Subscriptions

## Caregiver / Medical Support

* Medication
* Medical Supplies
* Transportation
* Food / Special Diet
* Mobility Equipment
* Home Health Support

## Transportation

* Gas
* Vehicle Repair
* Insurance
* Registration
* Rideshare Rental
* Parking
* Tolls

## Business

* Software
* Hosting
* Domain
* Equipment
* Office Supplies
* Client Expense
* Contractor
* Professional Services

## Legal

* Filing Fees
* Copies / Printing
* Postage
* Court Costs
* Legal Research
* Travel for Legal
* Evidence / Records

## Personal

* Food
* Clothing
* Personal Care
* Entertainment
* Subscriptions
* Miscellaneous

## Debt / Liability

* Loan Payment
* Credit Card Payment
* Cash Advance Repayment
* Overdraft / Fees
* Interest

## Transfers

* Internal Transfer
* Cash Withdrawal
* Cash Deposit
* Account Funding
* Clearing Movement

## Adjustments

* Balance Correction
* Duplicate Correction
* Manual Adjustment
* Unknown

---

# 19. Important Design Decisions

## Decision 1: One ledger, many contexts

Do not create separate ledgers for each bank.

Each bank/account is a source.

The unified ledger is the truth.

## Decision 2: Raw data stays raw

Imported rows remain untouched.

Normalized records link back to raw source rows.

## Decision 3: Clearing accounts are allowed

Clearing accounts are important for real life.

Examples:

* Mom Clearing
* Zai Clearing
* Household Clearing
* Cash Clearing
* Reimbursement Clearing

## Decision 4: Transfers need pairing

Money moving between accounts should not count as income or expense.

Use `transfer_group_id`.

## Decision 5: Reports should not require duplicate data

Reports should be generated from ledger views.

## Decision 6: Manual entry matters

Not every transaction will come from a bank statement.

Cash, informal repayments, and quick notes need manual entry.

---

# 20. Risk Register

## Risk: Overbuilding

Mitigation:
Keep MVP focused on ledger, inbox, import, reports.

## Risk: Accounting complexity

Mitigation:
Do not implement full double-entry in v1.

## Risk: Dirty imports

Mitigation:
Use raw transaction staging and source row hashes.

## Risk: Duplicate transactions

Mitigation:
Use hashes based on account/date/amount/description/reference.

## Risk: UI becomes spreadsheet hell

Mitigation:
Use card/list hybrid for review, not only tables.

## Risk: Reports become inaccurate

Mitigation:
Use reviewed status and reconciliation.

## Risk: Tool lock-in

Mitigation:
Use plain Supabase/Postgres schema, not proprietary app-builder logic.

---

# 21. Success Criteria

QiLedger v1 is successful when Cody can:

* import transactions from at least one account
* manually add cash/manual transactions
* categorize transactions quickly
* assign transactions to person/entity/context
* view all money activity in one ledger
* filter by household, business, legal, personal, caregiver
* export transactions for backup or tax/legal use
* identify uncategorized or unreviewed transactions
* produce a basic monthly household report
* produce a basic legal expense report
* produce a basic business expense report

---

# 22. Future Features

## AI-assisted categorization

Use prior reviewed transactions to suggest:

* vendor
* category
* entity
* context
* tax/legal relevance

## Natural language queries

Examples:

* “How much did we spend on Mom’s medical stuff last month?”
* “Show all legal expenses since January.”
* “How much did Zai-related spending cost this week?”
* “What did I spend at Walmart in April?”
* “Show all transactions over $100 that are unreviewed.”

## Receipt storage

Attach:

* receipt images
* PDFs
* statement files
* screenshots
* notes

## Statement parser

Support:

* CSV
* PDF
* screenshot/OCR later

## Recurring bill detection

Identify recurring bills and expected due dates.

## Budget layer

Add budget planning after ledger is stable.

## Forecasting

Predict upcoming cash needs based on:

* recurring bills
* average spending
* scheduled payments
* expected income

## Formal accounting mode

Later optional layer:

* double-entry journal entries
* chart of accounts
* balance sheet
* profit and loss
* equity/liability tracking

Not v1.

---

# 23. Build Instruction for Gemini / Codex

Use this as the project direction:

Build a mobile-first React + TypeScript + Vite web app connected to Supabase. The app is a custom financial ledger system called QiLedger. It should use Supabase Postgres as the source of truth and provide a fast user interface for importing, reviewing, categorizing, and reporting money activity across personal, household, business, legal, and caregiver contexts.

The first version should not attempt to recreate QuickBooks. It should focus on:

* accounts
* entities
* categories
* vendors
* contexts
* manual transaction entry
* CSV import
* raw transaction staging
* review inbox
* unified ledger
* basic reports
* CSV export

Design the UI for fast review and filtering. The default landing screen after login should be the Money Inbox. Use clean navigation, mobile-first layout, and minimal cognitive clutter.

The database should preserve raw imported transaction data separately from normalized ledger transactions. All reports should come from the normalized unified ledger and database views.

---

# 24. MVP Build Order

Build in this exact order:

1. Supabase schema
2. Auth and app shell
3. Accounts/categories/entities/contexts admin screens
4. Manual transaction entry
5. Unified ledger view
6. CSV import into raw transactions
7. Money Inbox review workflow
8. Basic reports
9. Rules engine
10. Reconciliation

Do not build dashboards first.

Dashboards come after transaction data is clean.

---

# 25. Bottom-Line Strategy

The win is not “having another finance app.”

The win is having a **money command center** that reflects real life:

* household chaos
* caregiver expenses
* personal survival money
* business operations
* legal documentation
* reimbursements
* shared responsibilities
* tax support
* messy bank data

QiLedger should make the money story visible.

Not perfect.
Visible.

Then visible becomes manageable.
Manageable becomes reportable.
Reportable becomes leverage.
