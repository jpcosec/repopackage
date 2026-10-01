---
id: atom-repopackage-what
title: Repopackage — What it is
five_wh_one_plus: what
tags:
- project:repopackage
- source:legacy-brief
- kind:code
provenance: atom-repopackage.md::What it is
---

# Repopackage — What it is

## Answer

Repopackage is a deterministic control plane that sits above Git and Google's `repo` tool to enable recursive, contract-based repository composition. It treats Git repositories as typed nodes in a dependency graph, allowing independent repos to evolve in parallel while maintaining schema-validated integration surfaces via `compose.yaml` project models and `integration.contract.yaml` contract files.
