from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIRECTORY = PROJECT_ROOT / "data" / "processed"

DISPLAY_COLUMNS = [
    "service_request_id",
    "source_file",
    "date_requested",
    "date_closed",
    "status",
    "case_age_days",
    "service_name",
]


def show_file(file_name: str, title: str) -> None:
    """Display the relevant fields from a quarantined dataset."""
    file_path = PROCESSED_DATA_DIRECTORY / file_name

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    data = pd.read_csv(file_path, low_memory=False)

    available_columns = [
        column
        for column in DISPLAY_COLUMNS
        if column in data.columns
    ]

    print(data[available_columns].to_string(index=False))


def main() -> None:
    """Inspect records excluded during dataset construction."""
    show_file(
        "cross_source_duplicate_ids.csv",
        "REPEATED SERVICE REQUEST IDS",
    )
    show_file(
        "invalid_date_records_2025.csv",
        "INVALID DATE RELATIONSHIPS",
    )


if __name__ == "__main__":
    main()