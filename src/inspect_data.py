from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"


def inspect_file(file_path: Path) -> None:
    """Print a basic profile of one raw CSV file."""
    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    data = pd.read_csv(file_path, low_memory=False)

    print(f"Rows: {len(data):,}")
    print(f"Columns: {len(data.columns)}")
    print("\nColumn names:")
    print(data.columns.tolist())

    if "service_request_id" in data.columns:
        print(
            f"\nUnique service request IDs: "
            f"{data['service_request_id'].nunique():,}"
        )

    if "status" in data.columns:
        print("\nStatus counts:")
        print(data["status"].value_counts(dropna=False))

    for date_column in ["date_requested", "date_closed"]:
        if date_column in data.columns:
            parsed_dates = pd.to_datetime(
                data[date_column],
                errors="coerce",
            )

            print(f"\n{date_column} range:")
            print(f"  Earliest: {parsed_dates.min()}")
            print(f"  Latest:   {parsed_dates.max()}")
            print(
                f"  Invalid or missing: "
                f"{parsed_dates.isna().sum():,}"
            )

    print("\nColumns with the most missing values:")
    missing_values = data.isna().sum().sort_values(ascending=False)
    print(missing_values.head(10))


def main() -> None:
    """Inspect every raw CSV file in the project."""
    csv_files = sorted(RAW_DATA_DIRECTORY.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DATA_DIRECTORY}"
        )

    for csv_file in csv_files:
        inspect_file(csv_file)


if __name__ == "__main__":
    main()