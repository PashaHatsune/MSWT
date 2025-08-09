import pkgutil
import importlib
from pathlib import Path
from aiogram import Router

from loguru import logger

def load_routers() -> list[Router]:
    modules_path = Path(__file__).parent
    module_name = __name__
    routers = []

    info = pkgutil.iter_modules(path=[str(modules_path)])
    for _, module_name_part, _ in info:
        module = importlib.import_module(f"{module_name}.{module_name_part}")

        found_router = False  # флаг для модуля

        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, Router):
                routers.append(obj)
                found_router = True
                logger.success(f"Роутер {attr} был загружен из модуля {module_name_part}")

        if not found_router:
            logger.error(f"В модуле {module_name_part} не найден ни один роутер!")

    return routers