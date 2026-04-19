# Design Spec: [Nombre de la Feature]

## Capa 0: Recolección (Contexto de Drawers)
- **Info Extraída:** (Problemas detectados, ideas previas, hilos de conversación).
- **IDs de Referencia en Drawers:** (Ej. CLI-01, ADAPTER-02).

## Capa 1: Microspec (El Mapa)
- **Objetivo:** ¿Qué vamos a resolver exactamente?
- **Prior Art (Repackaging):** ¿Qué librerías o repos vamos a usar/imitar?
- **UML de Alto Nivel:** (Ej. Etapas del pipeline, flujo general de la feature).

## Capa 2: Esqueleto (Las Fronteras)
- **Definición de Módulos:** (Qué módulos existen y qué responsabilidad tienen).
- **Contratos (I/O):** Definición estricta de entradas y salidas.
- **Diagrama de Componentes:** Cómo se conectan estos módulos entre sí.
- **Definición de E2E (Winning Condition):** ¿Qué flujo completo debe funcionar al final de la fase? (Definir el éxito global).


## Capa 3: Pseudocode (El Cerebro)
- **Lógica de Flujo:** Pseudocódigo detallado de las funciones principales.
- **Reutilización:** Cómo se inyectan o usan los componentes ya existentes del sistema.
- **UML de Detalle:** Clases y Funciones (Firmas y responsabilidades).

## Capa 4: Patterns (El Estilo)
- **Patrones de Diseño:** (Ej. Singleton para el Config, Factory para los Módulos).
- **Reglas de Conectividad:** Cómo interactuamos con librerías externas o APIs.
- **Guardrails de Estilo:** Reglas específicas de cómo debe verse el código final.

## Capa 5: Unit Tests (La Muralla)
- **Behavioral Guard:** Casos de prueba específicos que definen el éxito.
- **Casos de Borde:** Qué pasa si el input es nulo, corrupto o gigante.

---
**Resultado Esperado:** Un entorno listo para que el Executor implemente la Capa 6 (Código Final) sin necesidad de tomar decisiones arquitectónicas.
