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
