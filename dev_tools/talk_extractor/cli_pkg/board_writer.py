"""Board Writer logic."""

from __future__ import annotations


class BoardWriter:
    """Helper to build Board.md content."""

    def build(self, tasks: list[dict]) -> str:
        """Build the full Board.md content."""

        c = ["# Tasks Board\n", "> Single entry point for all active work.\n"]
        self._build_active(tasks, c)
        self._build_done(tasks, c)
        self._build_blocked(tasks, c)
        c.append("\n## Ready to Promote (from drawers/)\n| ID | Type | Domain | Item |\n|----|------|--------|------|")
        return "\n".join(c) + "\n"

    def _build_active(self, ts, c) -> None:
        """Add active tasks section."""

        c.append("## Active (status=open|in_progress)")
        c.append("| ID | Type | Domain | Task | Priority | Deps | Pills | Ph |")
        c.append("|----|------|--------|------|----------|------|-------|----|")
        active = [t for t in ts if t["Status"] in ("open", "in_progress")]
        for t in active:
            r = f"| {t['ID']} | {t['Type']} | {t['Domain']} | {t['Title']} | {t['Priority']} | {t['Depends On']} | {t['Pills']} | {t['Phase']} |"
            c.append(r)

    def _build_done(self, ts, c) -> None:
        """Add completed tasks section."""

        c.append("\n## Completed")
        c.append("| ID | Type | Domain | Task | Resolving Commit |")
        c.append("|----|------|--------|------|------------------|")
        done = [t for t in ts if t["Status"] == "done"]
        for t in done:
            r = f"| {t['ID']} | {t['Type']} | {t['Domain']} | {t['Title']} | {t['Resolving Commit']} |"
            c.append(r)

    def _build_blocked(self, ts, c) -> None:
        """Add blocked tasks section."""

        c.append("\n## Blocked (status=blocked)\n| ID | Type | Domain | Blocker | Gate |\n|----|------|--------|--------|------|")
        blocked = [t for t in ts if t["Status"] == "blocked"]
        for t in blocked:
            r = f"| {t['ID']} | {t['Type']} | {t['Domain']} | {t['Depends On']} | {t['Phase']} |"
            c.append(r)
