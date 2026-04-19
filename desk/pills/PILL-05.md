# PILL-05 - Task Atomization Logic

## Metadata
- **ID:** PILL-05
- **Type:** logic
- **Scope:** component
- **Language:** Python
- **Nature:** implementation

## Why
Facilitar la creación de micro-contextos. El Supervisor diseña en una tarea y el CLI genera los archivos de apoyo automáticamente.

## What
- Leer una tarea y buscar la sección "How to Do It (Suggested)" o una lista de "Checklist".
- Por cada item, generar un archivo `desk/pills/PILL-XXX.md`.
- Usar el template de `workflow/docs/template/context_pills.md`.

## How
El comando `desk tasks atomize` debe pedir un `task_id` y generar las píldoras vinculadas.

---
**Lifecycle:** Still needed? (Keep)
