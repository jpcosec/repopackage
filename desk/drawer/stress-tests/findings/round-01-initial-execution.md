# Round 01: Initial execution of repopackage stress tests

## Summary

- STs executed: ST-init, ST-entrypoints, ST-resolve, ST-sync, ST-validate, ST-status, ST-generate, ST-graph, ST-exports, ST-compose, ST-edge-cases
- Total findings: 38
- Total exit codes observed: 0 (success), 1 (handled error), 2 (argparse error)

## Findings

### Finding RP-01: `--help` lacks descriptions on all commands
- **ST**: All
- **Step**: 1 (all STs)
- **Command**: `rp <cmd> --help`
- **Expected**: Each subcommand's `--help` should describe what it does
- **Observed**: All 8 subcommands show only `usage: rp <cmd> [-h]` and `options: -h, --help` — zero description text. Examples:
  ```
  usage: rp init [-h]
  options:
    -h, --help  show this help message and exit
  ```
- **Severity**: medium
- **Type**: discoverability

### Finding RP-02: `rp init` silently overwrites existing compose.yaml
- **ST**: ST-init
- **Step**: 4, 8
- **Command**: `rp init` (with existing compose.yaml)
- **Expected**: Error: "compose.yaml already exists" or prompt to overwrite
- **Observed**: Step 4: "Initializing new project... Created compose.yaml" — no warning, file silently overwritten. Step 8: Custom content (`# Custom content`) was silently replaced.
- **Severity**: high
- **Type**: silent-failure / data-loss

### Finding RP-03: Permission error shows PermissionError traceback
- **ST**: ST-init
- **Step**: 5
- **Command**: `rp init` in `chmod -w` directory
- **Expected**: User-friendly "Permission denied: cannot write compose.yaml"
- **Observed**:
  ```
  Initializing new project...
  Traceback (most recent call last):
    File ".../cli/main.py", line 11, in main
      args.handler()
    File ".../cli/handlers.py", line 22, in handle_init
      with open(constants.COMPOSE_FILE, "w") as f:
  PermissionError: [Errno 13] Permission denied: 'compose.yaml'
  ```
  Note: "Initializing new project..." is printed before the crash, misleading the user.
- **Severity**: medium
- **Type**: error-message

### Finding RP-04: `rp init .` fails with "unrecognized arguments"
- **ST**: ST-init
- **Step**: 7
- **Command**: `rp init .`
- **Expected**: Either accept `.` as CWD, or show a helpful message like "rp init takes no arguments"
- **Observed**: `rp: error: unrecognized arguments: .` — argparse error, exit code 2
- **Severity**: low
- **Type**: error-message / discoverability

### Finding RP-05: No `--version` flag on rp or repopackage
- **ST**: ST-entrypoints
- **Step**: 5, 6
- **Command**: `rp --version`, `repopackage --version`
- **Expected**: Print version string (e.g., "0.1.1")
- **Observed**: Both show `rp: error: unrecognized arguments: --version` with exit code 2
- **Severity**: medium
- **Type**: discoverability

### Finding RP-06: `rp resolve` claims success but does not write compose.lock.yaml for projects without `uses`
- **ST**: ST-resolve, also verified independently
- **Step**: 2, 5
- **Command**: `rp resolve` on project with `uses: {}` or no uses
- **Expected**: If resolve completes, the lockfile should exist
- **Observed**:
  ```
  Resolved successfully. Wrote compose.lock.yaml
  ```
  But `ls compose.lock.yaml` returns `No such file or directory`. The exit code is 0 (success). This is a **silent failure** — the tool lies to the user.
- **Severity**: high
- **Type**: silent-failure

### Finding RP-07: Resolve error for missing local repos uses "Unexpected error:" prefix with FileNotFoundError
- **ST**: ST-resolve
- **Step**: 2
- **Command**: `rp resolve` when local repos are missing
- **Expected**: "Error: Local repository not found at /tmp/dummy_repos/ui-kit. Run `rp sync` to clone dependencies or update compose.yaml with valid URLs."
- **Observed**: `Unexpected error: Local repository not found at /tmp/dummy_repos/ui-kit` — the `Unexpected error:` prefix is developer-oriented.
- **Severity**: low
- **Type**: error-message

