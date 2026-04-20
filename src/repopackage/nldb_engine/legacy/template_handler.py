import re, ast
from typing import List, Dict, Any, Type, NamedTuple, Optional

class Marker(NamedTuple):
    mode: str
    trait: Optional[str]
    prop: str
    raw: str

class TemplateContract:
    def __init__(self, raw_template: str):
        self.raw = raw_template
        self.markers = self._discover_markers(raw_template)

    def _discover_markers(self, text: str) -> List[Marker]:
        results = []
        pattern = r"⸢([^⸥]+)⸥"
        for match in re.finditer(pattern, text):
            c = match.group(1)
            if "•" in c:
                instr, prop = c.split("•", 1)
                flags = instr.split(",")
                # Mode is either 'rev' or 'revop'. Trait is anything else.
                mode = next((f for f in flags if f in ("rev", "revop")), "ref")
                trait = next((f for f in flags if f not in ("rev", "revop")), None)
                results.append(Marker(mode=mode, trait=trait, prop=prop, raw=match.group(0)))
            else:
                results.append(Marker(mode="ref", trait=None, prop=c, raw=match.group(0)))
        return results

    def get_clean_pattern(self) -> str:
        return re.sub(r"⸢[^⸥]+⸥", "[[PAYLOAD]]", self.raw)
