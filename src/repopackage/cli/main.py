"""
Command Line Interface for Repopackage.
"""
import argparse
from . import handlers

def main():
    parser = _create_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.handler()
    else:
        parser.print_help()

def _create_parser():
    p = argparse.ArgumentParser(
        prog="rp",
        description="Repopackage (rp): Recursive, Contract-Based Repository Composition.\n\n"
                    "Treats Git repositories as nodes in a typed, recursive graph, "
                    "allowing parallel evolution via explicit I/O contracts."
    )
    sub = p.add_subparsers(title="commands", dest="command")
    _add_init(sub)
    _add_resolve(sub)
    _add_sync(sub)
    _add_validate(sub)
    _add_status(sub)
    _add_generate(sub)
    _add_graph(sub)
    _add_exports(sub)
    return p

def _add_init(sub):
    cmd = sub.add_parser("init", help="Bootstrap a new compose.yaml project.")
    cmd.set_defaults(handler=handlers.handle_init, func=True)

def _add_resolve(sub):
    cmd = sub.add_parser("resolve", help="Walk the graph and generate compose.lock.yaml.")
    cmd.set_defaults(handler=handlers.handle_resolve, func=True)

def _add_sync(sub):
    cmd = sub.add_parser("sync", help="Materialize workspace via Google Repo.")
    cmd.set_defaults(handler=handlers.handle_sync, func=True)

def _add_validate(sub):
    cmd = sub.add_parser("validate", help="Verify workspace physical/structural integrity.")
    cmd.set_defaults(handler=handlers.handle_validate, func=True)

def _add_status(sub):
    cmd = sub.add_parser("status", help="Show workspace sync and compatibility status.")
    cmd.set_defaults(handler=handlers.handle_status, func=True)

def _add_generate(sub):
    cmd = sub.add_parser("generate", help="Generate language-native types from contracts.")
    cmd.set_defaults(handler=handlers.handle_generate, func=True)

def _add_graph(sub):
    cmd = sub.add_parser("graph", help="Export the dependency graph (Mermaid/PlantUML).")
    cmd.set_defaults(handler=handlers.handle_graph, func=True)

def _add_exports(sub):
    cmd = sub.add_parser("exports", help="Enumerate and expose package-visible capabilities.")
    cmd.set_defaults(handler=handlers.handle_exports, func=True)

if __name__ == "__main__":
    main()
