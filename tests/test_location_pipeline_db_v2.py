from pathlib import Path

import pandas as pd
import pytest

from location_pipeline_db_v2.config import PipelineConfig
from location_pipeline_db_v2.pipeline import build_summary, clean_location_frame


@pytest.fixture
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "username": [" Alice ", "BOB", "alice"],
            "final_location_code": ["IR", "OUT", "IR"],
            "post_count_in_dataset": ["3", "bad", 5],
            "extra_column": ["x", "y", "z"],
        }
    )


def test_clean_location_frame_preserves_rows_and_normalizes(
    sample_frame: pd.DataFrame,
) -> None:
    cleaned = clean_location_frame(sample_frame)

    assert len(cleaned) == 3
    assert cleaned["__source_row_number"].tolist() == [1, 2, 3]
    assert cleaned["username"].tolist() == ["alice", "bob", "alice"]
    assert cleaned["post_count_in_dataset"].tolist() == [3, pd.NA, 5]
    assert cleaned["extra_column"].tolist() == ["x", "y", "z"]


def test_clean_location_frame_keeps_duplicate_users(
    sample_frame: pd.DataFrame,
) -> None:
    cleaned = clean_location_frame(sample_frame)

    assert cleaned["username"].tolist().count("alice") == 2


def test_clean_location_frame_requires_core_columns() -> None:
    frame = pd.DataFrame({"username": ["alice"]})

    with pytest.raises(ValueError, match="final_location_code"):
        clean_location_frame(frame)


def test_build_summary_counts_location_codes(
    sample_frame: pd.DataFrame,
) -> None:
    cleaned = clean_location_frame(sample_frame)
    summary = build_summary(cleaned)

    counts = dict(
        zip(
            summary["final_location_code"],
            summary["row_count"],
            strict=True,
        )
    )

    assert counts == {"IR": 2, "OUT": 1}


def test_pipeline_config_paths_are_explicit(tmp_path: Path) -> None:
    config = PipelineConfig(
        input_csv=tmp_path / "input.csv",
        output_parquet=tmp_path / "output.parquet",
        summary_parquet=tmp_path / "summary.parquet",
        benchmark_json=tmp_path / "benchmark.json",
        database_url="postgresql://example/test",
    )

    assert config.schema == "location_pipeline_db_v2"
    assert config.table == "user_locations"
    assert config.output_parquet.suffix == ".parquet"
