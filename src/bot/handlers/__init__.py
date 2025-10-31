import asyncio
import importlib
import inspect
import pkgutil
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

        found_router = False

        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, Router):
                routers.append(obj)
                found_router = True
                logger.success(f"Роутер {attr} был загружен из модуля {module_name_part}")

        if not found_router and module_name_part != "tasks":
            logger.error(f"В модуле {module_name_part} не найден ни один роутер!")

    return routers


async def start_background_tasks(bot):
    modules_path = Path(__file__).parent / "tasks"
    module_base = f"{__name__}.tasks"

    for _, module_name_part, _ in pkgutil.iter_modules(path=[str(modules_path)]):
        full_module_name = f"{module_base}.{module_name_part}"
        try:
            module = importlib.import_module(full_module_name)
        except Exception as e:
            logger.error(f"Не удалось импортировать модуль {full_module_name}: {e}")
            continue

        start_task_func = getattr(module, "start_task", None)
        if start_task_func is None:
            logger.warning(f"В модуле {module_name_part} не найдена функция start_task")
            continue

        if not inspect.iscoroutinefunction(start_task_func):
            logger.error(f"В модуле {module_name_part} функция start_task не является асинхронной")
            continue

        params = inspect.signature(start_task_func).parameters
        if len(params) != 1 or next(iter(params)) != 'bot':
            logger.error(f"Функция start_task в модуле {module_name_part} должна принимать ровно один аргумент 'bot'")
            continue

        asyncio.create_task(start_task_func(bot))
        logger.success(f"Запущена задача start_task из модуля {module_name_part}")
