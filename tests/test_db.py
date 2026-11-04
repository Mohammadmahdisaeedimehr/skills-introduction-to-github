import sqlite3

import pytest


@pytest.mark.parametrize("status", ["inside", "outside", "review"])
def test_db_accepts_valid_statuses(db_conn, status):
    db_conn.execute(
        "INSERT INTO user_summary (user_id, status, confidence) VALUES (?, ?, ?)",
        (f"user-{status}", status, 0.75),
    )
    db_conn.commit()

    row = db_conn.execute(
        "SELECT status, confidence FROM user_summary WHERE user_id = ?",
        (f"user-{status}",),
    ).fetchone()

    assert row == (status, 0.75)


@pytest.mark.parametrize("status", ["", "unknown", "INSIDE", None])
def test_db_rejects_invalid_statuses(db_conn, status):
    with pytest.raises(sqlite3.IntegrityError):
        db_conn.execute(
            "INSERT INTO user_summary (user_id, status, confidence) VALUES (?, ?, ?)",
            ("bad-status", status, 0.50),
        )


@pytest.mark.parametrize("confidence", [-0.01, -1.0, 1.01, 2.0])
def test_db_rejects_confidence_outside_range(db_conn, confidence):
    with pytest.raises(sqlite3.IntegrityError):
        db_conn.execute(
            "INSERT INTO user_summary (user_id, status, confidence) VALUES (?, ?, ?)",
            ("bad-confidence", "inside", confidence),
        )


@pytest.mark.parametrize("confidence", [0.0, 0.5, 1.0])
def test_db_accepts_confidence_boundaries(db_conn, confidence):
    user_id = f"boundary-{confidence}"
    db_conn.execute(
        "INSERT INTO user_summary (user_id, status, confidence) VALUES (?, ?, ?)",
        (user_id, "review", confidence),
    )

    stored = db_conn.execute(
        "SELECT confidence FROM user_summary WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]

    assert stored == confidence


def test_db_fixture_is_fresh_for_each_test(db_conn):
    count = db_conn.execute("SELECT COUNT(*) FROM user_summary").fetchone()[0]
    assert count == 0
