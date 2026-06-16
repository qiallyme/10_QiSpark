## 1. Purpose

CareLite is the lightweight daily-use layer for Mom’s care.

The existing full care app remains the long-term care record, admin system, inventory tracker, medical history archive, and reporting hub. CareLite is different. CareLite is the daily cockpit: big buttons, timers, quick logs, and immediate feedback.

The goal is not to model every medical detail perfectly. The goal is to help Mom and caregiver quickly answer:

* Did she take it?
* When did she take it?
* Is it too soon based on saved timing rules?
* How much has she had in the last 24 hours?
* Is the oxygen tank close to estimated empty?
* What bathroom/intake/events happened today?

CareLite should reduce paper notes, reduce timing confusion, reduce overdose risk, and reduce caregiver cognitive load.

## 2. Product Principle

Build the version she can use while tired, short of breath, annoyed, and holding a Powerade.

If the UI requires thinking, it failed.

If the schema requires debate every time something new is added, it failed.

If the app buries the useful thing behind a clinical admin interface, it failed.

## 3. Core Scope

CareLite tracks:

1. Breathing treatments
2. PRN medications
3. Morphine
4. Tylenol / acetaminophen exposure
5. Prednisone tablet count
6. AM medication checkoff
7. PM medication checkoff
8. Pee events
9. Poop events
10. Powerade intake
11. Quick notes
12. Oxygen tank estimated depletion

## 4. Non-Goals

CareLite is not:

* A full medication administration record
* A replacement for prescription instructions
* A clinical decision engine
* An oxygen regulator monitor
* A pharmacy inventory system
* A complete care plan builder
* A legal/medical compliance product

CareLite only calculates based on saved rules and user-entered events.

Use wording like:

* “Available based on saved timing rules”
* “Wait before next dose”
* “Limit reached based on saved rules”
* “Estimated tank time left”

Do not use wording like:

* “Safe to take”
* “Approved dose”
* “Tank definitely empty”
* “Medical recommendation”

## 5. MVP Definition

### MVP Must Have

* Separate `carelite` schema
* `carelite.items`
* `carelite.entries`
* `carelite.v_item_status`
* `carelite.oxygen_tank_profiles`
* `carelite.oxygen_tank_sessions`
* Big-button CareLite dashboard
* Tap-to-log for simple items
* Confirmation modal for higher-risk meds/treatments
* Prednisone quantity selector
* Powerade amount selector
* Poop quick options + optional note
* Quick Note text entry
* O2 Tank card with start / pause / resume / depleted / new tank flow
* Recent activity feed for today
* Simple admin editor for CareLite items and oxygen tank profiles

### MVP Should Have

* Mobile-first layout
* Clear status colors
* Countdown display for interval-based items
* Rolling 24-hour totals
* Today totals
* “Done today” status for AM/PM meds
* Warning state for oxygen tank low estimate
* A simple correction/void ability in recent feed

### MVP Can Wait

* Push notifications
* SMS alerts
* caregiver remote alerts
* charting/report PDFs
* full oxygen inventory integration
* barcode scanning
* medication bottle photo OCR
* MyChart ingestion
* predictive analytics
* AI analysis of notes

## 6. Aesthetic / UX Direction

### Visual Style

CareLite should look calm, obvious, and high-contrast.

Preferred style:

* Large rounded cards
* Big touch targets
* Minimal text
* Strong iconography
* Soft backgrounds
* Clear color states
* No dense tables on the main screen
* No tiny admin controls on the patient-facing screen

### Screen Personality

The UI should feel like:

* Kitchen timer
* Medication safety board
* Elder-friendly remote control
* Daily care cockpit

Not:

* Hospital EMR
* Spreadsheet
* Developer admin console
* Chart-heavy analytics dashboard

### Status Colors

Use consistent states:

| State  | Meaning                                               |
| ------ | ----------------------------------------------------- |
| Green  | Available / running / done / okay based on saved rule |
| Yellow | Caution / close to limit / prepare next tank          |
| Red    | Too soon / limit reached / estimated depleted         |
| Gray   | No active item / paused / neutral                     |
| Blue   | Informational / resumed / active but not urgent       |

### Card Design

Each card should show only the essentials:

* Name
* Icon
* Main status
* Last logged time
* Next allowed time or countdown if relevant
* Uses / amount if relevant
* One obvious action button

Example:

```text
Morphine
Last: 8:15 AM
Next: 12:15 PM
2 / 6 used
[Wait 1h 20m]
```

