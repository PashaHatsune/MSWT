#!/bin/bash

echo "=== Запуск скрипта ==="

echo "HOME: '$HOME'"
export HOME="${HOME:-/home/miku}"  # если HOME пустой — ставим по умолчанию
echo "После установки HOME: '$HOME'"

export PYENV_ROOT="$HOME/.pyenv"
echo "PYENV_ROOT: '$PYENV_ROOT'"

export PATH="$PYENV_ROOT/bin:$PATH"
echo "PATH после добавления PYENV_ROOT/bin: $PATH"

if command -v pyenv >/dev/null 2>&1; then
  echo "pyenv найден, инициализируем..."
  eval "$(pyenv init -)"
else
  echo "pyenv не найден"
fi

echo "PATH после pyenv init: $PATH"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "PROJECT_DIR: $PROJECT_DIR"

cd "$PROJECT_DIR" || { echo "Не могу перейти в $PROJECT_DIR"; exit 1; }
echo "Текущая директория после cd: $(pwd)"

while true; do
    export PYTHONPATH="$(dirname "$PROJECT_DIR")"
    echo "PYTHONPATH: $PYTHONPATH"

    echo "PATH перед активацией виртуального окружения: $PATH"
    source "$PROJECT_DIR/.venv/bin/activate"
    echo "PATH после активации виртуального окружения: $PATH"

    # Добавляем pyenv shims после активации, если еще нет
    case ":$PATH:" in
        *":$PYENV_ROOT/shims:"*) echo "pyenv shims уже в PATH";;
        *) export PATH="$PYENV_ROOT/shims:$PATH"; echo "Добавили pyenv shims в PATH";;
    esac

    echo "PATH перед запуском uv: $PATH"
    echo "Проверяем uv: $(which uv || echo 'uv не найден')"

    uv run -m MSWT

    echo "Бот упал с кодом $? - перезапускаю через 5 секунд..."
    sleep 5
done
