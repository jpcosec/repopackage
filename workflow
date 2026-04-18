#!/bin/bash
# Durable entry point for the Workflow CLI

# Get the absolute path of the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set PYTHONPATH to include dev_tools
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/dev_tools"

# Proxy all arguments to the workflow_pkg module
python3 -m workflow_pkg "$@"
