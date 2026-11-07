from __future__ import annotations

import json

from .benchmark import run_benchmark
from .pipeline import run_pipeline


def main() -> None:
    cleaned, summary = run_pipeline()
    report = run_benchmark()

    print(
        json.dumps(
            {
                "rows": len(cleaned),
                "summary_groups": len(summary),
                "benchmark": report,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
