CREATE OR REPLACE TASK summarize_daily_bids
  WAREHOUSE = compute_wh
  SCHEDULE = 'USING CRON 0 0 * * * UTC'  -- Runs daily at midnight UTC
AS
MERGE INTO bid_summary_table AS target
USING (
  SELECT
    CURRENT_DATE() AS summary_date,
    $1:site.domain::STRING AS site_domain,
    COUNT(*) AS total_bids
  FROM @bid_logs_stage (FILE_FORMAT => 'json')
  WHERE $1:site.domain IS NOT NULL
  GROUP BY $1:site.domain
) AS source
ON target.summary_date = source.summary_date
   AND target.site_domain = source.site_domain
WHEN NOT MATCHED THEN
  INSERT (summary_date, site_domain, total_bids)
  VALUES (source.summary_date, source.site_domain, source.total_bids);
