-- Create separate areas for imported data and analysis-ready data.

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- The staging table mirrors the CSV exactly.
-- Text columns prevent import failures from values such as 92113.0.

CREATE TABLE IF NOT EXISTS staging.service_requests_2025 (
    service_request_id TEXT,
    service_request_parent_id TEXT,
    date_requested TEXT,
    case_age_days TEXT,
    case_record_type TEXT,
    service_name TEXT,
    service_name_detail TEXT,
    date_closed TEXT,
    status TEXT,
    lat TEXT,
    lng TEXT,
    zipcode TEXT,
    council_district TEXT,
    comm_plan_code TEXT,
    comm_plan_name TEXT,
    park_name TEXT,
    case_origin TEXT,
    referred TEXT,
    source_file TEXT,
    is_duplicate_report TEXT,
    request_month TEXT,
    request_month_name TEXT,
    request_weekday TEXT,
    request_hour TEXT,
    calculated_case_age_days TEXT,
    has_invalid_date_order TEXT
);

-- The analytical table assigns meaningful PostgreSQL data types.

CREATE TABLE IF NOT EXISTS analytics.service_requests_2025 (
    service_request_id BIGINT PRIMARY KEY,
    service_request_parent_id BIGINT,
    date_requested TIMESTAMP NOT NULL,
    case_age_days INTEGER,
    case_record_type TEXT,
    service_name TEXT,
    service_name_detail TEXT,
    date_closed DATE,
    status TEXT NOT NULL
        CHECK (status IN ('Closed', 'Referred', 'In Process', 'New')),
    lat NUMERIC(10, 8),
    lng NUMERIC(11, 8),
    zipcode CHAR(5),
    council_district SMALLINT
        CHECK (council_district BETWEEN 1 AND 9),
    comm_plan_code SMALLINT,
    comm_plan_name TEXT,
    park_name TEXT,
    case_origin TEXT,
    referred TEXT,
    source_file TEXT NOT NULL
        CHECK (
            source_file IN (
                'closed_2025.csv',
                'closed_2026.csv',
                'open_requests.csv'
            )
        ),
    is_duplicate_report BOOLEAN NOT NULL,
    request_month SMALLINT NOT NULL
        CHECK (request_month BETWEEN 1 AND 12),
    request_month_name TEXT NOT NULL,
    request_weekday TEXT NOT NULL,
    request_hour SMALLINT NOT NULL
        CHECK (request_hour BETWEEN 0 AND 23),
    calculated_case_age_days INTEGER,
    has_invalid_date_order BOOLEAN NOT NULL
);