from pathlib import Path
from typing import List, Any

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2] / ".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )


class TelegramSettings(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix='tg_'
    )

    token: SecretStr
    owners: List[int]

    @field_validator("owners", mode="before")
    def parse_owners(cls, v: Any):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",")]
        return v


class Metadata(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix='meta_'
    )

    version: str


class Config(BaseSettings):
    telegram: TelegramSettings = Field(
        default_factory=TelegramSettings
    )
    meta: Metadata = Field(
        default_factory=Metadata
    )

    @classmethod
    def load(cls) -> Self:
        return cls()


config = Config.load()