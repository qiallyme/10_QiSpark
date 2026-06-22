# Validation Checklist

## Vertical Slice 1: Capture to Timeline
- [ ] Can capture raw text/files in the UI?
- [ ] Is it saved as an ingestion item in the DB?
- [ ] Does it trigger a Mock AI Draft?
- [ ] Can the draft be reviewed in the UI?
- [ ] Can the draft be approved/edited/rejected?
- [ ] Does approval create an official QiBit and Timeline entry?
- [ ] Are all actions logged in the `activity_log`?

## Storage and Dedupe
- [ ] Are uploaded files hashed?
- [ ] Does the system block exact duplicate blobs?
- [ ] Are files stored in the managed file vault (not raw repo)?

## Spaces
- [ ] Does data default to Cody Private?
- [ ] Can an item be shared to the Mom Care space?
- [ ] Is visibility correctly scoped by space selection?
