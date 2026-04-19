# PILL-11 - CLI como Thin Shell del Domain Layer

## Metadata
- **ID:** PILL-11
- **Type:** guardrail
- **Scope:** global
- **Domain:** cli
- **Language:** Python
- **Nature:** context
- **Status:** active
- **Reusable:** yes
- **Applies To:**
  - `src/repopackage/cli/`

## Why
El CLI actual implementa lógica de negocio directamente en los comandos (ej: `atomize_task` sabe cómo parsear checklists, generar IDs de pills, actualizar secciones). Esto hace que la misma lógica no sea accesible desde código Python, y obliga a los agentes a pensar en términos de "qué comando CLI correr" en lugar de "qué operación de workflow ejecutar".

## What
- Los comandos CLI deben ser ≤10 líneas de lógica real.
- Toda lógica de negocio vive en `src/repopackage/workflow/`.
- El CLI solo: parsea argumentos, instancia `Workspace()`, llama al método correcto, imprime resultado con `Rich`.
- Prohibido importar `MarkdownEngine`, `TaskParser`, `BoardWriter` directamente en comandos CLI.

## How
```python
# CORRECTO - CLI thin shell
@tasks_app.command(name="atomize")
def atomize_task(task_id: str):
    ws = Workspace()
    pills = ws.desk.tasks.atomize(task_id)
    for p in pills:
        typer.echo(f"Created: {p.id}")

# INCORRECTO - lógica en el comando
@tasks_app.command(name="atomize")
def atomize_task(task_id: str):
    engine = MarkdownEngine(...)
    checklist = engine.extract_checklist(...)
    for item in checklist:
        pill_id = f"PILL-{next_id:02d}"
        ...  # 50 líneas de lógica
```

---
**Lifecycle:** Still needed? (Keep)
