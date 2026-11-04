from loader import load_key_value_file
from normalizer import normalize_summary
from repository import UserSummaryRepository


def main() -> None:
    raw = load_key_value_file("user_summary.txt")
    summary = normalize_summary(raw)

    repository = UserSummaryRepository()
    repository.save(summary)

    found = repository.get_by_user_id(summary["user_id"])

    if found is None:
        print("User not found")
        return

    print(
        f'user_id={found["user_id"]} '
        f'status={found["status"]} '
        f'confidence={found["confidence"]}'
    )


if __name__ == "__main__":
    main()
