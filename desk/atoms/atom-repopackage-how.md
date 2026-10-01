---
id: atom-repopackage-how
title: Repopackage — How it's made
five_wh_one_plus: how
tags:
- project:repopackage
- source:legacy-brief
- kind:code
provenance: atom-repopackage.md::How it's made
---

# Repopackage — How it's made

## Answer

Python >=3.10 CLI application, installed via `pip install -e .` and invoked as `rp` or `repopackage`. Core dependencies: networkx (graph resolution), pygit2 (git inspection), ruamel.yaml (lockfile/model serialization), pydantic (typed models), semantic_version (version constraints), jsonschema (contract validation). Tests use pytest with test paths in `tests/`. Build entry point: `repopackage.cli.main:main`. Enforces strict 80/10 coding rules (max 80 lines per file, 10 lines per function).
