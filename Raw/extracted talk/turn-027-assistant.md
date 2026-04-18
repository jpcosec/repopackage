# Turn 027 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

1. Lenguaje de Implementación (Python)
Idoneidad técnica: Óptima para herramientas de orquestación, manipulación de archivos y CLI. El cuello de botella del sistema será I/O (red, disco, operaciones Git), no la capacidad de cómputo del procesador.

Librerías estructurales requeridas:

pygit2: Interfaz nativa en C para libgit2. Permite operaciones de bajo nivel como lectura de archivos de contrato directamente desde árboles de Git remotos o locales, sin requerir un checkout físico.

networkx: Implementación matemática de grafos. Provee algoritmos nativos para resolución topológica (Topological Sort) y detección de ciclos (DAG constraints).

jsonschema: Motor de validación estricta para asegurar que los contratos coincidan en tipos y estructuras.

ruamel.yaml: Lector/escritor YAML que preserva comentarios y orden estructural (necesario para modificar el compose.yaml sin destruir la legibilidad humana).

typer o click: Para la interfaz de línea de comandos.

2. Gestión de Ecosistemas Multi-lenguaje
Agnosticismo del Orquestador: El sistema diseñado opera exclusivamente en el Plano de Control. Evalúa la topología (Git) y las reglas de integración (YAML). Desconoce e ignora el código fuente subyacente.

Aislamiento Operativo (Local Traits): Los comandos específicos de cada lenguaje quedan encapsulados dentro de los repopackages. El orquestador ejecuta estos comandos a ciegas vía subprocess.

YAML
# ui-kit/contracts/local.traits.yaml (TypeScript)
test_runner: "npm run test"
build_cmd: "npm run build"
YAML
# auditor/contracts/local.traits.yaml (Python)
test_runner: "pytest"
build_cmd: "poetry build"
Interoperabilidad Tipada (Integration Contract): La compatibilidad entre lenguajes se garantiza mediante la validación matemática de JSON Schemas neutrales.

Nodo A (Go): Declara en su exports que emite un payload tipo UserAuth.v2 apuntando a su esquema local user_auth_v2.schema.json.

Nodo B (TypeScript): Declara en su consumes que requiere UserAuth.v2 apuntando a su propia copia del esquema local.

Validación: El orquestador compara criptográficamente y estructuralmente ambos archivos .schema.json para dar el estado de RESOLVED, sin compilar Go ni transpilar TypeScript.

Ejecución Unificada: Cuando se lanza compose test a nivel proyecto, el orquestador itera sobre el Composition Index resuelto, ingresa al subdirectorio materializado de cada paquete dependiente y dispara el string contenido en test_runner.

 ¿Quieres ver el diseño del módulo CLI y resolver en Python?
