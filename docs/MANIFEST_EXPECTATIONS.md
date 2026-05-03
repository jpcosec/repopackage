# Repopackage Manifest Expectations

This document defines the requirements and behavior for `repopackage` manifest generation and workspace synchronization.

## 1. Accepted URL Forms

`repopackage` supports the following repository URL forms in `compose.yaml`:

- **SSH**: `git@github.com:org/repo.git`
- **HTTPS**: `https://github.com/org/repo.git`
- **Local (Absolute)**: `/home/user/projects/repo`
- **Local (Relative)**: `../sibling-repo`

## 2. Fetch-Base Derivation

To support Google Repo's manifest structure, `repopackage` derives a `fetch` base and a `project name` from each URL:

| URL Form | Derived Fetch | Derived Name |
| :--- | :--- | :--- |
| `git@host:path/repo.git` | `git@host:` | `path/repo.git` |
| `https://host/path/repo.git`| `https://host` | `path/repo.git` |
| `/abs/path/repo` | `/abs/path` | `repo` |
| `../rel/path/repo` | `..` | `rel/path/repo` |

## 3. Sync Prerequisites

Before running `rp sync`, ensure the following:

1. **Google Repo Tool**: Must be installed and reachable (default: `~/bin/repo`).
2. **Git Credentials**: SSH keys or HTTPS helpers must be configured for non-public repositories.
3. **Workspace Directory**: The target directory for materialization must be writable.

## 4. Safety and Config

- **Git Config**: `repopackage` does NOT mutate your local or global `.gitconfig`. It uses environment variables (`GIT_AUTHOR_NAME`, etc.) for internal manifest repository operations.
- **Atomic Sync**: `rp sync` uses `repo sync -j4` for parallel, atomic synchronization of the entire workspace.
