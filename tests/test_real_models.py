import sys, os
from nldb.ast_handler import AST_Handler
from nldb.template_extractor import TemplateExtractor
from nldb.data_extractor import DataExtractor

# Import all models dynamically or explicitly
from repopackage.models.board import BoardModel
from repopackage.models.design_spec import DesignSpecModel
from repopackage.models.evidence import EvidenceModel
from repopackage.models.module_contract import ModuleContractModel
from repopackage.models.pill import PillModel
from repopackage.models.task import TaskModel

models_to_test = [
    BoardModel, DesignSpecModel, EvidenceModel, 
    ModuleContractModel, PillModel, TaskModel
]

ast_handler = AST_Handler()
tpl_extractor = TemplateExtractor()

for model in models_to_test:
    print(f"\\n=== Testing Template parse for: {model.__name__} ===")
    if not hasattr(model, '__template__'):
        print("  ❌ No __template__ found.")
        continue
        
    try:
        tpl_blocks = ast_handler.split_nodes(model.__template__)
        recipes = tpl_extractor.extract_nodes(tpl_blocks)
        print(f"  ✅ Extracted {len(recipes)} recipes successfully.")
        
        # Verify no | was used in the regexes resulting in empty property captures inside tables!
        for r in recipes:
            if r["handler"] == "table":
                if not r.get("props"):
                    print(f"  ⚠️ WARNING: Table handler generated a recipe with NO props! Check | delimiter!")
    except Exception as e:
        print(f"  ❌ FAILED completely: {e}")
