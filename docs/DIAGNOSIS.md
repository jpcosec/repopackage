# Repopackage — Bug Diagnosis

## Bug #1 — `GitAdapter._traverse_tree`: Nested path traversal fails (CRITICAL)

**File:** `src/repopackage/adapters/git.py:30–37`

**Root cause:** `tree[part]` returns a `pygit2.TreeEntry`, not a `Tree`. On the
second iteration of the loop, `entry` is a `TreeEntry`, which does not implement
`__contains__` or `__getitem__`. Any path with a `/` (including the required
`contracts/integration.contract.yaml`) raises `TypeError` at `part not in entry`.

**Fix:** Call `repo.get(entry.id)` after each subscript to resolve the `TreeEntry`
to its underlying `Tree` or `Blob` before continuing the walk.

---

## Bug #2 — `GitAdapter.read_file`: TreeEntry has no `.data` (CRITICAL)

**File:** `src/repopackage/adapters/git.py:24–28`

**Root cause:** `_traverse_tree` returns the final `TreeEntry`. `TreeEntry` has
no `.data` attribute; only a resolved `Blob` does. Even for single-component
paths like `"README.md"`, `entry.data.decode("utf-8")` raises `AttributeError`.

**Fix:** Same as Bug #1 — resolve the final `TreeEntry` via `repo.get(entry.id)`
before accessing `.data`.

---

## Bug #3 — `GitAdapter.get_commit_hash`: No clone/fetch logic (CRITICAL)

**File:** `src/repopackage/adapters/git.py:12–18`

**Root cause:** The method assumes the repo already exists in `cache_dir`. It
never calls `pygit2.clone_repository` or fetches. Any SSH/HTTPS URL that hasn't
been manually pre-cloned raises `FileNotFoundError`. The headline "zero-checkout
peeking" feature is absent.

**Impact:** `rp resolve` fails on any dependency not already on disk.

---

## Bug #4 — `CompositionSolver._expand_transitive`: URLs are fabricated (HIGH)

**File:** `src/repopackage/core/solver.py:52–57`

**Root cause:** Transitive dependency URLs are generated as
`git@github.com:org/{name}.git`. The `IntegrationContract.compatibility.requires`
field stores only `{name: semver_range}` — there is no URL field. The fabricated
URL will be wrong for any org that isn't literally `org` on `github.com`.

**Fix:** Extend `IntegrationContract` to carry explicit URLs for required deps,
or accept a URL resolver at construction time.

---

## Bug #5 — `RepoAdapter._build_manifest_xml`: SSH URL parsed as filesystem path (MEDIUM)

**File:** `src/repopackage/adapters/repo.py:50`

**Root cause:** `os.path.dirname("git@github.com:org/repo.git")` returns
`"git@github.com:org"` — `os.path` treats `:` as a regular character. Google
Repo will fail to initialise from this non-URL fetch string.

**Fix:** Parse the fetch base by splitting on `:` for SSH URLs, or require HTTPS
URLs where `os.path.dirname` is valid.

---

## Bug #6 — Three CLI commands are stubs (MEDIUM)

**File:** `src/repopackage/cli/handlers.py:73–88`

`handle_status`, `handle_generate`, and `handle_graph` print "Feature coming
soon." and return. No implementation exists.

---

## Bug #7 — `_load_contract` swallows all exceptions (LOW)

**File:** `src/repopackage/core/solver.py:45–50`

A bare `except Exception` replaces YAML parse errors, missing fields, and
network failures with a silent default contract `version="0.0.0"`. Malformed
contracts produce no warning and silently pass version/interface checks.

**Fix:** Log a warning at minimum; re-raise unexpected exceptions.

---

## Bug #8 — `Project.uses` is an untyped dict (LOW)

**File:** `src/repopackage/core/models.py:31–32`

`Dict[str, Dict[str, str]]` loses type safety and cannot express the `line`
field described in the README. Should be `Dict[str, DependencySpec]` with a
proper Pydantic model carrying `url`, `branch`, `version`, and `line`.

---

## Bug #9 — `Traits` model is dead code (LOW)

**File:** `src/repopackage/core/models.py:11–14`

`Traits` is referenced in `ComposableUnit.traits` but never read by the solver,
handlers, or CLI. Either wire it up or remove it.

---

## Test coverage map

| Bug | Covered by |
|-----|-----------|
| #1 nested traversal | `test_git_adapter.py::test_read_file_nested_path` |
| #2 TreeEntry .data  | `test_git_adapter.py::test_read_file_flat_path` |
| #3 no clone         | `test_git_adapter.py::test_get_commit_hash_missing_repo` |
| #4 fabricated URL   | `test_solver_graph.py::test_transitive_url_is_fabricated` |
| #5 SSH dirname      | `test_repo_adapter.py::test_manifest_fetch_url` |
| #6 stubs            | `test_handlers.py::test_handle_*_is_stub` |
| #7 silent swallow   | `test_solver_graph.py::test_bad_contract_yaml_raises` |
| #8 untyped uses     | `test_models.py::test_project_uses_untyped` |
| #9 dead Traits      | `test_models.py::test_traits_unused` |
