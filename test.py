#!/usr/bin/env python3
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

SERVICE_NAME = "mswt.service"
RESTART_SCRIPT = Path("/home/miku/dev/MSWT/restart-daemon.sh")

ERROR_PATTERNS = re.compile(
    r"TelegramConflictError|TelegramNetworkError|ClientConnectorError|ServerDisconnectedError",
    re.IGNORECASE
)

def restart_service():
    print(f"{datetime.now()}: Найдена ошибка в логе, перезапускаю сервис {SERVICE_NAME}")
    subprocess.run(["sh", str(RESTART_SCRIPT)], check=False)
    time.sleep(10)

def monitor_logs():
    print(f"Запускаю мониторинг логов сервиса {SERVICE_NAME}")
    process = subprocess.Popen(
        ["journalctl", "-fu", SERVICE_NAME],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        for line in process.stdout:
            line = line.strip()
            print(f"LOG: {line}")
            if ERROR_PATTERNS.search(line):
                restart_service()
    except KeyboardInterrupt:
        print("\nОстановка мониторинга...")
    finally:
        process.terminate()

if __name__ == "__main__":
    monitor_logs()
