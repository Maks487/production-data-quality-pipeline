from pathlib import Path
from pipeline.utils.db import execute_sql


def read_sql_file(file_path: str) -> str:
    path = Path(file_path)
    return path.read_text(encoding="utf-8")

def run_sql_file(file_path: str) -> None:
    sql = read_sql_file(file_path)
    execute_sql(sql)