from pathlib import Path

import pytest

from user_summary_tool.config import (
    ConfigError,
    get_data_dir,
    get_database_url,
    get_summary_path,
    load_environment,
)


def test_database_url_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://example/test")

    assert get_database_url() == "postgresql://example/test"


def test_missing_database_url_has_clear_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ConfigError, match="DATABASE_URL") as error:
        get_database_url()

    assert ".env.example" in str(error.value)


def test_paths_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_DATA_DIR", "./custom-data")
    monkeypatch.setenv("USER_SUMMARY_PATH", "./custom/input.txt")

    assert get_data_dir() == Path("./custom-data")
    assert get_summary_path() == Path("./custom/input.txt")


def test_path_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_DATA_DIR", raising=False)
    monkeypatch.delenv("USER_SUMMARY_PATH", raising=False)

    assert get_data_dir() == Path("./data")
    assert get_summary_path() == Path("./user_summary.txt")


def test_load_environment_does_not_override_shell_value(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DATABASE_URL=postgresql://from-file/db\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("DATABASE_URL", "postgresql://from-shell/db")

    load_environment(env_file)

    assert get_database_url() == "postgresql://from-shell/db"
