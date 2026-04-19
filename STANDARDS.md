# Project Standards

## 1. Coding Rules (The 80/10 Rule)
- **Max File Length:** No file shall exceed 80 lines of code.
- **Max Function Length:** No function shall exceed 10 lines of executable code.
- **Single Responsibility (SRP):** 
    - One file = One class or component.
    - One function = One atomic action.

## 2. Architectural Guardrails
- **Modularization:** Prefer "packaged" or "normalized" modules over flat structures.
- **Dependency Isolation:** Modules must communicate via strict I/O contracts (`module_contract.yaml`).
- **External Libraries:** Prioritize re-packaging existing libraries over reinventing implementations.

## 3. Testing Requirements
- **Unit Tests:** Mandatory for every code change.
- **E2E Tests:** Updated and cleared at the end of each Phase.
- **Commit Gate:** No task is closed without passing tests and linting.

## 4. Documentation
- **Self-Documenting Graph:** Code must be its own index. Use JSDoc/Docstrings to explain *why* something exists.
- **Pills to Docs:** Long-term reasoning from Context Pills must be promoted to permanent documentation (`docs/`).