Example:

```text
Powerade
Today: 36 oz
[Add Powerade]
```

Example:

```text
O2 Tank
Running · 2 L/min
Estimated 3h 42m left
[Pause Tank]
```

## 7. Recommended Navigation

Add route:

```text
/carelite
```

Optional admin route:

```text
/admin/carelite
```

Do not bury this under the larger care admin event system.

Primary nav label:

```text
CareLite
```

Alternate label:

```text
Today Buttons
```

Best label for Mom:

```text
Today
```

## 8. Database Architecture

Use a separate schema:

```sql
create schema if not exists carelite;
```

CareLite references the existing `care.patients` table. This keeps it tied to the real patient without polluting the heavier `care` schema.

## 9. Core Tables

### 9.1 `carelite.items`

Defines every button/action available in CareLite.

```sql
create table if not exists carelite.items (
  id uuid primary key default gen_random_uuid(),

  patient_id uuid not null references care.patients(id),

  name text not null,
  item_type text not null,
  -- med, treatment, scheduled_check, body_event, intake, note, oxygen_tank

  category text,
  -- breathing, pain, steroid, bathroom, hydration, general, daily_meds, oxygen

  icon text,
  color text,

  default_amount numeric,
  default_unit text,

  min_interval_minutes integer,
  max_uses_per_24h integer,
  max_amount_per_24h numeric,

  is_scheduled boolean not null default false,
  schedule_period text,
  -- AM, PM, BEDTIME, DAILY

  requires_confirmation boolean not null default false,
  allow_note boolean not null default true,
  active boolean not null default true,

  sort_order integer not null default 100,

  notes text,
  metadata_json jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

### 9.2 `carelite.entries`

Records every log/tap/note.

```sql
create table if not exists carelite.entries (
  id uuid primary key default gen_random_uuid(),

  patient_id uuid not null references care.patients(id),
  item_id uuid references carelite.items(id),

  entry_type text not null,
  -- copied from item_type when applicable

  occurred_at timestamptz not null default now(),

  amount numeric,
  unit text,

  status text not null default 'completed',
  -- completed, skipped, corrected, voided

  note text,

  metadata_json jsonb not null default '{}'::jsonb,

  created_by text,
  created_at timestamptz not null default now()
);
```

### 9.3 Indexes

```sql
create index if not exists idx_carelite_items_patient_active
on carelite.items(patient_id, active);

create index if not exists idx_carelite_entries_patient_occurred
on carelite.entries(patient_id, occurred_at desc);

create index if not exists idx_carelite_entries_item_occurred
on carelite.entries(item_id, occurred_at desc);

create index if not exists idx_carelite_entries_type_occurred
on carelite.entries(entry_type, occurred_at desc);
```

## 10. Status View

```sql
create or replace view carelite.v_item_status as
select
  i.id,
  i.patient_id,
  i.name,
  i.item_type,
  i.category,
  i.icon,
  i.color,
  i.default_amount,
  i.default_unit,
  i.min_interval_minutes,
  i.max_uses_per_24h,
  i.max_amount_per_24h,
  i.is_scheduled,
  i.schedule_period,
  i.requires_confirmation,
  i.allow_note,
  i.sort_order,
  i.active,

  max(e.occurred_at) filter (
    where e.status = 'completed'
  ) as last_occurred_at,

  count(e.id) filter (
    where e.status = 'completed'
      and e.occurred_at >= now() - interval '24 hours'
  ) as uses_last_24h,

  coalesce(sum(e.amount) filter (
    where e.status = 'completed'
      and e.occurred_at >= now() - interval '24 hours'
  ), 0) as amount_last_24h,

  count(e.id) filter (
    where e.status = 'completed'
      and e.occurred_at >= date_trunc('day', now())
  ) as uses_today,

  coalesce(sum(e.amount) filter (
    where e.status = 'completed'
      and e.occurred_at >= date_trunc('day', now())
  ), 0) as amount_today

from carelite.items i
left join carelite.entries e
  on e.item_id = i.id
