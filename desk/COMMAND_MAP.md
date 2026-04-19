# Workflow CLI Command Map

| Command | Location | Stub? | Purpose | Implementation Plan (Tools/Logic) |
| :--- | :--- | :--- | :--- | :--- |
| **system setup-project** | `system/init_command.py` | No | Scaffold workspace folders. | Uses `Path.mkdir(parents=True)` for `desk/`, `modules/`, `runs/`. Writes initial `Board.md` stubs. |
| **distill extract-turns** | `distill/extract_turns_command.py` | No | Split chat into turns. | Proxies to `workflow_pkg.distill.extract_gemini_turns.extract_file_to_directory`. Uses `bs4` for HTML. |
| **distill extract-artifacts** | `distill/extract_artifacts_command.py` | No | Extract blocks (UML, etc). | Proxies to `workflow_pkg.distill.artifact_extractor.extract_artifacts_from_file`. Regex-based. |
| **distill scaffold-workspace** | `distill/prepare_semantic_command.py` | No | Prepare semantic shell. | Uses `SemanticWorkspacePreparer`. Creates `semantic_output/` and `evidence.json` index. |
| **distill agent-prompt** | `distill/run_semantic_command.py` | No | Generate next prompt. | Uses `run_semantic_workflow`. Aggregates `evidence.json` into a brief for the next agent pass. |
| **distill show-entrypoints** | `distill/agent_prompt_command.py` | No | View contract pointers. | Reads `workflow_pkg/prompts/` and `workflow_pkg/CONSTRAINTS.md` to print absolute paths. |
| **standardize scaffold-module** | `standardize/standardize_command.py` | No | Create reusable modules. | Uses `StandardizeCreateCommand`. Writes `module.yaml` with `PyYAML` and creates `modules/` subdirs. |
| **drawers defer-spec** | `drawers/drawers_add_command.py` | No | Add design spec to backlog. | Reads `desk/drawers/Board.md`. Regex-extracts last ID. Appends new row with `Path.write_text`. |
| **drawers list-backlog** | `drawers/drawers_list_command.py` | No | View deferred work. | `Path("desk/drawers/Board.md").read_text()` and prints to stdout. |
| **drawers promote-spec** | `drawers/drawers_promote_command.py` | **Yes** | Spec -> Executable Task. | 1. `Path.read_text` the source spec in `desk/design/`. 2. Regex-extract `Goal:` and `Context:`. 3. Fill `task_contract.md` template. 4. `Path.write_text` to `desk/tasks/T-XXX.md`. |
| **drawers check-health** | `drawers/drawers_audit_command.py` | **Yes** | Verify backlog health. | 1. Parse `desk/drawers/Board.md` using `re.findall`. 2. Iterate rows. 3. `Path.exists()` check for every spec path. 4. Error if broken links found. |
| **desk split-tasks** | `desk/desk_tasks_command.py` | **Yes** | Atomize Task -> Pills. | 1. Parse `desk/tasks/T-XXX.md`. 2. Extract `# Checklist` items. 3. Create `desk/pills/PILL-XXX.md` for each item using `pill_contract.md` template. |
| **desk bind-context** | `desk/desk_pills_command.py` | **Yes** | Task -> Context injection. | 1. Use `mcp_serena_replace_content` logic to find `- Pills:` in `T-XXX.md`. 2. Append provided Pill IDs to the list. |
| **desk sync-board** | `desk/desk_board_command.py` | No | Rebuild Board from files. | Uses `TaskParser` (Regex) on all `desk/tasks/*.md`. Uses `BoardWriter` to rebuild `desk/tasks/Board.md`. |
| **exec execute-task** | `exec/exec_run_command.py` | **Yes** | Run agent on specific task. | 1. Read `T-XXX` and linked Pills. 2. `subprocess.run(["python", "-m", "workflow_pkg", "distill", "agent-prompt"])`. 3. Setup `runs/RUN-XXX/` env. |
| **exec batch-dispatch** | `exec/exec_dispatch_command.py` | **Yes** | Batch parallel execution. | 1. Load tasks from `desk/tasks/`. 2. Filter `Status: open`. 3. Use `concurrent.futures.ThreadPoolExecutor` to run `execute-task` in parallel. |
| **capture rescue-logs** | `capture/capture_rescue_command.py` | No | Pull raw agent logs. | Creates `runs/RUN-ID/raw/`. Future: `git logs` or `sys.stdin.read` redirect. |
| **capture format-evidence** | `capture/capture_normalize_command.py` | **Yes** | Normalize logs -> Evidence. | 1. Detect agent in `raw/` file headers. 2. Instantiate `ClaudeAdapter` or `GeminiAdapter`. 3. `Adapter.normalize()` -> `json.dump` to `normalized/evidence.json`. |
| **eval run-tests** | `eval/eval_test_command.py` | **Yes** | Run project test suite. | `subprocess.run(["pytest", "dev_tools/workflow_pkg/"])`. Capture output to `runs/RUN-ID/eval/tests.log`. |
| **eval run-linters** | `eval/eval_lint_command.py` | **Yes** | Run standard linters. | `subprocess.run(["ruff", "check", "dev_tools/workflow_pkg/"])`. If fail, print violations to stderr. |
| **eval audit-laws** | `eval/lint_constraints_command.py` | No | Verify 'Laws of Physics'. | Proxies to `workflow_pkg.eval.lint_constraints.main`. Custom AST parser for line counts/single-entity. |
| **eval full-gate** | `eval/eval_audit_command.py` | **Yes** | Complete quality check. | Boolean AND of `run-tests` + `run-linters` + `audit-laws`. Returns Exit Code 1 if any fail. |
| **integrate merge-work** | `integrate/integrate_merge_command.py` | **Yes** | Move code from run to src. | 1. `shutil.copytree` from `runs/RUN-ID/code/` to `dev_tools/workflow_pkg/`. 2. `git add`. 3. `git commit -m "feat: #TASK-ID ..."`. |
| **integrate revert-change** | `integrate/integrate_rollback_command.py` | **Yes** | Revert integration commit. | `subprocess.run(["git", "revert", "HEAD"])`. Verify clean tree first via `git status --porcelain`. |
| **integrate promote-artifacts** | `integrate/integrate_promote_command.py` | **Yes** | Push to production. | Stub for triggering external CI/CD or `git push` to a production branch. |
