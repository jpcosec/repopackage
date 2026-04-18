"""Standardize CLI command."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from workflow_pkg.cli_pkg.command_types import CommandBase


class StandardizeCreateCommand(CommandBase):
    """Create a new standardized or normed module."""

    def _configure_create(self, parser: argparse.ArgumentParser) -> None:
        """Configure the create subcommand."""

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--standardized", action="store_true", help="Create a reusable system module.")
        group.add_argument("--normed", action="store_true", help="Create a domain-specific module.")

        parser.add_argument("--name", required=True, help="Unique name for the module.")
        parser.add_argument("--domain", required=True, help="Problem domain (e.g., cli, io, domain).")
        parser.add_argument("--language", default="python", help="Primary implementation language.")
        parser.add_argument("--template", help="Path to a boilerplate template.")
        parser.add_argument("--rules", help="Path to a business rules file.")


    def run(self, args: argparse.Namespace) -> int:
        """Run the command."""

        kind = "standardized" if args.standardized else "normed"
        target_dir = Path.cwd() / "modules" / kind / args.name
        target_dir.mkdir(parents=True, exist_ok=True)

        data = self._build_data(args, kind)
        self._write_module(target_dir / "module.yaml", data)

        print(f"Created {kind} module: {args.name} at {target_dir}")
        return 0

    def _build_data(self, args: argparse.Namespace, kind: str) -> dict:
        """Build module.yaml data."""

        data = {
            "name": args.name, "kind": kind,
            "domain": args.domain, "language": args.language,
        }
        if args.template: data["template"] = args.template
        if args.rules: data["rules"] = args.rules
        return data

    def _write_module(self, path: Path, data: dict) -> None:
        """Write module.yaml file."""

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False)
