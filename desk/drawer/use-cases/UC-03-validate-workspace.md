# UC-03: Validate workspace integrity

El usuario tiene un workspace materializado y quiere verificar que todo está en orden: que los commits coinciden con el lockfile, que los contracts están presentes, y que la estructura física es correcta.

## Pasos

1. Ejecutar `rp validate` sobre un workspace sincronizado
2. Modificar intencionalmente un archivo en el workspace y re-validar
3. Ejecutar `rp validate` sobre un directorio sin lockfile

## Preguntas de estrés

- ¿El output de validate es detallado? ¿Lista qué verificó?
- ¿Los errores de validación son accionables? (¿sugieren cómo arreglarlos?)
- ¿Qué pasa si un commit no coincide? ¿El error incluye commit esperado vs actual?
- ¿Qué pasa si falta un contrato declarado?
- ¿Exit code es 0 solo si todo está bien?
- ¿Hay flag `--fix` o solo reporta?
