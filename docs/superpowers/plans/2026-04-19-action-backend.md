# Action Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `repopackage.models`, `repopackage.artifact`, and `repopackage.composers` — the full representation layer for the workflow artifact system.

**Architecture:** Three clean packages: `models/` (Pydantic data shapes), `artifact/` (generic Read/Write/Check interface + parser/checker backends), `composers/` (multi-artifact → artifact operations). No CLI, no subprocess, no execution logic.

**Tech Stack:** Python 3.9+, Pydantic v2, Jinja2, PyYAML, pytest

---

## File Structure

```
src/repopackage/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── base.py               # BaseArtifactModel (abstract Pydantic)
│   ├── task.py               # TaskModel + TaskStatus + TaskPriority + TaskLifecycle
│   ├── pill.py               # PillModel + PillMetadata + PillLifecycle
│   ├── board.py              # BoardModel + PhaseModel
│   ├── design_spec.py        # DesignSpecModel
│   ├── module_contract.py    # ModuleContractModel + ContractField + ValidationState
│   └── evidence.py           # EvidenceModel
├── templates/
│   ├── task.md.jinja2
│   ├── pill.md.jinja2
│   ├── board.md.jinja2
│   ├── design_spec.md.jinja2
│   ├── module_contract.yaml.jinja2
│   └── evidence.md.jinja2
├── artifact/
│   ├── __init__.py
│   ├── result.py             # CheckResult + Violation
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py           # ArtifactParser[M] abstract
│   │   ├── markdown.py       # MarkdownParser — section-based md → model
│   │   └── yaml_parser.py    # YamlParser — YAML → model
│   ├── checkers/
│   │   ├── __init__.py
│   │   ├── base.py           # ArtifactChecker[M] abstract
│   │   ├── task.py           # TaskChecker
│   │   ├── board.py          # BoardChecker
│   │   └── design_spec.py    # DesignSpecChecker
│   └── interface.py          # ArtifactInterface[M]
└── composers/
    ├── __init__.py
    ├── base.py               # Composer[Out] abstract
    ├── board.py              # BoardComposer
    ├── dispatch.py           # DispatchPackageComposer
    └── evidence.py           # EvidenceComposer

tests/
├── conftest.py               # shared fixtures (sample markdown strings)
├── models/
│   ├── test_task_model.py
│   ├── test_pill_model.py
│   ├── test_board_model.py
│   └── test_other_models.py
├── artifact/
│   ├── test_parsers.py
│   ├── test_checkers.py
│   └── test_interface.py
└── composers/
    ├── test_board_composer.py
    ├── test_dispatch_composer.py
    └── test_evidence_composer.py
```

---

## Task 1: Package scaffold

**Files:**
- Create: `src/repopackage/__init__.py`
- Create: `src/repopackage/models/__init__.py`
- Create: `src/repopackage/artifact/__init__.py`
- Create: `src/repopackage/artifact/parsers/__init__.py`
- Create: `src/repopackage/artifact/checkers/__init__.py`
- Create: `src/repopackage/composers/__init__.py`
- Create: `src/repopackage/templates/` (empty dir placeholder)
- Modify: `pyproject.toml` (fix package-data glob)
- Create: `tests/conftest.py`
- Create: `tests/models/__init__.py`
- Create: `tests/artifact/__init__.py`
- Create: `tests/composers/__init__.py`

- [ ] **Step 1: Create all `__init__.py` files**

```bash
mkdir -p src/repopackage/models
mkdir -p src/repopackage/templates
mkdir -p src/repopackage/artifact/parsers
mkdir -p src/repopackage/artifact/checkers
mkdir -p src/repopackage/composers
touch src/repopackage/__init__.py
touch src/repopackage/models/__init__.py
touch src/repopackage/artifact/__init__.py
touch src/repopackage/artifact/parsers/__init__.py
touch src/repopackage/artifact/checkers/__init__.py
touch src/repopackage/composers/__init__.py
mkdir -p tests/models tests/artifact tests/composers
touch tests/models/__init__.py tests/artifact/__init__.py tests/composers/__init__.py
```

- [ ] **Step 2: Fix `pyproject.toml` package-data**

In `pyproject.toml`, change:
```toml
[tool.setuptools.package-data]
repopackage = ["cli/templates/*.jinja2"]
```
to:
```toml
[tool.setuptools.package-data]
repopackage = ["templates/*.jinja2", "templates/*.yaml.jinja2"]
```

- [ ] **Step 3: Create `tests/conftest.py` with sample fixtures**

```python
import pytest

SAMPLE_TASK_MD = """\
# T-01 - Add BaseArtifactModel

## Traits (Composición)
`[Implementación] | [Schema] | [Python]`

## Explanation
Implement the base Pydantic model for all artifacts.

## Reference
- `src/repopackage/models/base.py`
- `tests/models/test_task_model.py`

## What to Fix / Implement
A BaseArtifactModel class with __template__ and __format__ classvars.

## How to Do It (Suggested)
1. Create base.py with abstract BaseArtifactModel
2. Add __template__ ClassVar[str]
3. Add __format__ ClassVar[Literal["markdown", "yaml"]]

## Induced Changes
- **Archivo:** `src/repopackage/models/base.py` | **Símbolo:** `BaseArtifactModel` | **Cambio:** Created.

## Depends On


## Priority
P0

---
**Status:** open
**Lifecycle:** target
**Commit SHA:**
"""

SAMPLE_PILL_MD = """\
# PILL-01 - Artifact Interface Contract

## Metadata
- **ID:** PILL-01
- **Type:** pattern
- **Scope:** global
- **Language:** Python
- **Nature:** context

## Why
All artifacts must share a common read/write interface to enable zero-context-sufficiency.

## What
ArtifactInterface[M] wraps any BaseArtifactModel and exposes from_disk, to_disk, to_agent, check.

## When
target

## Where
src/repopackage/artifact/interface.py

## How
Instantiate via ArtifactInterface.from_disk(path) or ArtifactInterface.create(**kwargs).

## Language & Conventions
Use generic TypeVar M bound to BaseArtifactModel.

---
**Lifecycle:** Keep
"""

SAMPLE_DESIGN_SPEC_MD = """\
# Design Spec: Action Backend

## Capa 0: Recolección (Contexto de Drawers)
- **Info Extraída:** Need a unified artifact interface.
- **IDs de Referencia en Drawers:** SPEC-01.

## Capa 1: Microspec (El Mapa)
- **Objetivo:** Implement R/W/Compose/Check for all artifact types.
- **Prior Art (Repackaging):** Pydantic v2, Jinja2.
- **UML de Alto Nivel:** ArtifactInterface[M] pattern.

## Capa 2: Esqueleto (Las Fronteras)
- **Definición de Módulos:** models, artifact, composers.
- **Contratos (I/O):** from_disk/to_disk/to_agent/check.
- **Diagrama de Componentes:** See action_backend.puml.
- **Definición de E2E (Winning Condition):** All artifacts round-trip through from_disk/to_disk.

## Capa 3: Pseudocode (El Cerebro)
- **Lógica de Flujo:** Parse raw text into model, validate, render via template.
- **Reutilización:** Jinja2 Environment shared across all writers.
- **UML de Detalle:** See action_backend.puml.

## Capa 4: Patterns (El Estilo)
- **Patrones de Diseño:** Generic ArtifactInterface, Strategy for parsers/checkers.
- **Reglas de Conectividad:** No subprocess, no CLI in this layer.
- **Guardrails de Estilo:** 80 lines per file, 10 lines per function.

## Capa 5: Unit Tests (La Muralla)
- **Behavioral Guard:** Round-trip parse → render produces equivalent content.
- **Casos de Borde:** Missing optional fields, empty depends_on list.
"""

SAMPLE_MODULE_CONTRACT_YAML = """\
module_name: "artifact-interface"
version: "1.0.0"
description: "Generic read/write/check interface for all artifact types."
interface:
  inputs:
    - name: path
      type: Path
      description: Filesystem path to the artifact file
  outputs:
    - name: artifact
      type: ArtifactInterface
      description: Loaded artifact with model populated
dependencies:
  external_libs:
    - name: pydantic
      version: ">=2.0"
    - name: jinja2
      version: ">=3.0"
  internal_modules:
    - "models"
traits:
  - "[Schema]"
  - "[Python]"
validation:
  unit_tests: false
  contract_tests: false
  linting_passed: false
"""

@pytest.fixture
def sample_task_md():
    return SAMPLE_TASK_MD

@pytest.fixture
def sample_pill_md():
    return SAMPLE_PILL_MD

@pytest.fixture
def sample_design_spec_md():
    return SAMPLE_DESIGN_SPEC_MD

@pytest.fixture
def sample_module_contract_yaml():
    return SAMPLE_MODULE_CONTRACT_YAML
```

