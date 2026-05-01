"""
Recursive Graph Solver for repository composition.
"""
import networkx as nx
import semantic_version
from typing import Dict, Any
from ruamel.yaml import YAML
from datetime import datetime
from .models import IntegrationContract, DependencySpec
from . import constants

class CompositionSolver:
    def __init__(self, git_adapter):
        self.git = git_adapter
        self.graph = nx.DiGraph()
        self.yaml = YAML(typ="safe")

    def resolve(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Resolves graph and returns lockfile data."""
        root = config["name"]
        self.graph.add_node(root, type="project", constraints=[], contract=None)
        self._build_graph(root, config.get("uses", {}))
        self._check_cycles()
        self._validate_all()
        return self._generate_lockfile(root)

    def _build_graph(self, parent: str, deps: Dict[str, Any]):
        for name, spec_data in deps.items():
            # If it's already a model, use it; otherwise coerce
            if isinstance(spec_data, dict):
                spec = DependencySpec(**spec_data)
            else:
                spec = spec_data
                
            url = spec.url
            if not url:
                # We can no longer fabricate URLs if they are missing
                raise ValueError(f"Missing URL for dependency '{name}' required by '{parent}'")
                
            branch = spec.branch or "master"
            self._add_or_update_node(parent, name, url, branch, spec)

    def _add_or_update_node(self, parent, name, url, branch, spec: DependencySpec | Dict[str, Any]):
        if isinstance(spec, dict):
            spec = DependencySpec(**spec)
            
        if not self.graph.has_node(name):
            commit = self.git.get_commit_hash(url, branch)
            contract = self._load_contract(url, commit, name)
            self.graph.add_node(name, type="pkg", url=url, branch=branch,
                                commit=commit, contract=contract,
                                constraints=[spec.version])
            self._expand_transitive(name, contract)
        else:
            self.graph.nodes[name]["constraints"].append(spec.version)
        self.graph.add_edge(parent, name)

    def _load_contract(self, url, commit, name):
        """Loads and validates the integration contract. Hard error if missing or invalid."""
        try:
            raw = self.git.read_file(url, commit, constants.CONTRACT_PATH)
            data = self.yaml.load(raw)
            return IntegrationContract(**data)
        except FileNotFoundError:
            raise RuntimeError(f"Contract {constants.CONTRACT_PATH} not found in {name} ({url} at {commit})")
        except Exception as e:
            raise RuntimeError(f"Failed to load/parse contract for {name}: {e}")

    def _expand_transitive(self, name, contract: IntegrationContract):
        reqs = contract.compatibility.get("requires", {})
        if reqs:
            # reqs is already Dict[str, DependencySpec] due to Pydantic coercion in model
            self._build_graph(name, reqs)

    def _check_cycles(self):
        try:
            c = list(nx.find_cycle(self.graph, orientation="original"))
            raise Exception(f"FAILED_CYCLE: {c}")
        except nx.NetworkXNoCycle: pass

    def _validate_all(self):
        nodes = list(nx.topological_sort(self.graph))
        for n in reversed(nodes):
            data = self.graph.nodes[n]
            if data["type"] == "pkg":
                self._check_version(n, data)
                self._check_interfaces(n, data)

    def _check_version(self, name, data):
        ver = semantic_version.Version(data["contract"].version)
        for c in data["constraints"]:
            if c != "*" and ver not in semantic_version.SimpleSpec(c):
                raise Exception(f"VERSION_MISMATCH: {name}@{ver} vs {c}")

    def _check_interfaces(self, name, data):
        for req in data["contract"].consumes:
            if not any(any(e.name == req.name for e in self.graph.nodes[d]["contract"].exports)
                       for d in nx.descendants(self.graph, name) if self.graph.nodes[d]["contract"]):
                raise Exception(f"CONTRACT_MISMATCH: {name} requires {req.name}")

    def _generate_lockfile(self, root) -> Dict[str, Any]:
        res = {"kind": "composition_index", "project": root,
               "resolved_at": datetime.utcnow().isoformat() + "Z",
               "repopackages": {}, "compatibility": {"status": "passed", "results": []}}
        for n, d in self.graph.nodes(data=True):
            if d["type"] == "pkg":
                res["repopackages"][n] = {"url": d["url"], "branch": d["branch"],
                                          "commit": d["commit"], "status": "resolved"}
                res["compatibility"]["results"].append({"package": n, "status": "passed"})
        return res
