# Tasks Board

> Single entry point for all active executable work.

## Active (status=open|in_progress)
| ID | Type | Domain | Task | Priority | Depends On | Pills | Phase |
|----|------|--------|------|----------|------------|-------|-------|
| T-01 | refactor| cli | Refactor CLI for categories | high | | 01, 03 | A |
| T-02 | impl | standardization | Implement `standardize create` | high | T-01 | 01, 02 | A |
| T-03 | impl | drawers | Implement `drawers` commands | high | T-01 | 01, 06 | A |
| T-04 | impl | desk | Implement `desk` mechanics | high | T-01 | 01, 04 | A |
| T-05 | impl | execution | Implement `exec` and `capture` | high | T-01, T-04 | 01, 05, 07 | A |
| T-06 | impl | integration | Implement `eval` and `integrate` | high | T-05 | 01, 08 | A |
| T-07 | design | workflow | Formalize Workflow Contracts | high | | | A |
| T-08 | impl | capture | Implement capture adapters | medium | T-05 | 07 | A |

## Completed
| ID | Type | Domain | Task | Resolving Commit |
|----|------|--------|------|------------------|
| 00 | chore| workflow| Initial Workflow Setup | a5a3650 |

## Blocked (status=blocked)
| ID | Type | Domain | Blocker | Gate |
|----|------|--------|--------|------|

## Ready to Promote (from drawers/)
| ID | Type | Domain | Item |
|----|------|--------|------|
