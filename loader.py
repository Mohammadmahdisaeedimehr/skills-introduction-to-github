from pathlib import Path

SourcePath = str | Path
RawSummary = dict[str, str]


def load_key_value_file(path: SourcePath) -> RawSummary:
    """Load a simple key=value file into a typed dictionary."""
    file_path = Path(path)
    data: RawSummary = {}

    for line_number, raw_line in enumerate(
        file_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()
        if not line:
            continue
        if "=" not in line:
            raise ValueError(f"Invalid line {line_number}: expected key=value")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError(f"Invalid line {line_number}: empty key")

        data[key] = value

    return data