- [ ] **Step 4: Verify pytest discovers tests**

```bash
cd /home/jp/repopackage && python -m pytest tests/ --collect-only -q 2>&1 | head -20
```
Expected: no errors, `0 tests collected` (nothing written yet).

- [ ] **Step 5: Commit scaffold**

```bash
git add src/ tests/conftest.py tests/models/__init__.py tests/artifact/__init__.py tests/composers/__init__.py pyproject.toml
git commit -m "chore(scaffold): initialize action_backend package structure"
```

---

## Task 2: BaseArtifactModel + TaskModel

**Files:**
- Create: `src/repopackage/models/base.py`
- Create: `src/repopackage/models/task.py`
- Create: `tests/models/test_task_model.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_task_model.py
import pytest
from repopackage.models.task import TaskModel, TaskStatus, TaskPriority, TaskLifecycle


def test_task_model_defaults():
    task = TaskModel(
        id="T-01",
        title="Test task",
        explanation="Some explanation",
        what_to_fix="Fix something",
        how_to_do_it="Do it this way",
    )
    assert task.id == "T-01"
    assert task.status == TaskStatus.OPEN
    assert task.priority == TaskPriority.P2
    assert task.lifecycle == TaskLifecycle.TARGET
    assert task.pills == []
    assert task.depends_on == []
    assert task.traits == []


def test_task_model_has_template_classvar():
    assert TaskModel.__template__ == "task.md.jinja2"
    assert TaskModel.__format__ == "markdown"


def test_task_status_enum_values():
    assert TaskStatus.OPEN == "open"
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskStatus.CLOSED == "closed"
    assert TaskStatus.BLOCKED == "blocked"


def test_task_priority_enum_values():
    assert TaskPriority.P0 == "P0"
    assert TaskPriority.P3 == "P3"


def test_task_lifecycle_enum_values():
    assert TaskLifecycle.TARGET == "target"
    assert TaskLifecycle.CURRENT == "current"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_task_model.py -v 2>&1 | tail -10
```
Expected: `ModuleNotFoundError: No module named 'repopackage'` or `ImportError`.

- [ ] **Step 3: Implement `base.py`**

```python
# src/repopackage/models/base.py
from typing import ClassVar, Literal
from pydantic import BaseModel


class BaseArtifactModel(BaseModel):
    __template__: ClassVar[str] = ""
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"
```

- [ ] **Step 4: Implement `task.py`**

```python
# src/repopackage/models/task.py
from typing import ClassVar, List, Literal, Optional
from pydantic import Field
from repopackage.models.base import BaseArtifactModel
from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TaskLifecycle(str, Enum):
    TARGET = "target"
    CURRENT = "current"


class TaskModel(BaseArtifactModel):
    __template__: ClassVar[str] = "task.md.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    id: str
    title: str
    traits: List[str] = Field(default_factory=list)
    explanation: str
    reference: List[str] = Field(default_factory=list)
    what_to_fix: str
    how_to_do_it: str
    induced_changes: Optional[str] = None
    depends_on: List[str] = Field(default_factory=list)
    priority: TaskPriority = TaskPriority.P2
    status: TaskStatus = TaskStatus.OPEN
    lifecycle: TaskLifecycle = TaskLifecycle.TARGET
    phase: Optional[str] = None
    pills: List[str] = Field(default_factory=list)
    commit_sha: Optional[str] = None
```

- [ ] **Step 5: Run test to verify it passes**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_task_model.py -v 2>&1 | tail -15
```
Expected: `5 passed`.

- [ ] **Step 6: Commit**

```bash
git add src/repopackage/models/base.py src/repopackage/models/task.py tests/models/test_task_model.py
git commit -m "feat(models): add BaseArtifactModel and TaskModel"
```

---

## Task 3: PillModel

**Files:**
- Create: `src/repopackage/models/pill.py`
- Create: `tests/models/test_pill_model.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_pill_model.py
from repopackage.models.pill import PillModel, PillMetadata, PillLifecycle


def test_pill_model_structure():
    pill = PillModel(
        title="Artifact Interface Contract",
        metadata=PillMetadata(
            id="PILL-01",
            type="pattern",
            scope="global",
            language="Python",
            nature="context",
        ),
        why="Needed for zero-context-sufficiency.",
        what="ArtifactInterface[M] contract.",
        when="target",
        where="src/repopackage/artifact/interface.py",
        how="Instantiate via from_disk or create.",
    )
    assert pill.metadata.id == "PILL-01"
    assert pill.lifecycle == PillLifecycle.KEEP
    assert pill.title == "Artifact Interface Contract"


def test_pill_has_template_classvar():
    assert PillModel.__template__ == "pill.md.jinja2"
    assert PillModel.__format__ == "markdown"


def test_pill_lifecycle_values():
    assert PillLifecycle.KEEP == "Keep"
    assert PillLifecycle.DELETE == "Delete"
    assert PillLifecycle.PROMOTE == "Promote"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_pill_model.py -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `pill.py`**

```python
# src/repopackage/models/pill.py
from typing import ClassVar, Literal
from pydantic import BaseModel
from enum import Enum
from repopackage.models.base import BaseArtifactModel


class PillLifecycle(str, Enum):
    KEEP = "Keep"
    DELETE = "Delete"
    PROMOTE = "Promote"


class PillMetadata(BaseModel):
    id: str
    type: str
    scope: str
    language: str
    nature: str


class PillModel(BaseArtifactModel):
    __template__: ClassVar[str] = "pill.md.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    title: str
    metadata: PillMetadata
    why: str
    what: str
    when: str = ""
    where: str = ""
    how: str
    lifecycle: PillLifecycle = PillLifecycle.KEEP
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_pill_model.py -v 2>&1 | tail -10
```
Expected: `3 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/repopackage/models/pill.py tests/models/test_pill_model.py
git commit -m "feat(models): add PillModel"
```

