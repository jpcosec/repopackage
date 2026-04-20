from typing import ClassVar, Literal, Optional
from repopackage.models.base import BaseArtifactModel


class EvidenceModel(BaseArtifactModel):
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    task_id: str
    passed: bool
    lint_ok: bool
    tests_ok: bool
    raw_log: str
    commit_sha: Optional[str] = None
