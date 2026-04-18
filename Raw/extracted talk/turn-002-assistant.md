# Turn 002 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Definición del Sistema (Qué es)
Modelo arquitectónico para la gestión distribuida y recursiva de código fuente.

Sistema de control de dependencias que trata los repositorios y ramas de Git como nodos en un grafo tipado de composición, superando las limitaciones de los gestores de paquetes tradicionales (estáticos) y los monorepos (acoplados).

Propósito (Para qué sirve)
Desacoplamiento del ciclo de vida: Permite que las herramientas y bibliotecas (repopackages) evolucionen independientemente, manteniendo su propio versionado y flujo Git.

Gestión de colisiones de contexto: Habilita el desarrollo de ramificaciones paralelas de un mismo paquete (development lines) para distintos proyectos, manteniendo la trazabilidad hacia la rama principal (central line).

Integración tipada: Valida la compatibilidad entre componentes de software usando esquemas estrictos de entrada/salida (contratos) en lugar de depender únicamente de identificadores de versión (semver).

Aislamiento de particularidades: Ignora las diferencias operativas locales (ej. herramientas de formateo o testing) al calcular la compatibilidad de integración.

Componentes y Lógicas de Arquitectura
Composable Unit: Nodo abstracto fundamental. Define un elemento con repositorio Git, historia, interfaces de entrada/salida y pruebas.

Repopackage (Rol): Nodo exportador. Contiene código genérico o reutilizable. Declarado mediante un Integration Contract (exports / consumes).

Project (Rol): Nodo ensamblador. Contiene lógica de negocio propia y declara sus reglas de orquestación mediante un Project Contract (accepts / dependencies / composition_rules).

Recursividad Composicional: Un nodo puede poseer ambos roles. Un Project que expone una API o SDK se convierte en un Repopackage para un nodo superior en el grafo.

Local Traits vs Integration Contract: Separación lógica estricta. Integration Contract dicta la viabilidad en el grafo; Local Traits dicta la ejecución interna del repositorio.

Composition Index: Estructura de datos dinámica que reemplaza al lockfile tradicional. Almacena punteros precisos: repositorios, ramas contextuales, commits específicos, linajes y versiones de contratos.

Focus Worktree: Entorno de desarrollo efímero. Aisla un repopackage inyectando dependencias falsas o versiones fijas de su entorno, garantizando validación sin montaje completo.

Flujo de Uso
Definición de Nodos: Crear repopackages y documentar sus capacidades exactas en archivos YAML de contrato.

Ensamblaje del Grafo: Crear un project y registrar los repopackages requeridos en el Composition Index.

Desarrollo Focalizado: Para modificar un paquete central, desplegar un focus worktree que simule los inputs del ecosistema real para ejecutar pruebas aisladas.

Bifurcación por Contexto: Si el project requiere una modificación exclusiva temporal, crear una development line en el repopackage en lugar de un fork duro.

Resolución de Dependencias: Antes de cualquier despliegue o fusión (merge), el Composition Graph valida estáticamente que los outputs de las dependencias coincidan algorítmicamente con los inputs requeridos por los componentes conectados.
