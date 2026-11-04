from argparse import ArgumentParser
from pathlib import Path

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
        default="user_summary.txt",
        type=Path,
        help="Path to a key=value summary file.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = normalize_summary(load_key_value_file(args.path))

    confidence = summary["confidence"]
    confidence_text = "missing" if confidence is None else f"{confidence:.2f}"

    print(
        f'user_id={summary["user_id"]} '
        f'status={summary["status"]} '
        f'confidence={confidence_text}'
    )
