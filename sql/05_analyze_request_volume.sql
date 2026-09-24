-- Compare total reports with approximate original issues by category.

SELECT
    service_name,
    COUNT(*) AS total_reports,
    COUNT(*) FILTER (
        WHERE NOT is_duplicate_report
    ) AS approximate_original_reports,
    COUNT(*) FILTER (
        WHERE is_duplicate_report
    ) AS duplicate_reports,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_duplicate_report)
        / COUNT(*),
        2
    ) AS duplicate_rate_percent
FROM analytics.service_requests_2025
WHERE service_name IS NOT NULL
GROUP BY service_name
ORDER BY total_reports DESC
LIMIT 15;

-- Compare monthly totals while accounting for different month lengths.

SELECT
    request_month,
    request_month_name,
    COUNT(*) AS total_reports,
    ROUND(
        COUNT(*)::NUMERIC
        / COUNT(DISTINCT date_requested::DATE),
        1
    ) AS average_reports_per_day,
    COUNT(*) FILTER (
        WHERE NOT is_duplicate_report
    ) AS approximate_original_reports,
    COUNT(*) FILTER (
        WHERE is_duplicate_report
    ) AS duplicate_reports,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_duplicate_report)
        / COUNT(*),
        2
    ) AS duplicate_rate_percent
FROM analytics.service_requests_2025
GROUP BY request_month, request_month_name
ORDER BY request_month;

-- Compare weekday activity while accounting for how many times
-- each weekday occurred during 2025.

SELECT
    request_weekday,
    COUNT(*) AS total_reports,
    COUNT(DISTINCT date_requested::DATE) AS calendar_days,
    ROUND(
        COUNT(*)::NUMERIC
        / COUNT(DISTINCT date_requested::DATE),
        1
    ) AS average_reports_per_day,
    COUNT(*) FILTER (
        WHERE is_duplicate_report
    ) AS duplicate_reports,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_duplicate_report)
        / COUNT(*),
        2
    ) AS duplicate_rate_percent
FROM analytics.service_requests_2025
GROUP BY request_weekday
ORDER BY CASE request_weekday
    WHEN 'Monday' THEN 1
    WHEN 'Tuesday' THEN 2
    WHEN 'Wednesday' THEN 3
    WHEN 'Thursday' THEN 4
    WHEN 'Friday' THEN 5
    WHEN 'Saturday' THEN 6
    WHEN 'Sunday' THEN 7
END;