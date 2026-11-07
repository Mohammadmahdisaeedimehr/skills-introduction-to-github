# location_pipeline_db_v2

This refactor keeps the month-one cleaning semantics while changing the primary
outputs from CSV-only files to PostgreSQL plus Parquet.

## Primary outputs

- PostgreSQL schema: `location_pipeline_db_v2`
- PostgreSQL table: `user_locations`
- PostgreSQL summary table: `location_summary`
- Full cleaned Parquet: `location_pipeline_db_v2.parquet`
- Summary Parquet: `location_pipeline_db_v2_summary.parquet`
- Benchmark report: `benchmark_csv_vs_postgres.json`

The PostgreSQL table keeps the main query fields as typed columns and also
stores the complete cleaned source row in JSONB, so source columns are not
discarded when the input CSV evolves.

## Month-one semantics retained

- preserve source row order with `__source_row_number`
- lowercase and trim `username`
- trim `final_location_code`
- coerce `post_count_in_dataset` to nullable integer when present
- retain duplicate users rather than silently deleting them
- fail clearly if required core columns are missing

## Benchmark

The benchmark asks the same analytical question through both storage paths:
count rows grouped by `final_location_code`.

It runs each path repeatedly and records minimum, median, and maximum elapsed
time. The generated JSON also records the median PostgreSQL-vs-CSV speedup.

The benchmark must be run on the local machine that has the real month-one CSV
and PostgreSQL database; CI intentionally does not require a live database.
