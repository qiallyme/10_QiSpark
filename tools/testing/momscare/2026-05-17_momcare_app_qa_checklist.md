---
title: MomCare App QA Checklist
date: 2026-05-17
type: qa-checklist
app: MomCare
status: draft
tags:
  - momcare
  - qa
  - testing
  - checklist
  - obsidian
---

# MomCare App QA Checklist

**Date Tested:**  
**Tester:** Cody  
**App Version / Branch:**  
**Device:**  
**Browser / OS:**  
**Environment:** Local / Dev / Production  

---

## 1. App Startup & Access

- [ ] App opens without crashing.
- [ ] No console errors appear on initial load.
- [ ] App loads within a reasonable time.
- [ ] User can access the main dashboard/home screen.
- [ ] App works on desktop.
- [ ] App works on mobile.
- [ ] Layout does not break on small screens.
- [ ] Navigation/menu is visible and usable.
- [ ] Page refresh does not break the app.
- [ ] Direct URL navigation works if applicable.

### Notes

---

## 2. Main Dashboard

- [ ] Dashboard clearly shows today’s care status.
- [ ] Dashboard shows the current date.
- [ ] Dashboard shows the caregiver name or active user if applicable.
- [ ] Dashboard shows urgent/open care items.
- [ ] Dashboard shows recent logs or last update.
- [ ] Dashboard shows upcoming appointments or reminders.
- [ ] Dashboard separates urgent from routine.
- [ ] Dashboard is readable at a glance.
- [ ] Dashboard does not feel cluttered.
- [ ] Dashboard has clear buttons for adding new entries.

### Notes

---

## 3. Daily Care Log

- [ ] User can create a new daily care log.
- [ ] Date defaults to today.
- [ ] User can edit the date if needed.
- [ ] User can add morning notes.
- [ ] User can add afternoon notes.
- [ ] User can add evening notes.
- [ ] User can save partial entries.
- [ ] User can edit saved entries.
- [ ] User can delete or archive incorrect entries.
- [ ] App confirms when an entry is saved.
- [ ] App warns before deleting.
- [ ] Saved logs appear in the correct order.
- [ ] Logs do not duplicate after saving.
- [ ] Required fields are clear.
- [ ] Optional fields are clearly optional.

### Notes

---

## 4. Vitals Tracking

- [ ] User can enter blood pressure.
- [ ] Blood pressure format is easy to understand.
- [ ] User can enter heart rate.
- [ ] User can enter oxygen saturation.
- [ ] User can enter temperature.
- [ ] User can enter glucose.
- [ ] User can enter pain level.
- [ ] User can mark whether vitals were taken before or after eating.
- [ ] User can add notes about symptoms or context.
- [ ] App handles missing vitals without crashing.
- [ ] App flags unusual values visually, if that feature exists.
- [ ] App does not provide unsafe medical advice.
- [ ] Vitals save correctly.
- [ ] Vitals display correctly in history.
- [ ] Vitals can be edited if entered wrong.
- [ ] Units are clear: °F, bpm, %, mg/dL, etc.

### Notes

---

## 5. Oxygen / Breathing Equipment Tracking

- [ ] User can record oxygen tubing check.
- [ ] User can record whether tubing has kinks.
- [ ] User can record oxygen tank count.
- [ ] User can record full tanks.
- [ ] User can record empty tanks.
- [ ] User can record concentrator status if applicable.
- [ ] User can record charger/battery status.
- [ ] User can mark needs reorder.
- [ ] App clearly shows low oxygen supply alerts if applicable.
- [ ] App allows caregiver notes for breathing treatments.
- [ ] App handles not checked without treating it as failure.

### Notes

---

## 6. Meals / Food / Intake

- [ ] User can log breakfast.
- [ ] User can log lunch.
- [ ] User can log dinner.
- [ ] User can log snacks.
- [ ] User can log drinks.
- [ ] User can mark appetite: good / okay / poor.
- [ ] User can note food reactions or stomach issues.
- [ ] User can mark after eating when logging glucose.
- [ ] Food entries save correctly.
- [ ] Food history is easy to review.
- [ ] App does not make the meal log too complicated.

### Notes

---

## 7. Hygiene / Bathroom / Personal Care

- [ ] User can log bathroom assistance.
- [ ] User can log hygiene assistance.
- [ ] User can use respectful wording, not demeaning labels.
- [ ] User can log wipes/cleaning.
- [ ] User can log clothing or bedding change if applicable.
- [ ] User can mark not needed.
- [ ] User can add private caregiver notes.
- [ ] Entries are easy to complete quickly.
- [ ] App avoids making routine care feel overly clinical.

### Notes

---

## 8. Safety Scan

