# Tasks Board

> Single entry point for all active executable work.

## Active (status=open|in_progress)
| ID | Type | Domain | Task | Priority | Depends On | Pills | Phase |
|----|------|--------|------|----------|------------|-------|-------|
| T-03 | impl | drawers | Implement `drawers` commands | high | T-01 | 01, 06 | A |
| T-04 | impl | desk | Implement `desk` mechanics | high | T-01 | 01, 04 | A |
| T-05 | impl | execution | Implement `exec` and `capture` | high | T-01, T-04 | 01, 05, 07 | A |
| T-06 | impl | integration | Implement `eval` and `integrate` | high | T-05 | 01, 08 | A |
| T-08 | impl | capture | Implement capture adapters | medium | T-05 | 07 | A |

## Completed
| ID | Type | Domain | Task | Resolving Commit |
|----|------|--------|------|------------------|
| T-07 | design | workflow | Formalize Workflow Contracts | <current> |
| T-02 | impl | standardization | Implement `standardize create` | 553c11d |
| T-01 | refactor| cli | Refactor CLI for categories | 892438b |
| 00 | chore| workflow| Initial Workflow Setup | a5a3650 |

## Blocked (status=blocked)
| ID | Type | Domain | Blocker | Gate |
|----|------|--------|--------|------|

## Ready to Promote (from drawers/)
| ID | Type | Domain | Item |
|----|------|--------|------|
