from contextlib import contextmanager
from pathlib import Path

from config import Config


def _connector():
    import mysql.connector

    return mysql.connector


def connection_config(include_database=True):
    config = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
    }
    if include_database:
        config["database"] = Config.DB_NAME
    return config


@contextmanager
def get_connection(include_database=True):
    connector = _connector()
    conn = connector.connect(**connection_config(include_database=include_database))
    try:
        yield conn
    finally:
        conn.close()


def database_available():
    if not Config.DB_ENABLED:
        return False
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except Exception:
        return False


def fetch_all(query, params=None):
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        return cursor.fetchall()


def fetch_one(query, params=None):
    rows = fetch_all(query, params)
    return rows[0] if rows else None


def execute(query, params=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid


def execute_many(query, rows, chunk_size=500):
    if not rows:
        return 0
    affected = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        for index in range(0, len(rows), chunk_size):
            chunk = rows[index : index + chunk_size]
            cursor.executemany(query, chunk)
            affected += cursor.rowcount
        conn.commit()
        return affected


def execute_sql_file(path, include_database=False):
    connector = _connector()
    sql = Path(path).read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
    with get_connection(include_database=include_database) as conn:
        cursor = conn.cursor()
        for statement in statements:
            try:
                cursor.execute(statement)
            except connector.Error as error:
                if error.errno not in (1061,):
                    raise
        conn.commit()
    return len(statements)
