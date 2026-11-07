from __future__ import annotations

import json
from statistics import median
from time import perf_counter
from collections.abc import Callable
from typing import Any

import pandas as pd
import psycopg
from psycopg import sql

from .config import PipelineConfig, get_pipeline_config, validate_input_path


def _measure(callable_obj: Callable[[], Any], repeats: int) -> dict[str, float]:
    timings: list[float] = []
    for _ in range(repeats):
        started = perf_counter()
        callable_obj()
        timings.append(perf_counter() - started)

    return {
        "min_seconds": min(timings),
        "median_seconds": median(timings),
        "max_seconds": max(timings),
    }


def _csv_query(config: PipelineConfig) -> dict[str, int]:
    frame = pd.read_csv(
        config.input_csv,
        usecols=["final_location_code"],
        low_memory=False,
    )
    grouped = (
        frame["final_location_code"]
        .astype("string")
        .str.strip()
        .value_counts(dropna=False)
    )
    return {str(key): int(value) for key, value in grouped.items()}


def _db_query(config: PipelineConfig) -> dict[str, int]:
    query = sql.SQL(
        """
        SELECT final_location_code, COUNT(*)
        FROM {}.{}
        GROUP BY final_location_code
        ORDER BY COUNT(*) DESC
        """
    ).format(sql.Identifier(config.schema), sql.Identifier(config.table))

    with psycopg.connect(config.database_url) as conn:
        rows = conn.execute(query).fetchall()

    return {
        "<NULL>" if code is None else str(code): int(count)
        for code, count in rows
    }


def run_benchmark(
    config: PipelineConfig | None = None,
    repeats: int = 5,
) -> dict[str, Any]:
    active = config or get_pipeline_config()
    validate_input_path(active)

    csv_result = _csv_query(active)
    db_result = _db_query(active)

    csv_timing = _measure(lambda: _csv_query(active), repeats)
    db_timing = _measure(lambda: _db_query(active), repeats)

    report: dict[str, Any] = {
        "repeats": repeats,
        "query": "count rows grouped by final_location_code",
        "csv": csv_timing,
        "postgres": db_timing,
        "result_group_count": {
            "csv": len(csv_result),
            "postgres": len(db_result),
        },
        "median_speedup_postgres_vs_csv": (
            csv_timing["median_seconds"] / db_timing["median_seconds"]
            if db_timing["median_seconds"] > 0
            else None
        ),
    }

    active.benchmark_json.parent.mkdir(parents=True, exist_ok=True)
    active.benchmark_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return report
