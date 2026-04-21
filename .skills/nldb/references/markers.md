# nlDB Marker Grammar

## Namespaces
- **`rev•`**: Reversible (Required). Must extract and render symmetrically. Use for the core "truth" of the document.
- **`optrev•`**: Optional Reversible. If missing in the Markdown, it returns `None` in the data instead of failing.
- **`render•`**: Render-only. Injected during rendering but ignored during extraction.
- **`py•`**: Python Expression. Evaluates code against the model data (e.g., `⸢py•len(items)⸥`).
- **`revop•`**: Project-specific convention for Operational Metadata (e.g., commit hashes).

## Handlers (Structural Context)
Use a comma after the namespace to trigger specific parsing logic:
- **`,list•`**: Maps repeated Markdown list items (bullets/ordered) to a list of scalars or objects.
- **`,dict•`**: Maps a YAML/Frontmatter block to a dictionary/Pydantic model.
- **`,table•`**: Used inside a Markdown table row template to map rows to a collection.

## Hybrid Mode
The renderer processes the entire document through **Jinja2** after resolving nlDB markers.
- Use `⸢rev•field⸥` for data you want to extract back.
- Use `{{ field }}` for presentation-only logic or formatting that should not be extracted.

## Pro-Tips
- **Table Delimiters**: Never use the pipe `|` inside a marker tag (e.g., `⸢rev|table⸥`) as it breaks Markdown table parsing. Use `⸢rev,table⸥` instead.
- **Anchoring**: Place markers near stable Markdown elements (Headings, Bold labels) to help the structural parser stay aligned.
