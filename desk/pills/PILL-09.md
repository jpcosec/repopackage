# PILL-09 - Workflow Domain Layer

## Metadata
- **ID:** PILL-09
- **Type:** pattern
- **Scope:** global
- **Domain:** workflow
- **Language:** Python
- **Nature:** implementation
- **Status:** active
- **Reusable:** yes
- **Applies To:**
  - `src/repopackage/workflow/`

## Why
El CLI actual actúa como cerebro: cada comando sabe exactamente qué archivos tocar y cómo. Esto hace que el CLI sea difícil de testear, que los agentes tengan que pensar en acciones concretas (qué archivo, qué sección), y que no haya API reutilizable desde código. La solución es una capa de dominio que modele el workflow como objetos con comportamiento.

## What
- Paquete `src/repopackage/workflow/` con clases que representan el workspace.
- `Workspace(root)` es el punto de entrada único.
- El CLI pasa a ser un reflejo delgado: `rp eval --last_phase` → `Workspace().last_phase().eval()`.
- Prohibido que el CLI implemente lógica de negocio directamente.

## How
```python
ws = Workspace()                        # rp <cualquier comando>
ws.last_phase().eval()                  # rp eval --last_phase
ws.desk.tasks.atomize("T-07")           # rp desk tasks atomize T-07
ws.desk.board_sync()                    # rp desk board sync
ws.drawers.promote("D-01")              # rp drawers promote D-01
ws.drawers.list()                       # rp drawers list
```

## Pattern Shape
```
Workspace
├── .desk → Desk
│   ├── .tasks → TaskCollection
│   │   ├── .all() → List[WorkflowTask]
│   │   ├── .atomize(task_id) → List[WorkflowPill]
│   │   └── .sync_board() → None
│   └── .pills → PillCollection
│       └── .inject(task_id, pill_id) → None
├── .drawers → Drawers
│   ├── .list() → List[DrawerSpec]
│   ├── .add(path, title, domain) → DrawerSpec
│   └── .promote(spec_id) → WorkflowTask
├── .phases() → List[Phase]
├── .last_phase() → Phase
└── .phase(id) → Phase

Phase
├── .tasks() → List[WorkflowTask]
└── .eval() → EvalResult
```

---
**Lifecycle:** Still needed? (Keep)
