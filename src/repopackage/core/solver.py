"""
Recursive Graph Solver for repository composition.
"""
import networkx as nx
import semantic_version
from typing import Dict, Any
from ruamel.yaml import YAML
from .models import IntegrationContract, DependencySpec
from . import constants


class SolverError(Exception):
    """Base class for solver-related errors."""
    pass


class CycleError(SolverError):
    """Raised when a dependency cycle is detected."""
    pass


class VersionMismatchError(SolverError):
    """Raised when version constraints cannot be satisfied."""
    pass


class ContractMismatchError(SolverError):
    """Raised when interface contracts are not satisfied."""
    pass


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
            spec = self._coerce_spec(spec_data, name, parent)
            self._add_or_update_node(parent, name, spec)

    def _coerce_spec(self, data: Any, name: str, parent: str) -> DependencySpec:
        if isinstance(data, dict):
            spec = DependencySpec(**data)
        else:
            spec = data
        if not spec.url:
            raise ValueError(f"Missing URL for dependency '{name}' required by '{parent}'")
        return spec

    def _add_or_update_node(self, parent, name, spec: DependencySpec):
        if not self.graph.has_node(name):
            self._create_node(name, spec)
        else:
            self.graph.nodes[name]["constraints"].append(spec.version)
        self.graph.add_edge(parent, name)

    def _create_node(self, name: str, spec: DependencySpec):
        url = spec.url
        branch = spec.branch or "master"
        commit = self.git.get_commit_hash(url, branch)
        contract = self._load_contract(url, commit, name)
        self.graph.add_node(name, type="pkg", url=url, branch=branch,
                            commit=commit, contract=contract,
                            constraints=[spec.version])
        self._expand_transitive(name, contract)

    def _load_contract(self, url, commit, name):
        """Loads and validates the integration contract."""
        try:
            path = constants.CONTRACT_PATH
            raw = self.git.read_file(url, commit, path)
            return IntegrationContract(**self.yaml.load(raw))
        except FileNotFoundError:
            raise RuntimeError(f"Contract {path} not found in {name}")
        except Exception as e:
            raise RuntimeError(f"Failed to load/parse contract for {name}: {e}")

    def _expand_transitive(self, name, contract: IntegrationContract):
        reqs = contract.compatibility.get("requires", {})
        if reqs:
            self._build_graph(name, reqs)

    def _check_cycles(self):
        try:
            cycle = list(nx.find_cycle(self.graph, orientation="original"))
            raise CycleError(f"FAILED_CYCLE: {cycle}")
        except nx.NetworkXNoCycle:
            pass

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
                raise VersionMismatchError(f"VERSION_MISMATCH: {name}@{ver} vs {c}")

    def _check_interfaces(self, name, data):
        for req in data["contract"].consumes:
            if not self._is_satisfied(name, req.name):
                raise ContractMismatchError(f"CONTRACT_MISMATCH: {name} requires {req.name}")

    def _is_satisfied(self, name, schema_name):
        descendants = nx.descendants(self.graph, name)
        for d in descendants:
            contract = self.graph.nodes[d].get("contract")
            if contract and any(e.name == schema_name for e in contract.exports):
                return True
        return False

    def _generate_lockfile(self, root) -> Dict[str, Any]:
        from .models import Lockfile
        packages = self._get_resolved_packages()
        m_hash = self._calculate_manifest_hash()
        lockfile = Lockfile(
            project=root,
            packages=packages,
            manifest_hash=m_hash,
            resolved_at=self._get_timestamp()
        )
        return self._inject_legacy_compat(lockfile.model_dump())

    def _get_resolved_packages(self) -> Dict[str, Any]:
        from .models import ResolvedPackage
        pkgs = {}
        for n, d in self.graph.nodes(data=True):
            if d["type"] == "pkg":
                pkgs[n] = ResolvedPackage(
                    name=n, url=d["url"], branch=d["branch"],
                    commit=d["commit"], compatibility_status="passed"
                )
        return pkgs

    def _calculate_manifest_hash(self) -> str:
        import hashlib
        import json
        state = {
            "nodes": sorted(list(self.graph.nodes())),
            "edges": sorted(list(self.graph.edges()))
        }
        return hashlib.sha256(json.dumps(state).encode()).hexdigest()

    def _get_timestamp(self) -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _inject_legacy_compat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pkgs = data.get("packages", {})
        data["compatibility"] = {
            "status": "passed",
            "results": [{"package": n, "status": "passed"} for n in pkgs]
        }
        return data
