import os
from pathlib import Path

from dotenv import load_dotenv

EnvPath = str | Path


class ConfigError(RuntimeError):
    """Raised when required application configuration is missing or invalid."""


def load_environment(env_file: EnvPath = ".env") -> None:
    """Load local .env values without overriding variables already set by the shell."""
    load_dotenv(dotenv_path=Path(env_file), override=False)


def get_database_url() -> str:
    value = os.getenv("DATABASE_URL")
    if value is None or not value.strip():
        raise ConfigError(
            "Missing required environment variable DATABASE_URL. "
            "Copy .env.example to .env and set DATABASE_URL before using database features."
        )
    return value.strip()


def get_data_dir() -> Path:
    value = os.getenv("APP_DATA_DIR", "./data").strip()
    if not value:
        raise ConfigError("APP_DATA_DIR cannot be empty when it is set.")
    return Path(value).expanduser()


def get_summary_path() -> Path:
    value = os.getenv("USER_SUMMARY_PATH", "./user_summary.txt").strip()
    if not value:
        raise ConfigError("USER_SUMMARY_PATH cannot be empty when it is set.")
    return Path(value).expanduser()
