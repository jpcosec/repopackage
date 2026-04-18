"""Module entrypoint for python -m workflow_pkg."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
