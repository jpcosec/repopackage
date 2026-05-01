---
id: 6
domain: manifest/sync
status: in-progress
priority: p1

created: "2026-05-01"
---

# Fix manifest generation

## Objective

Make lockfile-to-manifest translation safe enough for real workspace materialization.

## Reference

- `docs/DIAGNOSIS.md`
- `src/repopackage/adapters/repo.py`

## What to Fix

Current manifest assumptions are too simplistic for the intended system.
- Bug #5: SSH URLs like `git@github.com:org/repo.git` are parsed incorrectly by `os.path.dirname`, resulting in invalid `fetch` values in the manifest.
- Remote duplication: The current logic creates a new remote for every package, even if they share the same base URL.

## Current Step

**Status:** Implementing robust URL derivation and remote deduplication.

### Implementation Details

1.  **URL Derivation:**
    -   For SSH (`git@...`): Split at the first `:` to separate the host/user from the path.
    -   For HTTPS (`https://...`): Use `urllib.parse` to extract scheme and netloc as the `fetch` base.
    -   Fallback: Continue using `os.path` for simple filesystem-like paths.

2.  **Deduplication:**
    -   Use a dictionary to track unique `fetch` bases and assign stable remote names (`remote_0`, `remote_1`, etc.).

3.  **Code Snippet (Proposed for `RepoAdapter`):**
    ```python
    def _derive_fetch_and_name(self, url):
        if url.startswith("git@"):
            if ":" in url:
                base, path = url.split(":", 1)
                return f"{base}:", path
            return os.path.dirname(url), os.path.basename(url)
        elif "://" in url:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            fetch = f"{parsed.scheme}://{parsed.netloc}"
            return fetch, parsed.path.lstrip("/")
        return os.path.dirname(url), os.path.basename(url)
    ```

## Validation

- manifest generation produces coherent remotes/projects for supported URL forms.
- New test file `repopackage/tests/test_repo_adapter.py` created to verify multiple URL formats.
- All `repopackage` tests pass.
