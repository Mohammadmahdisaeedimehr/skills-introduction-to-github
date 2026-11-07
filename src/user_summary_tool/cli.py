from argparse import ArgumentParser
from pathlib import Path

from .config import get_summary_path, load_environment
from .loader import load_key_value_file
from .normalizer import normalize_summary


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="user-summary",
        description="Load and normalize a key=value user summary file.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        type=Path,
        help="Path to a key=value summary file. Defaults to USER_SUMMARY_PATH.",
    )
    return parser


def main() -> None:
    load_environment()
    args = build_parser().parse_args()
    path = args.path if args.path is not None else get_summary_path()

    summary = normalize_summary(load_key_value_file(path))

    confidence = summary["confidence"]
    confidence_text = "missing" if confidence is None else f"{confidence:.2f}"

    print(
        f'user_id={summary["user_id"]} '
        f'status={summary["status"]} '
        f'confidence={confidence_text}'
    )
