# UC-01: Initialize a project composition

El usuario tiene un multi-repo ecosystem y quiere definir cómo se componen los repos.
Usa `rp init` para crear el archivo `compose.yaml` que describe el proyecto y sus dependencias.

## Pasos

1. Ejecutar `rp init` en un directorio vacío
2. Inspeccionar el `compose.yaml` generado
3. Ejecutar `rp init` nuevamente (idempotencia)
4. Ejecutar `rp init` en un directorio donde ya existe un proyecto

## Preguntas de estrés

- ¿`rp init` produce output? ¿Dice qué archivo creó?
- ¿El `compose.yaml` generado es válido? ¿Se puede leer con `rp resolve` inmediatamente?
- ¿Qué pasa si se ejecuta en un directorio sin permisos de escritura?
- ¿Hay flag `--force` o `--overwrite`?
- ¿`rp init` y `repopackage init` se comportan igual?