- [ ] User can complete a daily safety scan.
- [ ] Checklist includes kitchen.
- [ ] Checklist includes living room.
- [ ] Checklist includes bathroom path.
- [ ] Checklist includes bedroom path.
- [ ] Checklist includes oxygen tubing.
- [ ] Checklist includes fall hazards.
- [ ] Checklist includes clutter/laundry.
- [ ] Checklist includes floor hazards.
- [ ] User can mark each area as clear / needs attention / not checked.
- [ ] User can add notes.
- [ ] User can create follow-up tasks from safety issues.
- [ ] Safety scan saves to the daily log.

### Notes

---

## 9. Tasks & Follow-Ups

- [ ] User can create a task.
- [ ] User can assign a task category.
- [ ] User can set priority.
- [ ] User can set due date.
- [ ] User can mark task as done.
- [ ] User can edit task.
- [ ] User can delete/archive task.
- [ ] Tasks can be linked to appointments, care logs, or provider instructions.
- [ ] Open tasks are visible on dashboard.
- [ ] Completed tasks are still accessible in history.
- [ ] App separates care tasks from admin tasks.
- [ ] App separates urgent tasks from routine follow-ups.

### Notes

---

## 10. Appointments

- [ ] User can add an appointment.
- [ ] User can enter appointment type.
- [ ] User can enter provider/location.
- [ ] User can enter date and time.
- [ ] User can add prep notes.
- [ ] User can add transportation notes.
- [ ] User can add follow-up notes after appointment.
- [ ] Appointment appears on dashboard or calendar view.
- [ ] Appointment can be edited.
- [ ] Appointment can be canceled/archived.
- [ ] Appointment does not disappear after the date passes.
- [ ] Past appointments are easy to review.

### Notes

---

## 11. Provider / MyChart Task Capture

- [ ] User can enter provider task manually.
- [ ] User can paste copied MyChart/task text.
- [ ] User can upload or attach screenshot/photo if supported.
- [ ] User can categorize provider tasks.
- [ ] User can mark task source: MyChart / provider / phone call / discharge papers / other.
- [ ] User can mark urgency.
- [ ] User can link provider task to Mom’s care record.
- [ ] User can mark provider task as scheduled.
- [ ] User can mark provider task as completed.
- [ ] App preserves original text/source notes.

### Notes

---

## 12. Voice / Quick Capture

- [ ] User can quickly add a note without filling out a huge form.
- [ ] User can capture messy real-life notes and clean them later.
- [ ] User can add quick note from dashboard.
- [ ] Quick notes are timestamped.
- [ ] Quick notes can be converted into tasks.
- [ ] Quick notes can be converted into care log entries.
- [ ] Quick notes can be edited after capture.
- [ ] App does not force perfection during capture.

### Notes

---

## 13. Search & History

- [ ] User can search care logs.
- [ ] User can search tasks.
- [ ] User can search appointments.
- [ ] User can filter by date.
- [ ] User can filter by category.
- [ ] User can filter by status.
- [ ] User can find a previous day’s log quickly.
- [ ] User can review trends without hunting.
- [ ] Search results are clear and readable.

### Notes

---

## 14. Reports / Export

- [ ] User can generate a daily summary.
- [ ] User can generate a weekly summary.
- [ ] User can generate an appointment prep summary.
- [ ] User can export to Markdown.
- [ ] User can export to PDF if supported.
- [ ] Export includes date range.
- [ ] Export includes vitals.
- [ ] Export includes tasks.
- [ ] Export includes appointments.
- [ ] Export includes caregiver notes.
- [ ] Export avoids clutter.
- [ ] Export is readable by a provider/family member.
- [ ] Export does not expose unnecessary private notes unless selected.

### Notes

---

## 15. Data Integrity

- [ ] Saved data persists after refresh.
- [ ] Saved data persists after closing/reopening app.
- [ ] Editing one entry does not change unrelated entries.
- [ ] Deleting one entry does not delete unrelated data.
- [ ] Duplicate records are not created accidentally.
- [ ] Dates are stored correctly.
- [ ] Times are stored correctly.
- [ ] Empty fields do not break the app.
- [ ] Special characters do not break saving.
- [ ] Long notes do not break layout or database save.
- [ ] App handles connection/database errors gracefully.

### Notes

---

## 16. Error Handling

- [ ] App shows useful error messages.
- [ ] Error messages explain what went wrong.
- [ ] Error messages tell user what to do next.
- [ ] App does not expose raw technical errors to normal users unless in dev mode.
- [ ] Failed saves are clearly shown.
- [ ] User does not think something saved when it failed.
- [ ] App protects against accidental duplicate submissions.
- [ ] App handles invalid input without crashing.

### Notes

---

## 17. UI / UX Sanity Check

- [ ] Buttons are clearly labeled.
- [ ] Forms are not too long.
- [ ] Most common actions are easy to reach.
- [ ] Text is readable.
- [ ] Spacing is clean.
- [ ] Important information is visually prioritized.
- [ ] Urgent items stand out.
- [ ] Routine items do not scream for attention.
- [ ] Mobile layout is usable one-handed.
- [ ] The app feels calm, not chaotic.
- [ ] The app supports caregiver reality, not fantasy-office workflow.

