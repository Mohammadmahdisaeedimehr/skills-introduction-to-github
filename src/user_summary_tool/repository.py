from collections.abc import Iterable

from .normalizer import NormalizedSummary, normalize_status


class UserSummaryRepository:
    def __init__(
        self,
        initial: Iterable[NormalizedSummary] | None = None,
    ) -> None:
        self._items: dict[str, NormalizedSummary] = {}

        if initial is not None:
            for summary in initial:
                self.save(summary)

    def save(self, summary: NormalizedSummary) -> None:
        self._items[summary["user_id"]] = summary

    def get_by_user_id(self, user_id: str) -> NormalizedSummary | None:
        return self._items.get(user_id)

    def list_by_status(self, status: str) -> list[NormalizedSummary]:
        normalized_status = normalize_status(status)
        return [
            summary
            for summary in self._items.values()
            if summary["status"] == normalized_status
        ]