### Finding RP-08: Resolve with nonexistent remote shows pygit2 internal error
- **ST**: ST-resolve
- **Step**: 6
- **Command**: `rp resolve` with cyclic deps pointing to nonexistent GitHub repos
- **Expected**: "Error: Cannot access repository https://github.com/example/a.git. Check the URL or network connection."
- **Observed**: `Unexpected error: remote authentication required but no callback set` — this is a raw pygit2/libgit2 error message.
- **Severity**: medium
- **Type**: error-message

### Finding RP-09: `rp sync` crashes with full traceback + Google Repo tool error
- **ST**: ST-sync
- **Step**: 2
- **Command**: `rp sync` on project with missing local repos
- **Expected**: Graceful error message suggesting how to fix
- **Observed**: Multi-layered error: Google Repo tool `SyncError` + `GitCommandError` + Python full traceback from `subprocess.CalledProcessError` propagating to user's terminal.
- **Severity**: high
- **Type**: error-message / traceback

### Finding RP-10: No `--format json` or machine-parseable output on any command
- **ST**: ST-status, ST-exports, ST-graph
- **Step**: Various
- **Command**: `rp status --format json`, `rp exports --format json`, `rp graph --format dot`
- **Expected**: At least one command supports machine-parseable output
- **Observed**: All unrecognized arguments. Exit code 2.
- **Severity**: high
- **Type**: discoverability / CI-readiness

### Finding RP-11: `rp sync` has no `--force` flag
- **ST**: ST-sync
- **Step**: 4
- **Command**: `rp sync --force`
- **Expected**: Either a --force flag exists, or a clear message
- **Observed**: `rp: error: unrecognized arguments: --force` — exit code 2
- **Severity**: low
- **Type**: discoverability

### Finding RP-12: No `--workspace` flag on validate
- **ST**: ST-validate
- **Step**: 7
- **Command**: `rp validate --workspace /tmp/rp-test-validate`
- **Expected**: Flag to validate a specific workspace path
- **Observed**: `rp: error: unrecognized arguments: --workspace /tmp/rp-test-validate` — exit code 2
- **Severity**: low
- **Type**: discoverability

### Finding RP-13: `rp validate` output is too minimal: just "Validation passed."
- **ST**: ST-validate
- **Step**: 2
- **Command**: `rp validate` on a valid project
- **Expected**: List of checks performed (e.g., "Checking workspace integrity... Checking commit hashes... Checking contract schemas...")
- **Observed**: Just `Validation passed.` — no detail on what was checked
- **Severity**: low
- **Type**: discoverability

### Finding RP-14: `rp status` returns exit 0 even when packages are MISSING
- **ST**: ST-status
- **Step**: 4
- **Command**: `rp status` in dir with lockfile but no workspace
- **Expected**: Exit code 1 to indicate non-OK status
- **Observed**: Exit code 0, but table shows "MISSING" for all packages. Should be exit 1.
- **Severity**: medium
- **Type**: edge-case / consistency

### Finding RP-15: `rp status` output has no machine-parseable format
- **ST**: ST-status
- **Step**: 5, 6
- **Command**: `rp status > file` and `rp status --format json`
- **Expected**: Tabular output redirects cleanly (good). But no --format flag for scripting.
- **Observed**: Output is fixed-width table (padded with spaces); no --format flag exists.
- **Severity**: low
- **Type**: CI-readiness

### Finding RP-16: `rp generate` produces no output files — user doesn't know what was generated
- **ST**: ST-generate
- **Step**: 2, 4
- **Command**: `rp generate`
- **Expected**: Should produce files (schemas, types, etc.) in a known location
- **Observed**: Stdout says "Found 2 contracts" but no `generated/` or `out/` directory is created. Output is stdout-only. No `--output` flag.
- **Severity**: high
- **Type**: discoverability / silent-failure

### Finding RP-17: `rp graph` shows full traceback when deps are missing
- **ST**: ST-graph
- **Step**: 2
- **Command**: `rp graph` in project with missing local repos
- **Expected**: "Error: Cannot resolve dependencies. Local repositories not found. Run `rp sync` first."
- **Observed**: Full 12-line Python traceback from `FileNotFoundError: Local repository not found at /tmp/dummy_repos/ui-kit`
- **Severity**: high
- **Type**: error-message / traceback

### Finding RP-18: `rp graph` for standalone project outputs only "graph TD" with no edges
- **ST**: ST-graph
- **Step**: 6
- **Command**: `rp graph` with project having `uses: {}`
- **Expected**: A single node representing the project, e.g., "graph TD; standalone[standalone]"
- **Observed**:
  ```
  Mermaid Dependency Graph:
  graph TD
  ```
  No nodes or edges rendered. Invalid Mermaid.
