# COVERAGE.md: repopackage stress-test coverage plan

## CLI surfaces

| Comando | ST | Estado |
|---------|----|--------|
| `rp init` | ST-init | executed |
| `rp resolve` | ST-resolve | executed |
| `rp sync` | ST-sync | executed |
| `rp validate` | ST-validate | executed |
| `rp status` | ST-status | executed |
| `rp generate` | ST-generate | executed |
| `rp graph` | ST-graph | executed |
| `rp exports` | ST-exports | executed |
| Entry points (rp, repopackage, python -m) | ST-entrypoints | executed |
| compose.yaml format | ST-compose | executed |
| Edge cases OS/IO | ST-edge-cases | executed |
| Python API | ST-api | seed |
| End-to-end pipeline | ST-pipeline | seed |
| compose.lock.yaml edge cases | ST-lockfile | seed |
| Test suite health | ST-test-suite | seed |
| Google Repo tool dependency | ST-repo-dep | seed |

## Use-cases cubiertos

| UC | Narrativa | STs que lo cubren |
|----|-----------|-------------------|
| UC-01 | Init project | ST-init, ST-compose, ST-entrypoints |
| UC-02 | Resolve deps | ST-resolve, ST-compose |
| UC-03 | Validate workspace | ST-validate, ST-status |
| UC-04 | Visualize deps | ST-graph |
| UC-05 | Export capabilities | ST-exports, ST-generate |
| UC-06 | Sync workspace | ST-sync |

## Superficies por cubrir

| Superficie | ST | Prioridad |
|------------|----|-----------|
| Python API (models, solver, git client) | ST-api | Media |
| Tests suite health | ST-test-suite | Alta |
| Pipeline completo: init → resolve → sync → validate | ST-pipeline | Alta |
| compose.lock.yaml formato (edge cases) | ST-lockfile | Media |
| Google Repo tool dependency | ST-repo-dep | Media |
<!--
Template:
| `rp <comando>` | ST-XXX | seed/executed/complete |
-->
