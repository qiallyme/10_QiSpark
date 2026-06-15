# QiLife Seed Data Spec

This document defines the canonical seed data for v1. The purpose of seeds is to validate the spine, not to simulate a complete life ledger.

## Seed Conventions

- Use ULIDs for every non-static seeded record.
- Use `amount_cents` for money.
- Use ISO 8601 datetimes for timestamp fields.
- Prefer realistic but minimal linked records that prove the core doctrine.
- Ensure important actions and money records point back to source QiBits where applicable.

## 1. Buckets

Seed all canonical buckets from the `buckets` static table:

`00`, `10`, `20`, `30`, `40`, `50`, `60`, `70`, `80`, `90`, `100`, `110`, `900`, `990`

## 2. People

1. Cody
   - `id`: `01JWNX2D3Q4A5B6C7D8E9F0G1H`
   - `display_name`: `"Cody"`
   - `legal_name`: `"Cody"`
   - `type`: `"person"`
   - `relationship`: `"self"`
   - `notes`: `"Owner, agent, and primary operator of this Personal LifeDesk."`

2. Zai
   - `id`: `01JWNX2D3Q4A5B6C7D8E9F0G1J`
   - `display_name`: `"Zai"`
   - `legal_name`: `"Zaituallah Jan Khebarkhil"`
   - `type`: `"person"`
   - `relationship`: `"friend/collaborator"`
   - `phone`: `"+1-555-0199"`
   - `notes`: `"Lyft driving companion and roommate."`

3. State Revenue Agency
   - `id`: `01JWNX2D3Q4A5B6C7D8E9F0G1K`
   - `display_name`: `"State Revenue Agency"`
   - `legal_name`: `"Department of Revenue"`
   - `type`: `"agency"`
   - `relationship`: `"tax authority"`
   - `notes`: `"Source of the missing tax surplus check."`

## 3. Threads

1. Lyft Income Sprint
   - `id`: `01JWNX8F6R7S8T9U0V1W2X3Y4A`
   - `bucket_code`: `"50"`
   - `status`: `"active"`
   - `priority`: `"high"`

2. Surplus Check Recovery
   - `id`: `01JWNX8F6R7S8T9U0V1W2X3Y4B`
   - `bucket_code`: `"70"`
   - `status`: `"open"`
   - `priority`: `"critical"`

3. QiLife Build
   - `id`: `01JWNX8F6R7S8T9U0V1W2X3Y4C`
   - `bucket_code`: `"80"`
   - `status`: `"active"`
   - `priority`: `"high"`

## 4. QiBits

1. QiLife Core Purpose
   - `id`: `01JWNY1H2J3K4L5M6N7P8Q9R0A`
   - `qibit_type`: `"note"`
   - `bucket_code`: `"80"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4C`
   - `future_slot`: `"knowledge_base"`
   - `status`: `"reference"`

2. Gas Loan Capture
   - `id`: `01JWNY1H2J3K4L5M6N7P8Q9R0B`
   - `raw_capture`: `"Zai owes me $40 for gas."`
   - `qibit_type`: `"obligation_seed"`
   - `bucket_code`: `"60"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4A`
   - `future_slot`: `"waiting_on"`
   - `status`: `"open"`

3. Lyft Weekend Quota
   - `id`: `01JWNY1H2J3K4L5M6N7P8Q9R0C`
   - `raw_capture`: `"Need to finish the Lyft ride target this weekend."`
   - `qibit_type`: `"task_seed"`
   - `bucket_code`: `"50"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4A`
   - `future_slot`: `"today"`
   - `status`: `"triaged"`

4. Check Mail Reminder
   - `id`: `01JWNY1H2J3K4L5M6N7P8Q9R0D`
   - `raw_capture`: `"Check the mailbox for the surplus check letter."`
   - `qibit_type`: `"task_seed"`
   - `bucket_code`: `"70"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4B`
   - `future_slot`: `"today"`
   - `status`: `"triaged"`

## 5. Actions & Steps

1. Finish 11 Lyft rides
   - `id`: `01JWNY9K3L4M5N6P7Q8R9S0T1A`
   - `source_qibit_id`: `01JWNY1H2J3K4L5M6N7P8Q9R0C`
   - `bucket_code`: `"50"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4A`
   - `status`: `"in_progress"`
   - `scheduled_for`: `"2026-05-29T09:00:00-05:00"`

2. Check mail for surplus check
   - `id`: `01JWNY9K3L4M5N6P7Q8R9S0T1B`
   - `source_qibit_id`: `01JWNY1H2J3K4L5M6N7P8Q9R0D`
   - `bucket_code`: `"70"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4B`
   - `status`: `"open"`
   - `scheduled_for`: `"2026-05-29T16:00:00-05:00"`
   - steps:
     - Walk to physical mailbox
     - Review incoming letters for State Revenue logo

## 6. Money Records

1. Gas Share Obligation
   - `id`: `01JWNZ4M5N6P7Q8R9S0T1U2V3A`
   - `owed_by_label`: `"Zai"`
   - `owed_to_label`: `"Cody"`
   - `obligation_type`: `"money"`
   - `amount_cents`: `4000`
   - `currency`: `"USD"`
   - `reason`: `"Gas payment share for Lyft driving run"`
   - `status`: `"open"`
   - `source_qibit_id`: `01JWNY1H2J3K4L5M6N7P8Q9R0B`

2. Gas Station Transaction
   - `id`: `01JWNZ4M5N6P7Q8R9S0T1U2V3B`
   - `date`: `"2026-05-29"`
   - `amount_cents`: `6523`
   - `currency`: `"USD"`
   - `direction`: `"out"`
   - `from_label`: `"Cody"`
   - `to_label`: `"Shell Gas Station"`
   - `category`: `"gas"`
   - `bucket_code`: `"60"`
   - `thread_id`: `01JWNX8F6R7S8T9U0V1W2X3Y4A`
   - `status`: `"cleared"`
   - `source_qibit_id`: `01JWNY1H2J3K4L5M6N7P8Q9R0B`

## 7. Knowledge Items

1. QiBit Lifecycle Doctrine
   - `id`: `01JWP01N6P7Q8R9S0T1U2V3W4A`
   - `bucket_code`: `"110"`
   - `knowledge_type`: `"doctrine"`
   - `source_type`: `"repo_doc"`
   - `source_path`: `"docs/10_product/01_qibit_lifecycle.md"`
   - `confidence`: `"confirmed"`
   - `visibility`: `"system"`

## 8. Links

Example relationships the seed should prove:

- QiBit `01JWNY1H2J3K4L5M6N7P8Q9R0B` `created_from` obligation `01JWNZ4M5N6P7Q8R9S0T1U2V3A`
- Obligation `01JWNZ4M5N6P7Q8R9S0T1U2V3A` `relates_to` person `01JWNX2D3Q4A5B6C7D8E9F0G1J`
- Transaction `01JWNZ4M5N6P7Q8R9S0T1U2V3B` `belongs_to` thread `01JWNX8F6R7S8T9U0V1W2X3Y4A`
- Knowledge item `01JWP01N6P7Q8R9S0T1U2V3W4A` `explains` thread `01JWNX8F6R7S8T9U0V1W2X3Y4C`
