from repopackage.workflow.tasks import TaskCollection
from repopackage.workflow.pills import PillCollection

class WorkflowOperations:
    def __init__(self, workspace):
        self.workspace = workspace
        self.tasks = TaskCollection(workspace)
        self.pills = PillCollection(workspace)

    def inject_pill(self, task_id: str, pill_id: str):
        task = self.tasks.get_task(task_id)
        pill = self.pills.get_pill(pill_id)
        if not task or not pill: return
        
        if pill.metadata.id not in task.traits:
            task.traits.append(pill.metadata.id)
            
        pill_ref = f"desk/pills/{pill.metadata.id}.md"
        if pill_ref not in task.reference:
            task.reference.append(pill_ref)
            
        change = f"- Injected pill {pill.metadata.id}"
        if not task.induced_changes:
            task.induced_changes = change
        elif change not in task.induced_changes:
            task.induced_changes += f"\n{change}"
            
        self.tasks.save_task(task)
