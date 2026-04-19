# Biblioteca de Categorías (Traits) para Composición

Este catálogo permite al Supervisor definir tareas mediante la combinación de etiquetas pre-configuradas. Cada etiqueta inyecta sus propias reglas de diseño y validación.

## 1. Naturaleza de la Tarea (Action)
- `[Implementación]`: Creación de lógica nueva.
- `[Refactoring]`: Mejora de estructura sin cambiar comportamiento.
- `[Fix]`: Corrección de un bug identificado.
- `[Testing]`: Foco exclusivo en aumentar cobertura o crear E2E.
- `[Doc]`: Documentación de código o procesos.

## 2. Dominio Arquitectónico (Pattern)
- `[CLI]`: Interfaz de línea de comandos (Reglas: Typer, Argumentos jerárquicos).
- `[Pipeline]`: Flujo de datos secuencial (Reglas: Inmutabilidad, Logs de etapa).
- `[Graph/LangGraph]`: Lógica de agentes o estados (Reglas: Persistencia de estado, HITL).
- `[UI/React]`: Interfaz de usuario (Reglas: Componentes funcionales, Hooks).
- `[API/FastAPI]`: Endpoints y servicios (Reglas: Validación Pydantic).

## 3. Stack Tecnológico (Stack)
- `[Python]`: (Reglas: Type hints, PEP8, Ruff).
- `[Typescript]`: (Reglas: Interfaces estrictas, Prettier).
- `[PostgreSQL]`: (Reglas: Migraciones, SQL normalizado).

## 4. Interfaz / Contrato (Interface)
- `[Schema]`: Definición de modelos de datos.
- `[Adapter]`: Conexión con librerías externas.
- `[Event]`: Comunicación asíncrona.

## 5. Calidad y Observabilidad (Reliability)
- `[Error-Handling]`: Estrategia de excepciones y fallos (Reglas: Try/Except atómicos, Errores tipados).
- `[Logging]`: Trazabilidad y telemetría (Reglas: Niveles de log, Estructura JSON).
- `[Linting]`: Calidad y formato de código (Reglas: Ruff, MyPy, Prettier).
- `[Performance]`: Optimización de recursos (Reglas: Profiling, Complejidad algorítmica).


---
**Ejemplo de Composición:**
`Tarea 01: [Implementación] | [CLI] | [Python] | [Ref: Typer]`
*Resultado:* El Executor sabe que debe crear lógica nueva para un CLI en Python usando la librería Typer, siguiendo los estándares de cada etiqueta.
