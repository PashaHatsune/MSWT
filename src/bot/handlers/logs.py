from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from .sh_utils import LOG_DIR, get_log_path, list_sh_files, resolve_script_path

router = Router(name=__name__)


@router.message(Command("logs"))
async def logs_sh_process(
    message: Message
) -> None:
    cmd_text = (message.reply_to_message.text if message.reply_to_message
                else (message.text.split(maxsplit=1)[1] if len(message.text.split(maxsplit=1)) > 1 else None))

    if not cmd_text:
        available = []
        if LOG_DIR.exists():
            available = sorted([p.name for p in LOG_DIR.glob("*.log") if p.is_file()])

        # fallback to list .sh if no logs yet
        if not available:
            sh_files = list_sh_files()
            if not sh_files:
                await message.reply(
                    text="😢 | <b>No logs or .sh files found</b>"
                )
                return
            await message.reply(
                text="📁 | <b>No logs yet. Available .sh files:</b>\n" + "\n".join(
                    f"- <code>{f}</code>" for f in sh_files
                )
            )
            return

        await message.reply(
            text="🗒️ | <b>Available log files:</b>\n" + "\n".join(
                f"- <code>{f}</code>" for f in available
            )
        )
        return

    script_path = resolve_script_path(cmd_text)
    log_path = get_log_path(script_path)

    if not log_path.exists():
        await message.reply(
            text=f"😢 | <b>No log file found for:</b> <code>{script_path.name}</code>"
        )
        return

    try:
        await message.reply_document(
            FSInputFile(
                path=log_path,
                filename=log_path.name
            ),
            caption=f"🗒️ | <b>Logs for</b> <code>{script_path.name}</code>"
        )
    except Exception as exc:
        await message.reply(
            text=f"❌ | <b>Failed to send log</b>\n<code>{exc}</code>"
        )
