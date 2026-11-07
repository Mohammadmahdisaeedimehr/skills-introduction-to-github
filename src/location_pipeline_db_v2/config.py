import os
from dataclasses import dataclass
from pathlib import Path

from user_summary_tool.config import ConfigError, get_database_url, load_environment


@dataclass(frozen=True)
class PipelineConfig:
    input_csv: Path
    output_parquet: Path
    summary_parquet: Path
    benchmark_json: Path
    database_url: str
    schema: str = "location_pipeline_db_v2"
    table: str = "user_locations"
    summary_table: str = "location_summary"
    chunk_size: int = 5_000


def get_pipeline_config() -> PipelineConfig:
    load_environment()

    input_csv = Path(
        os.getenv(
            "LOCATION_INPUT_CSV",
            "data/raw/IRANIAN_unique_users_location_FINAL_v4.csv",
        )
    ).expanduser()

    output_dir = Path(
        os.getenv("LOCATION_OUTPUT_DIR", "data/processed")
    ).expanduser()

    return PipelineConfig(
        input_csv=input_csv,
        output_parquet=output_dir / "location_pipeline_db_v2.parquet",
        summary_parquet=output_dir / "location_pipeline_db_v2_summary.parquet",
        benchmark_json=output_dir / "benchmark_csv_vs_postgres.json",
        database_url=get_database_url(),
    )


def validate_input_path(config: PipelineConfig) -> None:
    if not config.input_csv.exists():
        raise ConfigError(
            "Location input CSV not found: "
            f"{config.input_csv}. Set LOCATION_INPUT_CSV in .env."
        )