---

## Task 4: BoardModel + PhaseModel

**Files:**
- Create: `src/repopackage/models/board.py`
- Create: `tests/models/test_board_model.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_board_model.py
from repopackage.models.board import BoardModel, PhaseModel


def test_board_model_empty():
    board = BoardModel(phases=[], pills=[])
    assert board.phases == []
    assert board.pills == []


def test_phase_model_contains_task_ids():
    phase = PhaseModel(id="1", tasks=["T-01", "T-02"])
    assert phase.id == "1"
    assert "T-01" in phase.tasks


def test_board_contains_phases():
    board = BoardModel(
        phases=[PhaseModel(id="1", tasks=["T-01"])],
        pills=["PILL-01"],
    )
    assert board.phases[0].id == "1"
    assert board.pills == ["PILL-01"]


def test_board_has_template_classvar():
    assert BoardModel.__template__ == "board.md.jinja2"
    assert BoardModel.__format__ == "markdown"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_board_model.py -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `board.py`**

```python
# src/repopackage/models/board.py
from typing import ClassVar, List, Literal
from pydantic import BaseModel, Field
from repopackage.models.base import BaseArtifactModel


class PhaseModel(BaseModel):
    id: str
    tasks: List[str] = Field(default_factory=list)


class BoardModel(BaseArtifactModel):
    __template__: ClassVar[str] = "board.md.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    phases: List[PhaseModel] = Field(default_factory=list)
    pills: List[str] = Field(default_factory=list)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_board_model.py -v 2>&1 | tail -10
```
Expected: `4 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/repopackage/models/board.py tests/models/test_board_model.py
git commit -m "feat(models): add BoardModel and PhaseModel"
```

---

## Task 5: DesignSpecModel + ModuleContractModel + EvidenceModel

**Files:**
- Create: `src/repopackage/models/design_spec.py`
- Create: `src/repopackage/models/module_contract.py`
- Create: `src/repopackage/models/evidence.py`
- Create: `tests/models/test_other_models.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/models/test_other_models.py
from repopackage.models.design_spec import DesignSpecModel
from repopackage.models.module_contract import ModuleContractModel, ContractField, ValidationState
from repopackage.models.evidence import EvidenceModel


def test_design_spec_model():
    spec = DesignSpecModel(
        name="Action Backend",
        layer_0="Context collected.",
        layer_1="Build artifact system.",
        layer_2="Three packages: models, artifact, composers.",
        layer_3="ArtifactInterface[M] generic pattern.",
        layer_4="Strategy pattern for parsers and checkers.",
        layer_5="Round-trip tests for all artifact types.",
    )
    assert spec.name == "Action Backend"
    assert DesignSpecModel.__template__ == "design_spec.md.jinja2"
    assert DesignSpecModel.__format__ == "markdown"


def test_module_contract_model():
    contract = ModuleContractModel(
        module_name="artifact-interface",
        version="1.0.0",
        description="Generic R/W/Check interface.",
        inputs=[ContractField(name="path", type="Path", description="File path")],
        outputs=[ContractField(name="artifact", type="ArtifactInterface", description="Loaded artifact")],
        traits=["[Schema]", "[Python]"],
        validation=ValidationState(),
    )
    assert contract.module_name == "artifact-interface"
    assert ModuleContractModel.__template__ == "module_contract.yaml.jinja2"
    assert ModuleContractModel.__format__ == "yaml"
    assert contract.validation.unit_tests is False


def test_evidence_model():
    ev = EvidenceModel(
        task_id="T-01",
        passed=True,
        lint_ok=True,
        tests_ok=True,
        raw_log="All tests passed.",
    )
    assert ev.task_id == "T-01"
    assert ev.passed is True
    assert ev.commit_sha is None
    assert EvidenceModel.__template__ == "evidence.md.jinja2"
    assert EvidenceModel.__format__ == "markdown"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/test_other_models.py -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `design_spec.py`**

```python
# src/repopackage/models/design_spec.py
from typing import ClassVar, Literal
from repopackage.models.base import BaseArtifactModel


class DesignSpecModel(BaseArtifactModel):
    __template__: ClassVar[str] = "design_spec.md.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    name: str
    layer_0: str
    layer_1: str
    layer_2: str
    layer_3: str
    layer_4: str
    layer_5: str
```

- [ ] **Step 4: Implement `module_contract.py`**

```python
# src/repopackage/models/module_contract.py
from typing import ClassVar, List, Literal
from pydantic import BaseModel, Field
from repopackage.models.base import BaseArtifactModel


class ContractField(BaseModel):
    name: str
    type: str
    description: str


class ValidationState(BaseModel):
    unit_tests: bool = False
    contract_tests: bool = False
    linting_passed: bool = False


class ModuleContractModel(BaseArtifactModel):
    __template__: ClassVar[str] = "module_contract.yaml.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "yaml"

    module_name: str
    version: str
    description: str
    inputs: List[ContractField] = Field(default_factory=list)
    outputs: List[ContractField] = Field(default_factory=list)
    traits: List[str] = Field(default_factory=list)
    validation: ValidationState = Field(default_factory=ValidationState)
```

- [ ] **Step 5: Implement `evidence.py`**

```python
# src/repopackage/models/evidence.py
from typing import ClassVar, Literal, Optional
from repopackage.models.base import BaseArtifactModel


class EvidenceModel(BaseArtifactModel):
    __template__: ClassVar[str] = "evidence.md.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    task_id: str
    passed: bool
    lint_ok: bool
    tests_ok: bool
    raw_log: str
    commit_sha: Optional[str] = None
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
cd /home/jp/repopackage && python -m pytest tests/models/ -v 2>&1 | tail -15
```
Expected: all model tests pass.

- [ ] **Step 7: Commit**

```bash
git add src/repopackage/models/design_spec.py src/repopackage/models/module_contract.py src/repopackage/models/evidence.py tests/models/test_other_models.py
git commit -m "feat(models): add DesignSpecModel, ModuleContractModel, EvidenceModel"
```

---

## Task 6: Jinja2 Templates

**Files:**
- Create: `src/repopackage/templates/task.md.jinja2`
- Create: `src/repopackage/templates/pill.md.jinja2`
- Create: `src/repopackage/templates/board.md.jinja2`
- Create: `src/repopackage/templates/design_spec.md.jinja2`
- Create: `src/repopackage/templates/module_contract.yaml.jinja2`
- Create: `src/repopackage/templates/evidence.md.jinja2`

No tests for this task — templates are verified indirectly by the interface round-trip tests in Task 8.

- [ ] **Step 1: Create `task.md.jinja2`**

```jinja2
# {{ task.id }} - {{ task.title }}

## Traits (Composición)
`{{ task.traits | join(' | ') }}`

## Explanation
{{ task.explanation }}

## Reference
{% for ref in task.reference %}- `{{ ref }}`
{% endfor %}
## What to Fix / Implement
{{ task.what_to_fix }}

## How to Do It (Suggested)
{{ task.how_to_do_it }}

## Induced Changes
{{ task.induced_changes or '(Completar por Executor)' }}

## Depends On
{% for dep in task.depends_on %}- {{ dep }}
{% endfor %}
## Priority
{{ task.priority.value }}

---
**Status:** {{ task.status.value }}
**Lifecycle:** {{ task.lifecycle.value }}
**Commit SHA:** {{ task.commit_sha or '' }}
```

