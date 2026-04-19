import re
from typing import List, Dict, Any, Type, NamedTuple, Optional

class Marker(NamedTuple):
    mode: str
    trait: Optional[str]
    prop: str
    raw: str

class TemplateContract:
    """Decomposes a string template into instructions and data properties."""
    def __init__(self, raw_template: str):
        self.raw = raw_template
        self.markers = self._discover_markers(raw_template)

    def _discover_markers(self, text: str) -> List[Marker]:
        results = []
        # Matches ⸢mode,trait•prop⸥ or ⸢mode•prop⸥
        pattern = r"⸢([^⸥]+)⸥"
        for match in re.finditer(pattern, text):
            full_content = match.group(1)
            
            # Split by the primary 'Bullet' separator
            if "•" in full_content:
                instruction, prop = full_content.split("•", 1)
                # Parse flags (rev, table, dict, etc.)
                flags = instruction.split(",")
                mode = flags[0]
                trait = flags[1] if len(flags) > 1 else None
                results.append(Marker(mode=mode, trait=trait, prop=prop, raw=match.group(0)))
            else:
                # Fallback for simple reference ⸢prop⸥
                results.append(Marker(mode="ref", trait=None, prop=full_content, raw=match.group(0)))
        return results

    def get_clean_pattern(self) -> str:
        """Returns the template text with markers replaced by placeholders."""
        return re.sub(r"⸢[^⸥]+⸥", "[[PAYLOAD]]", self.raw)
