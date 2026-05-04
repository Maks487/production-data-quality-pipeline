import os
import pymssql

from contextlib import contextmanager

def get_mssql_config() -> dict:
    return {
        "server": os.getenv("MSSQL_HOST", "mssql"),
        "user": os.getenv("MSSQL_USER","sa"),
        "password": os.getenv("MSSQL_PASSWORD"),
        "database": os.getenv("MSSQL_DB","master"),
        "port": int(os.getenv("MSSQL_PORT","1433")),

    }

@contextmanager
def get_mssql_connection():
    config = get_mssql_config()
    conn = pymssql.connect(**config)

    try:
        yield conn
    finally:
        conn.close()


def execute_sql(sql: str) -> None:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

def fetch_one(sql: str):
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
