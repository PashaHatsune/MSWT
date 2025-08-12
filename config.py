from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

print(Path(__file__).parent)

class Settings(BaseSettings):
    token: SecretStr
    owner: list
    version: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8" 
    )


config = Settings()