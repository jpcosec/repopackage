"""Notes about what is lintable in talk_extractor."""

# Constraint Linting

- Objective rules can be linted automatically.
- Semantic rules need heuristics or review.

## Objective

- file length
- function length
- class length
- module docstring
- class docstring
- function docstring
- multiple public classes per file

## Heuristic

- double responsibility in a class
- double responsibility in a function
- whether inheritance is the best split
- whether a file split is conceptually clean

## Command

```bash
python talk_extractor/lint_constraints.py
```
