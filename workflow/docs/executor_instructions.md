# Instrucciones de Protocolo: Executor

## Manual de Operaciones (Paso a Paso)

### Paso 1: Recepción y Entendimiento
1. **Identificar:** Tomar la tarea asignada en `desk/tasks/Board.md` (estado `Active`).
2. **Leer:** Estudiar el archivo de la tarea (`.md`) y TODAS las Píldoras de Contexto vinculadas.
3. **Validar Contexto:** ¿Es la tarea 100% clara? ¿Tienes toda la información para proceder sin preguntar?
   - **Si NO:** Detenerse y pedir al Supervisor que actualice la Píldora o la Tarea. **No adivinar.**
   - **Si SÍ:** Mover el status de la tarea a `in_progress`.

### Paso 2: Preparación del Entorno
1. **Sincronizar:** Asegurarse de estar trabajando sobre la última versión de la rama actual.
2. **Baseline:** Ejecutar los tests existentes relacionados para confirmar que el punto de partida es estable.

### Paso 3: Implementación Quirúrgica
1. **Codificar:** Aplicar los cambios exclusivamente en `src/` (o la carpeta de código correspondiente).
2. **Respetar Límites:** Mantener la regla de 80 líneas por archivo y 10 por función.
3. **Seguir el Patrón:** Si hay una píldora `target`, la implementación DEBE seguir ese patrón estrictamente.

### Paso 4: Verificación Individual (Unit Testing)
1. **Crear/Actualizar Tests:** Escribir tests unitarios que validen específicamente el cambio realizado.
2. **Ejecutar:** Correr los tests. No se permite entregar código que no pase sus propios tests unitarios.

### Paso 5: Documentación de Cambios Inducidos
1. **Mapear:** Identificar cada archivo y símbolo (clase, función, variable) que fue modificado.
2. **Registrar:** Actualizar la sección `Induced Changes` en el archivo de la tarea (`.md`).
   - Ejemplo: `Archivo: user_service.py | Símbolo: validate_email | Cambio: Añadida lógica de Regex`.

### Paso 6: Commit y Entrega
1. **Commit Único:** Crear exactamente UN commit para esta tarea.
2. **Formato:** Usar el formato estándar: `<type>(<scope>): #ID descripcion`.
3. **Finalizar:** 
   - Actualizar el campo `Commit SHA` en el archivo de la tarea.
   - Cambiar el status de la tarea a `closed` (o el estado final indicado).
   - Informar al Supervisor para la auditoría.

---

## Reglas Inmutables

1. **Foco Estricto:** Prohibido realizar refactorizaciones o cambios fuera del alcance de la tarea asignada.
2. **Prohibido el Batching:** Nunca mezclar dos tareas en un mismo commit.
3. **Honestidad en Induced Changes:** Si el commit toca un archivo, ese archivo DEBE estar listado en la tarea.
4. **Cero Inventiva:** Si el diseño parece erróneo, no lo "corrijas" en silencio. Reporta el problema al Supervisor.
