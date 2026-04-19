# Design Spec: Repopackage CLI (rp)

## Capa 0: Recolección (Contexto de Drawers)
- **Info Extraída:** Necesidad de unificar la destilación de charlas, la gestión de la mesa de trabajo (desk) y la ejecución de agentes bajo una interfaz jerárquica.
- **IDs de Referencia:** CLI-01 a CLI-07 (Unified CLI), TOOL-01 a TOOL-08 (Enhancement Tools).
- **Fricción Identificada:** Los comandos planos no escalan; se requiere una estructura `rp <category> <subject> <action>`.

## Capa 1: Microspec (El Mapa)
- **Objetivo:** Crear una interfaz de línea de comandos que automatice la burocracia del workflow.
- **Visual:** [UML: Fases de Implementación](./cli_implementation_phases.puml)
- **Prior Art (Repackaging):**
    - `Typer`, `Pydantic`, `Rich`, `talk_extractor` (Legacy).

## Capa 2: Esqueleto (Las Fronteras)
- **Visual:** [UML: Arquitectura de Componentes](./cli_components_architecture.puml)
- **Módulos:**
    - `cli.core`, `cli.system`, `cli.desk`, `cli.drawers`, `cli.exec`, `cli.eval`.

- **Contratos (I/O):**
    - Entrada: Argumentos de CLI y archivos Markdown de tareas/píldoras.
    - Salida: Estructura de carpetas, archivos Markdown actualizados, JSON de evidencias.
- **Definición de E2E (Winning Condition):** 
    - "Un usuario puede inicializar un proyecto, añadir una spec a drawers, promocionarla a task, asignarle una píldora y sincronizar el board sin editar un archivo manualmente".

## Capa 3: Pseudocode (El Cerebro)
- **Visual:** [UML: Diagrama de Clases Detallado](./cli_class_diagram.puml)

### Lógica: Task Atomizer (rp desk tasks atomize)
```python
1. LEER task_file (desk/tasks/T-XXX.md)
2. EXTRAER section "Explanation" y checklist
3. PARA CADA item en checklist:
    a. GENERAR pill_id secuencial (PILL-XXX)
    b. RELLENAR template (workflow/docs/template/context_pills.md)
    c. ESCRIBIR en desk/pills/PILL-XXX.md
4. ACTUALIZAR task_file con la lista de Pills vinculadas
5. EJECUTAR 'rp desk board sync'
```

### Lógica: Board Synchronizer (rp desk board sync)
```python
1. ESCANEAR desk/tasks/*.md
2. PARA CADA archivo:
    a. PARSEAR frontmatter y metadatos (ID, Status, Priority, Deps)
    b. CLASIFICAR por estado (Active, Completed, Blocked)
3. GENERAR tabla Markdown con el estado actual
4. SOBREESCRIBIR desk/tasks/Board.md con la nueva tabla
```

### Lógica: Git Commit Automator (rp exec commit)
```python
1. VALIDAR que el árbol esté limpio (excepto los Induced Changes)
2. LEER metadatos de la tarea activa
3. CONSTRUIR mensaje usando template: "<type>(<scope>): #<ID> <desc>"
4. EJECUTAR git commit -m "..."
5. CAPTURAR SHA y actualizar el archivo .md de la tarea
```

## Capa 4: Patterns (El Estilo)
- **Patrón Command:** Cada acción del CLI debe encapsularse en una clase que herede de `CommandBase`. Esto permite testear la lógica de cada comando de forma aislada.
- **Patrón Adapter (Markdown):** La interacción con archivos `.md` no debe ser directa. Se usará un adaptador que traduzca el contenido Markdown a objetos Pydantic y viceversa, protegiendo el formato del archivo.
- **Reglas de Conectividad:**
    - `Typer`: Se usará exclusivamente para el routing y la interfaz de usuario.
    - `Pydantic`: Se usará para validar la integridad de cada tarea/píldora al ser cargada en memoria.
- **Guardrails de Estilo:**
    - Los comandos deben ser idempotentes (ejecutar `board sync` dos veces no debe cambiar nada).
    - Los errores deben ser "limpios" (usar `Rich` para mostrar el error y una sugerencia de solución, no un stacktrace crudo).

## Capa 5: Unit Tests (La Muralla)
- **Behavioral Guard:**
    - [ ] El comando `init-project` crea exactamente las 4 zonas y archivos base.
    - [ ] El `TaskParser` puede leer una tarea con y sin dependencias.
    - [ ] El `BoardWriter` detecta correctamente tareas duplicadas por ID.
    - [ ] El `GitEngine` falla si se intenta commitear una tarea sin tests asociados.
- **Casos de Borde:**
    - Archivo de tarea vacío o con formato corrupto.
    - Dependencias circulares entre tareas (debe lanzar error controlado).
