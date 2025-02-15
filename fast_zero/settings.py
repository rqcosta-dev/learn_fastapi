from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import ClassVar


class Settings(BaseSettings):
    env: ClassVar[str] = os.getenv("ENVIRONMENT", "dev")
    env_file: ClassVar[str] = f".env.{env}"
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=env_file, env_file_encoding="utf-8", extra="allow"
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


# Debugging code to check if the correct .env file is loaded
if not os.path.exists(Settings.env_file):
    print(f"WARNING {Settings.env_file} file not found")
else:
    print(f"INFO {Settings.env_file} file found and loaded")
