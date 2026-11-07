from __future__ import annotations

import json
from typing import Any

import pandas as pd
import psycopg
from psycopg import sql

from .config import PipelineConfig, get_pipeline_config, validate_input_path

REQUIRED_COLUMNS = {"username", "final_location_code"}


def clean_location_frame(frame: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_text}")

    cleaned = frame.copy()

    if "__source_row_number" not in cleaned.columns:
        cleaned.insert(0, "__source_row_number", range(1, len(cleaned) + 1))

    cleaned["username"] = (
        cleaned["username"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    cleaned["final_location_code"] = (
        cleaned["final_location_code"]
        .astype("string")
        .str.strip()
    )

    if "post_count_in_dataset" in cleaned.columns:
        cleaned["post_count_in_dataset"] = pd.to_numeric(
            cleaned["post_count_in_dataset"],
            errors="coerce",
        ).astype("Int64")

    return cleaned


def build_summary(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby("final_location_code", dropna=False)
        .size()
        .rename("row_count")
        .reset_index()
        .sort_values(["row_count", "final_location_code"], ascending=[False, True])
        .reset_index(drop=True)
    )


def _to_json_payload(row: pd.Series) -> str:
    payload: dict[str, Any] = {}
    for key, value in row.items():
        if pd.isna(value):
            payload[str(key)] = None
        elif hasattr(value, "item"):
            payload[str(key)] = value.item()
        else:
            payload[str(key)] = value
    return json.dumps(payload, ensure_ascii=False, default=str)


def _create_schema_and_tables(conn: psycopg.Connection[Any], config: PipelineConfig) -> None:
    schema = sql.Identifier(config.schema)
    table = sql.Identifier(config.table)
    summary_table = sql.Identifier(config.summary_table)

    conn.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(schema))

    conn.execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {}.{} (
                source_row_number BIGINT PRIMARY KEY,
                username TEXT,
                final_location_code TEXT,
                post_count_in_dataset BIGINT,
                row_payload JSONB NOT NULL
            )
            """
        ).format(schema, table)
    )

    conn.execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {}.{} (
                final_location_code TEXT,
                row_count BIGINT NOT NULL
            )
            """
        ).format(schema, summary_table)
    )

    conn.execute(
        sql.SQL(
            "CREATE INDEX IF NOT EXISTS {} ON {}.{} (final_location_code)"
        ).format(
            sql.Identifier(f"{config.table}_location_idx"),
            schema,
            table,
        )
    )


def load_postgres(
    frame: pd.DataFrame,
    summary: pd.DataFrame,
    config: PipelineConfig,
) -> None:
    with psycopg.connect(config.database_url) as conn:
        _create_schema_and_tables(conn, config)

        schema = sql.Identifier(config.schema)
        table = sql.Identifier(config.table)
        summary_table = sql.Identifier(config.summary_table)

        conn.execute(sql.SQL("TRUNCATE TABLE {}.{}").format(schema, table))
        conn.execute(sql.SQL("TRUNCATE TABLE {}.{}").format(schema, summary_table))

        copy_query = sql.SQL(
            """
            COPY {}.{} (
                source_row_number,
                username,
                final_location_code,
                post_count_in_dataset,
                row_payload
            ) FROM STDIN
            """
        ).format(schema, table)

        with conn.cursor().copy(copy_query) as copy:
            for _, row in frame.iterrows():
                post_count = row.get("post_count_in_dataset")
                copy.write_row(
                    (
                        int(row["__source_row_number"]),
                        None if pd.isna(row["username"]) else str(row["username"]),
                        (
                            None
                            if pd.isna(row["final_location_code"])
                            else str(row["final_location_code"])
                        ),
                        None if post_count is None or pd.isna(post_count) else int(post_count),
                        _to_json_payload(row),
                    )
                )

        summary_copy = sql.SQL(
            "COPY {}.{} (final_location_code, row_count) FROM STDIN"
        ).format(schema, summary_table)

        with conn.cursor().copy(summary_copy) as copy:
            for _, row in summary.iterrows():
                code = row["final_location_code"]
                copy.write_row(
                    (
                        None if pd.isna(code) else str(code),
                        int(row["row_count"]),
                    )
                )

        conn.execute(sql.SQL("ANALYZE {}.{}").format(schema, table))
        conn.execute(sql.SQL("ANALYZE {}.{}").format(schema, summary_table))


def write_parquet(
    frame: pd.DataFrame,
    summary: pd.DataFrame,
    config: PipelineConfig,
) -> None:
    config.output_parquet.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(config.output_parquet, index=False)
    summary.to_parquet(config.summary_parquet, index=False)


def run_pipeline(config: PipelineConfig | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    active = config or get_pipeline_config()
    validate_input_path(active)

    raw = pd.read_csv(active.input_csv, low_memory=False)
    cleaned = clean_location_frame(raw)
    summary = build_summary(cleaned)

    write_parquet(cleaned, summary, active)
    load_postgres(cleaned, summary, active)

    return cleaned, summary
