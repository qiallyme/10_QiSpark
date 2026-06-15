# Spaces & Access Schema
QiLife supports scoped shared access via Spaces.

## Planned Tables
- `spaces`
- `space_members`
- `share_events`

## Major Record Fields
- `space_id`
- `visibility` (private, space_visible, restricted, archived)
- `created_by_person_id`

Mom Care acts as a scoped shared space, not a full EMR. Keep it simple: lightweight buckets, date/time notes, optional archive, and Cody-approved sharing from private records to Care Notes.
