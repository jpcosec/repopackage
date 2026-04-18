"""Task Parser logic."""

from __future__ import annotations

import re


class TaskParser:
    """Parser for task markdown files."""

    def parse(self, text: str) -> dict:
        """Parse task metadata from markdown text."""

        data = self._init_data()
        self._parse_title(text, data)
        self._parse_base_fields(text, data)
        self._parse_lists(text, data)
        self._parse_commit(text, data)
        return data

    def _init_data(self) -> dict:
        """Initialize task data dictionary."""

        return {"ID": "", "Title": "", "Type": "", "Domain": "", "Status": "",
                "Priority": "", "Depends On": "", "Pills": "", "Phase": "",
                "Resolving Commit": ""}

    def _parse_title(self, text: str, data: dict) -> None:
        """Parse ID and Title from header."""

        match = re.search(r"^# ([\w-]+) - (.*)$", text, re.M)
        if match: data["ID"], data["Title"] = match.groups()

    def _parse_base_fields(self, text: str, data: dict) -> None:
        """Parse core single-line fields."""

        for key in ["Type", "Domain", "Status", "Priority", "Phase"]:
            m = re.search(fr"^- {key}: (.*)$", text, re.M)
            if m: data[key] = m.group(1).strip()

    def _parse_lists(self, text: str, data: dict) -> None:
        """Parse multiline lists like Depends On and Pills."""

        for key in ["Depends On", "Pills"]:
            m = re.search(fr"^- {key}:\n((?:  - .*\n)*)", text, re.M)
            if m:
                items = re.findall(r"  - (.*)", m.group(1))
                data[key] = ", ".join(items)

    def _parse_commit(self, text: str, data: dict) -> None:
        """Parse resolving commit hash."""

        commit = re.search(r"^- commit: `(.*)`", text, re.M)
        if commit: data["Resolving Commit"] = commit.group(1)
