# PILL-04 - Board Synchronization Logic

## Metadata
- **ID:** PILL-04
- **Type:** pattern
- **Scope:** component
- **Language:** Python
- **Nature:** implementation

## Why
El `Board.md` es propenso a errores de formato cuando se edita manualmente. La sincronización automática garantiza que el board siempre refleje la realidad de los archivos `.md` en `desk/tasks/`.

## What
- Escanear todos los archivos `desk/tasks/T-*.md`.
- Extraer: ID, Status, Priority, Depends On, Pills, Phase.
- Generar tres tablas: `Active`, `Blocked`, `Completed`.
- Sobreescribir el archivo `desk/tasks/Board.md` manteniendo los encabezados.

## How
Usar `TaskParser` para convertir archivos en objetos `TaskModel`. Usar una clase `BoardWriter` para renderizar las tablas Markdown.

---
**Lifecycle:** Still needed? (Keep)
