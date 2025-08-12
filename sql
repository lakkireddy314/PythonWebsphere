SELECT
    p.PROJECT_NAME AS process_app_name,
    COUNT(CASE WHEN i.CREATE_TIME >= CURRENT_DATE - 3 MONTHS THEN 1 END) AS last_3_months_count,
    COUNT(CASE WHEN i.CREATE_TIME >= CURRENT_DATE - 6 MONTHS THEN 1 END) AS last_6_months_count
FROM
    LSW_BPD_INSTANCE i
JOIN
    LSW_PROJECT p
    ON i.PROCESS_APP_ID = p.PROJECT_ID
-- Only include active or completed instances if needed:
-- WHERE i.STATUS IN (0, 1, 2)  -- example status filter
GROUP BY
    p.PROJECT_NAME
ORDER BY
    p.PROJECT_NAME;
