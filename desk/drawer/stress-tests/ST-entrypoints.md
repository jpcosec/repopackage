# ST-entrypoints: rp vs repopackage vs python -m

**Basado en:** UC-01

## Script

```bash
# 1. Comparar rp --help y repopackage --help
rp --help > /tmp/rp-help.txt 2>&1
repopackage --help > /tmp/repopackage-help.txt 2>&1
diff /tmp/rp-help.txt /tmp/repopackage-help.txt || echo "DIFFERENT"

# 2. python -m repopackage --help
python -m repopackage --help 2>&1

# 3. ¿python -m repopackage y rp producen mismo output?
python -m repopackage --help > /tmp/python-help.txt 2>&1
diff /tmp/rp-help.txt /tmp/python-help.txt || echo "DIFFERENT"

# 4. rp --help vs rp (sin args)
rp --help 2>&1 | head -5
echo "---"
rp 2>&1 | head -5

# 5. ¿Hay rp --version?
rp --version 2>&1 || echo "No --version flag"

# 6. ¿Hay repopackage --version?
repopackage --version 2>&1 || echo "No --version flag"

# 7. ¿Python API entry point funciona?
python3 -c "from repopackage.cli.main import main; print('CLI main importable')"
python3 -c "from repopackage.core.models import Project, Lockfile; print('Models importable')"
python3 -c "from repopackage.core.solver import CompositionSolver; print('Solver importable')"
python3 -c "from repopackage.git.client import GitClient; print('GitClient importable')"
python3 -c "from repopackage.repo.manifest import ManifestBuilder; print('ManifestBuilder importable')"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿rp y repopackage son idénticos? |
| 2 | ¿python -m funciona? |
| 3 | ¿Mismo output que entry point CLI? |
| 4 | ¿Sin args muestra help o error? |
| 5 | ¿Hay --version? |
| 6 | ¿Consistente con rp? |
| 7 | ¿Import paths son intuitivos? |

## Modos de fracaso

- `rp` y `repopackage` difieren en output o comportamiento
- `python -m repopackage` no funciona
- Sin `--version` flag
- Import paths no intuitivos (ej: `repopackage.cli.main` en vez de `repopackage`)
