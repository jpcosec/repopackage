# Repopackage

**Recursive, Contract-Based Repository Composition.**

Repopackage treats Git repositories as nodes in a typed, recursive graph. It overcomes the limitations of flat package managers and monolithic repos by allowing independent repositories to evolve in parallel while maintaining strict, schema-validated integration surfaces.

## Core Concepts

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for a deep dive into the recursive model.

*   **Typed Integration**: Mathematical certainty of compatibility across repo and language boundaries.
*   **Decoupled Lifecycles**: Repositories evolve independently but remain traceable.
*   **Recursion**: Projects can be consumed as modules by higher-level projects without limit.
*   **Zero-Checkout Peeking**: Inspect contracts and resolve graphs without downloading gigabytes of source code.

## Examples

### 1. `compose.yaml` (Project Model)
```yaml
kind: project
name: my-assembler
uses:
  ui-kit:
    url: git@github.com:org/ui-kit.git
    branch: main
    version: "^1.0.0"
  auditor:
    url: git@github.com:org/auditor.git
    line: contextual
    branch: feat/new-rules
```

### 2. `contracts/integration.contract.yaml`
```yaml
kind: integration_contract
name: ui-kit
version: 1.2.0
exports:
  - name: ComponentRegistry
    schema: schemas/registry.json
compatibility:
  requires:
    foundation-engine: ">=2.0.0"
```

## Installation

Install locally in editable mode:
```bash
pip install -e .
```

## CLI Usage

Repopackage provides a Control Plane for your multi-repo ecosystem via the `rp` command (alias `repopackage`):

*   `rp init`: Bootstrap a new `compose.yaml` project model.
*   `rp resolve`: Walk the dependency graph and generate a `compose.lock.yaml`.
*   `rp sync`: Use Google Repo to physically materialize the resolved workspace.
*   `rp validate`: Verify physical integrity and schema consistency across the materialized workspace.
*   `rp status`: Show workspace sync and compatibility status.
*   `rp generate`: Generate language-native types from contracts.
*   `rp graph`: Export the dependency graph (Mermaid/PlantUML).

## Standards

This project follows the **80/10 Rule**:
- Max file length: 80 lines.
- Max function length: 10 lines.
- Strict SRP: One file per component.
