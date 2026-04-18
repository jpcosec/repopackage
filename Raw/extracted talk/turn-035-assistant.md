# Turn 035 - assistant

- Source: `Talk.md`
- Speaker: `assistant`

Implementación corregida utilizando networkx para delegar la teoría de grafos (detección de ciclos y ordenamiento topológico) a la librería especializada.

Python
import networkx as nx
import semantic_version

class CompositionSolver:
    def __init__(self, git_adapter):
        self.git = git_adapter
        # Instanciación del Grafo Dirigido
        self.graph = nx.DiGraph()

    def resolve(self, compose_manifest: dict) -> dict:
        # 1. Nodo raíz (el proyecto mismo)
        project_name = compose_manifest["name"]
        self.graph.add_node(project_name, type="project")

        # 2. Construcción recursiva del grafo
        self._build_graph(project_name, compose_manifest.get("uses", {}))

        # 3. Detección matemática de ciclos (NetworkX nativo)
        try:
            ciclos = list(nx.find_cycle(self.graph, orientation="original"))
            raise Exception(f"FAILED_CYCLE: Dependencia circular detectada: {ciclos}")
        except nx.NetworkXNoCycle:
            pass # El ecosistema es un DAG (Directed Acyclic Graph) válido

        # 4. Validación de contratos cruzados (Top-down)
        self._validate_contracts()

        # 5. Generación de Lockfile
        return self._generate_lockfile()

    def _build_graph(self, parent_name: str, dependencies: dict):
        for pkg_name, config in dependencies.items():

            # Si el nodo no existe, se inicializa y se expande
            if not self.graph.has_node(pkg_name):
                url = config["url"]
                branch = config.get("branch", config.get("fallback", "main"))

                # I/O a través del Adapter
                commit = self.git.get_commit_hash(url, branch)
                contract_raw = self.git.read_file(url, commit, "contracts/integration.contract.yaml")
                contract = parse_yaml(contract_raw)

                # Registro del nodo
                self.graph.add_node(
                    pkg_name,
                    type="repopackage",
                    url=url,
                    branch=branch,
                    commit=commit,
                    contract=contract,
                    version_constraints=[config.get("version", "*")]
                )

                # Expansión transitiva recursiva
                transitive_deps = contract.get("compatibility", {}).get("requires", {})
                if transitive_deps:
                    mocked_uses = {
                        k: {"url": f"git@github.com:org/{k}.git", "version": v}
                        for k, v in transitive_deps.items()
                    }
                    self._build_graph(pkg_name, mocked_uses)
            else:
                # Si el nodo ya existe, solo añadimos la nueva restricción al pool
                self.graph.nodes[pkg_name]["version_constraints"].append(config.get("version", "*"))

            # Creación de la arista (Edge): Quien requiere -> Quien provee
            self.graph.add_edge(parent_name, pkg_name, constraint=config.get("version", "*"))

    def _validate_contracts(self):
        # Iterar sobre el grafo usando ordenamiento topológico (de las hojas a la raíz)
        # Garantiza que validamos los proveedores antes que los consumidores
        ordered_nodes = list(nx.topological_sort(self.graph))
        ordered_nodes.reverse()

        for node_name in ordered_nodes:
            node_data = self.graph.nodes[node_name]
            if node_data["type"] == "project":
                continue

            # Unificación de Versiones
            try:
                final_spec = semantic_version.SimpleSpec(*node_data["version_constraints"])
                node_version = semantic_version.Version(node_data["contract"]["version"])
                if node_version not in final_spec:
                    raise Exception(f"FAILED_VERSION_MISMATCH: {node_name}")
            except ValueError:
                raise Exception(f"FAILED_UNRESOLVABLE_VERSION: {node_name} -> {node_data['version_constraints']}")

            # Validación de Interfaces vía predecesores (NetworkX nativo)
            consumes = node_data["contract"].get("consumes", [])
            for req in consumes:
                interface_name = req["name"]
                provider_found = False

                # nx.descendants retorna todos los nodos alcanzables desde node_name
                # Buscamos quién expone la interfaz requerida en el subgrafo dependiente
                for dep in nx.descendants(self.graph, node_name):
                    dep_contract = self.graph.nodes[dep]["contract"]
                    if any(exp["name"] == interface_name for exp in dep_contract.get("exports", [])):
                        provider_found = True
                        break

                if not provider_found:
                    raise Exception(f"FAILED_CONTRACT_MISMATCH: {node_name} requiere '{interface_name}'")
nx.DiGraph(): Sustituye la gestión manual de diccionarios para el mapeo de la topología.

nx.find_cycle(): Reemplaza la lógica de marcadores de paso (blanco/gris/negro) delegándola al algoritmo en C de networkx. Retorna la ruta exacta del ciclo para debugeo.

nx.topological_sort(): Asegura que el cruce matemático de las versiones y contratos ocurra en el orden algorítmico correcto (resolviendo dependencias profundas antes que las superficiales).

nx.descendants(): Facilita la validación de interfaces buscando a través de los nodos hijos en tiempo de complejidad O(V+E).
