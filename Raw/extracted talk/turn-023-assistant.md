# Turn 023 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

1. Capa de Integración ("Tentáculos" VCS)
Se implementa mediante el patrón Adapter para aislar la lógica del sistema operativo y de los binarios.

GitAdapter (Interacción Git):

Implementación: Llamadas a subprocess o uso de pygit2 (bindings de libgit2).

Operaciones requeridas:

get_commit_hash(repo_path, branch) -> str

get_base_commit(repo_path, branch1, branch2) -> str

read_file_from_tree(repo_path, commit_hash, file_path) -> str (Crucial para leer contratos sin hacer checkout físico).

RepoAdapter (Interacción Google Repo):

Implementación: Lector/Escritor XML (xml.etree.ElementTree o lxml) para el manifiesto + subprocess para ejecución.

Operaciones requeridas:

generate_manifest(composition_plan) -> manifest.xml

execute_sync(manifest_path)

inspect_workspace() -> dict[repo_name, commit_hash]

2. Validadores de Grafo (Validación Estática)
Un conjunto de funciones puras que operan sobre el estado en memoria una vez que los archivos YAML han sido parseados.

TopologyValidator (Detección de Ciclos):

Algoritmo: Búsqueda en Profundidad (DFS) con marcado de nodos (blanco = no visitado, gris = visitando, negro = visitado).

Regla: Si al explorar las aristas (uses) se encuentra un nodo gris, hay un ciclo. Retorna FAILED_CYCLE.

ContractMatcher (Resolución de Tipos y Versiones):

Implementación: Usa librerías de parseo SemVer (ej. semantic_version en Python).

Lógica:

Itera sobre la lista de consumes de cada nodo.

Busca en los nodos dependientes un exports con el mismo name.

Interseca los rangos de versiones exigidos (ej. >=1.0.0 ∩ <2.0.0). Si la intersección es vacía, falla.

SchemaValidator (Integridad de Datos):

Implementación: Librería estándar de validación JSON Schema (jsonschema).

Lógica: Verifica que los .schema.json declarados en los exports sean esquemas válidos y que los tipos referenciados coincidan estructuralmente si se requiere compatibilidad estricta.

3. Solver (Motor de Resolución)
El componente central. Funciona como un resolutor de restricciones (Constraint Satisfaction Problem).

Estrategia base: Resolución topológica descendente (Top-down) combinada con Backtracking para ramas contextuales.

Estructura de Datos: Grafo Dirigido Acíclico (DAG) instanciado en memoria.

Flujo del Algoritmo:

Inicialización: Lee compose.yaml (nodo raíz).

Expansión (BFS/DFS): Para cada dependencia en uses:

Pide el Integration Contract usando el GitAdapter para leer el YAML directamente del árbol remoto/local de la rama especificada (contextual branch si existe, sino central line).

Registra las dependencias transitivas.

Unificación: Si dos paquetes en el grafo requieren el paquete C:

Se calcula la intersección de las restricciones de versión.

Se verifica si el proyecto raíz forzó una rama contextual para C. Las reglas de composición del proyecto raíz sobreescriben las exigencias transitivas (inyección de dependencias).

Emisión: Construye el estado final y genera el árbol de datos para compose.lock.yaml.

 ¿Quieres ver el pseudocódigo Python del algoritmo del Solver?