### Notes

---

## 18. Accessibility & Low-Energy Use

- [ ] App can be used when caregiver is tired.
- [ ] App can be used quickly during interruptions.
- [ ] Labels are plain language.
- [ ] Click/tap targets are large enough.
- [ ] Color is not the only way status is shown.
- [ ] Important items have text labels.
- [ ] Forms can be completed in under 1–2 minutes where possible.
- [ ] App does not require perfect typing.
- [ ] App supports capture now, organize later.

### Notes

---

## 19. Privacy / Permissions

- [ ] Sensitive notes are not exposed on public screens.
- [ ] Export does not include private notes by default.
- [ ] User roles/permissions work if applicable.
- [ ] Family-facing view is separate from caregiver/admin view if applicable.
- [ ] App does not leak private data in console logs.
- [ ] App does not store unnecessary sensitive data.
- [ ] Backups/export files are named clearly.

### Notes

---

## 20. Final Retest Checklist

- [ ] App still starts.
- [ ] Dashboard still loads.
- [ ] Daily log still saves.
- [ ] Vitals still save.
- [ ] Tasks still save.
- [ ] Appointments still save.
- [ ] Search/history still works.
- [ ] No new console errors.
- [ ] Previous bug is fixed.
- [ ] No obvious new bug was introduced.
- [ ] Updated behavior matches the requested fix.
- [ ] Documentation/notes were updated if behavior changed.

### Notes

---

# 2026-05-18 Initial Smoke Pass

**Environment:** Local dev  
**URL:** `http://127.0.0.1:5173`  
**Build:** Passed via `npm run build`  
**Direct route probe:** `/`, `/vitals`, `/tasks`, and `/admin/dashboard` all returned HTTP 200 in local dev  
**Rendered browser validation:** Blocked in this session because sandboxed Chromium/Edge headless runs failed with Windows access-denied profile/lock errors

## Initial Findings

### ISSUE-001 - README/docs alignment is not usable yet

**Priority:** P1  
**Type:** Docs  
**Area:** Documentation  
**Status:** Open

**Expected**  
MomsCare should have a real README that explains what the app is, how to run it locally, and how the caregiver/admin surfaces are organized.

**Actual**  
`apps/frontend/README.md` is still the stock Vite template, and the repo root `README.md` only contains `# momscare`.

**Evidence**  
- `apps/frontend/README.md` contains generic Vite boilerplate
- `README.md` at the repo root is only a one-line placeholder

**Impact**  
Checklist items around local run instructions, troubleshooting, and current app behavior cannot be verified from the repo docs.

### ISSUE-002 - Production bundle size is a mobile-load risk

**Priority:** P2  
**Type:** Performance  
**Area:** Startup / Mobile  
**Status:** Open

**Expected**  
The caregiver app should stay lean enough that startup remains reasonable on phone-class devices.

**Actual**  
The current production build emits a single `assets/index-DRPCntrI.js` bundle of about `1,386.74 kB`, and Vite warns that some chunks are larger than the recommended threshold.

**Evidence**  
Observed in the local `npm run build` output during this smoke pass.

**Impact**  
This does not fail the build, but it is a real risk against the checklist goals for quick loading and low-friction mobile use.

# Issue Capture Template

## ISSUE-000 — Short Title

**Priority:** P0 / P1 / P2 / P3  
**Type:** Bug / UI / UX / Data / Performance / Feature / Safety / Export  
**Area:** Dashboard / Daily Log / Vitals / Tasks / Appointments / Reports / Other  
**Status:** Open / Sent to AI / Fixed / Retest Needed / Closed / Deferred  

### Expected

What should have happened?

### Actual

What happened instead?

### Steps to Reproduce

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

### Evidence

Screenshot, traceback, console error, wrong output, broken layout, etc.

### Impact

Why does this matter?

### AI Instruction

Tell the AI exactly what to fix.

Example:

Fix the daily care log save behavior so entries persist after refresh. Do not change unrelated dashboard layout. Add a simple test or manual verification note showing that saved logs remain visible after reload.

---

# AI Work Order Template

## MomCare App Work Order

**Goal:**  
Fix the highest-priority testing issues without redesigning unrelated parts of the app.

## Rules

- [ ] Fix P0 and P1 issues first.
- [ ] Do not refactor unrelated architecture.
- [ ] Do not rename fields unless required.
- [ ] Preserve existing data structure unless a migration is necessary.
- [ ] Keep forms fast and caregiver-friendly.
- [ ] Update documentation if behavior changes.
- [ ] Summarize files changed, fixes made, and how to retest.

## Issues to Fix

- [ ] ISSUE-001:
- [ ] ISSUE-002:
- [ ] ISSUE-003:

## Done Criteria

- [ ] App launches.
- [ ] Core care log flow works.
- [ ] Vitals/tasks/appointments save correctly.
- [ ] No new obvious console errors.
- [ ] Retest checklist passes.
