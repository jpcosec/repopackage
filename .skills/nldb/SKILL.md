---
name: nldb
description: Bidirectional transformation between Markdown and structured data (JSON/YAML). Use when a Markdown document serves as a "database" record that must be programmatically updated or extracted without losing human readability.
---

# nldb

Use `nldb` to treat Markdown as a structured, reversible data store.

## Core Workflow
1. **Scaffold**: Run `nldb example` to see a reference implementation.
2. **Model**: Define a Pydantic model inheriting from `StructuredNLDoc`.
3. **Template**: Place the Markdown structure in the `__template__` attribute using semantic markers:
   - Scalar: `⸢rev•field⸥`
   - List: `⸢rev,list•field⸥`
   - YAML Block: `⸢rev,dict•field⸥`
4. **Validate**: **Always** run `nldb validate` to ensure your template is idempotent.

## Commands
- `nldb extract <model> <input.md> <output.json>`: Document -> Data.
- `nldb render <model> <input.json> <output.md>`: Data -> Document.
- `nldb validate <model> --input <input.md>`: Checks idempotency.
- `nldb example [path]`: Creates a comprehensive example project.
- `nldb init [path]`: Initializes this skill in a new project.

## Advanced Usage
For complex namespaces (`optrev`, `py`, `render`) and structural handlers, see [references/markers.md](references/markers.md).

## Safety Rules
- **No Pipes in Tags**: Use `,` not `|` for handlers (e.g., `⸢rev,table⸥`) to avoid breaking Markdown table parsing.
- **Round-trip Integrity**: If a document change is made, verify that `extract` still produces the expected JSON before committing.
