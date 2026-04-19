from typing import ClassVar, Optional
from repopackage.models.base import BaseArtifactModel

class EvidenceModel(BaseArtifactModel):
    __template__: ClassVar[str] = """
# Evidence: ⸢rev•task_id⸥

## Result
- **Passed:** ⸢rev•passed⸥
- **Lint OK:** ⸢rev•lint_ok⸥
- **Tests OK:** ⸢rev•tests_ok⸥

## Raw Log
```
⸢rev•raw_log⸥
```

---
**Commit SHA:** ⸢revop•commit_sha⸥
""".strip()

    task_id: str
    passed: bool
    lint_ok: bool
    tests_ok: bool
    raw_log: str
    commit_sha: Optional[str] = None
