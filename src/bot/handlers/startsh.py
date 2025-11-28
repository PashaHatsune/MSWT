from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .sh_utils import list_sh_files, resolve_script_path, start_script_with_logs

router = Router(name=__name__)


@router.message(Command("startsh"))
async def start_sh_process(
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
    if not script_path.is_file():
        await message.reply(
            text=f"😢 | <b>File not found:</b> <code>{script_path.name}</code>"
        )
        return

    try:
        pid, log_path = start_script_with_logs(script_path)
    except Exception as exc:
        await message.reply(
            text=f"❌ | <b>Failed to start</b> <code>{script_path.name}</code>\n<code>{exc}</code>"
        )
        return

    await message.reply(
        "✅ | <b>Shell module started</b>\n"
        f"🎯 | Script: <code>{script_path.name}</code>\n"
        f"🗒️ | Log: <code>{log_path.name}</code>\n"
        f"🔢 | PID: <code>{pid}</code>"
    )
