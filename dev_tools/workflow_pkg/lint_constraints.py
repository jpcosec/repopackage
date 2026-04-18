"""Lint structural constraints for workflow_pkg."""

from __future__ import annotations

from workflow_pkg.lint_checks import lint_file
from workflow_pkg.lint_io import print_violations, python_files


def main() -> int:
    """Run the constraint linter."""

    items = [issue for path in python_files() for issue in lint_file(path)]
    print_violations(items)
    print(f"Violations: {len(items)}")
    return 1 if items else 0


if __name__ == "__main__":
    raise SystemExit(main())
