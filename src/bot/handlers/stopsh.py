from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import psutil

from .sh_utils import (
    collect_related_processes,
    find_script_processes,
    list_sh_files,
    resolve_script_path,
)

router = Router(name=__name__)


@router.message(Command("stopsh"))
async def stop_sh_process(
    message: Message
) -> None:

    cmd_text = (message.reply_to_message.text if message.reply_to_message
                else (message.text.split(maxsplit=1)[1] if len(message.text.split(maxsplit=1)) > 1 else None))

    if not cmd_text:
        files = list_sh_files()
        if not files:
            await message.reply(
                text="😢 | <b>No .sh files found in ./sh-module</b>"
            )
            return
        await message.reply(
            text="📁 | <b>Available .sh files:</b>\n" + "\n".join(
                f"- <code>{f}</code>" for f in files
            )
        )
        return

    script_path = resolve_script_path(cmd_text)
    script_name = script_path.name

    found = find_script_processes(script_path)
    if not found:
        await message.reply(
            text=f"😢 | <b>No running process found for {script_name}</b>"
        )
        return

    targets = collect_related_processes(found)
    terminated, killed, errors = [], [], []

    for proc in targets:
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            errors.append(f"{proc.pid} ({exc})")

    gone, alive = psutil.wait_procs(targets, timeout=5)
    terminated.extend([p.pid for p in gone])

    for proc in alive:
        try:
            proc.kill()
            killed.append(proc.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            errors.append(f"{proc.pid} ({exc})")

    await message.reply(
        "🛑 | <b>Stopped shell module</b>\n"
        f"🎯 | Script: <code>{script_name}</code>\n"
        f"✅ | Terminated: <code>{', '.join(map(str, terminated)) or 'none'}</code>\n"
        f"💀 | Killed: <code>{', '.join(map(str, killed)) or 'none'}</code>\n"
        f"⚠️ | Errors: <code>{'; '.join(errors) or 'none'}</code>"
    )
