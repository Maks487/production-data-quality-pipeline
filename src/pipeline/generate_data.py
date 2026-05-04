import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


DATA_DIR = Path("/opt/airflow/data")
OUTPUT_FILE = DATA_DIR / "machine_events.csv"


MACHINES = ["MCH_01", "MCH_02", "MCH_03", "MCH_04", "MCH_05"]
PRODUCTION_LINES = ["LINE_A", "LINE_B", "LINE_C"]
SIGNALS = ["temperature", "pressure", "speed", "vibration"]
STATUSES = ["OK", "WARNING", "ERROR"]


def generate_event(event_number: int) -> dict:
    event_time = datetime.utcnow() - timedelta(minutes=random.randint(0, 240))
    created_at = event_time + timedelta(seconds=random.randint(0, 120))

    row = {
        "event_id": f"EVT_{event_number:06d}",
        "machine_id": random.choice(MACHINES),
        "production_line": random.choice(PRODUCTION_LINES),
        "event_timestamp": event_time.isoformat(),
        "signal_name": random.choice(SIGNALS),
        "signal_value": round(random.uniform(10, 120), 2),
        "status": random.choice(STATUSES),
        "batch_id": f"BATCH_{random.randint(1, 20):03d}",
        "created_at": created_at.isoformat(),
    }

    return row


def inject_data_quality_issues(row: dict) -> dict:
    issue_type = random.choice([
        "missing_machine_id",
        "invalid_signal_value",
        "invalid_timestamp",
        "unknown_status",
        "missing_batch_id",
        "no_issue",
        "no_issue",
        "no_issue",
    ])

    if issue_type == "missing_machine_id":
        row["machine_id"] = None

    elif issue_type == "invalid_signal_value":
        row["signal_value"] = "not_a_number"

    elif issue_type == "invalid_timestamp":
        row["event_timestamp"] = "wrong_date"

    elif issue_type == "unknown_status":
        row["status"] = "UNKNOWN_STATUS"

    elif issue_type == "missing_batch_id":
        row["batch_id"] = None

    return row


def generate_machine_events(number_of_rows: int = 500) -> str:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    for event_number in range(1, number_of_rows + 1):
        row = generate_event(event_number)
        row = inject_data_quality_issues(row)
        rows.append(row)

    fieldnames = [
        "event_id",
        "machine_id",
        "production_line",
        "event_timestamp",
        "signal_name",
        "signal_value",
        "status",
        "batch_id",
        "created_at",
    ]

    with OUTPUT_FILE.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(OUTPUT_FILE)


if __name__ == "__main__":
    output_path = generate_machine_events()
    print(f"Generated file: {output_path}")