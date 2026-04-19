# Action Backend

## What

The action backend is the representation layer for all workflow artifacts. It provides a unified interface to **read, write, compose, and check** the markdown and YAML documents that drive the Supervisor/Executor workflow.

Artifacts are the atomic units of the system: Tasks, Pills, DesignSpecs, ModuleContracts, Board, and Evidence. Each is a structured document on disk that any agent can consume with zero prior context.

---

## Why

The workflow is built around "Zero Context Sufficiency" — any agent should be able to pick up a single artifact and act on it without understanding the rest of the repository. This requires that artifacts be:

- **Self-contained**: all relevant context is in the document itself
- **Schema-validated**: malformed artifacts are caught before they reach an agent
- **Renderable**: models can always be written back to disk in canonical format
- **Agent-ready**: any artifact can be serialized to YAML for direct LLM consumption

The action backend enforces these guarantees in one place so that nothing above it (CLI, agents, composers) has to worry about parsing or validation.

---

## Architecture

Three packages, strictly layered:

```
models/          ← data shape only (Pydantic)
artifact/        ← read / write / check (generic interface + strategies)
composers/       ← compose multiple artifacts into one
```

### models/

Pure Pydantic models. No I/O, no business logic. Each model carries two class variables:

| ClassVar | Purpose |
|---|---|
| `__template__` | Jinja2 template filename used for rendering |
| `__format__` | `"markdown"` or `"yaml"` — drives parser selection |

| Model | Format | Zone |
|---|---|---|
| `TaskModel` | markdown | desk/tasks/ |
| `PillModel` | markdown | desk/pills/ |
| `BoardModel` | markdown | desk/tasks/Board.md |
| `PhaseModel` | (embedded in Board) | — |
| `DesignSpecModel` | markdown | desk/design/ |
| `ModuleContractModel` | yaml | drawers/ |
| `EvidenceModel` | markdown | runs/ |

### artifact/

`ArtifactInterface[M]` wraps any model and exposes four operations:

| Method | Action | Notes |
|---|---|---|
| `from_disk(model_class, path)` | Read | Selects parser from `M.__format__` |
| `create(model_class, **kwargs)` | Read | Constructs model in-memory |
| `to_disk(path)` | Write | Renders `M.__template__` via Jinja2 |
| `to_agent()` | Write | YAML dump of model for LLM consumption |
| `check()` | Check | Delegates to the registered checker for `M` |

Parsers and checkers are strategy classes — the interface stays thin, the format-specific logic lives in subclasses.

**Parsers** (`artifact/parsers/`):
- `MarkdownParser` — section-based parsing (`## Header\ncontent`), footer parsing (`**Key:** value` after `---`). Handles `TaskModel` and `PillModel`.
- `YamlParser` — `yaml.safe_load` + `model_validate`. Handles `ModuleContractModel`.

**Checkers** (`artifact/checkers/`):
- `TaskChecker` — required fields non-empty, closed tasks must have `commit_sha`
- `BoardChecker` — no task ID appears in multiple phases
- `DesignSpecChecker` — all 6 layers (`layer_0`..`layer_5`) non-empty

### composers/

Composers take multiple `ArtifactInterface` instances and produce a new one (or a string). They are the only place where multi-artifact logic lives.

| Composer | Input | Output |
|---|---|---|
| `BoardComposer` | `List[ArtifactInterface[TaskModel]]` | `ArtifactInterface[BoardModel]` |
| `DispatchPackageComposer` | task + pills | `str` (YAML concat for agent) |
| `EvidenceComposer` | task + test_log + lint_log | `ArtifactInterface[EvidenceModel]` |

---

## How to Use

### Read an artifact from disk

```python
from pathlib import Path
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel

artifact = ArtifactInterface.from_disk(TaskModel, Path("desk/tasks/T-01.md"))
print(artifact.model.title)
print(artifact.model.status)
```

### Create an artifact in memory

```python
artifact = ArtifactInterface.create(
    TaskModel,
    id="T-05",
    title="Add YamlParser",
    explanation="Implement YAML parsing for ModuleContractModel.",
    what_to_fix="YamlParser class in artifact/parsers/yaml_parser.py",
    how_to_do_it="Use yaml.safe_load + model_validate.",
)
```

### Write an artifact to disk

```python
artifact.to_disk(Path("desk/tasks/T-05.md"))
```

### Serialize for an agent (to_agent)

```python
prompt = artifact.to_agent()
# Returns a YAML string — pass directly to an LLM
```

### Validate an artifact

```python
result = artifact.check()
if not result.passed:
    for v in result.violations:
        print(f"[{v.rule}] {v.field}: {v.message}")
```

### Compose a Board from tasks

```python
from repopackage.composers.board import BoardComposer

task_artifacts = [
    ArtifactInterface.from_disk(TaskModel, p)
    for p in Path("desk/tasks").glob("T-*.md")
]
board = BoardComposer(task_artifacts).compose()
board.to_disk(Path("desk/tasks/Board.md"))
```

### Build a dispatch package for an executor

```python
from repopackage.composers.dispatch import DispatchPackageComposer
from repopackage.models.pill import PillModel

task = ArtifactInterface.from_disk(TaskModel, Path("desk/tasks/T-01.md"))
pills = [
    ArtifactInterface.from_disk(PillModel, p)
    for p in Path("desk/pills").glob("PILL-*.md")
    if p.stem in task.model.pills
]
package = DispatchPackageComposer(task, pills).compose()
# Send `package` to the executor agent
```

### Capture evidence after execution

```python
from repopackage.composers.evidence import EvidenceComposer

ev = EvidenceComposer(
    task=task,
    test_log="5 passed in 0.3s",
    lint_log="",
).compose()
ev.to_disk(Path(f"runs/{task.model.id}/evidence.md"))
```

---

## How to Extend

### Add a new artifact type

1. **Create the model** in `src/repopackage/models/<name>.py`:
   - Inherit from `BaseArtifactModel`
   - Set `__template__` and `__format__`

2. **Create the template** in `src/repopackage/templates/<name>.<ext>.jinja2`.

3. **Add a parser** if the format is new (markdown/YAML are already covered). Subclass `ArtifactParser` in `artifact/parsers/` and add a dispatch branch in `MarkdownParser.parse()` or create a new parser class.

4. **Add a checker** (optional) in `artifact/checkers/`. Subclass `ArtifactChecker[YourModel]` and register it in `_CHECKERS` in `artifact/interface.py`.

5. **Add tests** in `tests/models/` and `tests/artifact/`.

### Add a new composer

Subclass `Composer[OutModel]` in `src/repopackage/composers/<name>.py`, implement `compose()`, add tests in `tests/composers/`.

### Add a new checker rule

Open the relevant checker file (e.g. `artifact/checkers/task.py`) and append a `Violation` to the list. Rules are just conditionals — keep each one under 3 lines.

### Add a new markdown section to TaskModel

1. Add the field to `TaskModel` in `models/task.py`.
2. Update the `## Section Name` block in `templates/task.md.jinja2`.
3. Add the section extraction in `MarkdownParser._parse_task()` in `artifact/parsers/markdown.py`.
4. Add a test in `tests/artifact/test_parsers.py`.
