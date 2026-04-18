# Turn 031 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Un pipeline CI/CD no es un Project. Es el entorno de ejecución que consume e interpreta el Composition Index (compose.lock.yaml).

El mapeo arquitectónico se divide en tres enfoques según el objetivo:

1. El Pipeline como ejecutor del Grafo
Las etapas clásicas de un pipeline se delegan a la capa de orquestación iterando sobre los nodos del proyecto.

Etapa de Materialización: Ejecuta compose resolve y compose sync. Fija el estado físico de los repositorios.

Etapa de Validación Estática: Ejecuta compose validate. Evalúa algorítmicamente que los exports y consumes del grafo cumplan con los JSON Schemas estipulados.

Etapa de Pruebas Distribuidas: Ejecuta compose test. El orquestador lee los Local Traits de cada paquete resuelto en el índice y dispara sus respectivos test_runner (independiente del lenguaje de cada nodo).

2. Prueba aislada de etapas (Focus Worktree)
Si el objetivo es probar una etapa o un paquete sin levantar los repositorios conexos.

Se instancia un Focus Worktree definiendo el paquete objetivo.

El compose.yaml inyecta dependencias falsas (mocks o stubs de red) que emulan los exports de otros repopackages.

Permite ejecutar análisis estático, linter o compilación de una sola unidad garantizando que sus contratos de salida siguen siendo válidos.

3. El código del Pipeline como Repopackages
Si desarrollas librerías modulares de CI/CD (ej. Custom GitHub Actions, módulos de Terraform, Jenkins Shared Libraries, imágenes de Docker de despliegue), estas sí se modelan como repopackages.

Nodos de Infraestructura: El código del pipeline posee su propio repositorio, Central Line e historia Git.

Contrato de Integración: Su YAML expone los requerimientos de la infraestructura. Ej: consumes: DockerImage.v2, consumes: KubeConfigSecret.

Composición: El Project principal agrega el pipeline a su Composition Index como una dependencia más.

Divergencia (Customización): Si un proyecto requiere una variante temporal del pipeline, bifurca una Development Line del repositorio de infraestructura y la ancla en su archivo compose.yaml local.