where i.active = true
group by i.id;
```

## 11. Oxygen Tank Tables

Oxygen tank tracking is session-based. Do not force it into only `carelite.entries`.

### 11.1 `carelite.oxygen_tank_profiles`

```sql
create table if not exists carelite.oxygen_tank_profiles (
  id uuid primary key default gen_random_uuid(),

  patient_id uuid not null references care.patients(id),

  name text not null,
  tank_type text,

  starting_pressure_psi numeric not null default 2000,
  usable_liters numeric not null,
  default_flow_lpm numeric not null default 2,

  warning_minutes_remaining integer not null default 30,

  active boolean not null default true,

  notes text,
  metadata_json jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

### 11.2 `carelite.oxygen_tank_sessions`

```sql
create table if not exists carelite.oxygen_tank_sessions (
  id uuid primary key default gen_random_uuid(),

  patient_id uuid not null references care.patients(id),
  tank_profile_id uuid not null references carelite.oxygen_tank_profiles(id),

  status text not null default 'running',
  -- running, paused, depleted, replaced, voided

  started_at timestamptz not null default now(),
  ended_at timestamptz,

  flow_lpm numeric not null default 2,
  starting_pressure_psi numeric not null default 2000,
  usable_liters numeric not null,

  total_runtime_seconds integer not null default 0,

  last_started_at timestamptz,
  last_paused_at timestamptz,

  depleted_at timestamptz,
  replaced_at timestamptz,

  note text,
  metadata_json jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

### 11.3 Oxygen Indexes

```sql
create index if not exists idx_carelite_o2_profiles_patient_active
on carelite.oxygen_tank_profiles(patient_id, active);

create index if not exists idx_carelite_o2_sessions_patient_status
on carelite.oxygen_tank_sessions(patient_id, status);

create index if not exists idx_carelite_o2_sessions_patient_started
on carelite.oxygen_tank_sessions(patient_id, started_at desc);
```

## 12. Oxygen Tank Logic

Important: 2000 PSI alone does not determine tank runtime. The app needs usable liters from the tank profile.

Estimated total runtime:

```text
usable_liters / flow_lpm
```

Estimated total seconds:

```text
(usable_liters / flow_lpm) * 60
```

If running:

```text
runtime_used_seconds = total_runtime_seconds + seconds_since(last_started_at)
```

If paused:

```text
runtime_used_seconds = total_runtime_seconds
```

Remaining:

```text
estimated_total_seconds - runtime_used_seconds
```

Do not update the database every second. The frontend calculates the live countdown. The database updates only on:

* start tank
* pause tank
* resume tank
* mark depleted
* replace tank
* void/correct session

## 13. Oxygen Tank State Machine

### No Active Tank

Display:

```text
O2 Tank
No tank running
[Start Tank]
```

On click:

* Find active tank profile
* Create new oxygen tank session
* status = running
* started_at = now
* last_started_at = now
* total_runtime_seconds = 0

### Running

Display:

```text
O2 Tank
Running · 2 L/min
Estimated 3h 42m left
[Pause Tank]
```

On pause:

* Calculate seconds since `last_started_at`
* Add to `total_runtime_seconds`
* Set `last_paused_at = now()`
* Set `status = paused`

### Paused

Display:

```text
O2 Tank
Paused
Estimated 3h 20m left
[Resume Tank]
```

On resume:

* Set `status = running`
* Set `last_started_at = now()`

### Warning

If remaining seconds <= warning threshold:

```text
Prepare next tank
Estimated 24m left
```

### Depleted

If remaining seconds <= 0:

```text
O2 Tank
Estimated empty
Is this a new tank?
[No] [Yes, New Tank]
```

If Yes:

* Mark current session replaced
* Set ended_at
* Set replaced_at
* Create new running session

If No:

* Keep current session paused/depleted
* Do not reset timer

## 14. Seed Data

Replace `PATIENT_ID_HERE`.

```sql
insert into carelite.items
(patient_id, name, item_type, category, icon, default_amount, default_unit, min_interval_minutes, max_uses_per_24h, max_amount_per_24h, is_scheduled, schedule_period, requires_confirmation, sort_order, notes)
values
(
  'PATIENT_ID_HERE',
  'Breathing Treatment',
  'treatment',
  'breathing',
  'lungs',
  1,
  'treatment',
  180,
  6,
  null,
  false,
  null,
  true,
  10,
  'PRN breathing treatment. Confirm med-specific rules with prescription/care team.'
),
(
  'PATIENT_ID_HERE',
  'O2 Tank',
  'oxygen_tank',
  'oxygen',
  'gauge',
  2,
  'L/min',
  null,
  null,
  null,
  false,
  null,
  false,
  15,
  'Tracks estimated oxygen tank depletion using flow rate and tank profile.'
),
(
  'PATIENT_ID_HERE',
  'AM Meds',
  'scheduled_check',
  'daily_meds',
  'sunrise',
  1,
  'set',
  null,
  1,
  null,
  true,
  'AM',
  false,
  20,
  'Daily morning medication checkoff.'
),
(
  'PATIENT_ID_HERE',
  'PM Meds',
  'scheduled_check',
  'daily_meds',
  'moon',
  1,
  'set',
  null,
  1,
  null,
  true,
  'PM',
  false,
  30,
  'Daily evening medication checkoff.'
),
(
  'PATIENT_ID_HERE',
  'Prednisone',
  'med',
  'steroid',
  'pill',
  1,
  'tablet',
  null,
  null,
  null,
  false,
  null,
  true,
  40,
  'Track number of prednisone tablets taken.'
),
(
  'PATIENT_ID_HERE',
  'Tylenol',
  'med',
  'pain',
  'pill',
  500,
  'mg',
  null,
  null,
  3000,
  false,
  null,
  true,
  50,
  'Track acetaminophen amount in rolling 24 hours. Confirm actual max with care team.'
),
(
  'PATIENT_ID_HERE',
  'Morphine',
  'med',
  'pain',
  'shield-alert',
  5,
  'mg',
  240,
  6,
  null,
  false,
  null,
  true,
  60,
  'PRN medication. Confirm interval and max with prescription instructions.'
),
(
  'PATIENT_ID_HERE',
  'Pee',
  'body_event',
  'bathroom',
  'droplets',
  1,
  'time',
  null,
  null,
  null,
  false,
  null,
  false,
  70,
  'Track urination events.'
),
(
  'PATIENT_ID_HERE',
  'Poop',
  'body_event',
  'bathroom',
  'toilet',
  1,
  'time',
  null,
  null,
  null,
  false,
  null,
  false,
  80,
  'Track bowel movements. Use notes for loose, hard, normal, constipation, etc.'
),
(
  'PATIENT_ID_HERE',
  'Powerade',
  'intake',
  'hydration',
  'cup-soda',
  12,
  'oz',
  null,
  null,
  null,
  false,
  null,
  false,
  90,
  'Track Powerade intake.'
),
(
  'PATIENT_ID_HERE',
  'Quick Note',
  'note',
  'general',
  'sticky-note',
  null,
  null,
  null,
  null,
  null,
  false,
  null,
  false,
  100,
  'Fast note capture.'
);
```

Seed oxygen profile:

```sql
insert into carelite.oxygen_tank_profiles
(patient_id, name, tank_type, starting_pressure_psi, usable_liters, default_flow_lpm, warning_minutes_remaining, notes)
values
(
  'PATIENT_ID_HERE',
  'Standard O2 Tank',
  'VERIFY',
  2000,
  625,
  2,
  30,
  'Placeholder estimate. Verify actual tank type/capacity with supplier label.'
);
```

## 15. Frontend Components

Recommended component breakdown:

```text
src/features/carelite/
  CareLitePage.tsx
  CareLiteDashboard.tsx
  CareLiteCard.tsx
  CareLiteRecentFeed.tsx
  CareLiteAdminPage.tsx
  modals/
    ConfirmLogModal.tsx
    PrednisoneLogModal.tsx
    PoweradeLogModal.tsx
    PoopLogModal.tsx
    QuickNoteModal.tsx
    OxygenTankModal.tsx
  hooks/
    useCareLiteItems.ts
    useCareLiteEntries.ts
    useCareLiteStatus.ts
    useOxygenTankSession.ts
  utils/
    careliteStatus.ts
    oxygenTankMath.ts
    timeFormat.ts
```

Adjust paths to match the existing app conventions.

## 16. CareLite Dashboard Sections

Recommended grouping:

1. Oxygen + Priority

   * O2 Tank
   * Breathing Treatment
   * Morphine
   * Tylenol
   * Prednisone

2. Daily Meds

   * AM Meds
   * PM Meds

3. Bathroom

   * Pee
   * Poop

4. Intake

   * Powerade

5. Notes

   * Quick Note

6. Recent Activity

   * Today’s logs newest first

## 17. Logging Behavior

### Simple Immediate Log

For Pee:

* Tap card
* Insert entry immediately
* Refresh status/feed

### Confirmation Log

For breathing treatment, morphine, Tylenol:

* Tap card
* Show confirm modal
* Insert entry on confirm
* Refresh status/feed

### Prednisone

* Tap card
* Show quantity selector
* Default 1 tablet
* Allow increment/decrement
* Save amount and unit

### Powerade

* Tap card
* Show options: 8 oz, 12 oz, 16 oz, 20 oz, Custom
* Save selected amount and unit

### Poop

* Tap card
* Show options: Normal, Loose, Hard, Tiny, Constipated
* Optional note
* Save selected stool type in `metadata_json`

Example:

```json
{
  "stool_type": "loose"
}
```

### Quick Note

* Tap card
* Show text area
* Save note to `carelite.entries.note`

## 18. Recent Activity Feed

Display today’s entries newest first.

Each row:

```text
10:42 AM · Breathing Treatment · 1 treatment
9:15 AM · Powerade · 12 oz
8:05 AM · Quick Note · Coughing more after walking
```

Include correction options for caregiver/admin:

* Void entry
* Edit note
* Correct time later, optional

MVP can start with void only.

## 19. Status Calculation Rules

For each item:

```text
last_occurred_at = latest completed entry
uses_last_24h = completed count in rolling 24h
amount_last_24h = completed sum in rolling 24h
uses_today = completed count since local day start
amount_today = completed sum since local day start
```

If `min_interval_minutes` exists:

```text
next_allowed_at = last_occurred_at + min_interval_minutes
is_too_soon = now < next_allowed_at
```

If `max_uses_per_24h` exists:

```text
use_limit_reached = uses_last_24h >= max_uses_per_24h
```

If `max_amount_per_24h` exists:

```text
amount_limit_reached = amount_last_24h >= max_amount_per_24h
```

For scheduled items:

```text
is_done_today = uses_today >= 1
```

## 20. Safety Rules

The UI must avoid overclaiming.

Use:

```text
Available based on saved timing rules
```

Not:

```text
Safe to take
```

Use:

```text
Estimated empty
```

Not:

```text
Empty
```

Use:

```text
Confirm actual limits with prescription/care team
```

Not:

```text
This is the correct dose
```

## 21. Build Order

### Step 1: Database Migration

* Create `carelite` schema
* Create tables
* Create indexes
* Create view
* Seed initial items/profile

### Step 2: Types

* Regenerate Supabase TypeScript types
* Confirm `carelite` schema appears in generated types
* Add helper types if needed

### Step 3: Data Hooks

* Fetch item status
* Fetch today entries
* Insert entry
* Void entry
* Fetch active oxygen profile
* Fetch active oxygen session
* Start/pause/resume/replace oxygen session

### Step 4: Main Dashboard

* Build layout
* Group cards
* Add status colors
* Add simple log flow

### Step 5: Special Modals

* Prednisone
* Powerade
* Poop
* Quick Note
* Confirmation modal

### Step 6: Oxygen Card

* Add oxygen math utility
* Add state machine behavior
* Add warning/depleted flow

### Step 7: Admin

* Item editor
* Tank profile editor
* Active/inactive toggles

### Step 8: QA

* Test rolling 24h totals
* Test AM/PM reset
* Test too-soon lockout/warning
* Test oxygen start/pause/resume/new tank
* Test mobile layout
* Test void/correct entries

## 22. Local Dev Commands

Adjust package manager based on the repo.

### Install

```bash
npm install
```

or

```bash
pnpm install
```

### Run dev server

```bash
npm run dev
```

or

```bash
pnpm dev
```

### Typecheck

```bash
npm run typecheck
```

or

```bash
pnpm typecheck
```

### Lint

```bash
npm run lint
```

or

```bash
pnpm lint
```

### Build

```bash
npm run build
```

or

```bash
pnpm build
```

### Supabase type generation

Use the project’s existing command if already present.

Common pattern:

```bash
supabase gen types typescript --project-id YOUR_PROJECT_ID --schema care,carelite > src/types/supabase.ts
```

If the project uses local Supabase:

```bash
supabase gen types typescript --local --schema care,carelite > src/types/supabase.ts
```

## 23. Codex Setup

Install Codex CLI if needed:

```bash
npm install -g @openai/codex
```

Alternative:

```bash
brew install --cask codex
```

Run inside the repo:

```bash
cd /path/to/mom-care-app
codex
```

Recommended Codex usage:

* Use Codex for implementation
* Give it one bounded task at a time
* Require it to inspect existing patterns before creating new abstractions
* Require it to run tests/typecheck/build
* Require it to summarize changed files

Do not tell Codex to “build the whole thing” in one vague prompt. That is how it makes a weird castle of nonsense.

## 24. Codex Command: Phase 1 Database

```text
You are working in the existing Mom Care App repo.

Task: Add CareLite database support only.

Requirements:
1. Inspect the repo for existing Supabase migration patterns, SQL folder conventions, type generation scripts, and patient references.
2. Add a new carelite schema migration without modifying or breaking the existing care schema.
3. Create:
   - carelite.items
   - carelite.entries
   - carelite.v_item_status
   - carelite.oxygen_tank_profiles
   - carelite.oxygen_tank_sessions
4. Add the indexes documented in CareLite dev documentation.
5. Add seed SQL for initial items and one oxygen tank profile, but make sure patient_id is configurable or clearly marked as needing replacement.
6. Use existing project conventions for migrations.
7. Do not touch unrelated UI yet.
8. Run typecheck/build if available.
9. At the end, summarize:
   - files changed
   - migration name
   - any manual steps needed
   - any risks
```

## 25. Codex Command: Phase 2 Types + Data Layer

```text
Task: Add CareLite TypeScript data layer.

Requirements:
1. Inspect existing Supabase client usage and hooks/services patterns.
2. Regenerate or update Supabase types to include carelite schema if the project uses generated types.
3. Create hooks/services for:
   - fetching carelite.v_item_status for active patient
   - fetching today’s carelite.entries
   - inserting a carelite entry
   - voiding/correcting an entry
   - fetching active oxygen tank profile
   - fetching active oxygen tank session
   - starting oxygen tank session
   - pausing oxygen tank session
   - resuming oxygen tank session
   - replacing oxygen tank session
4. Add utility functions for:
   - next allowed time
   - uses/amount warning states
   - oxygen runtime calculation
   - formatting remaining time
5. Follow existing project conventions.
6. Do not build UI yet except minimal tests if needed.
7. Run lint/typecheck/build.
8. Summarize changed files and any assumptions.
```

## 26. Codex Command: Phase 3 Main CareLite Page

```text
Task: Build the CareLite main dashboard UI.

Route:
/carelite

Requirements:
1. Add a mobile-first CareLite page using existing routing conventions.
2. Show large card buttons grouped into:
   - Oxygen + Priority
   - Daily Meds
   - Bathroom
   - Intake
   - Notes
   - Recent Activity
3. Use carelite.v_item_status for card state.
4. Each card should show:
   - icon
   - name
   - last logged time
   - countdown/next allowed if relevant
   - uses in last 24h vs max if relevant
   - amount in last 24h vs max if relevant
   - today total if relevant
5. Add status colors:
   - green available/done/running
   - yellow caution/warning
   - red too soon/limit/depleted
   - gray neutral/paused
6. Implement basic tap behavior:
   - Pee logs immediately
   - AM/PM meds log immediately or with lightweight confirmation
   - generic confirmation for requires_confirmation items
7. Do not overbuild charts or admin UI yet.
8. Run lint/typecheck/build.
9. Summarize changed files and known gaps.
```

## 27. Codex Command: Phase 4 Special Modals

```text
Task: Add CareLite special logging modals.

Requirements:
1. Add reusable modal/panel components following existing UI conventions.
2. Add special flows:
   - Prednisone: quantity selector for tablets
   - Powerade: 8 oz, 12 oz, 16 oz, 20 oz, Custom
   - Poop: Normal, Loose, Hard, Tiny, Constipated, optional note
   - Quick Note: text area
   - Confirmation modal for higher-risk meds/treatments
3. Insert logs into carelite.entries with:
   - patient_id
   - item_id
   - entry_type
   - amount
   - unit
   - note
   - metadata_json if special selection exists
4. Refresh status and recent feed after save.
5. Keep the UI big, simple, and mobile-friendly.
6. Run lint/typecheck/build.
7. Summarize changed files and edge cases.
```

## 28. Codex Command: Phase 5 Oxygen Tank Card

```text
Task: Implement the CareLite oxygen tank runtime card.

Requirements:
1. Use carelite.oxygen_tank_profiles and carelite.oxygen_tank_sessions.
2. Add oxygen tank card to the top of CareLite dashboard.
3. States:
   - no active tank: Start Tank
   - running: show estimated remaining time and Pause Tank
   - paused: show estimated remaining time and Resume Tank
   - warning: show Prepare Next Tank
   - depleted: show Is this a new tank? with No / Yes New Tank
4. Implement frontend countdown without updating the database every second.
5. Database updates only on:
   - start
   - pause
   - resume
   - depleted
   - replace
   - void/correct if added
6. Use estimated wording everywhere.
7. Add optional carelite.entries records for major oxygen events.
8. Run lint/typecheck/build.
9. Summarize changed files and manual QA steps.
```

## 29. Codex Command: Phase 6 Admin

```text
Task: Add CareLite admin management screens.

Requirements:
1. Add /admin/carelite or integrate into existing admin navigation.
2. Create/edit carelite.items.
3. Create/edit carelite.oxygen_tank_profiles.
4. Fields for items:
   - name
   - item_type
   - category
   - icon
   - color
   - default_amount
   - default_unit
   - min_interval_minutes
   - max_uses_per_24h
   - max_amount_per_24h
   - is_scheduled
   - schedule_period
   - requires_confirmation
   - allow_note
   - active
   - sort_order
   - notes
5. Fields for oxygen tank profiles:
   - name
   - tank_type
   - starting_pressure_psi
   - usable_liters
   - default_flow_lpm
   - warning_minutes_remaining
   - active
   - notes
6. Keep admin separate from Mom-facing CareLite page.
7. Run lint/typecheck/build.
8. Summarize changed files and risks.
```

## 30. Gemini CLI Setup

Install/run Gemini CLI using one of these:

```bash
npx @google/gemini-cli
```

or

```bash
npm install -g @google/gemini-cli
```

or:

```bash
brew install gemini-cli
```

Run inside the repo:

```bash
cd /path/to/mom-care-app
gemini
```

Non-interactive example:

```bash
gemini -p "Explain the architecture of this codebase"
```

Structured output example:

```bash
gemini -p "Review this CareLite migration for risks" --output-format json
```

## 31. Gemini Usage Strategy

Use Gemini as reviewer/planner, not primary implementer.

Best Gemini jobs:

* Review architecture
* Find missing edge cases
* Compare schema against requirements
* Inspect code for hidden coupling
* Generate QA checklist
* Review accessibility/mobile usability
* Review whether Codex changed unrelated files

Do not let both Codex and Gemini edit the same files at the same time. That is merge-conflict soup.

## 32. Gemini Command: Architecture Review

```bash
gemini -p "Review the proposed CareLite architecture in this repo. Focus on schema boundaries, whether the carelite schema is properly isolated from the care schema, risks with oxygen tank session tracking, and whether the implementation is overcomplicated. Do not modify files. Return a concise issue list with severity and recommended fixes."
```

## 33. Gemini Command: Migration Review

```bash
gemini -p "Review the CareLite Supabase migration files. Check for missing indexes, unsafe constraints, bad defaults, RLS concerns, patient_id consistency, and whether the oxygen tank session model correctly supports start/pause/resume/replace. Do not modify files. Return exact file/line concerns and recommended SQL changes."
```

## 34. Gemini Command: UI Review

```bash
gemini -p "Review the CareLite UI for mobile usability and caregiver/patient simplicity. The user is older and may be tired or short of breath. Check whether the UI has too much text, too-small buttons, unclear status colors, or unsafe wording like 'safe to take'. Do not modify files. Return prioritized fixes."
```

## 35. Gemini Command: Test Plan

```bash
gemini -p "Create a QA checklist for CareLite. Include med timing, rolling 24-hour limits, AM/PM daily reset, prednisone quantity logging, Powerade intake logging, pee/poop tracking, quick notes, oxygen tank start/pause/resume/depleted/new tank flow, mobile layout, and recent activity feed. Do not modify files."
```

## 36. Gemini Command: Diff Review

```bash
gemini -p "Review the current git diff for the CareLite feature. Identify unrelated changes, risky changes, missing tests, type errors likely to appear, and places where the implementation deviates from the CareLite dev documentation. Do not modify files. Return a short punch list."
```

## 37. IDE Workflow

Recommended IDE: VS Code or Cursor.

### Extensions / Tools

* Supabase extension, optional
* ESLint
* Prettier
* TypeScript tooling
* GitLens, optional
* Tailwind IntelliSense if Tailwind is used

### IDE Rules

Keep these files open while building:

1. CareLite dev documentation
2. Supabase migration file
3. CareLite page/component
4. CareLite data hook/service
5. Existing app route/nav file
6. Generated Supabase types

### IDE Build Loop

1. Pull latest repo
2. Create feature branch
3. Ask Codex to inspect patterns
4. Apply one phase only
5. Review diff manually
6. Run app locally
7. Run typecheck/build
8. Ask Gemini to review diff
9. Fix punch list
10. Commit

## 38. Git Workflow

Create branch:

```bash
git checkout -b feature/carelite-daily-tracker
```

After each phase:

```bash
git status
git diff
npm run typecheck
npm run lint
npm run build
```

Commit by phase:

```bash
git add .
git commit -m "Add CareLite database schema"
```

```bash
git add .
git commit -m "Add CareLite data hooks"
```

```bash
git add .
git commit -m "Add CareLite dashboard"
```

```bash
git add .
git commit -m "Add CareLite logging modals"
```

```bash
git add .
git commit -m "Add oxygen tank runtime tracking"
```

```bash
git add .
git commit -m "Add CareLite admin management"
```

## 39. Full Tool Workflow

### Best Practical Loop

1. You write/confirm the phase goal.
2. Codex implements the phase.
3. You run the app and check obvious UI/function issues.
4. Gemini reviews the diff as a second brain.
5. Codex fixes specific punch-list items.
6. You commit.
7. Move to the next phase.

### Do Not Do This

Do not give Codex the entire CareLite documentation and say:

```text
Build all of this.
```

That is how scope explodes.

Instead use phased prompts.

### Good Pattern

```text
Codex: implement Phase 3 only.
Gemini: review Phase 3 diff only.
Codex: fix these 5 issues only.
Commit.
```

## 40. QA Checklist

### Database

* `carelite` schema exists
* all tables exist
* view returns active items
* indexes exist
* seed data exists for patient
* oxygen tank profile exists

### Med / Treatment

* Breathing treatment logs
* Breathing treatment countdown works
* Max uses warning works
* Morphine interval works
* Morphine max uses works
* Tylenol amount total works
* Tylenol max amount warning works
* Prednisone logs custom tablet count

### Daily Checks

* AM meds can be marked done
* PM meds can be marked done
* Done status resets next day
* Duplicate daily tap is handled clearly

### Bathroom

* Pee logs immediately
* Poop modal opens
* Poop stool type saves to metadata
* Poop optional note appears in recent feed

### Intake

* Powerade amount selector works
* Custom amount works if implemented
* Today total updates

### Quick Notes

* Note modal opens
* Note saves
* Note appears in feed

### Oxygen

* No tank state works
* Start tank creates session
* Running countdown works
* Pause freezes estimated remaining time
* Resume continues from paused runtime
* Warning appears near threshold
* Depleted prompt appears at zero
* Yes New Tank replaces session and starts new
* No does not reset timer
* No database writes every second

### UX

* Cards are usable on phone
* Text is readable
* Buttons are large
* Colors are clear
* No unsafe wording
* Recent feed is understandable

## 41. Known Data Assumptions To Verify

These must be verified against real prescription/tank labels:

* Actual breathing treatment medication names
* Breathing treatment minimum interval
* Breathing treatment daily max
* Morphine dose
* Morphine minimum interval
* Morphine max daily uses or amount
* Tylenol max 24-hour amount
* Prednisone taper schedule
* Oxygen tank type
* Oxygen usable liters
* Oxygen flow rate

Until verified, label values as placeholders.

## 42. Risk Register

| Risk                                |   Severity | Mitigation                                                           |
| ----------------------------------- | ---------: | -------------------------------------------------------------------- |
| Mom trusts app as medical authority |       High | Use saved-rule/estimated wording only                                |
| Wrong oxygen tank capacity          |       High | Store tank profile and label placeholder as VERIFY                   |
| Wrong med max dose                  |       High | Make rules editable; verify prescriptions                            |
| Too many UI options                 |     Medium | Big buttons, special modals only where needed                        |
| Duplicate logs                      |     Medium | Recent feed + void option                                            |
| Timer drift                         | Low/Medium | Use timestamps, not per-second DB writes                             |
| Schema sprawl                       |     Medium | Keep generic `items` + `entries`; special table only for O2 sessions |

## 43. Definition of Done

CareLite MVP is done when:

* Mom/caregiver can open `/carelite`
* All key buttons are visible without hunting
* Breathing treatment timing is visible
* PRN meds log correctly
* Prednisone quantity is loggable
* Bathroom events are loggable
* Powerade intake is loggable
* Quick notes are loggable
* O2 tank timer can start/pause/resume/replace
* Recent activity shows today’s logs
* Admin can edit item rules and tank profile
* App builds without errors
* No existing care app features are broken

## 44. Final Implementation Bias

Prefer boring and reliable.

Do not make a “smart medical app.”

Make a clean daily button board that captures reality and prevents obvious timing mistakes.

That is the win.

(No sub-items found)

(No sub-items found)
