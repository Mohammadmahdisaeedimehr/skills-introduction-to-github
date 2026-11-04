from collections.abc import Mapping
from typing import TypedDict

VALID_STATUSES: frozenset[str] = frozenset({"inside", "outside", "review"})


class NormalizedSummary(TypedDict):
    user_id: str
    status: str
    confidence: float | None


def normalize_status(status: str) -> str:
    normalized = status.strip().lower()
    if normalized not in VALID_STATUSES:
        raise ValueError(f"Unsupported status: {status!r}")
    return normalized


def normalize_confidence(value: str | int | float | None) -> float | None:
    """Return None when confidence is missing, otherwise a validated float."""
    if value is None:
        return None

    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        confidence = float(stripped)
    else:
        confidence = float(value)

    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")

    return confidence


def normalize_summary(raw: Mapping[str, str]) -> NormalizedSummary:
    user_id = raw.get("user_id", "").strip()
    if not user_id:
        raise ValueError("user_id is required")

    status = normalize_status(raw.get("status", "review"))
    confidence = normalize_confidence(raw.get("confidence"))

    return {
        "user_id": user_id,
        "status": status,
        "confidence": confidence,
    }
