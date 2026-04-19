# PILL-10 - IO Layer: Jinja2 + stdlib

## Metadata
- **ID:** PILL-10
- **Type:** pattern
- **Scope:** global
- **Domain:** io
- **Language:** Python
- **Nature:** implementation
- **Status:** active
- **Reusable:** yes
- **Applies To:**
  - `src/repopackage/cli/engines/`
  - `src/repopackage/cli/templates/`
  - `src/repopackage/workflow/`

## Why
El código actual mezcla responsabilidades: `MarkdownEngine` lee Y escribe, `atomize_task` usa `.replace()` en templates. Esto viola el principio de que Jinja2 es el único responsable de la composición/escritura, y que el código no debe reimplementar lo que stdlib ya provee.

## What
- **Lectura:** `MarkdownEngine` (regex) se mantiene para extraer secciones de `.md` existentes. No reemplazar.
- **Escritura/Composición:** Jinja2 exclusivamente. Todo `.md` generado sale de un template.
- **File ops:** `pathlib.Path` para todo. `Path(__file__).parent` para rutas relativas a módulos. No usar strings como rutas.
- **Templates:** `FileSystemLoader` debe usar path absoluto derivado de `__file__`, no del cwd.

## How
```python
# CORRECTO - path absoluto derivado del módulo
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# CORRECTO - composición via Jinja2
template = env.get_template("task.md.jinja2")
content = template.render(task=task_model)
output_path.write_text(content)

# CORRECTO - file ops con pathlib
tasks = list(tasks_dir.glob("T-*.md"))
pill_path = pills_dir / f"{pill_id}.md"

# INCORRECTO - no usar strings como paths
Path("src/repopackage/cli/templates")  # ← frágil, depende del cwd
template_content.replace("PILL-XX", pill_id)  # ← no usar replace para templates
```

## Templates requeridos
- `board.md.jinja2` — ya existe ✓
- `pill.md.jinja2` — ya existe ✓
- `task.md.jinja2` — pendiente (T-07)

---
**Lifecycle:** Still needed? (Keep)
