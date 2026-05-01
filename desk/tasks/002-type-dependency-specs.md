---
id: 2
domain: models/solver
status: done
priority: p0

created: "2026-05-01"
---

# Type dependency specs

## Objective

Replace untyped dependency maps with an explicit dependency spec model that can represent real project intent.

## Reference

- `docs/ARCHITECTURE.md`
- `docs/DIAGNOSIS.md`
- `src/repopackage/core/models.py`
- `src/repopackage/core/solver.py`

## What to Fix

`Project.uses` is currently too weak to model the intended system correctly.

At minimum it must represent:

- `url`
- `branch`
- `version`
- `line`

## How to Do It

1. define `DependencySpec`
2. update `Project.uses`
3. update solver expectations and tests
4. make room for later explicit transitive metadata

## Validation

- dependency specs are typed
- the documented fields are representable
- tests stop relying on raw nested dicts as the intended model
