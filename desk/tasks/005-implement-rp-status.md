---
id: 5
domain: cli/status
status: open
priority: p1

created: "2026-05-01"
---

# Implement `rp status`

## Objective

Replace the current stub with a real workspace status command.

## Reference

- `src/repopackage/cli/handlers.py`
- `tests/test_handlers.py`
- `desk/SPEC.md`

## What to Fix

`rp status` currently prints placeholder text and provides no real control-plane visibility.

## How to Do It

1. define the minimum status report
2. compare lockfile state with materialized workspace state
3. report missing lockfile, missing packages, drift, or healthy state explicitly

## Validation

- `rp status` is not a stub
- output reflects real workspace conditions
- tests cover at least healthy and unhealthy cases
