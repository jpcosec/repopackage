# PILL-03 - Contract Validation (Pydantic)

## Metadata
- **ID:** PILL-03
- **Type:** model
- **Scope:** global
- **Language:** Python
- **Nature:** implementation

## Why
Garantizar que los archivos `task.md` y `context_pill.md` cumplen el contrato antes de procesarlos.

## What
- Modelos Pydantic para `Task`, `Pill` y `ModuleContract`.
- Validación estricta de Enums (Status, Priority).
- Transformación automática de rutas relativas a objetos `Path`.

## How
El `MarkdownEngine` debe devolver diccionarios que se inyecten en estos modelos.

---
**Lifecycle:** Still needed? (Keep)
