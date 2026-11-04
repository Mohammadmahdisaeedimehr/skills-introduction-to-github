VALID_STATUSES = {"inside", "outside", "review"}


def normalize_status(status):
    return status.strip().lower()


def build_user_summary(user_id, status, confidence):
    normalized_status = normalize_status(status)
    return {
        "user_id": user_id,
        "status": normalized_status,
        "confidence": confidence,
    }


def is_valid_status(status):
    return normalize_status(status) in VALID_STATUSES
