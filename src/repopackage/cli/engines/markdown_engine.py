import re
from typing import Dict, Optional, List

class MarkdownEngine:
    """
    Engine to read and write sections in Markdown files using Regex.
    Preserves the rest of the document.
    """
    
    SECTION_HEADER_PATTERN = re.compile(r'^##\s+(.*?)$', re.MULTILINE)
    TITLE_PATTERN = re.compile(r'^#\s+(.*?)$', re.MULTILINE)

    def __init__(self, content: str):
        self.content = content

    def get_title(self) -> Optional[str]:
        match = self.TITLE_PATTERN.search(self.content)
        if match:
            return match.group(1).strip()
        return None

    def _get_sections_with_spans(self):
        matches = list(self.SECTION_HEADER_PATTERN.finditer(self.content))
        sections = []
        for i, match in enumerate(matches):
            header = match.group(1).strip()
            name = header.lower().replace(" ", "_")
            start = match.start()
            
            if i + 1 < len(matches):
                end = matches[i+1].start()
            else:
                end = len(self.content)
            
            sections.append({
                "name": name,
                "header": header,
                "start": start,
                "end": end,
                "content": self.content[match.end():end].strip()
            })
        return sections

    def extract_sections(self) -> Dict[str, str]:
        return {s["name"]: s["content"] for s in self._get_sections_with_spans()}

    def extract_section(self, name: str) -> Optional[str]:
        sections = self.extract_sections()
        normalized_name = name.strip().lower().replace(" ", "_")
        return sections.get(normalized_name)

    def update_section(self, section_name: str, new_content: str) -> str:
        normalized_target = section_name.strip().lower().replace(" ", "_")
        sections = self._get_sections_with_spans()
        
        target = None
        for s in sections:
            if s["name"] == normalized_target:
                target = s
                break
        
        if target:
            new_text = f"## {target['header']}\n{new_content.strip()}\n"
            self.content = self.content[:target["start"]] + new_text + self.content[target["end"]:]
        else:
            if not self.content.endswith('\n'):
                self.content += '\n'
            self.content += f"\n## {section_name}\n{new_content.strip()}\n"
            
        return self.content

    def read_metadata_list(self, section_name: str) -> List[str]:
        content = self.extract_section(section_name)
        if not content:
            return []
        
        if "[" in content and "]" in content and "|" in content:
            return [item.strip("[] ") for item in content.split("|")]
        
        items = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("- "):
                items.append(line[2:].strip())
            elif line.startswith("* "):
                items.append(line[2:].strip())
            elif line:
                items.append(line)
        return items

    def read_key_value_pairs(self, section_name: str) -> Dict[str, str]:
        content = self.extract_section(section_name)
        if not content:
            return {}
        
        pairs = {}
        for line in content.splitlines():
            line = line.strip()
            if line.startswith(("- ", "* ")):
                line = line[2:]
            
            if ":" in line:
                key, value = line.split(":", 1)
                pairs[key.strip()] = value.strip()
        return pairs

    def extract_checklist(self, section_name: str) -> List[str]:
        """Extract items from a list in a specific section."""
        content = self.extract_section(section_name)
        if not content:
            return []
        
        items = []
        for line in content.splitlines():
            line = line.strip()
            # Match 1. Item, - Item, * Item
            match = re.match(r'^(\d+\.|\-|\*)\s+(.*)', line)
            if match:
                items.append(match.group(2).strip())
        return items
