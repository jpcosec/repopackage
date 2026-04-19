from pathlib import Path
import typer

BOARD_TEMPLATE = """# Tasks Board

> Single entry point for all active work.

## Active (status=open|in_progress)
| ID | Type | Domain | Task | Priority | Deps | Pills | Ph |
|----|------|--------|------|----------|------|-------|----|

## Blocked (status=blocked)
| ID | Type | Domain | Blocker | Gate |
|----|------|--------|---------|------|

## Completed
| ID | Type | Domain | Task | Resolving Commit |
|----|------|--------|------|------------------|

## Ready to Promote (from drawers/)
| ID | Domain | Item |
|----|--------|------|
"""

def init_project_command():
    """Initializes the project structure."""
    base_path = Path.cwd()
    
    # Define required zones
    zones = [
        "desk/tasks",
        "desk/pills",
        "desk/design",
        "drawers",
        "modules",
        "runs"
    ]
    
    for zone in zones:
        Path(base_path / zone).mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created zone: {zone}")
        
    board_path = base_path / "desk/tasks/Board.md"
    if not board_path.exists():
        board_path.write_text(BOARD_TEMPLATE)
        typer.echo("Created Board.md")
    else:
        typer.echo("Board.md already exists, skipping.")

    typer.echo("Project initialized successfully.")
