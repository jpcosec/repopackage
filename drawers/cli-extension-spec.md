# talk-extractor CLI Extension Spec

## Purpose
Extend `talk_extractor` CLI to cover full workflow (steps 0-8).

## Command Structure

```
talk-extractor
├── extract-*        # Design (existing)
│   ├── extract-turns
│   ├── extract-artifacts
│   ├── prepare-semantic
│   ├── run-semantic
│   └── agent-prompt
├── standardize     # Step 2
├── drawers         # Step 3
├── desk            # Step 4
├── exec            # Step 5
├── capture         # Step 6
├── eval            # Step 7
└── integrate       # Step 8
```

---

## Step 2: Standardize

### `standardize create --standardized <name>`
Create a new standardized (reusable) module.

**Options**:
- `--name, -n` (required): module name
- `--domain`: problem space
- `--language`: implementation language
- `--template`: boilerplate template

**Output**: 
- Creates `modules/standardized/<name>/`
- Initializes `module.yaml` with standardized contract

### `standardize create --normed <name>`
Create a new normed (domain-specific) module.

**Options**:
- `--name, -n` (required): module name
- `--domain`: problem space
- `--language`: implementation language
- `--rules`: business rules file

**Output**:
- Creates `modules/normed/<name>/`
- Initializes `module.yaml` with normed contract

### `standardize list`
List all standardized/normed modules.

### `standardize validate <name>`
Validate module against its contract.

---

## Step 3: Drawers

### `drawers add <spec> --title <title> --domain <domain>`
Add a spec to drawers.

**Options**:
- `<spec>` (required): path to spec file
- `--title, -t`: human-readable title
- `--domain`: problem space
- `--type`: spec type (design, architecture, api, etc.)

**Output**:
- Registers spec in `desk/drawers/Board.md`

### `drawers list`
List all specs in drawers.

**Output**:
- Table from `desk/drawers/Board.md`

### `drawers promote <spec-id> --to <destination>`
Promote spec from drawers to execution.

**Options**:
- `<spec-id>` (required): spec ID from Board
- `--to`: destination (tasks, pills, or direct to src/)

### `drawers audit`
Audit all specs in drawers for completeness.

---

## Step 4: Desk

### `tasks atomize <task> --min-size <n>`
Atomize a task into smallest executable pills.

**Options**:
- `<task>` (required): task description or file
- `--min-size, -m`: minimum pill size (default: 1)

**Output**:
- Creates pill files in `desk/tasks/`
- Updates `desk/tasks/Board.md`

### `pills inject <pill-id> --with <pill1> --with <pill2>`
Inject context pills into a task.

**Options**:
- `<pill-id>` (required): target task/pill
- `--with, -w`: context pill IDs to inject

### `board sync`
Synchronize task board.

**Output**:
- Regenerates `desk/tasks/Board.md` from task files
- Updates status, progress

### `board status`
Show current board status.

---

## Step 5: Execution

### `exec run <agent> --task <task-id> --context <pill-ids>`
Run an agent on a task.

**Options**:
- `<agent>` (required): claude, gemini, opencode, pi
- `--task, -t`: task ID to execute
- `--context, -c`: context pill IDs to inject
- `--mode`: cli, api, interactive
- `--capture`: enable capture mode (default: true)

**Output**:
- Creates `runs/RUN-XXX/`
- Captures raw artifacts
- Returns run ID

### `exec dispatch <agent> --tasks <task-ids>`
Dispatch agent to multiple tasks.

**Options**:
- `<agent>` (required): agent type
- `--tasks`: comma-separated task IDs

### `exec status <run-id>`
Show status of a run.

---

## Step 6: Capture

### `capture rescue <run-id>`
Rescue raw artifacts from a run.

**Options**:
- `<run-id>` (required): run identifier

**Output**:
- Creates `runs/RUN-XXX/raw/`
- Captures stdout, stderr, transcripts

### `capture normalize <run-id> --tool <tool>`
Normalize raw artifacts to standard format.

**Options**:
- `<run-id>` (required): run identifier
- `--tool, -t`: claude, gemini, opencode, pi (auto-detect if omitted)

**Output**:
- Creates `runs/RUN-XXX/normalized/`
- Creates `runs/RUN-XXX/adapters/capture_report.json`

### `capture validate <run-id>`
Validate run package completeness.

### `capture list`
List all captured runs.

---

## Step 7: Evaluation

### `eval test <run-id> --scope <scope>`
Run tests for a completed run.

**Options**:
- `<run-id>` (required): run identifier
- `--scope`: unit, integration, e2e (default: all)

**Output**:
- Test results
- Updates `runs/RUN-XXX/normalized/result_manifest.json`

### `eval lint <run-id>`
Run linting for a completed run.

**Options**:
- `<run-id>` (required): run identifier
- `--rules`: custom rules file

### `eval audit <run-id>`
Full audit: tests + lint + constraints.

**Options**:
- `<run-id>` (required): run identifier

---

## Step 8: Integration

### `integrate merge <run-id>`
Merge run results into project.

**Options**:
- `<run-id>` (required): run identifier

**Output**:
- Copies outputs to target locations
- Updates `CHANGELOG.md`
- Creates integration commit

### `integrate promote <artifact> --to <destination>`
Promote artifact to production/staging.

**Options**:
- `<artifact>` (required): artifact ID
- `--to`: destination (prod, staging, release)

### `integrate rollback <run-id>`
Rollback a previous integration.

---

## Common Options

All commands support:
- `--help, -h`: show help
- `--verbose, -v`: verbose output
- `--dry-run`: show what would happen without executing

---

## Output Format

All list commands support:
- `--format table` (default)
- `--format json`
- `--format yaml`

---

## Exit Codes

- 0: success
- 1: general error
- 2: validation error
- 3: not found
- 4: conflict