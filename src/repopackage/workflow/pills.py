from pathlib import Path
from typing import List, Optional
from repopackage.models.pill import PillModel
from nldb.ast_handler import AST_Handler
from nldb.template_extractor import TemplateExtractor
from nldb.data_extractor import DataExtractor
from nldb.renderer import NLDBRenderer

class PillCollection:
    def __init__(self, workspace):
        self.workspace = workspace
        self.ast_handler = AST_Handler()
        self.tpl_extractor = TemplateExtractor()
        self.data_extractor = DataExtractor()
        self.renderer = NLDBRenderer()

    def get_pill(self, pill_id: str) -> Optional[PillModel]:
        if not pill_id.startswith("PILL-"): pill_id = f"PILL-{pill_id}"
        path = self.workspace.pills_path / f"{pill_id}.md"
        if not path.exists(): return None
        
        tpl_blocks = self.ast_handler.split_nodes(PillModel.__template__)
        recipes = self.tpl_extractor.extract_nodes(tpl_blocks)
        data_blocks = self.ast_handler.split_nodes(path.read_text())
        payload = self.data_extractor.extract_values(data_blocks, recipes)
        
        return PillModel(**payload)

    def all(self) -> List[PillModel]:
        pills = []
        for f in sorted(self.workspace.pills_path.glob("PILL-*.md")):
            pill = self.get_pill(f.stem)
            if pill: pills.append(pill)
        return pills

    def save_pill(self, pill: PillModel):
        path = self.workspace.pills_path / f"{pill.metadata.id}.md"
        rendered = self.renderer.render(pill)
        path.write_text(rendered)
