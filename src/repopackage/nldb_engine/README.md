# nlDB Engine

A highly decoupled, structurally aware Markdown extraction and template mapping architecture based fundamentally on `mdast` principles natively applied over GitHub Flavored Markdown (GFM).

## The Core Philosophy

The primary mechanism resolves around creating completely decoupled search instructions ("**Recipes**") compiled natively from `__template__` string definitions declared directly on Pydantic models. Our engine extracts nested semantic keys intelligently across the data without relying on inherently fragile, blind index-tree counting. 

It accomplishes this via **Stateful Sequential Cursor Mapping** and generic **Array Mapping Factories**.

## Architecture Layers

### 1. `AST_Handler` 
*File: `ast_handler.py`*
Splits raw string markdown natively into top-level blocks while fully preserving their inner syntax boundaries using standard `markdown-it-py` syntax traversal.

### 2. `TemplateExtractor`
*File: `template_extractor.py`*
A compilation pass. It walks securely over Template blocks, utilizing the `SharedNodeHandler` router to parse markers.
It spits out concrete array mappings, producing a searchable Recipe dictionary listing:
- `outer_type` and `outer_tag`
- `inner_path` down to the exact payload Literal (for generic structures).
- `handler_key` dynamically deciding what handles it.

### 3. `DataExtractor`
*File: `data_extractor.py`*
Executes real structural extraction on the Target Data markdown files via stateful cursor mapping.
A sequential `search_index` is tracked to ensure identical blocks (like two identically shaped `.tag == 'h2'` containers) are processed logically from top to bottom, securely avoiding recursive overlap mapping issues.

### 4. `SharedNodeHandler` 
*File: `node_handler.py`*
The central routing Factory bridging logic natively across parsing and extracting utilizing a **2-Step Block Strategy**:
1. **Outer Block Handling**: Identifies the container (`ordered_list`, `bullet_list`, `tbody`) and computes its internal data boundary limits structurally for iteration.
2. **Inner Iterators**: Recursively steps into child items (`tr`, `li`) mapping arbitrarily deep nested payloads without fixed scalar path collisions automatically.

* **`TextNodeHandler`**: Natively targets basic Literals exclusively (Headings, Paragraphs, Quotes, Fences, HTML). Iteratively avoids double-mapping generic parent components by explicitly refusing nodes with children.
* **`ListNodeHandler`** & **`TableNodeHandler`**: Polymorphic container interceptors operating on the 2-Step model. They eat AST arrays cleanly mapping `N-depth` properties natively `{prop: val}`.

### The Comma Delimiter Trait Rule
*CRITICAL:* Pydantic structural templates must **NEVER** use the pipe `|` character when isolating traits inside extraction markers (e.g. `⸢rev|table•col1⸥`). Since standard `mdast` / `markdown-it` parsing processes pipes as formal cell column delineators, it will rip the marker payload apart across multiple cells and break structural alignment. 

Always use **commas** for inner-modifier lists:
✅ **Correct:** `⸢rev,table•col1⸥`
❌ **Broken AST:** `⸢rev|table•col1⸥`
