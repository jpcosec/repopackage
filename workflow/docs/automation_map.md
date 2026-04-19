# Mapa de Automatización: LLM vs. CLI

Este documento separa las responsabilidades del **Juicio Creativo (LLM Exclusive)** de las **Operaciones Mecánicas (Programmable)**. El objetivo es que el CLI se encargue de todo lo que sea predecible para garantizar la integridad del sistema.

## 1. Ciclo del Supervisor

| Paso | Responsabilidad | Tipo | Acción del CLI (Propuesta) |
| :--- | :--- | :--- | :--- |
| **Saneamiento** | Detectar archivos >80 líneas o funciones >10. | **Programmable** | `rp check health` |
| **Atomización** | Decidir cómo romper una feature en tareas lógicas. | **LLM Exclusive** | - |
| **Creación de Tareas** | Generar archivos `.md` desde el template. | **Programmable** | `rp desk tasks add --title "..."` |
| **Redacción de Píldoras** | Explicar el "Por qué" y el patrón de diseño. | **LLM Exclusive** | - |
| **Indexación** | Calcular dependencias y actualizar el `Board.md`. | **Programmable** | `rp desk tasks index` |
| **Despacho** | Mover tareas a `Active` y preparar el paquete. | **Programmable** | `rp exec dispatch --task-id 01` |
| **Auditoría de Cierre** | Verificar formato de commit, tests pasados y linting. | **Programmable** | `rp eval audit --task-id 01` |
| **Calidad de Código** | Revisar que la lógica sea correcta y atomizada. | **LLM Exclusive** | - |
| **Limpieza de Fase** | Borrar tareas cerradas y actualizar E2E. | **Programmable** | `rp phase clean --id A` |
| **Promoción** | Mover píldoras útiles a `docs/`. | **Programmable** | `rp pills promote --id PILL-01` |

## 2. Ciclo del Executor

| Paso | Responsabilidad | Tipo | Acción del CLI (Propuesta) |
| :--- | :--- | :--- | :--- |
| **Preparación** | Sync de git y correr baseline de tests. | **Programmable** | `rp exec prep` |
| **Implementación** | Escribir el código y resolver el problema. | **LLM Exclusive** | - |
| **Unit Testing** | Escribir los casos de prueba. | **LLM Exclusive** | - |
| **Ejecución de Tests** | Correr la suite y capturar resultados. | **Programmable** | `rp eval test` |
| **Induced Changes** | Detectar qué archivos y símbolos cambiaron. | **Programmable** | `rp exec diff --task-id 01` |
| **Commit** | Generar el commit con el formato del template. | **Programmable** | `rp exec commit --task-id 01` |

## 3. Blueprinting (Diseño)

| Capa | Responsabilidad | Tipo | Acción del CLI (Propuesta) |
| :--- | :--- | :--- | :--- |
| **L1: Skeleton** | Crear la jerarquía de archivos vacíos. | **Programmable** | `rp design scaffold --spec-id 01` |
| **L2-L4: Content** | Escribir pseudocódigo, patrones y tests. | **LLM Exclusive** | - |
| **L4: Test Run** | Confirmar que los tests fallan (Red state). | **Programmable** | `rp eval test --expected fail` |

---

## Heurística para el Supervisor (Agente)

1. **Usa el CLI como tu brazo mecánico:** Siempre que una tarea sea "Mover", "Crear desde template", "Verificar formato" o "Listar", busca el comando del CLI.
2. **Reserva tu contexto para el diseño:** No gastes tokens formateando tablas en el `Board.md` manualmente; deja que el CLI lo regenere.
3. **Falla si el CLI falla:** Si un comando de automatización (`rp check health`) da error, no intentes "arreglarlo" manualmente en el código; reporta la fricción.

## Heurística para el Desarrollador del CLI

1. **Idempotencia:** Todos los comandos programables deben poder ejecutarse varias veces sin romper el estado.
2. **Validación de Esquema:** El CLI debe ser el "muro" que impida que un LLM escriba un `.md` que no cumpla el contrato.
3. **Integración con Git:** El CLI debe automatizar los mensajes de commit para que la trazabilidad sea perfecta por defecto.
