---
id: atom-repopackage-why
title: Repopackage — Why
five_wh_one_plus: why
tags:
- project:repopackage
- source:legacy-brief
- kind:code
provenance: atom-repopackage.md::Why
---

# Repopackage — Why

## Answer

Multi-repo ecosystems lack a formal composition layer: flat package managers cannot express versioned cross-repo dependencies, monolithic repos force lockstep lifecycle, and `google repo` provides workspace materialization but no type-safe dependency resolution or contract validation. Repopackage fills that gap by adding typed dependency specs, deterministic lockfiles (`compose.lock.yaml`), and validation between resolved and materialized state. It is built for the hum-ecosystem meta-repo to allow tools like deskops and hum-scrapper to evolve independently while remaining composable.
