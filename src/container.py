from aiogram import Bot
from dependency_injector import containers, providers

from .services import UserService
from .settings import config

class Container(containers.DeclarativeContainer):
    bot = providers.Dependency(instance_of=Bot)

    user_service: UserService = providers.Factory(
        UserService,
        config=config
    )  