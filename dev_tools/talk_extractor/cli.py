"""CLI entrypoint for talk_extractor."""

from __future__ import annotations

from talk_extractor.cli_pkg.app import CliApp


def main() -> int:
    """Run the central talk_extractor CLI."""

    parser = CliApp().build()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