- **Severity**: medium
- **Type**: edge-case

### Finding RP-19: No `--focus`, `--depth`, or `--format` flags on graph
- **ST**: ST-graph
- **Step**: 7, 8, 9
- **Command**: `rp graph --focus X`, `--depth 1`, `--format dot`
- **Expected**: At least one filtering/formatting option
- **Observed**: All unrecognized. Exit code 2.
- **Severity**: medium
- **Type**: discoverability

### Finding RP-20: `rp exports` outputs empty markdown heading with no content
- **ST**: ST-exports
- **Step**: 2
- **Command**: `rp exports`
- **Expected**: List of packages with their commands, contracts, and procedures
- **Observed**:
  ```
  ## Ecosystem Export Surface (Target: repopackage)
  ```
  That's it. An empty markdown H2 heading. No package list, no exports, no syntax guide.
- **Severity**: high
- **Type**: silent-failure

### Finding RP-21: No `--package` filter on exports
- **ST**: ST-exports
- **Step**: 6
- **Command**: `rp exports --package repopackage`
- **Expected**: Filter exports to a specific package
- **Observed**: `rp: error: unrecognized arguments: --package repopackage` — exit code 2
- **Severity**: low
- **Type**: discoverability

### Finding RP-22: Incomplete compose.yaml (missing url/branch) resolves "successfully"
- **ST**: ST-compose
- **Step**: 2
- **Command**: `rp resolve` with `name: incomplete` (missing kind, url, branch)
- **Expected**: Error: "compose.yaml missing required fields: kind, url, branch"
- **Observed**: `Resolved successfully. Wrote compose.lock.yaml` — exit code 0, no validation error
- **Severity**: high
- **Type**: silent-failure / validation

### Finding RP-23: Invalid YAML in compose.yaml shows full ruamel.yaml traceback
- **ST**: ST-compose
- **Step**: 3
- **Command**: `rp resolve` with `invalid: yaml: :`
- **Expected**: "Error parsing compose.yaml: mapping values are not allowed here at line 1, column 14"
- **Observed**: Full 18-line ruamel.yaml traceback referencing scanner/parser internals
- **Severity**: medium
- **Type**: error-message / traceback

### Finding RP-24: Unknown fields in compose.yaml silently ignored
- **ST**: ST-compose
- **Step**: 5
- **Command**: `rp resolve` with `unknown_field: should_not_be_here`
- **Expected**: Warning: "Unknown field 'unknown_field' in compose.yaml"
- **Observed**: `Resolved successfully. Wrote compose.lock.yaml` — no validation, no warning
- **Severity**: medium
- **Type**: silent-failure / validation

### Finding RP-25: UTF-8 names with emoji accepted in compose.yaml resolve
- **ST**: ST-compose
- **Step**: 6
- **Command**: `rp resolve` with `name: proyecto-ñoño-🎉`
- **Expected**: Either valid or error
- **Observed**: `Resolved successfully. Wrote compose.lock.yaml` — accepted (but see RP-06: lockfile not actually written)
- **Severity**: low
- **Type**: edge-case

### Finding RP-26: Path traversal URLs in compose.yaml not validated
- **ST**: ST-edge-cases
- **Step**: 2
- **Command**: `rp resolve` with url `https://github.com/../../etc/passwd`
- **Expected**: Warning or error about suspicious URL
- **Observed**: `Resolved successfully. Wrote compose.lock.yaml` — exit code 0, no validation
- **Severity**: medium
- **Type**: edge-case / validation

### Finding RP-27: Corrupt lockfile error shows Python internal class name
- **ST**: ST-edge-cases
- **Step**: 3
- **Command**: `rp validate` with corrupt compose.lock.yaml
- **Expected**: "Error parsing compose.lock.yaml: invalid format"
- **Observed**: `Error parsing lockfile: repopackage.core.models.Lockfile() argument after ** must be a mapping, not str` — exposes internal Pydantic constructor
- **Severity**: medium
- **Type**: error-message

### Finding RP-28: 1000-char project name accepted without validation
- **ST**: ST-edge-cases
- **Step**: 6
- **Command**: `rp resolve` with 1000-character project name
- **Expected**: Warning about excessive name length, or reject
- **Observed**: `Resolved successfully. Wrote compose.lock.yaml` (but lockfile not actually written — see RP-06)
- **Severity**: low
- **Type**: edge-case

