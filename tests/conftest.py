import sqlite3

import pytest


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE user_summary (
            user_id TEXT PRIMARY KEY,
            status TEXT NOT NULL CHECK (status IN ('inside', 'outside', 'review')),
            confidence REAL NOT NULL CHECK (confidence >= 0 AND confidence <= 1)
        )
        """
    )
    yield conn
    conn.close()
