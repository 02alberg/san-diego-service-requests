from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "service_requests_2025_clean.csv"
)


def main() -> None:
    """Print a concise quality summary of the clean analytical dataset."""
    data = pd.read_csv(CLEAN_DATA_FILE, low_memory=False)

    data["date_requested"] = pd.to_datetime(
        data["date_requested"],
        errors="coerce",
    )
    data["date_closed"] = pd.to_datetime(
        data["date_closed"],
        errors="coerce",
    )

    print("=" * 70)
    print("CLEAN 2025 DATASET SUMMARY")
    print("=" * 70)

    print(f"Rows: {len(data):,}")
    print(f"Columns: {len(data.columns)}")
    print(
        "Unique service request IDs: "
        f"{data['service_request_id'].nunique():,}"
    )

    duplicate_reports = data["is_duplicate_report"].sum()
    duplicate_percentage = duplicate_reports / len(data) * 100

    print(f"Recognized duplicate reports: {duplicate_reports:,}")
    print(f"Duplicate-report percentage: {duplicate_percentage:.2f}%")

    print("\nRequest-date range:")
    print(f"  Earliest: {data['date_requested'].min()}")
    print(f"  Latest:   {data['date_requested'].max()}")

    print("\nStatus counts:")
    print(data["status"].value_counts(dropna=False))

    print("\nSource-file counts:")
    print(data["source_file"].value_counts(dropna=False))

    print("\nTop 15 service categories:")
    print(data["service_name"].value_counts(dropna=False).head(15))

    print("\nRequests by month:")
    monthly_counts = (
        data.groupby(
            ["request_month", "request_month_name"],
            dropna=False,
        )
        .size()
        .reset_index(name="request_count")
        .sort_values("request_month")
    )
    print(monthly_counts.to_string(index=False))

    print("\nMissing values in analytical fields:")
    analytical_columns = [
        "service_request_id",
        "date_requested",
        "date_closed",
        "status",
        "service_name",
        "zipcode",
        "council_district",
        "comm_plan_name",
        "lat",
        "lng",
    ]
    print(data[analytical_columns].isna().sum())


if __name__ == "__main__":
    main()