# Drawer Spec Package Contract

## Purpose
- Define the durable planning/spec package stored in `desk/drawers/specs/`.

## Required Layout

```text
desk/drawers/specs/<topic>/
  spec.md
  decisions.md
  promotion.md
  open_questions.md
  source_manifest.json
  artifacts/
```

## Required Meanings
- `spec.md` - consolidated state and target model
- `decisions.md` - decision history relevant to the spec
- `promotion.md` - promotion readiness and candidate tasks/pills
- `open_questions.md` - unresolved ambiguities and blockers
- `source_manifest.json` - source provenance and evidence inventory
- `artifacts/` - curated design artifacts only

## Rules
- Drawer specs are concrete but not yet executable by default.
- Promotion status must be explicit in `promotion.md`.
- Redundant artifacts must not be copied in.
