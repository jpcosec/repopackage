"""CLI entrypoint for workflow_pkg."""

from __future__ import annotations

from workflow_pkg.cli_pkg.app import CliApp


def main() -> int:
    """Run the central workflow_pkg CLI."""

    parser = CliApp().build()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