- [ ] **Step 2: Create `pill.md.jinja2`**

```jinja2
# {{ pill.metadata.id }} - {{ pill.title }}

## Metadata
- **ID:** {{ pill.metadata.id }}
- **Type:** {{ pill.metadata.type }}
- **Scope:** {{ pill.metadata.scope }}
- **Language:** {{ pill.metadata.language }}
- **Nature:** {{ pill.metadata.nature }}

## Why
{{ pill.why }}

## What
{{ pill.what }}

## When
{{ pill.when }}

## Where
{{ pill.where }}

## How
{{ pill.how }}

---
**Lifecycle:** {{ pill.lifecycle.value }}
```

- [ ] **Step 3: Create `board.md.jinja2`**

```jinja2
# Board

{% for phase in board.phases %}
## Phase {{ phase.id }}

| Task | Status |
|------|--------|
{% for task_id in phase.tasks %}| {{ task_id }} | - |
{% endfor %}
{% endfor %}
{% if board.pills %}
## Pills

{% for pill_id in board.pills %}- {{ pill_id }}
{% endfor %}
{% endif %}
```

- [ ] **Step 4: Create `design_spec.md.jinja2`**

```jinja2
# Design Spec: {{ spec.name }}

## Capa 0: Recolección (Contexto de Drawers)
{{ spec.layer_0 }}

## Capa 1: Microspec (El Mapa)
{{ spec.layer_1 }}

## Capa 2: Esqueleto (Las Fronteras)
{{ spec.layer_2 }}

## Capa 3: Pseudocode (El Cerebro)
{{ spec.layer_3 }}

## Capa 4: Patterns (El Estilo)
{{ spec.layer_4 }}

## Capa 5: Unit Tests (La Muralla)
{{ spec.layer_5 }}
```

- [ ] **Step 5: Create `module_contract.yaml.jinja2`**

```jinja2
module_name: "{{ contract.module_name }}"
version: "{{ contract.version }}"
description: "{{ contract.description }}"
interface:
  inputs:
{% for f in contract.inputs %}    - name: "{{ f.name }}"
      type: {{ f.type }}
      description: "{{ f.description }}"
{% endfor %}  outputs:
{% for f in contract.outputs %}    - name: "{{ f.name }}"
      type: {{ f.type }}
      description: "{{ f.description }}"
{% endfor %}traits:
{% for t in contract.traits %}  - "{{ t }}"
{% endfor %}validation:
  unit_tests: {{ contract.validation.unit_tests | lower }}
  contract_tests: {{ contract.validation.contract_tests | lower }}
  linting_passed: {{ contract.validation.linting_passed | lower }}
```

- [ ] **Step 6: Create `evidence.md.jinja2`**

```jinja2
# Evidence: {{ evidence.task_id }}

## Result
- **Passed:** {{ evidence.passed }}
- **Lint OK:** {{ evidence.lint_ok }}
- **Tests OK:** {{ evidence.tests_ok }}

## Raw Log
```
{{ evidence.raw_log }}
```

---
**Commit SHA:** {{ evidence.commit_sha or '' }}
```

- [ ] **Step 7: Commit**

```bash
git add src/repopackage/templates/
git commit -m "feat(templates): add Jinja2 templates for all artifact types"
```

---

## Task 7: CheckResult + Violation

**Files:**
- Create: `src/repopackage/artifact/result.py`
- Create: `tests/artifact/test_checkers.py` (stub with result tests only for now)

- [ ] **Step 1: Write the failing test**

```python
# tests/artifact/test_checkers.py
from repopackage.artifact.result import CheckResult, Violation


def test_check_result_passed():
    result = CheckResult(passed=True, violations=[])
    assert result.passed is True
    assert result.violations == []


def test_check_result_failed_has_violations():
    v = Violation(rule="required_field", message="explanation is empty", field="explanation")
    result = CheckResult(passed=False, violations=[v])
    assert result.passed is False
    assert len(result.violations) == 1
    assert result.violations[0].rule == "required_field"


def test_violation_optional_field():
    v = Violation(rule="dep_missing", message="T-99 not found")
    assert v.field is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_checkers.py -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `result.py`**

```python
# src/repopackage/artifact/result.py
from typing import List, Optional
from pydantic import BaseModel


class Violation(BaseModel):
    rule: str
    message: str
    field: Optional[str] = None


class CheckResult(BaseModel):
    passed: bool
    violations: List[Violation]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_checkers.py -v 2>&1 | tail -10
```
Expected: `3 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/repopackage/artifact/result.py tests/artifact/test_checkers.py
git commit -m "feat(artifact): add CheckResult and Violation value objects"
```

---

## Task 8: ArtifactParser — base + MarkdownParser

**Files:**
- Create: `src/repopackage/artifact/parsers/base.py`
- Create: `src/repopackage/artifact/parsers/markdown.py`
- Create: `tests/artifact/test_parsers.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/artifact/test_parsers.py
import pytest
from repopackage.artifact.parsers.markdown import MarkdownParser
from repopackage.models.task import TaskModel, TaskStatus, TaskPriority
from repopackage.models.pill import PillModel


def test_markdown_parser_parses_task(sample_task_md):
    parser = MarkdownParser(TaskModel)
    model = parser.parse(sample_task_md)
    assert model.id == "T-01"
    assert model.title == "Add BaseArtifactModel"
    assert model.status == TaskStatus.OPEN
    assert model.priority == TaskPriority.P0
    assert "src/repopackage/models/base.py" in model.reference


def test_markdown_parser_parses_task_traits(sample_task_md):
    parser = MarkdownParser(TaskModel)
    model = parser.parse(sample_task_md)
    assert "Implementación" in model.traits


def test_markdown_parser_parses_pill(sample_pill_md):
    parser = MarkdownParser(PillModel)
    model = parser.parse(sample_pill_md)
    assert model.metadata.id == "PILL-01"
    assert model.metadata.type == "pattern"
    assert model.title == "Artifact Interface Contract"
    assert "zero-context-sufficiency" in model.why


def test_markdown_parser_pill_lifecycle(sample_pill_md):
    parser = MarkdownParser(PillModel)
    model = parser.parse(sample_pill_md)
    from repopackage.models.pill import PillLifecycle
    assert model.lifecycle == PillLifecycle.KEEP
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_parsers.py -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `parsers/base.py`**

```python
# src/repopackage/artifact/parsers/base.py
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar
from repopackage.models.base import BaseArtifactModel

M = TypeVar("M", bound=BaseArtifactModel)


class ArtifactParser(ABC, Generic[M]):
    def __init__(self, model_class: Type[M]):
        self.model_class = model_class

    @abstractmethod
    def parse(self, raw: str) -> M:
        ...
```

- [ ] **Step 4: Implement `parsers/markdown.py`**

The markdown format uses `## Section Name\ncontent` blocks. The title line is `# ID - Title`. Footer fields are `**Key:** value` after `---`.

