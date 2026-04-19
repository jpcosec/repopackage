# Recomendaciones y Heurística: Supervisor

## Sobre las Píldoras "Current"
- **Evita la redundancia:** Si el código es claro, no escribas qué hace.
- **Usa 'Current' solo para 'Trampas':** Si hay un comportamiento extraño que parece un bug pero es intencional, documéntalo como píldora `current` para que el Executor no intente "arreglarlo" por error.

## Sobre el Paralelismo
- Al indexar, busca tareas que toquen archivos o módulos diferentes. Estas son las mejores candidatas para ejecución paralela.
- Si dos tareas tocan el mismo archivo pequeño (atomizado), ponlas en secuencia para evitar conflictos de git.

## Sobre la Limpieza del "Desk"
- No esperes al final del proyecto para limpiar. Limpia el `desk/tasks/` al final de cada fase.
- Antes de borrar una píldora de contexto, pregúntate: "¿Este razonamiento es útil para el futuro?". Si la respuesta es sí, muévelo a `docs/` o a un `README.md` del módulo antes de eliminarlo del `desk/`.

## Sobre la Deuda Técnica
- El Supervisor es el guardián de la calidad. Si un Executor propone una solución "sucia" (hack) para cumplir la tarea, recházala aunque pase los tests. La atomización es sagrada.
