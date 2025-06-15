CREATE OR REPLACE TASK summarize_daily_bids
  WAREHOUSE = compute_wh
  SCHEDULE = 'USING CRON 0 0 * * * UTC'
AS
  WITH domain_counts AS (
    SELECT
      $1:site.domain::string AS site_domain,
      COUNT(*) AS total_bids
    FROM @bid_logs_stage (FILE_FORMAT => 'json')
    WHERE $1:site.domain IS NOT NULL
    GROUP BY $1:site.domain
  )
  INSERT INTO bid_summary_table
  SELECT CURRENT_DATE(), site_domain, total_bids
  FROM domain_counts;
