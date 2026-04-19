import re
from typing import List, Dict
from repopackage.cli.models.task import TaskModel, TaskStatus

class BoardWriter:
    """
    Generates Markdown tables for the Tasks Board based on TaskModels.
    """
    def __init__(self, tasks: List[TaskModel]):
        self.tasks = tasks

    def _get_type_domain(self, traits: List[str]) -> Dict[str, str]:
        t_type = "-"
        t_domain = "-"
        
        for trait in traits:
            clean_trait = trait.strip("[]")
            if clean_trait == "Implementación":
                t_type = "Impl"
            elif clean_trait == "Diseño":
                t_type = "Design"
            
            # Detect domain
            if clean_trait in ["CLI", "Schema", "System", "Engine"]:
                t_domain = clean_trait
        
        return {"type": t_type, "domain": t_domain}

    def generate_active_table(self) -> str:
        header = "| ID | Type | Domain | Task | Priority | Deps | Pills | Ph |"
        separator = "|----|------|--------|------|----------|------|-------|----|"
        rows = [header, separator]
        
        active_tasks = [t for t in self.tasks if t.status in [TaskStatus.OPEN, TaskStatus.IN_PROGRESS]]
        active_tasks.sort(key=lambda x: x.id)
        
        for t in active_tasks:
            td = self._get_type_domain(t.traits)
            deps = ", ".join(t.depends_on) if t.depends_on and t.depends_on != ["None"] else "-"
            pills = ", ".join(t.pills) if t.pills else "-"
            phase = t.phase or "-"
            row = f"| {t.id} | {td['type']} | {td['domain']} | {t.title} | {t.priority} | {deps} | {pills} | {phase} |"
            rows.append(row)
            
        return "\n".join(rows)

    def generate_blocked_table(self) -> str:
        header = "| ID | Type | Domain | Blocker | Gate |"
        separator = "|----|------|--------|---------|------|"
        rows = [header, separator]
        
        blocked_tasks = [t for t in self.tasks if t.status == TaskStatus.BLOCKED]
        blocked_tasks.sort(key=lambda x: x.id)
        
        for t in blocked_tasks:
            td = self._get_type_domain(t.traits)
            blocker = ", ".join(t.depends_on) if t.depends_on and t.depends_on != ["None"] else "-"
            row = f"| {t.id} | {td['type']} | {td['domain']} | {blocker} | - |"
            rows.append(row)
            
        return "\n".join(rows)

    def generate_completed_table(self) -> str:
        header = "| ID | Type | Domain | Task | Resolving Commit |"
        separator = "|----|------|--------|------|------------------|"
        rows = [header, separator]
        
        completed_tasks = [t for t in self.tasks if t.status == TaskStatus.CLOSED]
        completed_tasks.sort(key=lambda x: x.id)
        
        for t in completed_tasks:
            td = self._get_type_domain(t.traits)
            commit = t.commit_sha or "-"
            row = f"| {t.id} | {td['type']} | {td['domain']} | {t.title} | {commit} |"
            rows.append(row)
            
        return "\n".join(rows)

    def write_board(self, current_content: str) -> str:
        from repopackage.cli.engines.markdown_engine import MarkdownEngine
        engine = MarkdownEngine(current_content)
        
        engine.update_section("Active (status=open|in_progress)", self.generate_active_table())
        engine.update_section("Blocked (status=blocked)", self.generate_blocked_table())
        engine.update_section("Completed", self.generate_completed_table())
        
        return engine.content
