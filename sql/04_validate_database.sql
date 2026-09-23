-- Validate the typed PostgreSQL dataset against the Python pipeline
-- and confirm that derived fields remain internally consistent.

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT service_request_id) AS unique_request_ids,
    MIN(date_requested) AS earliest_request,
    MAX(date_requested) AS latest_request
FROM analytics.service_requests_2025;


-- Status counts should match the clean-data summary.

SELECT
    status,
    COUNT(*) AS request_count
FROM analytics.service_requests_2025
GROUP BY status
ORDER BY request_count DESC;


-- Confirm how many retained records came from each City extract.

SELECT
    source_file,
    COUNT(*) AS request_count
FROM analytics.service_requests_2025
GROUP BY source_file
ORDER BY request_count DESC;


-- These checks compare pipeline-created fields with values that
-- PostgreSQL can independently derive from the typed source fields.

SELECT
    COUNT(*) FILTER (
        WHERE is_duplicate_report
              IS DISTINCT FROM (service_request_parent_id IS NOT NULL)
    ) AS duplicate_flag_mismatches,

    COUNT(*) FILTER (
        WHERE request_month <> EXTRACT(MONTH FROM date_requested)
    ) AS month_mismatches,

    COUNT(*) FILTER (
        WHERE request_month_name <> TO_CHAR(date_requested, 'FMMonth')
    ) AS month_name_mismatches,

    COUNT(*) FILTER (
        WHERE request_weekday <> TO_CHAR(date_requested, 'FMDay')
    ) AS weekday_mismatches,

    COUNT(*) FILTER (
        WHERE request_hour <> EXTRACT(HOUR FROM date_requested)
    ) AS hour_mismatches,

    COUNT(*) FILTER (
        WHERE date_closed IS NOT NULL
          AND calculated_case_age_days
              IS DISTINCT FROM (date_closed - date_requested::DATE)
    ) AS calculated_age_mismatches
FROM analytics.service_requests_2025;


-- Closed and referred cases should have closure dates, while currently
-- open cases should not have them.

SELECT
    status,
    COUNT(*) AS request_count,
    COUNT(*) FILTER (WHERE date_closed IS NULL) AS missing_closure_dates,
    COUNT(*) FILTER (WHERE date_closed IS NOT NULL) AS present_closure_dates
FROM analytics.service_requests_2025
GROUP BY status
ORDER BY request_count DESC;