### Finding RP-29: Spaces in paths work correctly for init
- **ST**: ST-edge-cases
- **Step**: 7
- **Command**: `rp init` in directory with spaces
- **Expected**: Should work (or clear error)
- **Observed**: Works — `Initializing new project... Created compose.yaml` — exit code 0
- **Severity**: none (positive finding)
- **Type**: edge-case

### Finding RP-30: Test suite has 1 failing test
- **ST**: (test suite health)
- **Command**: `python -m pytest tests/ -v`
- **Expected**: All 52 tests pass
- **Observed**: 51 passed, 1 FAILED: `test_ecosystem_fixture_resolution_and_validation` — fails because `compose.lock.yaml` not found after resolve (same root cause as RP-06). References `/home/jp/proyectos/wikipu-ecosystem/repopackage/tests/` (different project path).
- **Severity**: high
- **Type**: error-message / silent-failure

### Finding RP-31: `rp resolve` error for deps without URL is clear
- **ST**: ST-compose
- **Step**: 4
- **Command**: `rp resolve` with dep missing `url` field
- **Expected**: Clear error message
- **Observed**: `Unexpected error: Missing URL for dependency 'dep1' required by 'test'` — semantic and actionable despite "Unexpected" prefix
- **Severity**: low
- **Type**: error-message (positive finding)

### Finding RP-32: `rp validate` detects missing workspace packages clearly
- **ST**: ST-validate
- **Step**: 4
- **Command**: `rp validate` with lockfile but no workspace
- **Expected**: List missing packages
- **Observed**: `Validation failed: - ui-kit missing from workspace! - code-quality-auditor missing from workspace!` — clear
- **Severity**: none (positive finding)
- **Type**: error-message

### Finding RP-33: `compose.yaml not found!` error is consistent and clear
- **ST**: Multiple
- **Step**: Various
- **Command**: Various commands without compose.yaml
- **Expected**: Clear error
- **Observed**: All commands show `compose.yaml not found!` or `compose.lock.yaml not found! Run 'rp resolve' first.` — consistent and actionable
- **Severity**: none (positive finding)
- **Type**: error-message

### Finding RP-34: Google Repo tool IS required for sync
- **ST**: ST-sync
- **Step**: 8
- **Command**: `which repo && repo --version`
- **Expected**: Check dependency
- **Observed**: `repo` is installed at `/home/jp/bin/repo` (v2.54). Sync command calls `repo sync -q -j4` via subprocess. Without repo tool, sync would fail with a different error. The dependency is hard-coded and not mockable.
- **Severity**: medium
- **Type**: edge-case

### Finding RP-35: ST-resolve step 5 had a misleading success
- **ST**: ST-resolve
- **Step**: 5
- **Command**: `rp resolve` with `uses: {}` and nonexistent project URL
- **Expected**: Error about URL validation
- **Observed**: `Resolved successfully. Wrote compose.lock.yaml` — but no lockfile written (RP-06). The project URL was not validated either.
- **Severity**: medium
- **Type**: silent-failure

### Finding RP-36: `rp exports --help` is empty (no description)
- **ST**: ST-exports
- **Step**: 1
- **Command**: `rp exports --help`
- **Expected**: Description of what exports does
- **Observed**: Same as all other subcommands — no description text
- **Severity**: low
- **Type**: discoverability

### Finding RP-37: `rp` without subcommand shows full help (same as `--help`)
- **ST**: ST-entrypoints
- **Step**: 4
- **Command**: `rp` (no args)
- **Expected**: Error or shortened help
- **Observed**: Shows same full help as `rp --help` but with exit code 2 (argparse error). This means piping output to check success would work, but exit code differs.
- **Severity**: low
- **Type**: consistency

### Finding RP-38: `rp status` and `rp validate` give different levels of info
- **ST**: ST-status
- **Step**: 7
- **Command**: Compare `rp status` and `rp validate`
- **Expected**: Consistent or complementary
- **Observed**:
  - `rp status` shows per-package table with SHAs and status (OK/MISSING)
  - `rp validate` says just "Validation passed." or "Validation failed: - X missing from workspace!"
  - They show different information, which is good (not redundant), but validate could be more detailed.
- **Severity**: low
- **Type**: consistency
