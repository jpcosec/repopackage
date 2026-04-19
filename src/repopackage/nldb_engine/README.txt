nlDB Engine: Natural Language Database Engine
=================================================

The nlDB Engine is a high-fidelity, bidirectional bridge between structured 
Pydantic data models and human-readable (and LLM-navigable) Markdown documents.

It implements a "Closed Loop" philosophy where the document is the database, 
and the template is the schema.

---
HOW IT WORKS
---
1. The Schema: You define a Pydantic model inheriting from StructuredNLDoc.
2. The Template: You define a __template__ ClassVar using ⸢ ⸥ delimiters.
3. The Mapping: The engine compiles the template's AST (Abstract Syntax Tree) 
   to create a deterministic "Extraction Mask".
4. Bidirectionality: 
   - Renderer: Data + Logic -> Structured Markdown.
   - Extractor: Structured Markdown + AST Mask -> Validated Data.

---
MARKER TYPES
---
⸢rev|field_name⸥
   Required Reversible. The Extractor MUST pull this field. It must appear 
   exactly once in the template for every required field in the model.

⸢revop|field_name⸥
   Optional Reversible. For optional fields. 

⸢field_name⸥
   Reference (Read-Only). Displays the data but is ignored during extraction. 
   Useful for repeating information in multiple places.

⸢rev|table|field_name⸥
   Atomic Table. Automatically renders a list of dicts (or models) into a 
   GFM table and extracts it back into structured records.

⸢rev|dict|field_name⸥
   Atomic Dictionary. Renders a dict as a "Key : Value" bullet list and 
   extracts it back into a Python dictionary.

⸢jinja2|{{ logic }}⸥
   Computed View. Executes Jinja2 code. Non-recoverable by the Extractor.

⸢python|logic⸥
   Computed View. Evaluates Python expressions. Non-recoverable.

---
USAGE EXAMPLE
---
from repopackage.nldb_engine.engine import StructuredNLDoc, render_nl_doc

class Task(StructuredNLDoc):
    __template__ = "# ⸢rev|id⸥: ⸢rev|title⸥\nStatus: ⸢rev|status⸥"
    id: str
    title: str
    status: str = "open"

# To render
task = Task(id="T-01", title="Hello")
markdown = render_nl_doc(task)

# To extract
extracted_task = extract_nl_doc(Task, markdown)

---
EXTENDING THE ENGINE
---
- To add new Trait types: Update the `replacer` in `render_nl_doc` and 
  add a corresponding handler in `extract_nl_doc`.
- To support new AST nodes: Update the `walk` function in `compile_template_ast` 
  to handle the new node signature and recording strategy.

---
INDUSTRIAL RIGOR
---
- Contract Validation: The engine raises a ValueError if the template 
  does not satisfy the Pydantic model (missing fields or duplicates).
- Fuzzy Extraction: The Extractor uses semantic pathing and fuzzy matching 
  to find tables and lists even if the AST structure shifts during rendering.
- Deterministic Identity: Rendering and Extracting are inverse operations 
  of the same mapping.
