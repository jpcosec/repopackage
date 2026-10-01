# UC-02: Resolve dependency graph

El usuario definió su proyecto con dependencias en `compose.yaml` y quiere resolver el grafo de dependencias transitivas, generando un `compose.lock.yaml` con versiones concretas.

## Pasos

1. Ejecutar `rp resolve` sobre un compose.yaml con dependencias válidas
2. Inspeccionar el lockfile generado
3. Modificar una dependencia en compose.yaml y re-resolver

## Preguntas de estrés

- ¿El output de `resolve` muestra qué dependencias resolvió? ¿Progreso?
- ¿Qué pasa si una dependencia tiene un URL de git inaccesible?
- ¿Qué pasa si hay un ciclo de dependencias?
- ¿Qué pasa si hay version conflict?
- ¿El lockfile es human-readable? ¿Tiene metadatos (timestamp, resolved_at)?
- ¿`rp resolve` es idempotente? (mismo compose.yaml → mismo lockfile)
