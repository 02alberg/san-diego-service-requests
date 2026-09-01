# Data Dictionary

This document describes the columns in
`service_requests_2025_clean.csv`.

The dataset contains City of San Diego Get It Done service requests
submitted during 2025. Each row represents one service request, not
necessarily one distinct physical problem.

## Source Columns

| Column | Description |
|---|---|
| `service_request_id` | Unique identifier assigned to the service request by the City. |
| `service_request_parent_id` | ID of an earlier related request when the City recognizes this report as a duplicate or child request. Missing values usually indicate an original report. |
| `date_requested` | Date and time when the service request was submitted. |
| `case_age_days` | City-provided age of the case in days. For closed cases, this generally represents time until closure. For open cases, it represents age when the source file was downloaded. |
| `case_record_type` | City classification describing the type of case record. |
| `service_name` | Primary service category, such as Illegal Dumping, Pothole, or Parking Violation. |
| `service_name_detail` | More specific service classification when available. |
| `date_closed` | Date when the City recorded the request as closed or referred. Missing for requests that remain open. |
| `status` | Current recorded status: Closed, Referred, In Process, or New. |
| `lat` | Latitude associated with the reported location. |
| `lng` | Longitude associated with the reported location. |
| `zipcode` | ZIP code associated with the request location. |
| `council_district` | San Diego City Council district associated with the request. |
| `comm_plan_code` | City code for the applicable community planning area. |
| `comm_plan_name` | Name of the applicable community planning area. |
| `park_name` | Name of the associated park when the request concerns a park location. |
| `case_origin` | Channel or system through which the request originated. |
| `referred` | Agency or organization to which the request was referred, when applicable. |

## Pipeline Columns

These columns were created by the Python transformation pipeline.

| Column | Description |
|---|---|
| `source_file` | Raw City extract from which the retained version of the record came. |
| `is_duplicate_report` | Boolean value indicating whether `service_request_parent_id` is present. This identifies City-recognized duplicate reports, not accidental duplicate rows. |
| `request_month` | Numeric month in which the request was submitted, from 1 through 12. |
| `request_month_name` | Name of the month in which the request was submitted. |
| `request_weekday` | Name of the weekday on which the request was submitted. |
| `request_hour` | Hour of submission using a 24-hour clock, from 0 through 23. |
| `calculated_case_age_days` | Number of calendar days between the normalized request and closure dates. Missing for open requests. |
| `has_invalid_date_order` | Boolean flag identifying a closure date earlier than the request date. Such records are excluded from the clean dataset and preserved separately. |

## Interpretation Notes

A service request represents a documented resident contact with the
City. Multiple residents may report the same physical problem, so the
number of service requests is not necessarily the number of distinct
issues.

A status of `Closed` indicates that the City concluded its handling of
the request. It does not necessarily prove that physical repair work
was completed.

The field `case_age_days` should be interpreted as administrative
case-handling time rather than guaranteed repair time.

Records with impossible date relationships are stored separately in
`invalid_date_records_2025.csv`. Competing versions of requests found
in multiple source extracts are preserved in
`cross_source_duplicate_ids.csv`.