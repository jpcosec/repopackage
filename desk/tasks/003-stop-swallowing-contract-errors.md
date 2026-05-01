---
id: 3
domain: solver/contracts
status: done
priority: p0

created: "2026-05-01"
---

# Stop swallowing contract errors

## Objective

Make contract-loading failures explicit enough to debug and safe enough to trust.

## Reference

- `docs/DIAGNOSIS.md`
- `src/repopackage/core/solver.py`
- `tests/test_solver_graph.py`

## What to Fix

Malformed or unreadable contracts currently fall back too silently.

## How to Do It

1. define which failures are recoverable and which are hard errors
2. remove bare silent fallback behavior
3. update tests so bad contracts do not look like successful resolution

## Validation

- malformed contracts produce visible failure or explicit degraded status
- fallback behavior, if any, is deliberate and test-covered
