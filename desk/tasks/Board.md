# Workflow Board

## To Do
- [ ] **Sync Board Implementation:** Complete the `Desk.sync_board` logic using the cleaned `BoardModel`.
- [ ] **Task Atomization:** Implement the `atomize` feature to break down large tasks into sub-tasks.
- [ ] **Verification:** Run a full structural round-trip test for all RepoPackage models (Pill, Task, Board, Contract).
- [ ] **Consistency Check:** Ensure all models in `src/repopackage/models/` follow the `rev•` prefix standard for round-trip fields.

## In Progress
- [x] **NLDB Engine Redesign:** Core `Renderer` and `DataExtractor` logic implemented with structural awareness.
- [x] **Jinja2 Purge:** Removed all Jinja2 dependencies and "noise" from `src/`.
- [x] **Model Standardisation:** Updated `TaskModel`, `PillModel`, `BoardModel`, and `ModuleContractModel` to use native structural markers.

## Done
- [x] **Workflow Logic Restoration:** Recovered and verified `src/repopackage/workflow/` directory.
- [x] **YAML Metadata Handler:** Implemented native support for YAML code blocks and frontmatter.
- [x] **Renderer Round-trip:** Implemented Pydantic-to-Markdown rendering path.
- [x] **nlDB Standalone Repackaging:** Created standalone library in `modules/normed/nldb/`.