```python
# src/repopackage/artifact/parsers/markdown.py
import re
from typing import Any, Dict, Type, TypeVar
from repopackage.artifact.parsers.base import ArtifactParser
from repopackage.models.base import BaseArtifactModel
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel, PillMetadata

M = TypeVar("M", bound=BaseArtifactModel)


def _extract_title_line(raw: str) -> tuple[str, str]:
    """Returns (id_or_name, title) from '# ID - Title' line."""
    match = re.match(r"^#\s+([\w-]+)\s+-\s+(.+)", raw.strip().splitlines()[0])
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", raw.strip().splitlines()[0].lstrip("# ").strip()


def _extract_sections(raw: str) -> Dict[str, str]:
    """Split markdown into {section_name: content} using ## headers."""
    sections: Dict[str, str] = {}
    current = None
    lines = []
    for line in raw.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(lines).strip()
            current = line[3:].strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        sections[current] = "\n".join(lines).strip()
    return sections


def _extract_footer(raw: str) -> Dict[str, str]:
    """Parse **Key:** value pairs from the footer (after ---)."""
    footer: Dict[str, str] = {}
    in_footer = False
    for line in raw.splitlines():
        if line.strip() == "---":
            in_footer = True
            continue
        if in_footer:
            match = re.match(r"\*\*(.+?):\*\*\s*(.*)", line.strip())
            if match:
                footer[match.group(1).strip()] = match.group(2).strip()
    return footer


def _parse_bullet_list(text: str) -> list[str]:
    """Extract items from a bullet list, stripping backticks."""
    items = []
    for line in text.splitlines():
        line = line.strip().lstrip("- ").strip("`").strip()
        if line:
            items.append(line)
    return items


def _parse_trait_tags(text: str) -> list[str]:
    """Extract [Tag] items from a traits line like `[A] | [B]`."""
    return re.findall(r"\[([^\]]+)\]", text)


def _parse_key_value_bullets(text: str) -> Dict[str, str]:
    """Parse '- **Key:** value' lines into a dict."""
    result: Dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"-\s+\*\*(.+?):\*\*\s*(.*)", line.strip())
        if match:
            result[match.group(1).strip()] = match.group(2).strip()
    return result


class MarkdownParser(ArtifactParser[M]):
    def parse(self, raw: str) -> M:
        if self.model_class is TaskModel:
            return self._parse_task(raw)  # type: ignore[return-value]
        if self.model_class is PillModel:
            return self._parse_pill(raw)  # type: ignore[return-value]
        raise NotImplementedError(f"No markdown parser for {self.model_class}")

    def _parse_task(self, raw: str) -> TaskModel:
        artifact_id, title = _extract_title_line(raw)
        sections = _extract_sections(raw)
        footer = _extract_footer(raw)

        return TaskModel(
            id=artifact_id,
            title=title,
            traits=_parse_trait_tags(sections.get("Traits (Composición)", "")),
            explanation=sections.get("Explanation", ""),
            reference=_parse_bullet_list(sections.get("Reference", "")),
            what_to_fix=sections.get("What to Fix / Implement", ""),
            how_to_do_it=sections.get("How to Do It (Suggested)", ""),
            induced_changes=sections.get("Induced Changes") or None,
            depends_on=_parse_bullet_list(sections.get("Depends On", "")),
            priority=footer.get("Priority", "P2"),
            status=footer.get("Status", "open"),
            lifecycle=footer.get("Lifecycle", "target"),
            commit_sha=footer.get("Commit SHA") or None,
        )

    def _parse_pill(self, raw: str) -> PillModel:
        _, title = _extract_title_line(raw)
        sections = _extract_sections(raw)
        footer = _extract_footer(raw)
        meta_kv = _parse_key_value_bullets(sections.get("Metadata", ""))

        return PillModel(
            title=title,
            metadata=PillMetadata(
                id=meta_kv.get("ID", ""),
                type=meta_kv.get("Type", ""),
                scope=meta_kv.get("Scope", ""),
                language=meta_kv.get("Language", ""),
                nature=meta_kv.get("Nature", ""),
            ),
            why=sections.get("Why", ""),
            what=sections.get("What", ""),
            when=sections.get("When", ""),
            where=sections.get("Where", ""),
            how=sections.get("How", ""),
            lifecycle=footer.get("Lifecycle", "Keep"),
        )
```

- [ ] **Step 5: Run test to verify it passes**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_parsers.py -v 2>&1 | tail -15
```
Expected: `4 passed`.

- [ ] **Step 6: Commit**

```bash
git add src/repopackage/artifact/parsers/ tests/artifact/test_parsers.py
git commit -m "feat(artifact): add ArtifactParser base and MarkdownParser for Task and Pill"
```

---

## Task 9: YamlParser

**Files:**
- Create: `src/repopackage/artifact/parsers/yaml_parser.py`
- Modify: `tests/artifact/test_parsers.py` (add YAML tests)

- [ ] **Step 1: Add failing tests to `test_parsers.py`**

Append to the existing file:
```python
from repopackage.artifact.parsers.yaml_parser import YamlParser
from repopackage.models.module_contract import ModuleContractModel


def test_yaml_parser_parses_module_contract(sample_module_contract_yaml):
    parser = YamlParser(ModuleContractModel)
    model = parser.parse(sample_module_contract_yaml)
    assert model.module_name == "artifact-interface"
    assert model.version == "1.0.0"
    assert len(model.inputs) == 1
    assert model.inputs[0].name == "path"
    assert model.validation.unit_tests is False


def test_yaml_parser_traits(sample_module_contract_yaml):
    parser = YamlParser(ModuleContractModel)
    model = parser.parse(sample_module_contract_yaml)
    assert "[Schema]" in model.traits
```

- [ ] **Step 2: Run to verify they fail**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_parsers.py::test_yaml_parser_parses_module_contract -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `yaml_parser.py`**

```python
# src/repopackage/artifact/parsers/yaml_parser.py
import yaml
from typing import TypeVar
from repopackage.artifact.parsers.base import ArtifactParser
from repopackage.models.base import BaseArtifactModel

M = TypeVar("M", bound=BaseArtifactModel)


class YamlParser(ArtifactParser[M]):
    def parse(self, raw: str) -> M:
        data = yaml.safe_load(raw)
        return self.model_class.model_validate(data)
```

- [ ] **Step 4: Run to verify it passes**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_parsers.py -v 2>&1 | tail -15
```
Expected: all parser tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/repopackage/artifact/parsers/yaml_parser.py tests/artifact/test_parsers.py
git commit -m "feat(artifact): add YamlParser"
```

---

## Task 10: ArtifactCheckers

**Files:**
- Create: `src/repopackage/artifact/checkers/base.py`
- Create: `src/repopackage/artifact/checkers/task.py`
- Create: `src/repopackage/artifact/checkers/board.py`
- Create: `src/repopackage/artifact/checkers/design_spec.py`
- Modify: `tests/artifact/test_checkers.py` (add checker tests)

- [ ] **Step 1: Add failing checker tests to `test_checkers.py`**

