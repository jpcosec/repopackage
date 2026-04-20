from repopackage.workflow.workspace import Workspace
from repopackage.workflow.tasks import TaskCollection
from repopackage.workflow.pills import PillCollection
from repopackage.workflow.operations import WorkflowOperations
from repopackage.models.board import BoardModel, PhaseModel
from nldb.renderer import NLDBRenderer

class Desk:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.tasks = TaskCollection(workspace)
        self.pills = PillCollection(workspace)
        self.ops = WorkflowOperations(workspace)
        self.renderer = NLDBRenderer()
        
    def sync_board(self):
        tasks = self.tasks.all()
        pills = self.pills.all()
        
        # Group tasks by phase
        phases_dict = {}
        for t in tasks:
            p_id = t.phase or "1"
            if p_id not in phases_dict:
                phases_dict[p_id] = []
            phases_dict[p_id].append(t.id)
            
        phases = [
            PhaseModel(id=p_id, tasks=sorted(t_ids))
            for p_id, t_ids in sorted(phases_dict.items())
        ]
        
        board = BoardModel(
            phases=phases,
            pills=[p.metadata.id for p in pills]
        )
        
        board_file = self.workspace.tasks_path / "Board.md"
        rendered = self.renderer.render(board)
        board_file.write_text(rendered)
