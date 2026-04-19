# PILL-01 - CLI Hierarchy & Routing

## Metadata
- **ID:** PILL-01
- **Type:** pattern
- **Scope:** component
- **Language:** Python
- **Nature:** context

## Why
Evitar comandos planos. El sistema debe escalar mediante categorías para mantener la usabilidad.

## What
- Estructura obligatoria: `rp <category> <subject> <action>`.
- Ejemplo: `rp desk tasks atomize`.
- Librería base: `Typer`.

## How
Cada categoría debe ser un sub-app de Typer. Cada comando debe heredar de `CommandBase` para mantener la lógica separada del routing.

---
**Lifecycle:** Still needed? (Keep)
