# Instrucciones de Protocolo: Supervisor

## Manual de Operaciones (Paso a Paso)

### Paso 1: Saneamiento (Atomización Previa)
1. **Analizar:** Leer los archivos afectados por la nueva feature.
2. **Evaluar:** ¿Algún archivo supera las 80 líneas? ¿Alguna función supera las 10 líneas?
3. **Ejecutar:** Si la respuesta es SÍ, crear tareas de refactorización pura ANTES de tocar la feature.
4. **Validar:** El código base debe estar "limpio" y atomizado antes de expandirlo.

### Paso 2: Especificación (Atomización de Feature)
1. **Diseñar:** Trocear la feature en las unidades mínimas de implementación posibles.
2. **Documentar:** Crear un archivo `.md` en `desk/tasks/` para cada unidad usando el template oficial.
3. **Contextualizar:** Crear Píldoras de Contexto (`target`) en `desk/pills/` para explicar patrones o decisiones de diseño.
4. **Vincular:** Asegurar que cada tarea tenga sus dependencias (`Depends On`) correctamente seteadas.

### Paso 3: Indexación y Orquestación
1. **Mapear:** Generar el grafo de dependencias de las tareas.
2. **Fasear:** Identificar qué tareas no tienen dependencias pendientes. Esas forman la **Fase Actual**.
3. **Publicar:** Actualizar `desk/tasks/Board.md` moviendo las tareas de la Fase Actual a `Active`.

### Paso 4: Despacho y Validación (Bucle de Ejecución)
1. **Asignar:** Entregar una tarea `Active` y sus píldoras a un Executor.
2. **Auditar:** Al recibir la tarea terminada, verificar:
   - **Commit único:** Un solo commit con el formato correcto.
   - **Induced Changes:** Que el Executor haya listado los símbolos y archivos modificados en el `.md`.
   - **Unit Tests:** Que los tests unitarios pasen y cubran el cambio.
3. **Cerrar:** Marcar la tarea como `closed` y moverla fuera de la sección activa.

### Paso 5: Cierre de Fase (Ritual E2E)
1. **Actualizar E2E:** Revisar los tests de integración/E2E. Eliminar los que el nuevo diseño dejó obsoletos.
2. **Validar Fase:** Correr la suite E2E completa.
3. **Limpiar:** Eliminar los archivos `.md` de las tareas cerradas de `desk/tasks/`.

### Paso 6: Cierre de Feature (Limpieza Final)
1. **Promocionar:** Mover las Píldoras de Contexto útiles a la documentación permanente (`docs/`).
2. **Eliminar:** Borrar el diseño en `desk/design/` y las píldoras temporales.
3. **Resetear:** Dejar `Board.md` vacío y `desk/tasks/` sin archivos.
4. **Finalizar:** Hacer un commit de cierre de feature.

---

## Reglas Inmutables

1. **No hay construcción sobre barro:** Prohibido implementar sobre código no atomizado o sobre un **árbol de Git sucio**. El entorno debe estar limpio antes de cada fase.
2. **Un commit, una tarea:** Nunca aceptar un commit que mezcle dos tareas. La historia de Git DEBE mapear 1:1 con las tareas.
3. **Trazabilidad vía ID:** El commit message DEBE incluir el `#ID` de la tarea para que `git log` sea el índice de búsqueda.
4. **Suficiencia de Contexto Cero:** Si el Executor pregunta algo, el Supervisor falló al redactar la Píldora o la Tarea. Actualizar la documentación antes de responder.
