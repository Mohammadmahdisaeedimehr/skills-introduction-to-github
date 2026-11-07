from pathlib import Path

import pytest

from loader import load_key_value_file
from normalizer import normalize_confidence, normalize_summary
from repository import UserSummaryRepository


def test_loader_accepts_path_object(tmp_path: Path) -> None:
    file_path = tmp_path / "summary.txt"
    file_path.write_text(
        "user_id=user_001\nstatus=inside\nconfidence=0.91\n",
        encoding="utf-8",
    )

    loaded = load_key_value_file(file_path)

    assert loaded["user_id"] == "user_001"


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        ("", None),
        ("   ", None),
        ("0.0", 0.0),
        (0.5, 0.5),
        (1, 1.0),
    ],
)
def test_normalize_confidence_optional_union(
    value: str | float | None,
    expected: float | None,
) -> None:
    assert normalize_confidence(value) == expected


@pytest.mark.parametrize("value", ["-0.01", 1.01, 2])
def test_normalize_confidence_rejects_out_of_range(
    value: str | float,
) -> None:
    with pytest.raises(ValueError):
        normalize_confidence(value)


def test_repository_get_returns_optional() -> None:
    repository = UserSummaryRepository()

    assert repository.get_by_user_id("missing") is None


def test_normalize_summary_missing_confidence_is_none() -> None:
    summary = normalize_summary(
        {
            "user_id": "user_001",
            "status": "review",
        }
    )

    assert summary["confidence"] is None
