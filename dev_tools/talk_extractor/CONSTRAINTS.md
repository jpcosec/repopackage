# Talk Extractor Constraints

## Function Size

- No function longer than 10 code lines.
- Do not count docstrings toward that limit.
- A function should do one thing only.
- If a function has multiple stages, split it into smaller functions.
- If a function handles multiple categories or data types, split by stage or type.

## Class Design

- Use OOP structure.
- Prefer one main class per file.
- Keep classes under 50 lines when possible.
- A class should have one responsibility only.
- If a class does two things, extract a primitive base or split into specialized subclasses.

## File Size

- No file longer than 80 lines.
- If a file grows past 80 lines, split it cleanly by responsibility.
- Prefer small modules with narrow scope.

## Docstrings

- Every file must start with a docstring.
- Every class must have its own docstring.
- Every function must have its own docstring.
- Keep docstrings short unless something is genuinely hard to understand.

## General Principle

- Prefer decomposition over accumulation.
- Prefer explicit structure over helper piles.
- Prefer small primitives composed together over large multifunction units.
