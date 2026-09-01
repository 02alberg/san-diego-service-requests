# San Diego Service Request Analysis

An end-to-end data analytics project examining City of San Diego
Get It Done service requests submitted during 2025.

The project uses Python to acquire, inspect, clean, validate, and
prepare public service-request data for analysis. Later stages will
use PostgreSQL and Power BI to explore patterns in request volume,
location, category, status, and case-handling time.

## Project Questions

This project is designed to investigate:

- Which service categories receive the most reports?
- How does request volume change by month and weekday?
- Which communities and council districts generate the most requests?
- How long do different categories remain open?
- What proportion of reports are recognized duplicates?
- How do request patterns vary geographically?
- Which categories or locations may show unusually long case times?

## Dataset

The source data comes from the City of San Diego Get It Done system.
A service request is a documented report concerning a non-emergency
public issue, such as illegal dumping, graffiti, potholes, parking
violations, missed collections, or damaged public infrastructure.

The raw extracts include:

- Requests closed during 2025
- Requests closed during 2026
- Requests that remained open when downloaded

These broader extracts are combined because a request submitted during
2025 may have been closed in 2025, closed later in 2026, or still open.

## Current Results

The pipeline currently produces:

- 735,549 rows across the three raw source extracts
- 11 service-request IDs found in more than one source extract
- 389,940 requests submitted during 2025
- 44,616 City-recognized duplicate reports before quality filtering
- 3 records quarantined for impossible date relationships
- 389,937 clean analytical records
- 26 retained analytical columns

Within the clean dataset:

- 44,613 requests are recognized duplicate reports
- Duplicate reports represent 11.44% of clean records
- Illegal Dumping and Parking Violation are the largest categories
- August has the highest monthly request volume
- Every retained service-request ID is unique

## Data Processing

The Python pipeline:

1. Downloads the official City extracts.
2. Profiles their structure and missing values.
3. Combines the three source files.
4. Parses and validates request and closure dates.
5. Resolves requests appearing in multiple extracts.
6. Filters to requests submitted during 2025.
7. Flags City-recognized duplicate reports.
8. Quarantines impossible date relationships.
9. Removes unnecessary descriptive and internal fields.
10. Produces and validates the clean analytical dataset.

When a request appears in multiple source extracts, the pipeline keeps
the currently open version when available. Otherwise, it keeps the
latest closed version. Competing versions remain preserved for audit.

## Project Structure

```text
san-diego-service-requests/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── data_dictionary.md
├── powerbi/
├── sql/
├── src/
│   ├── build_2025_dataset.py
│   ├── download_data.py
│   ├── inspect_anomalies.py
│   ├── inspect_data.py
│   └── summarize_clean_data.py
├── .gitignore
├── README.md
└── requirements.txt