#!/bin/bash

source /home/miku/dev/MSWT/.venv/bin/activate

cd /home/miku/dev/MSWT/

# Запускаем бота
uv run -m src.bot
