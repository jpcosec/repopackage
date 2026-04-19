# Tasks Board

> Single entry point for all active work.

## Active (status=open|in_progress)
| ID | Type | Domain | Task | Priority | Deps | Pills | Ph |
|----|------|--------|------|----------|------|-------|----|
| T-07 | Fix | CLI/IO | Fix IO Layer: Jinja2 Templates + stdlib Paths | P0 | T-02 | PILL-10 | A |
| T-08 | Impl | Workflow | Implement Workflow Domain Layer | P0 | T-02, T-07 | PILL-09, PILL-10, PILL-11 | A |
| T-09 | Refactor | CLI | Wire CLI Commands to Domain Layer | P0 | T-07, T-08 | PILL-11 | B |
| T-10 | Impl | CLI | Implement rp drawers CLI Submodule | P1 | T-08 | PILL-09, PILL-11 | B |
| T-11 | Impl | CLI | Implement rp eval CLI Submodule | P1 | T-08, T-09 | PILL-09, PILL-11 | C |

## Blocked (status=blocked)
| ID | Type | Domain | Blocker | Gate |
|----|------|--------|---------|------|

## Completed
| ID | Type | Domain | Task | Resolving Commit |
|----|------|--------|------|------------------|
| T-01 | - | CLI | Setup Core CLI Package | e0d6131 |
| T-02 | - | Schema | Implement Markdown Integrity Engine | d4a7b2c |
| T-03 | - | CLI | Implement rp system init-project | 7094624 |
| T-04 | - | CLI | Implement rp desk board sync | f1a2b3c |
| T-05 | - | CLI | Implement rp desk tasks atomize | c3d4e5f |
| T-06 | - | CLI | Implement rp desk pills inject | d5e6f7a |

## Ready to Promote (from drawers/)
| ID | Domain | Item |
|----|--------|------|
