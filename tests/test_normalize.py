import pytest

from review_demo import normalize_status


@pytest.mark.parametrize(
    "raw_status, expected",
    [
        ("inside", "inside"),
        (" INSIDE ", "inside"),
        ("Outside", "outside"),
        (" review\n", "review"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_normalize_status(raw_status, expected):
    assert normalize_status(raw_status) == expected


@pytest.mark.parametrize("bad_status", [None, 1, 0.91, [], {}])
def test_normalize_status_rejects_non_strings(bad_status):
    with pytest.raises(AttributeError):
        normalize_status(bad_status)
