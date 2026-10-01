# UC-06: Sync workspace

El usuario resolvió las dependencias y quiere materializar el workspace: clonar los repos, checkout en los commits correctos, y preparar el entorno de desarrollo.

## Pasos

1. Ejecutar `rp sync` sobre un proyecto resuelto (con lockfile presente)
2. Verificar que los repos se clonaron en los paths correctos
3. Verificar que los commits son los correctos

## Preguntas de estrés

- ¿`rp sync` muestra progreso (clonando repo X)?
- ¿Qué pasa si un repo ya está clonado? (¿git pull? ¿checkout? ¿error?)
- ¿Qué pasa si no hay lockfile? (debería fallar con mensaje claro)
- ¿Qué pasa si hay un conflicto de git (dirty workspace)?
- ¿Qué pasa si un repo tiene submodules?
- ¿El sync requiere que Google Repo tool esté instalado? ¿O usa pygit2 internamente?
- ¿Hay flag `--force`?
