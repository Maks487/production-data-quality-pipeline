import csv
from pathlib import Path

from pipeline.utils.db import get_mssql_connection

DATA_FILE = Path("/opt/airflow/data/machine_events.csv")
SOURCE_FILE_NAME = "machine_events.csv"


def truncate_raw_table() -> None:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('TRUNCATE TABLE raw.machine_events_raw')
        conn.commit()


def load_raw_events() -> int:
    inserted_rows = 0

    with DATA_FILE.open(mode="r", newline="",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        with get_mssql_connection() as conn:
            cursor = conn.cursor()

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO raw.machine_events_raw (
                        source_file_name,
                        event_id,
                        machine_id,
                        production_line,
                        event_timestamp,
                        signal_name,
                        signal_value,
                        status,
                        batch_id,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        SOURCE_FILE_NAME,
                        row["event_id"],
                        row["machine_id"],
                        row["production_line"],
                        row["event_timestamp"],
                        row["signal_name"],
                        row["signal_value"],
                        row["status"],
                        row["batch_id"],
                        row["created_at"],
                    ),
                )

                inserted_rows += 1
            conn.commit()
    return inserted_rows


if __name__ == "__main__":
    truncate_raw_table()
    rows_loaded = load_raw_events()
    print(f"Loaded rows: {rows_loaded}")