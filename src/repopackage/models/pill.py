from enum import Enum
from typing import ClassVar
from pydantic import BaseModel
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
    __template__: ClassVar[str] = """
# ⸢jinja2|{{ metadata.id }} - {{ title }}⸥

## Metadata
⸢rev|dict|metadata⸥

## Why
⸢rev|why⸥

## What
⸢rev|what⸥

## When
⸢revop|when⸥

## Where
⸢revop|where⸥

## How
⸢rev|how⸥

---
**Lifecycle:** ⸢rev|lifecycle⸥
""".strip()

    title: str
    metadata: PillMetadata
    why: str
    what: str
    when: str = ""
    where: str = ""
    how: str
    lifecycle: PillLifecycle = PillLifecycle.KEEP
