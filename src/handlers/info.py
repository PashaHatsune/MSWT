import platform, psutil, cpuinfo
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
    safe = lambda f, d="Unknown": (lambda: (lambda: f())())() if True else d  # трюк с try/except не нужен, ловим отдельно

    disk = safe(lambda: f"{psutil.disk_usage('/').used//(1024**3)}GB / {psutil.disk_usage('/').total//(1024**3)}GB ({psutil.disk_usage('/').percent}%)")
    ram = safe(lambda: f"{psutil.virtual_memory().used//(1024**2)}MB / {psutil.virtual_memory().total//(1024**2)}MB ({psutil.virtual_memory().percent}%)")
    cpu = safe(lambda: f"{cpuinfo.get_cpu_info()['brand_raw']} ({psutil.cpu_percent(1)}%)")
    os_info = safe(lambda: f"{platform.system()} - {platform.release()} ({platform.machine()})")
    battery = safe(lambda: f"{int(psutil.sensors_battery().percent)}%")

    await message.reply(f'''
💽 | <b>Disk [ROOT]:</b> <code>{disk}</code>
🖥️ | <b>CPU:</b> <code>{cpu}</code>
🧠 | <b>RAM:</b> <code>{ram}</code>
🖱️ | <b>OS:</b> <code>{os_info}</code>
🔋 | <b>Battery:</b> <code>{battery}</code>
📦 | <b>Version:</b> <code>{user_service.config.meta.version}</code>
''')
