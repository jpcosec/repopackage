# PILL-12 - Typed __init__ Attributes for py2puml

## Metadata
- **ID:** PILL-12
- **Type:** guardrail
- **Scope:** global
- **Language:** Python
- **Nature:** context

## Why
`py2puml` genera el diagrama UML real del código comparándolo contra el ideal en `desk/design/cli_class_diagram.puml`. Para que detecte composición (`*--`), todo atributo de instancia en `__init__` debe tener anotación de tipo explícita. Sin ella, py2puml ve `None` y no puede trazar las relaciones.

## What
Todo atributo asignado en `__init__` DEBE llevar anotación explícita:

```python
# correcto
self.root: Path = root or Path.cwd()
self.desk: Desk = Desk(self)

# incorrecto — py2puml no detecta la composición
self.desk = Desk(self)
```

## How
Al escribir cualquier clase en `src/repopackage/workflow/`:
1. Anotar cada `self.attr` en `__init__` con su tipo concreto.
2. Correr `py2puml src/repopackage repopackage` y verificar que aparezcan las flechas `*--` esperadas.
3. Comparar la salida contra `desk/design/cli_class_diagram.puml` para detectar divergencias.

---
**Lifecycle:** Still needed? (Keep)
