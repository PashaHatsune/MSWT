#!/bin/bash

CURRENT_DIR="$(pwd)"

VENV_DIR="$CURRENT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
  source "$VENV_DIR/bin/activate"
else
  echo "Virtual environment .venv not found in $CURRENT_DIR"
fi

cd "$CURRENT_DIR" || exit 1
uv run bot.py
sh start-server.sh