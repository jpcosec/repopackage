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
