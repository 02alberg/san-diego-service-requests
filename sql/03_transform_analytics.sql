-- Rebuild the analytical table from the staging data.
-- This makes the transformation repeatable without creating duplicates.

TRUNCATE TABLE analytics.service_requests_2025;

INSERT INTO analytics.service_requests_2025 (
    service_request_id,
    service_request_parent_id,
    date_requested,
    case_age_days,
    case_record_type,
    service_name,
    service_name_detail,
    date_closed,
    status,
    lat,
    lng,
    zipcode,
    council_district,
    comm_plan_code,
    comm_plan_name,
    park_name,
    case_origin,
    referred,
    source_file,
    is_duplicate_report,
    request_month,
    request_month_name,
    request_weekday,
    request_hour,
    calculated_case_age_days,
    has_invalid_date_order
)
SELECT
    service_request_id::BIGINT,
    NULLIF(service_request_parent_id, '')::NUMERIC::BIGINT,
    date_requested::TIMESTAMP,
    NULLIF(case_age_days, '')::NUMERIC::INTEGER,
    NULLIF(case_record_type, ''),
    NULLIF(service_name, ''),
    NULLIF(service_name_detail, ''),
    NULLIF(date_closed, '')::DATE,
    status,
    NULLIF(lat, '')::NUMERIC(10, 8),
    NULLIF(lng, '')::NUMERIC(11, 8),

    -- ZIP codes are geographic labels. The numeric conversion removes
    -- the CSV's trailing .0 before storing them as five-character text.
    LPAD(
        NULLIF(zipcode, '')::NUMERIC::INTEGER::TEXT,
        5,
        '0'
    )::CHAR(5),

    NULLIF(council_district, '')::NUMERIC::SMALLINT,
    NULLIF(comm_plan_code, '')::NUMERIC::SMALLINT,
    NULLIF(comm_plan_name, ''),
    NULLIF(park_name, ''),
    NULLIF(case_origin, ''),
    NULLIF(referred, ''),
    source_file,
    is_duplicate_report::BOOLEAN,
    request_month::SMALLINT,
    request_month_name,
    request_weekday,
    request_hour::SMALLINT,
    NULLIF(calculated_case_age_days, '')::NUMERIC::INTEGER,
    has_invalid_date_order::BOOLEAN
FROM staging.service_requests_2025;

-- Validate the most important figures against the Python pipeline.

SELECT
    COUNT(*) AS analytical_rows,
    COUNT(DISTINCT service_request_id) AS unique_request_ids,
    COUNT(*) FILTER (WHERE is_duplicate_report) AS duplicate_reports,
    COUNT(*) FILTER (WHERE date_closed IS NULL) AS missing_closure_dates,
    COUNT(*) FILTER (WHERE has_invalid_date_order) AS invalid_date_rows
FROM analytics.service_requests_2025;