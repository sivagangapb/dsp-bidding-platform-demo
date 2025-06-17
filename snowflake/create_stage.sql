CREATE OR REPLACE STAGE bid_logs_stage
  URL = 's3://dsp-bid-logs-sivaganga/logs/'
  STORAGE_INTEGRATION = DSP_S3_INT
  FILE_FORMAT = (
    TYPE = 'JSON'
  );
