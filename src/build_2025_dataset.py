from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIRECTORY = PROJECT_ROOT / "data" / "processed"

SOURCE_FILES = [
    "closed_2025.csv",
    "closed_2026.csv",
    "open_requests.csv",
]

TEXT_COLUMNS = [
    "case_record_type",
    "service_name",
    "service_name_detail",
    "status",
    "zipcode",
    "council_district",
    "comm_plan_name",
    "park_name",
    "case_origin",
    "referred",
]

UNNEEDED_SENSITIVE_COLUMNS = [
    "public_description",
    "street_address",
    "sap_notification_number",
    "iamfloc",
    "floc",
]


def load_source_file(file_name: str) -> pd.DataFrame:
    """Load one source file and retain its filename for traceability."""
    file_path = RAW_DATA_DIRECTORY / file_name
    data = pd.read_csv(file_path, low_memory=False)
    data["source_file"] = file_name

    print(f"Loaded {file_name}: {len(data):,} rows")
    return data


def clean_text_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Remove unnecessary whitespace from categorical text fields."""
    for column in TEXT_COLUMNS:
        if column in data.columns:
            data[column] = data[column].astype("string").str.strip()

    return data


def main() -> None:
    """Build the prepared analytical dataset for 2025."""
    PROCESSED_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    source_frames = [
        load_source_file(file_name)
        for file_name in SOURCE_FILES
    ]

    combined = pd.concat(source_frames, ignore_index=True)

    print(f"\nCombined source rows: {len(combined):,}")

    combined["date_requested"] = pd.to_datetime(
        combined["date_requested"],
        errors="coerce",
    )
    combined["date_closed"] = pd.to_datetime(
        combined["date_closed"],
        errors="coerce",
    )

    combined = clean_text_columns(combined)

    duplicate_id_mask = combined.duplicated(
        subset="service_request_id",
        keep=False,
    )

    cross_source_duplicates = combined.loc[duplicate_id_mask].copy()

    repeated_id_count = (
        cross_source_duplicates["service_request_id"].nunique()
    )

    print(
        "Rows with repeated service request IDs across source files: "
        f"{len(cross_source_duplicates):,}"
    )
    print(
        "Unique repeated service request IDs: "
        f"{repeated_id_count:,}"
    )

    if not cross_source_duplicates.empty:
        duplicate_output = (
            PROCESSED_DATA_DIRECTORY
            / "cross_source_duplicate_ids.csv"
        )
        cross_source_duplicates.to_csv(duplicate_output, index=False)

    source_priority = {
        "closed_2025.csv": 1,
        "closed_2026.csv": 2,
        "open_requests.csv": 3,
    }

    combined["_source_priority"] = (
        combined["source_file"].map(source_priority)
    )

    combined = (
        combined
        .sort_values(
            by=[
                "service_request_id",
                "_source_priority",
                "date_closed",
            ],
            na_position="last",
        )
        .drop_duplicates(
            subset="service_request_id",
            keep="last",
        )
        .drop(columns="_source_priority")
        .reset_index(drop=True)
    )

    requests_2025 = combined.loc[
        combined["date_requested"].dt.year == 2025
    ].copy()

    print(f"Requests submitted during 2025: {len(requests_2025):,}")

    requests_2025["is_duplicate_report"] = (
        requests_2025["service_request_parent_id"].notna()
    )

    requests_2025["request_month"] = (
        requests_2025["date_requested"].dt.month
    )
    requests_2025["request_month_name"] = (
        requests_2025["date_requested"].dt.month_name()
    )
    requests_2025["request_weekday"] = (
        requests_2025["date_requested"].dt.day_name()
    )
    requests_2025["request_hour"] = (
        requests_2025["date_requested"].dt.hour
    )

    request_dates = requests_2025["date_requested"].dt.normalize()
    closure_dates = requests_2025["date_closed"].dt.normalize()

    requests_2025["calculated_case_age_days"] = (
        closure_dates - request_dates
    ).dt.days

    requests_2025["has_invalid_date_order"] = (
        requests_2025["date_closed"].notna()
        & (request_dates > closure_dates)
    )

    invalid_dates = requests_2025.loc[
        requests_2025["has_invalid_date_order"]
    ].copy()

    clean_data = requests_2025.loc[
        ~requests_2025["has_invalid_date_order"]
    ].copy()

    print(
        "Recognized duplicate reports in 2025: "
        f"{requests_2025['is_duplicate_report'].sum():,}"
    )
    print(
        "Rows with request dates after closure dates: "
        f"{len(invalid_dates):,}"
    )
    print(f"Clean analytical rows: {len(clean_data):,}")

    invalid_output = (
        PROCESSED_DATA_DIRECTORY
        / "invalid_date_records_2025.csv"
    )
    clean_output = (
        PROCESSED_DATA_DIRECTORY
        / "service_requests_2025_clean.csv"
    )

    invalid_dates.to_csv(invalid_output, index=False)

    clean_data = clean_data.drop(
        columns=UNNEEDED_SENSITIVE_COLUMNS,
        errors="ignore",
    )
    clean_data.to_csv(clean_output, index=False)

    print(f"\nSaved clean dataset to: {clean_output}")
    print(f"Saved invalid-date records to: {invalid_output}")


if __name__ == "__main__":
    main()