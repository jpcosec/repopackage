# Jinja2 Deferral

## Status: DEFERRED
All Jinja2-related rendering and template logic has been archived (commented out) in the `src/` directory to simplify the `nlDB Engine` core logic and maintain structural purity.

## Impacted Areas
- `src/repopackage/nldb_engine/renderer.py`: Template rendering logic.
- `src/repopackage/nldb_engine/node_handler.py`: Marker identification logic.
- `src/repopackage/models/*.py`: Jinja2 loops and markers in `__template__` strings.
- `src/doc_logic/models/*.py`: References to `.jinja2` files.

## Deferral Pattern
Archived blocks are wrapped in:
```python
""" REFERED: jinja2 
{archived code}
"""
```
