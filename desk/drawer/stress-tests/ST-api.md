# ST-api: Python API — import paths, type hints, docs

**Basado en:** UC-01, UC-02

## Script

```bash
# 1. Import top-level package
python3 -c "import repopackage; print(dir(repopackage))"

# 2. Import CLI main
python3 -c "from repopackage.cli.main import main; print('CLI main:', type(main))"

# 3. Import core models — Project, Lockfile, ComposableUnit
python3 -c "
from repopackage.core.models import Project, Lockfile, ComposableUnit
print('Project fields:', list(Project.model_fields.keys()))
print('Lockfile fields:', list(Lockfile.model_fields.keys()))
print('ComposableUnit fields:', list(ComposableUnit.model_fields.keys()))
"

# 4. Create a Project instance from dict
python3 -c "
from repopackage.core.models import Project
p = Project.model_validate({'name': 'test', 'url': 'https://example.com/repo.git', 'kind': 'project'})
print('Project created:', p.name, p.kind)
"

# 5. Create a Lockfile instance
python3 -c "
from repopackage.core.models import Lockfile, ComposableUnit
unit = ComposableUnit(name='dep1', url='https://example.com/dep.git', branch='main', commit='abc123')
lock = Lockfile(project='test-project', version='1.0', packages={'dep1': unit})
print('Lockfile created:', lock.project, len(lock.packages))
"

# 6. Import and inspect solver
python3 -c "
from repopackage.core.solver import CompositionSolver
import inspect
sig = inspect.signature(CompositionSolver.__init__)
print('Solver __init__ params:', list(sig.parameters.keys()))
print('Solver methods:', [m for m in dir(CompositionSolver) if not m.startswith('_')])
"

# 7. Import and inspect git client
python3 -c "
from repopackage.git.client import GitClient
import inspect
sig = inspect.signature(GitClient.__init__)
print('GitClient __init__ params:', list(sig.parameters.keys()))
print('GitClient methods:', [m for m in dir(GitClient) if not m.startswith('_')])
"

# 8. Check type hints on key model fields
python3 -c "
from repopackage.core.models import Project, Lockfile, ComposableUnit
from pydantic import BaseModel
print('Project inherits from:', Project.__bases__)
print('Lockfile inherits from:', Lockfile.__bases__)
print('ComposableUnit inherits from:', ComposableUnit.__bases__)
"

# 9. Try invalid model data (expect validation error)
python3 -c "
from repopackage.core.models import Project
try:
    p = Project.model_validate({'name': 123})  # name should be str
    print('ERROR: should have failed')
except Exception as e:
    print(f'Validation works: {type(e).__name__}')
"

# 10. Check __init__.py exports (what does top-level import expose?)
python3 -c "
import repopackage
print('Top-level exports:', [x for x in dir(repopackage) if not x.startswith('_')])
"
```

## Puntos de estrés

| Paso | Qué observar |
|------|-------------|
| 1 | ¿El paquete tiene `__init__.py` con exports? |
| 2 | ¿CLI main es importable sin efectos secundarios? |
| 3 | ¿Los modelos tienen type hints? ¿Usan Pydantic? |
| 4 | ¿Validación de datos funciona con model_validate? |
| 5 | ¿Lockfile acepta dict de packages? |
| 6 | ¿Solver tiene API documentada? |
| 7 | ¿GitClient requiere parámetros en __init__? |
| 8 | ¿Modelos heredan de BaseModel? |
| 9 | ¿Pydantic validation errors son claros? |
| 10 | ¿Top-level __init__.py exporta algo útil? |

## Modos de fracaso

- Import paths no intuitivos (ej: `repopackage.cli.main` en vez de `repopackage`)
- Modelos sin type hints o con tipos incorrectos
- Pydantic no usado o mal configurado
- Solver/GitClient constructor con efectos secundarios (ej: conexiones al importar)
- Model validation no rechaza datos inválidos
- `__init__.py` vacío que obliga a imports profundos
