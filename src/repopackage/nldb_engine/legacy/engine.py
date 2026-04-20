import re
from typing import Dict, Any, Type, List
from repopackage.nldb_engine.template_handler import TemplateContract
from repopackage.nldb_engine.ast_handler import AstPairingEngine
from repopackage.nldb_engine.node_router import NodeRouter
from repopackage.nldb_engine.models import StructuredNLDoc, M

class nlDBEngine:
    def __init__(self):
        self.ast_handler = AstPairingEngine()
        self.router = NodeRouter()

    def render(self, instance: Any) -> str:
        fields = instance.model_dump()
        template_dsl = instance.__template__
        lines = template_dsl.splitlines()
        tpl_nodes = self.ast_handler.get_all_nodes(template_dsl)
        rendered_parts = []
        rendered_lines = set()

        for t_node in tpl_nodes:
            if not t_node.map: continue
            s, e = t_node.map
            block_range = tuple(range(s, e))
            if any(n in rendered_lines for n in block_range): continue

            raw_text = "\n".join(lines[s:e])
            contract = TemplateContract(raw_text)
            
            if not contract.markers:
                rendered_parts.append(raw_text)
            else:
                handler = self.router.route(t_node, contract)
                rendered_parts.append(handler.render(contract, None, fields))
            
            for n in block_range: rendered_lines.add(n)
            
        return "\n\n".join(rendered_parts)

    def extract(self, model_cls: Type[M], raw_markdown: str) -> M:
        pairs = self.ast_handler.pair_trees(model_cls.__template__, raw_markdown)
        data = {}
        lines = model_cls.__template__.splitlines()
        processed_tpl_nodes = set()

        for t_node, d_node in pairs:
            if id(t_node) in processed_tpl_nodes: continue
            if t_node.map:
                s, e = t_node.map
                raw_tpl_text = "\n".join(lines[s:e])
            else: raw_tpl_text = self.router.handlers["standard"].get_text(t_node)
                
            contract = TemplateContract(raw_tpl_text)
            if not contract.markers: continue
            
            handler = self.router.route(d_node, contract)
            extracted = handler.extract(d_node, contract, model_cls)
            data.update(extracted)
            processed_tpl_nodes.add(id(t_node))
            
        return model_cls.model_validate(data)

def render_nl_doc(instance: Any) -> str: return nlDBEngine().render(instance)
def extract_nl_doc(cls: Type[M], raw: str) -> M: return nlDBEngine().extract(cls, raw)
