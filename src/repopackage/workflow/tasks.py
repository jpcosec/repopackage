from pathlib import Path
from typing import List, Optional
from repopackage.models.task import TaskModel
from nldb.ast_handler import AST_Handler
from nldb.template_extractor import TemplateExtractor
from nldb.data_extractor import DataExtractor
from nldb.renderer import NLDBRenderer

class TaskCollection:
    def __init__(self, workspace):
        self.workspace = workspace
        self.ast_handler = AST_Handler()
        self.tpl_extractor = TemplateExtractor()
        self.data_extractor = DataExtractor()
        self.renderer = NLDBRenderer()

    def get_task(self, task_id: str) -> Optional[TaskModel]:
        if not task_id.startswith("T-"): task_id = f"T-{task_id}"
        path = self.workspace.tasks_path / f"{task_id}.md"
        if not path.exists(): return None
        
        tpl_blocks = self.ast_handler.split_nodes(TaskModel.__template__)
        recipes = self.tpl_extractor.extract_nodes(tpl_blocks)
        data_blocks = self.ast_handler.split_nodes(path.read_text())
        payload = self.data_extractor.extract_values(data_blocks, recipes)
        
        return TaskModel(**payload)

    def all(self) -> List[TaskModel]:
        tasks = []
        for f in sorted(self.workspace.tasks_path.glob("T-*.md")):
            task = self.get_task(f.stem)
            if task: tasks.append(task)
        return tasks

    def save_task(self, task: TaskModel):
        path = self.workspace.tasks_path / f"{task.id}.md"
        rendered = self.renderer.render(task)
        path.write_text(rendered)
