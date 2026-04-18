# Turn 033 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

El motor de resolución (Solver) opera como un analizador estático de grafos dirigidos. Su responsabilidad es recorrer el árbol de dependencias, detectar dependencias circulares (ciclos) y asegurar que las promesas de los contratos (exports) satisfagan las necesidades (consumes) sin conflictos de versión.

Aquí tienes la implementación del núcleo algorítmico en Python.

1. Estructuras Base y Dependencias
Python
from typing import Dict, List, Set
from dataclasses import dataclass
import semantic_version # Para cruce de versiones (ej: ">=1.0.0" vs "<2.0.0")

@dataclass
class ResolvedNode:
    name: str
    repo_url: str
    branch: str
    commit_hash: str
    contract: dict
    version_constraints: List[str] # Acumula todas las exigencias hacia este paquete
2. El Algoritmo del Solver
El algoritmo utiliza Búsqueda en Profundidad (DFS) para expandir el grafo y unificar dependencias transitivas.

Python
class CompositionSolver:
    def __init__(self, git_adapter):
        self.git = git_adapter
        self.resolved_graph: Dict[str, ResolvedNode] = {}
        self.visiting_path: Set[str] = set() # Marcadores para detección de ciclos

    def resolve(self, compose_manifest: dict) -> dict:
        """Punto de entrada: orquesta la resolución del project model."""

        # 1. Fase de Expansión (DFS)
        for pkg_name, config in compose_manifest.get("uses", {}).items():
            self._expand_node(
                pkg_name=pkg_name,
                url=config["url"],
                branch=config.get("branch", config.get("fallback", "main")),
                constraint=config.get("version", "*")
            )

        # 2. Fase de Unificación y Validación
        self._validate_contracts()

        # 3. Generación del Lockfile
        return self._generate_lockfile()

    def _expand_node(self, pkg_name: str, url: str, branch: str, constraint: str):
        """Expande transitivamente un repopackage y previene ciclos."""

        # Detección estricta de ciclos (DFS Back-edge)
        if pkg_name in self.visiting_path:
            raise Exception(f"FAILED_CYCLE: Dependencia circular detectada {self.visiting_path} -> {pkg_name}")

        # Unificación temprana: Si el nodo ya existe, solo añadimos la nueva restricción de versión
        if pkg_name in self.resolved_graph:
            self.resolved_graph[pkg_name].version_constraints.append(constraint)
            return

        self.visiting_path.add(pkg_name)

        # Interacción I/O: Lectura remota/local sin hacer checkout físico
        commit_hash = self.git.get_commit_hash(url, branch)
        contract_raw = self.git.read_file(url, commit_hash, "contracts/integration.contract.yaml")
        contract = parse_yaml(contract_raw)

        # Registrar el nodo resuelto
        self.resolved_graph[pkg_name] = ResolvedNode(
            name=pkg_name,
            repo_url=url,
            branch=branch,
            commit_hash=commit_hash,
            contract=contract,
            version_constraints=[constraint]
        )

        # Expansión recursiva: Leer qué exige este paquete (transitividad)
        transitive_deps = contract.get("compatibility", {}).get("requires", {})
        for sub_pkg, sub_constraint in transitive_deps.items():
             # Asumimos que la URL viene de un registro o convención de la org
            sub_url = f"git@github.com:org/{sub_pkg}.git"
            self._expand_node(sub_pkg, sub_url, branch="main", constraint=sub_constraint)

        self.visiting_path.remove(pkg_name)
3. Validación Matemática de Contratos
Una vez construido el grafo en memoria, debemos cruzar matemáticamente las exigencias de versiones e interfaces.

Python
    def _validate_contracts(self):
        """Cruza los 'consumes' contra los 'exports' de todo el ecosistema."""

        # 1. Validar que las versiones convergen (No hay conflictos tipo Dependency Hell)
        for pkg_name, node in self.resolved_graph.items():
            try:
                # Cruza todas las exigencias (ej: [">=1.0", "<3.0", "==2.5.0"])
                final_spec = semantic_version.SimpleSpec(*node.version_constraints)
                node_version = semantic_version.Version(node.contract["version"])

                if node_version not in final_spec:
                    raise Exception(f"FAILED_VERSION_MISMATCH: {pkg_name}@{node_version} no cumple {node.version_constraints}")
            except ValueError:
                raise Exception(f"FAILED_UNRESOLVABLE_VERSION: Conflictos insalvables para {pkg_name}: {node.version_constraints}")

        # 2. Validar Interfaces (IO Mapeo)
        for pkg_name, node in self.resolved_graph.items():
            consumes_list = node.contract.get("consumes", [])

            for requirement in consumes_list:
                interface_name = requirement["name"]
                provider_found = False

                # Buscar qué paquete del grafo expone esta interfaz
                for provider_name, provider_node in self.resolved_graph.items():
                    exports_list = provider_node.contract.get("exports", [])
                    if any(exp["name"] == interface_name for exp in exports_list):
                        provider_found = True
                        break # Encontramos un proveedor válido en el grafo

                if not provider_found:
                     raise Exception(f"FAILED_CONTRACT_MISMATCH: {pkg_name} requiere '{interface_name}', pero ningún paquete en el ecosistema lo exporta.")
Resolución Topológica vs Materialización: Nota cómo este código no clona repositorios físicamente ni ejecuta Google repo. Se apoya exclusivamente en el GitAdapter para leer hashes y YAMLs al vuelo. Esto permite fallar rápido (en milisegundos) antes de descargar gigabytes de código a disco.

 Para refinar la arquitectura del solver:

 ¿Qué pasa si dos paquetes requieren versiones incompatibles?

 Ver la implementación del GitAdapter
