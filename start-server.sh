#!/bin/bash

PROJECT_DIR="/home/miku/dev/MSWT/"

export HOME=/home/miku
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

cd "$PROJECT_DIR" || exit 1

while true; do
    uv run bot.py
    echo "Бот упал с кодом $? - перезапускаю через 5 секунд..."
    sleep 5
done