Append to the existing file:
```python
from repopackage.artifact.checkers.task import TaskChecker
from repopackage.artifact.checkers.board import BoardChecker
from repopackage.artifact.checkers.design_spec import DesignSpecChecker
from repopackage.models.task import TaskModel, TaskStatus
from repopackage.models.board import BoardModel, PhaseModel
from repopackage.models.design_spec import DesignSpecModel


def test_task_checker_passes_valid_task():
    task = TaskModel(
        id="T-01", title="Do something",
        explanation="Detailed explanation here.",
        what_to_fix="Fix the thing.",
        how_to_do_it="Step by step.",
    )
    result = TaskChecker().check(task)
    assert result.passed is True
    assert result.violations == []


def test_task_checker_fails_empty_explanation():
    task = TaskModel(
        id="T-01", title="Do something",
        explanation="",
        what_to_fix="Fix it.",
        how_to_do_it="Do it.",
    )
    result = TaskChecker().check(task)
    assert result.passed is False
    assert any(v.field == "explanation" for v in result.violations)


def test_task_checker_fails_closed_without_sha():
    task = TaskModel(
        id="T-01", title="Done",
        explanation="Explanation.",
        what_to_fix="Fixed.",
        how_to_do_it="Did it.",
        status=TaskStatus.CLOSED,
        commit_sha=None,
    )
    result = TaskChecker().check(task)
    assert result.passed is False
    assert any(v.field == "commit_sha" for v in result.violations)


def test_board_checker_passes_empty_board():
    board = BoardModel(phases=[], pills=[])
    result = BoardChecker().check(board)
    assert result.passed is True


def test_board_checker_detects_duplicate_task_ids():
    board = BoardModel(
        phases=[
            PhaseModel(id="1", tasks=["T-01", "T-02"]),
            PhaseModel(id="2", tasks=["T-01"]),
        ],
        pills=[],
    )
    result = BoardChecker().check(board)
    assert result.passed is False
    assert any("T-01" in v.message for v in result.violations)


def test_design_spec_checker_passes_complete_spec():
    spec = DesignSpecModel(
        name="Test",
        layer_0="Context.", layer_1="Goal.", layer_2="Skeleton.",
        layer_3="Pseudocode.", layer_4="Patterns.", layer_5="Tests.",
    )
    result = DesignSpecChecker().check(spec)
    assert result.passed is True


def test_design_spec_checker_fails_empty_layer():
    spec = DesignSpecModel(
        name="Test",
        layer_0="", layer_1="Goal.", layer_2="Skeleton.",
        layer_3="Pseudocode.", layer_4="Patterns.", layer_5="Tests.",
    )
    result = DesignSpecChecker().check(spec)
    assert result.passed is False
    assert any(v.field == "layer_0" for v in result.violations)
```

- [ ] **Step 2: Run to verify they fail**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_checkers.py -v 2>&1 | tail -15
```
Expected: new tests fail with `ImportError`.

- [ ] **Step 3: Implement `checkers/base.py`**

```python
# src/repopackage/artifact/checkers/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from repopackage.models.base import BaseArtifactModel
from repopackage.artifact.result import CheckResult

M = TypeVar("M", bound=BaseArtifactModel)


class ArtifactChecker(ABC, Generic[M]):
    @abstractmethod
    def check(self, model: M) -> CheckResult:
        ...
```

- [ ] **Step 4: Implement `checkers/task.py`**

```python
# src/repopackage/artifact/checkers/task.py
from repopackage.artifact.checkers.base import ArtifactChecker
from repopackage.artifact.result import CheckResult, Violation
from repopackage.models.task import TaskModel, TaskStatus


class TaskChecker(ArtifactChecker[TaskModel]):
    def check(self, model: TaskModel) -> CheckResult:
        violations = []
        if not model.explanation.strip():
            violations.append(Violation(rule="required_field", message="explanation is empty", field="explanation"))
        if not model.what_to_fix.strip():
            violations.append(Violation(rule="required_field", message="what_to_fix is empty", field="what_to_fix"))
        if not model.how_to_do_it.strip():
            violations.append(Violation(rule="required_field", message="how_to_do_it is empty", field="how_to_do_it"))
        if model.status == TaskStatus.CLOSED and not model.commit_sha:
            violations.append(Violation(rule="closed_needs_sha", message="closed task must have commit_sha", field="commit_sha"))
        return CheckResult(passed=len(violations) == 0, violations=violations)
```

- [ ] **Step 5: Implement `checkers/board.py`**

```python
# src/repopackage/artifact/checkers/board.py
from repopackage.artifact.checkers.base import ArtifactChecker
from repopackage.artifact.result import CheckResult, Violation
from repopackage.models.board import BoardModel


class BoardChecker(ArtifactChecker[BoardModel]):
    def check(self, model: BoardModel) -> CheckResult:
        violations = []
        seen = set()
        for phase in model.phases:
            for task_id in phase.tasks:
                if task_id in seen:
                    violations.append(Violation(rule="duplicate_task", message=f"{task_id} appears in multiple phases", field="phases"))
                seen.add(task_id)
        return CheckResult(passed=len(violations) == 0, violations=violations)
```

- [ ] **Step 6: Implement `checkers/design_spec.py`**

```python
# src/repopackage/artifact/checkers/design_spec.py
from repopackage.artifact.checkers.base import ArtifactChecker
from repopackage.artifact.result import CheckResult, Violation
from repopackage.models.design_spec import DesignSpecModel


class DesignSpecChecker(ArtifactChecker[DesignSpecModel]):
    def check(self, model: DesignSpecModel) -> CheckResult:
        violations = []
        for i in range(6):
            field = f"layer_{i}"
            if not getattr(model, field, "").strip():
                violations.append(Violation(rule="empty_layer", message=f"{field} is empty", field=field))
        return CheckResult(passed=len(violations) == 0, violations=violations)
```

- [ ] **Step 7: Run all checker tests**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_checkers.py -v 2>&1 | tail -20
```
Expected: all pass.

- [ ] **Step 8: Commit**

```bash
git add src/repopackage/artifact/checkers/ tests/artifact/test_checkers.py
git commit -m "feat(artifact): add ArtifactChecker base, TaskChecker, BoardChecker, DesignSpecChecker"
```

---

## Task 11: ArtifactInterface

**Files:**
- Create: `src/repopackage/artifact/interface.py`
- Create: `tests/artifact/test_interface.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/artifact/test_interface.py
import pytest
import yaml
from pathlib import Path
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel, TaskStatus
from repopackage.models.pill import PillModel
from repopackage.models.module_contract import ModuleContractModel


def test_interface_create_task():
    artifact = ArtifactInterface.create(TaskModel,
        id="T-02", title="New task",
        explanation="Do the thing.",
        what_to_fix="Fix it.",
        how_to_do_it="Steps.",
    )
    assert artifact.model.id == "T-02"
    assert isinstance(artifact.model, TaskModel)


def test_interface_to_agent_returns_yaml():
    artifact = ArtifactInterface.create(TaskModel,
        id="T-01", title="Test",
        explanation="Explanation.",
        what_to_fix="Fix.",
        how_to_do_it="Do.",
    )
    agent_str = artifact.to_agent()
    data = yaml.safe_load(agent_str)
    assert data["id"] == "T-01"
    assert data["title"] == "Test"


def test_interface_to_disk_roundtrip_task(tmp_path, sample_task_md):
    from repopackage.artifact.parsers.markdown import MarkdownParser
    parser = MarkdownParser(TaskModel)
    model = parser.parse(sample_task_md)
    artifact = ArtifactInterface(model=model)
    out_path = tmp_path / "T-01.md"
    artifact.to_disk(out_path)
    assert out_path.exists()
    rendered = out_path.read_text()
    assert "T-01" in rendered
    assert "Add BaseArtifactModel" in rendered


def test_interface_from_disk_task(tmp_path, sample_task_md):
    task_file = tmp_path / "T-01.md"
    task_file.write_text(sample_task_md)
    artifact = ArtifactInterface.from_disk(TaskModel, task_file)
    assert artifact.model.id == "T-01"
    assert artifact.model.status == TaskStatus.OPEN


def test_interface_check_valid_task():
    artifact = ArtifactInterface.create(TaskModel,
        id="T-01", title="Test",
        explanation="Explanation.",
        what_to_fix="Fix.",
        how_to_do_it="Do.",
    )
    result = artifact.check()
    assert result.passed is True


def test_interface_check_invalid_task():
    artifact = ArtifactInterface.create(TaskModel,
        id="T-01", title="Test",
        explanation="",
        what_to_fix="Fix.",
        how_to_do_it="Do.",
    )
    result = artifact.check()
    assert result.passed is False


def test_interface_from_disk_module_contract(tmp_path, sample_module_contract_yaml):
    contract_file = tmp_path / "contract.yaml"
    contract_file.write_text(sample_module_contract_yaml)
    artifact = ArtifactInterface.from_disk(ModuleContractModel, contract_file)
    assert artifact.model.module_name == "artifact-interface"
```

