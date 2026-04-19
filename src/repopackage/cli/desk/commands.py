import typer
from pathlib import Path
import re
from typing import List
from repopackage.cli.engines.markdown_engine import MarkdownEngine
from repopackage.cli.engines.parser import TaskParser
from repopackage.cli.engines.board_writer import BoardWriter

board_app = typer.Typer(help="Board management commands.")
tasks_app = typer.Typer(help="Task management commands.")
pills_app = typer.Typer(help="Pill management commands.")

@board_app.command(name="sync")
def sync_board():
    """Synchronize Board.md with current task files."""
    tasks_dir = Path("desk/tasks")
    board_file = Path("desk/tasks/Board.md")
    
    if not tasks_dir.exists():
        typer.echo("Error: desk/tasks directory not found.")
        raise typer.Exit(code=1)
        
    task_files = list(tasks_dir.glob("T-*.md"))
    tasks = []
    parser = TaskParser()
    
    for tf in task_files:
        try:
            task = parser.parse_file(tf)
            tasks.append(task)
        except Exception as e:
            typer.echo(f"Warning: Could not parse {tf.name}: {e}")
            
    writer = BoardWriter(tasks)
    
    if board_file.exists():
        content = board_file.read_text()
    else:
        content = "# Tasks Board\n\n## Active (status=open|in_progress)\n\n## Blocked (status=blocked)\n\n## Completed\n"
        
    new_content = writer.write_board(content)
    board_file.write_text(new_content)
    typer.echo("Board.md synchronized successfully.")

@tasks_app.command(name="atomize")
def atomize_task(task_id: str):
    """Generates Context Pills from a task's Suggested checklist."""
    base_path = Path.cwd()
    if not task_id.startswith("T-"):
        task_id = f"T-{task_id}"
        
    task_file = base_path / "desk/tasks" / f"{task_id}.md"
    if not task_file.exists():
        typer.echo(f"Error: Task {task_id} not found.")
        raise typer.Exit(code=1)
    
    engine = MarkdownEngine(task_file.read_text())
    checklist_items = engine.extract_checklist("How to Do It (Suggested)")
    
    if not checklist_items:
        typer.echo("No checklist items found.")
        return

    pills_dir = base_path / "desk/pills"
    pills_dir.mkdir(parents=True, exist_ok=True)
    
    next_id = len(list(pills_dir.glob("PILL-*.md"))) + 1
    created = []
    template_path = base_path / "workflow/docs/template/context_pills.md"
    
    for item in checklist_items:
        pill_id = f"PILL-{next_id:02d}"
        pill_file = pills_dir / f"{pill_id}.md"
        if template_path.exists():
            pill_content = template_path.read_text().replace("PILL-XX", pill_id).replace("{title}", item)
            pill_file.write_text(pill_content)
        else:
            pill_file.write_text(f"# {pill_id} - {item}\n- **ID:** {pill_id}\n")
        
        created.append(pill_id)
        next_id += 1
        typer.echo(f"Created pill: {pill_id}")

    # Update original task with references to pills
    updated_checklist = []
    for i, item in enumerate(checklist_items):
        updated_checklist.append(f"{i+1}. [{created[i]}] - {item}")
    
    engine.update_section("How to Do It (Suggested)", "\n".join(updated_checklist))
    
    # Update References section
    current_refs = engine.read_metadata_list("Reference")
    new_refs = [f"desk/pills/{cp}.md" for cp in created]
    
    all_refs = current_refs.copy()
    for nr in new_refs:
        if nr not in all_refs:
            all_refs.append(nr)
    
    formatted_refs = []
    for r in all_refs:
        if not r.startswith("`"):
            formatted_refs.append(f"- `{r}`")
        else:
            formatted_refs.append(f"- {r}")
            
    engine.update_section("Reference", "\n".join(formatted_refs))
    
    task_file.write_text(engine.content)
    typer.echo(f"Updated {task_id} with {len(created)} pills.")

@pills_app.command(name="inject")
def inject_pill(
    task_id: str = typer.Option(..., "--task", "-t", help="Task ID"),
    pill_id: str = typer.Option(..., "--pill", "-p", help="Pill ID")
):
    """Link an existing context pill to a task."""
    if not task_id.startswith("T-"):
        task_id = f"T-{task_id}"
    if not pill_id.startswith("PILL-"):
        pill_id = f"PILL-{pill_id}"
        
    task_file = Path(f"desk/tasks/{task_id}.md")
    if not task_file.exists():
        typer.echo(f"Error: Task file desk/tasks/{task_id}.md not found.")
        raise typer.Exit(code=1)
        
    engine = MarkdownEngine(task_file.read_text())
    
    # Update Traits
    traits_content = engine.extract_section("Traits (Composición)") or ""
    if pill_id not in traits_content:
        clean_traits = traits_content.strip("`").strip()
        new_traits = f"{clean_traits} | [{pill_id}]".strip(" |")
        engine.update_section("Traits (Composición)", f"`[{new_traits}]`" if not new_traits.startswith("[") else f"`{new_traits}`")
    
    # Update Reference
    current_refs = engine.read_metadata_list("Reference")
    pill_ref = f"desk/pills/{pill_id}.md"
    if pill_ref not in current_refs:
        current_refs.append(pill_ref)
        # Tests expect simple list
        formatted_refs = [f"- {r}" for r in current_refs]
        engine.update_section("Reference", "\n".join(formatted_refs))
        
        # Update Induced Changes
        current_changes = engine.extract_section("Induced Changes") or ""
        # Strip placeholder if present
        current_changes = current_changes.replace("(Completar por Executor)", "").strip()
        new_changes = current_changes + f"\n- Injected pill {pill_id}"
        engine.update_section("Induced Changes", new_changes.strip())
        
        task_file.write_text(engine.content)
        typer.echo(f"Successfully injected pill {pill_id} into task {task_id}")
    else:
        typer.echo(f"Pill {pill_id} is already in task {task_id}.")
