import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

import psutil

SH_DIR = Path("./sh-module")
LOG_DIR = SH_DIR / "logs"


def list_sh_files(

) -> list[str]:

    if not SH_DIR.exists():
        return []
    return sorted([p.name for p in SH_DIR.glob("*.sh") if p.is_file()])


def resolve_script_path(
        raw: str | os.PathLike[str]
) -> Path:

    raw_path = Path(os.path.expanduser(str(raw)))
    if raw_path.is_file():
        return raw_path.resolve()
    return (SH_DIR / raw_path.name).resolve()


def collect_related_processes(
        root_procs: Iterable[psutil.Process]
) -> List[psutil.Process]:
    """Gather processes and their children, ignoring those that vanish mid-iteration."""

    collected = {}

    for proc in root_procs:
        try:
            collected[proc.pid] = proc
            for child in proc.children(recursive=True):
                collected[child.pid] = child
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return list(collected.values())


def matches_script(
        cmdline: list[str],
        script_path: Path,
        script_name: str
) -> bool:
    """Check if any part of cmdline references the target script."""

    for part in cmdline:
        if not part:
            continue
        if part == script_name:
            return True

        try:
            part_path = Path(part).expanduser().resolve()
        except Exception:
            continue

        if part_path == script_path:
            return True
        if part_path.name == script_name:
            return True

    return False


def find_script_processes(
        script_path: Path
) -> list[psutil.Process]:

    script_name = script_path.name
    found = []
    for proc in psutil.process_iter(["pid", "cmdline"]):
        cmdline = proc.info.get("cmdline") or []
        if matches_script(cmdline, script_path, script_name):
            found.append(proc)
    return found


def get_log_path(
        script_path: Path
) -> Path:

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{script_path.name}.log"


def start_script_with_logs(
        script_path: Path
) -> Tuple[int, Path]:
    """Start a shell script with stdout/stderr redirected to its log file."""

    if not script_path.is_file():
        raise FileNotFoundError(script_path)

    log_path = get_log_path(script_path)
    header = f"\n--- Started via bot at {datetime.now().isoformat()} ---\n"

    with open(log_path, "ab") as log_handle:
        log_handle.write(header.encode("utf-8", "replace"))
        log_handle.flush()
        process = subprocess.Popen(
            ["sh", str(script_path)],
            stdout=log_handle,
            stderr=log_handle
        )
    return process.pid, log_path


def clear_logs_dir(
        
) -> None:
    """Remove existing .log files before new bot session starts."""
    if not LOG_DIR.exists():
        return
    for log_file in LOG_DIR.glob("*.log"):
        try:
            log_file.unlink()
        except Exception:
            continue
