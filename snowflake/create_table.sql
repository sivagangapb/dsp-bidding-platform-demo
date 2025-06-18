CREATE OR REPLACE TABLE bid_summary_table (
  summary_date DATE,
  site_domain STRING,
  total_bids NUMBER,
  CONSTRAINT unique_daily_domain UNIQUE (summary_date, site_domain)
);
