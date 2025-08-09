import psutil
import platform

import cpuinfo
from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from config import config

info = Router()

@info.message(Command("info"))
async def disk(message: Message) -> None:
    info = await message.reply(
        text = "Loading..."
    )

    try:
        diskTotal = int(psutil.disk_usage('/').total / (1024 * 1024 * 1024))
        diskUsed = int(psutil.disk_usage('/').used / (1024 * 1024 * 1024))
        diskPercent = psutil.disk_usage('/').percent
        disk = f"{diskUsed}GB / {diskTotal}GB ({diskPercent}%)"
    except:
        disk = "Unknown"

    await info.edit_text(
        text = "Get RAM and ROM info..."
    )

    try:
        ramTotal = int(psutil.virtual_memory().total / (1024 * 1024))
        ramUsage = int(psutil.virtual_memory().used / (1024 * 1024))
        ramUsagePercent = psutil.virtual_memory().percent
        ram = f"{ramUsage}MB / {ramTotal} MB ({ramUsagePercent}%)"
    except:
        ram = "Unknown"

    await info.edit_text(
        text = "Test CPU..."
    )
    try:
        cpuInfo = cpuinfo.get_cpu_info()['brand_raw']
        cpuUsage = psutil.cpu_percent(interval=1)
        cpu = f"{cpuInfo} ({cpuUsage}%)"
    except:
        cpu = "Unknown"

    await info.edit_text(
        text = "Get OS version..."
    )
    try:
        os = f"{platform.system()} - {platform.release()} ({platform.machine()})"
    except:
        os = "Unknown"

    await info.edit_text(
        text = "Get Battery info..."
    )
    try:
        battery = f"{int(psutil.sensors_battery().percent)}%"
    except:
        battery = f"Unknown"

    msg = f'''
Disk: **{disk}**
CPU: **{cpu}**
RAM: **{ram}**
OS: **{os}**
Battery: **{battery}**
Version: **{config.version}**
'''
    await info.edit_text(
        text = msg
    )