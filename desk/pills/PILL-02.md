# PILL-02 - Markdown Integrity Engine

## Metadata
- **ID:** PILL-02
- **Type:** guardrail
- **Scope:** global
- **Language:** Python
- **Nature:** implementation

## Why
Los agentes suelen romper el formato de los Markdown al editarlos manualmente. El motor debe ser inmune a cambios menores de espaciado.

## What
- Usar **Regex** para extraer secciones específicas.
- No usar parsers de Markdown que regeneren el archivo completo (ej. Mistune/CommonMark) porque alteran el estilo del usuario.
- Preservar comentarios HTML y frontmatter.

## How
Implementar una clase `MarkdownEngine` con métodos `extract_section(name)` y `update_section(name, content)`.

---
**Lifecycle:** Still needed? (Keep)
