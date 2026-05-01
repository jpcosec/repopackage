---
id: 7
domain: validation
status: open
priority: p1

created: "2026-05-01"
---

# Validate materialized workspace

## Objective

Strengthen `rp validate` so it checks the real materialized workspace against lockfile and contract expectations.

## Reference

- `src/repopackage/cli/handlers.py`
- `tests/test_solver_validation.py`
- `desk/SPEC.md`

## What to Fix

Validation should prove that the materialized workspace matches the resolved composition state, not just that some files exist.

## How to Do It

1. align validation with lockfile semantics
2. check package presence and contract presence
3. make failures explicit and actionable

## Validation

- `rp validate` reports meaningful structural failures
- validation reflects the same workspace model used by resolve/status
