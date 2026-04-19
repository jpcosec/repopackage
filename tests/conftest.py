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
