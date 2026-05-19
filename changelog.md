# Changelog

## 2026-05-15

- hardened `GitAdapter`: implemented URL hashing for cache paths to avoid collisions
- hardened `CompositionSolver`: introduced specialized `SolverError` hierarchy and refactored for 80/10 compliance
- hardened `models.py`: added semantic descriptions to all model fields following project mandates
- hardened `RepoAdapter`: refactored for 80/10 compliance and improved manifest generation logic
- hardened CLI `handlers.py`: refactored for 80/10 compliance and improved error propagation
- refactored `GitAdapter`: aligned implementation with 80/10 coding standards (file/function length)

## 2026-05-01

- resolved task `003-stop-swallowing-contract-errors`: Stop swallowing contract errors

- resolved task `002-type-dependency-specs`: Type dependency specs

- resolved task `001-fix-git-adapter`: Fix git adapter for real repo inspection

- resolved task `006-fix-manifest-generation`: Fix manifest generation

- resolved task `009-run-end-to-end-composition-flow`: Run end-to-end composition flow

- resolved task `008-create-real-use-case-fixture`: Create real use case fixture

- resolved task `007-validate-materialized-workspace`: 007-validate-materialized-workspace

- resolved task `005-implement-rp-status`: 005-implement-rp-status

- resolved task `004-define-lockfile-state`: 004-define-lockfile-state

- resolved tasks 001, 002, 003: Hardened repopackage control plane (git adapter, solver models, error handling)
