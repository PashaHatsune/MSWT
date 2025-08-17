import platform

import cpuinfo
import psutil
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from ..container import Container
from ..services import UserService

router = Router(name=__name__)

@inject
@router.message(Command("info"))
async def system_info(
    message: Message,
    user_service: UserService = Provide[
        Container.user_service
    ]
) -> None:
    info = await message.reply(
        text = "🔄 | <b>Loading.</b>"
    )

    try:
        diskTotal = int(psutil.disk_usage('/').total / (1024 * 1024 * 1024))
        diskUsed = int(psutil.disk_usage('/').used / (1024 * 1024 * 1024))
        diskPercent = psutil.disk_usage('/').percent
        disk = f"{diskUsed}GB / {diskTotal}GB ({diskPercent}%)"
    except:
        disk = "Unknown"

    await info.edit_text(
        text = "🔄 | <b>Get RAM and ROM info..</b>"
    )

    try:
        ramTotal = int(psutil.virtual_memory().total / (1024 * 1024))
        ramUsage = int(psutil.virtual_memory().used / (1024 * 1024))
        ramUsagePercent = psutil.virtual_memory().percent
        ram = f"{ramUsage}MB / {ramTotal} MB ({ramUsagePercent}%)"
    except:
        ram = "Unknown"

    await info.edit_text(
        text = "🔄 | <b>Test CPU...</b>"
    )
    try:
        cpuInfo = cpuinfo.get_cpu_info()['brand_raw']
        cpuUsage = psutil.cpu_percent(interval=1)
        cpu = f"{cpuInfo} ({cpuUsage}%)"
    except:
        cpu = "Unknown"

    await info.edit_text(
        text = "🔄 | <b>Get OS version....</b>"
    )
    try:
        os = f"{platform.system()} - {platform.release()} ({platform.machine()})"
    except:
        os = "Unknown"

    await info.edit_text(
        text = "🔄 | <b>Get Battery info.....</b>"
    )
    try:
        battery = f"{int(psutil.sensors_battery().percent)}%"
    except:
        battery = f"Unknown"

    msg = f'''
💽 | <b>Disk [ROOT]:</b> <code>{disk}</code>
🖥️ | <b>CPU:</b> <code>{cpu}</code>
🧠 | <b>RAM:</b> <code>{ram}</code>
🖱️ | <b>OS:</b> <code>{os}</code>
🔋 | <b>Battery:</b> <code>{battery}</code>
📦 | <b>Version:</b> <code>{user_service.config.meta.version}</code>

'''
    await info.edit_text(
        text = msg
    )