- [ ] **Step 2: Run to verify they fail**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_interface.py -v 2>&1 | tail -15
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `interface.py`**

```python
# src/repopackage/artifact/interface.py
from pathlib import Path
from typing import Generic, Type, TypeVar
import yaml
from jinja2 import Environment, PackageLoader

from repopackage.models.base import BaseArtifactModel
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel
from repopackage.models.module_contract import ModuleContractModel
from repopackage.artifact.result import CheckResult
from repopackage.artifact.parsers.markdown import MarkdownParser
from repopackage.artifact.parsers.yaml_parser import YamlParser
from repopackage.artifact.checkers.task import TaskChecker
from repopackage.artifact.checkers.board import BoardChecker
from repopackage.artifact.checkers.design_spec import DesignSpecChecker

M = TypeVar("M", bound=BaseArtifactModel)

_MARKDOWN_MODELS = {TaskModel, PillModel}
_YAML_MODELS = {ModuleContractModel}

_CHECKERS = {
    TaskModel: TaskChecker(),
    # BoardModel and DesignSpecModel added by import when needed
}


def _get_jinja_env() -> Environment:
    return Environment(loader=PackageLoader("repopackage", "templates"))


class ArtifactInterface(Generic[M]):
    def __init__(self, model: M):
        self.model = model

    @classmethod
    def from_disk(cls, model_class: Type[M], path: Path) -> "ArtifactInterface[M]":
        raw = path.read_text()
        if model_class.__format__ == "yaml":
            parser = YamlParser(model_class)
        else:
            parser = MarkdownParser(model_class)
        return cls(model=parser.parse(raw))

    @classmethod
    def create(cls, model_class: Type[M], **kwargs) -> "ArtifactInterface[M]":
        return cls(model=model_class(**kwargs))

    def to_disk(self, path: Path) -> None:
        env = _get_jinja_env()
        template = env.get_template(self.model.__template__)
        model_name = type(self.model).__name__.replace("Model", "").lower()
        content = template.render(**{model_name: self.model})
        path.write_text(content)

    def to_agent(self) -> str:
        return yaml.dump(self.model.model_dump(), allow_unicode=True, sort_keys=False)

    def check(self) -> CheckResult:
        from repopackage.models.board import BoardModel
        from repopackage.models.design_spec import DesignSpecModel
        checkers = {
            TaskModel: TaskChecker(),
            BoardModel: BoardChecker(),
            DesignSpecModel: DesignSpecChecker(),
        }
        checker = checkers.get(type(self.model))
        if checker is None:
            return CheckResult(passed=True, violations=[])
        return checker.check(self.model)
```

- [ ] **Step 4: Run tests**

```bash
cd /home/jp/repopackage && python -m pytest tests/artifact/test_interface.py -v 2>&1 | tail -20
```
Expected: all pass. If `PackageLoader` fails because package isn't installed, run `pip install -e .` first.

- [ ] **Step 5: Full test suite**

```bash
cd /home/jp/repopackage && python -m pytest tests/ -v 2>&1 | tail -20
```
Expected: all tests across models + artifact pass.

- [ ] **Step 6: Commit**

```bash
git add src/repopackage/artifact/interface.py tests/artifact/test_interface.py
git commit -m "feat(artifact): add ArtifactInterface with from_disk/to_disk/to_agent/check"
```

---

## Task 12: Composers

**Files:**
- Create: `src/repopackage/composers/base.py`
- Create: `src/repopackage/composers/board.py`
- Create: `src/repopackage/composers/dispatch.py`
- Create: `src/repopackage/composers/evidence.py`
- Create: `tests/composers/test_board_composer.py`
- Create: `tests/composers/test_dispatch_composer.py`
- Create: `tests/composers/test_evidence_composer.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/composers/test_board_composer.py
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.composers.board import BoardComposer


def _make_task(id: str, phase: str = "1") -> ArtifactInterface:
    return ArtifactInterface.create(TaskModel,
        id=id, title=f"Task {id}", explanation="Explanation.",
        what_to_fix="Fix.", how_to_do_it="Do.", phase=phase,
    )


def test_board_composer_groups_by_phase():
    tasks = [_make_task("T-01", "1"), _make_task("T-02", "1"), _make_task("T-03", "2")]
    board_artifact = BoardComposer(tasks).compose()
    board = board_artifact.model
    assert len(board.phases) == 2
    phase_ids = [p.id for p in board.phases]
    assert "1" in phase_ids
    assert "2" in phase_ids


def test_board_composer_phase_contains_task_ids():
    tasks = [_make_task("T-01", "1"), _make_task("T-02", "1")]
    board_artifact = BoardComposer(tasks).compose()
    phase_1 = next(p for p in board_artifact.model.phases if p.id == "1")
    assert "T-01" in phase_1.tasks
    assert "T-02" in phase_1.tasks


def test_board_composer_empty_tasks():
    board_artifact = BoardComposer([]).compose()
    assert board_artifact.model.phases == []
```

```python
# tests/composers/test_dispatch_composer.py
import yaml
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel, PillMetadata
from repopackage.composers.dispatch import DispatchPackageComposer


def _make_task() -> ArtifactInterface:
    return ArtifactInterface.create(TaskModel,
        id="T-01", title="Test task",
        explanation="Explanation.", what_to_fix="Fix it.", how_to_do_it="Do it.",
    )


def _make_pill(pill_id: str) -> ArtifactInterface:
    return ArtifactInterface.create(PillModel,
        title="Context pill",
        metadata=PillMetadata(id=pill_id, type="pattern", scope="global", language="Python", nature="context"),
        why="Why.", what="What.", how="How.",
    )


def test_dispatch_package_contains_task_yaml():
    task = _make_task()
    result = DispatchPackageComposer(task, []).compose()
    assert "T-01" in result
    assert "Test task" in result


def test_dispatch_package_contains_pill_yaml():
    task = _make_task()
    pills = [_make_pill("PILL-01"), _make_pill("PILL-02")]
    result = DispatchPackageComposer(task, pills).compose()
    assert "PILL-01" in result
    assert "PILL-02" in result


def test_dispatch_package_is_yaml_parseable():
    task = _make_task()
    pills = [_make_pill("PILL-01")]
    result = DispatchPackageComposer(task, pills).compose()
    # Should be a concatenation of YAML docs separated by ---
    parts = [p.strip() for p in result.split("---") if p.strip()]
    assert len(parts) >= 1
```

