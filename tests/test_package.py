from pathlib import Path

from user_summary_tool import (
    UserSummaryRepository,
    load_key_value_file,
    normalize_summary,
)


def test_installed_package_imports_and_runs(tmp_path: Path) -> None:
    source = tmp_path / "summary.txt"
    source.write_text(
        "user_id=user_100\nstatus=Review\nconfidence=0.75\n",
        encoding="utf-8",
    )

    summary = normalize_summary(load_key_value_file(source))
    repository = UserSummaryRepository([summary])

    assert repository.get_by_user_id("user_100") == {
        "user_id": "user_100",
        "status": "review",
        "confidence": 0.75,
    }
