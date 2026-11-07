import psycopg

DATABASE_URL = "postgresql://development:development123@127.0.0.1:5432/development_db"


def find_user(username):
    with psycopg.connect(DATABASE_URL) as conn:
        query = f"SELECT user_id, username FROM social_lab_v2.users WHERE username = '{username}'"
        return conn.execute(query).fetchone()


def rename_user(user_id, new_username):
    conn = psycopg.connect(DATABASE_URL)
    conn.execute(
        f"UPDATE social_lab_v2.users SET username = '{new_username}' WHERE user_id = {user_id}"
    )
    conn.commit()
    return True
