#!/usr/bin/env bash
# Activate the project's local Python virtual environment.
# Usage: source activate.sh

VENV_DIR=".venv"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"

if [ ! -f "$ACTIVATE_SCRIPT" ]; then
  echo "Error: virtual environment activate script not found at $ACTIVATE_SCRIPT"
  echo "Run python3 -m venv .venv first, or verify the .venv directory exists."
  return 1 2>/dev/null || exit 1
fi

# shellcheck disable=SC1091
source "$ACTIVATE_SCRIPT"
