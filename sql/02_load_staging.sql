-- Clear the staging table so this script can be rerun without
-- accidentally duplicating the imported records.

TRUNCATE TABLE staging.service_requests_2025;

-- psql requires the complete \copy command to remain on one line.

\copy staging.service_requests_2025 FROM 'data/processed/service_requests_2025_clean.csv' WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8')

-- Confirm that the complete clean dataset reached PostgreSQL.

SELECT COUNT(*) AS staging_row_count
FROM staging.service_requests_2025;