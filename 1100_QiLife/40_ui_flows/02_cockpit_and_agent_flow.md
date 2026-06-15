# Cockpit and Agent Flow
The UI serves as a Cockpit for managing the AI Life Copilot.

## Core Interaction
- “What happened?” / “Talk to QiLife” / “Handle this.”
- The home screen focuses on today's state, pending AI drafts, open loops, and an insight feed.

## Feature Toggles / Adoption Modes
QiLife supports feature toggles through a central feature registry (`frontend/src/config/features.ts`).
Adoption Presets: Simple Mode, Care Mode, Full Mode.
Toggling a feature off hides it from navigation but does not delete data.