```python
# tests/composers/test_evidence_composer.py
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.composers.evidence import EvidenceComposer


def _make_task() -> ArtifactInterface:
    return ArtifactInterface.create(TaskModel,
        id="T-01", title="Task", explanation="Explanation.",
        what_to_fix="Fix.", how_to_do_it="Do.",
    )


def test_evidence_composer_passed():
    task = _make_task()
    ev_artifact = EvidenceComposer(task, test_log="5 passed", lint_log="All clean").compose()
    ev = ev_artifact.model
    assert ev.task_id == "T-01"
    assert ev.passed is True
    assert ev.tests_ok is True
    assert ev.lint_ok is True


def test_evidence_composer_failed_tests():
    task = _make_task()
    ev_artifact = EvidenceComposer(task, test_log="2 failed, 3 passed", lint_log="All clean").compose()
    ev = ev_artifact.model
    assert ev.passed is False
    assert ev.tests_ok is False
    assert ev.lint_ok is True


def test_evidence_composer_failed_lint():
    task = _make_task()
    ev_artifact = EvidenceComposer(task, test_log="5 passed", lint_log="E501 line too long").compose()
    ev = ev_artifact.model
    assert ev.passed is False
    assert ev.lint_ok is False
```

- [ ] **Step 2: Run to verify they fail**

```bash
cd /home/jp/repopackage && python -m pytest tests/composers/ -v 2>&1 | tail -10
```
Expected: `ImportError`.

- [ ] **Step 3: Implement `composers/base.py`**

```python
# src/repopackage/composers/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from repopackage.models.base import BaseArtifactModel
from repopackage.artifact.interface import ArtifactInterface

Out = TypeVar("Out", bound=BaseArtifactModel)


class Composer(ABC, Generic[Out]):
    @abstractmethod
    def compose(self) -> ArtifactInterface[Out]:
        ...
```

- [ ] **Step 4: Implement `composers/board.py`**

```python
# src/repopackage/composers/board.py
from typing import List
from repopackage.artifact.interface import ArtifactInterface
from repopackage.composers.base import Composer
from repopackage.models.board import BoardModel, PhaseModel
from repopackage.models.task import TaskModel


class BoardComposer(Composer[BoardModel]):
    def __init__(self, tasks: List[ArtifactInterface[TaskModel]]):
        self._tasks = tasks

    def compose(self) -> ArtifactInterface[BoardModel]:
        phase_map: dict[str, list[str]] = {}
        for artifact in self._tasks:
            phase_id = artifact.model.phase or "1"
            phase_map.setdefault(phase_id, []).append(artifact.model.id)
        phases = [PhaseModel(id=pid, tasks=tids) for pid, tids in sorted(phase_map.items())]
        return ArtifactInterface(model=BoardModel(phases=phases, pills=[]))
```

- [ ] **Step 5: Implement `composers/dispatch.py`**

```python
# src/repopackage/composers/dispatch.py
from typing import List
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel


class DispatchPackageComposer:
    def __init__(self, task: ArtifactInterface[TaskModel], pills: List[ArtifactInterface[PillModel]]):
        self._task = task
        self._pills = pills

    def compose(self) -> str:
        parts = [self._task.to_agent()]
        for pill in self._pills:
            parts.append(pill.to_agent())
        return "---\n".join(parts)
```

- [ ] **Step 6: Implement `composers/evidence.py`**

```python
# src/repopackage/composers/evidence.py
from repopackage.artifact.interface import ArtifactInterface
from repopackage.composers.base import Composer
from repopackage.models.evidence import EvidenceModel
from repopackage.models.task import TaskModel


class EvidenceComposer(Composer[EvidenceModel]):
    def __init__(self, task: ArtifactInterface[TaskModel], test_log: str, lint_log: str):
        self._task = task
        self._test_log = test_log
        self._lint_log = lint_log

    def compose(self) -> ArtifactInterface[EvidenceModel]:
        tests_ok = "failed" not in self._test_log
        lint_ok = "failed" not in self._lint_log.lower() and "error" not in self._lint_log.lower()
        passed = tests_ok and lint_ok
        model = EvidenceModel(
            task_id=self._task.model.id,
            passed=passed,
            lint_ok=lint_ok,
            tests_ok=tests_ok,
            raw_log=self._test_log + "\n" + self._lint_log,
        )
        return ArtifactInterface(model=model)
```

- [ ] **Step 7: Run all composer tests**

```bash
cd /home/jp/repopackage && python -m pytest tests/composers/ -v 2>&1 | tail -20
```
Expected: all pass.

- [ ] **Step 8: Full suite**

```bash
cd /home/jp/repopackage && python -m pytest tests/ -v 2>&1 | tail -25
```
Expected: all tests across all three packages pass.

- [ ] **Step 9: Commit**

```bash
git add src/repopackage/composers/ tests/composers/
git commit -m "feat(composers): add BoardComposer, DispatchPackageComposer, EvidenceComposer"
```

---

## Self-Review

### Spec Coverage

| UML Component | Task | Status |
|---|---|---|
| `BaseArtifactModel` | Task 2 | ✓ |
| `TaskModel` + enums | Task 2 | ✓ |
| `PillModel` + `PillMetadata` | Task 3 | ✓ |
| `BoardModel` + `PhaseModel` | Task 4 | ✓ |
| `DesignSpecModel` | Task 5 | ✓ |
| `ModuleContractModel` + `ContractField` + `ValidationState` | Task 5 | ✓ |
| `EvidenceModel` | Task 5 | ✓ |
| Jinja2 templates (all 6) | Task 6 | ✓ |
| `CheckResult` + `Violation` | Task 7 | ✓ |
| `ArtifactParser` base | Task 8 | ✓ |
| `MarkdownParser` (Task + Pill) | Task 8 | ✓ |
| `YamlParser` (ModuleContract) | Task 9 | ✓ |
| `ArtifactChecker` base | Task 10 | ✓ |
| `TaskChecker` | Task 10 | ✓ |
| `BoardChecker` | Task 10 | ✓ |
| `DesignSpecChecker` | Task 10 | ✓ |
| `ArtifactInterface[M]` | Task 11 | ✓ |
| `Composer[Out]` base | Task 12 | ✓ |
| `BoardComposer` | Task 12 | ✓ |
| `DispatchPackageComposer` | Task 12 | ✓ |
| `EvidenceComposer` | Task 12 | ✓ |

**Gaps:**
- `MarkdownParser` only handles `TaskModel` and `PillModel`. `BoardModel`, `DesignSpecModel`, `EvidenceModel` parsers not needed yet (Board is generated, not parsed; DesignSpec/Evidence can be added in a later iteration when those read paths are needed). This is intentional YAGNI.
- `GitCommit` is a format string, not a Pydantic model — not implemented. Correct per UML note.

### Placeholder Scan
No TBDs, TODOs, or "similar to Task N" patterns found.

### Type Consistency
- `ArtifactInterface.create(model_class, **kwargs)` — consistent across Tasks 11 and 12.
- `ArtifactInterface(model=model)` direct constructor — consistent.
- `Composer.compose() -> ArtifactInterface[Out]` — consistent except `DispatchPackageComposer.compose() -> str` (intentional, matches UML spec).
