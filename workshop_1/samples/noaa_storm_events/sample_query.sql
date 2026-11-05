-- Workshop 1 / W1-K03
-- Logical equivalent of the PowerShell evidence-extraction script.
-- Proposed feasibility sample only. Region approval remains pending.
-- The LIMIT is 250 so the evidence remains above the 200-record minimum if the
-- workshop report later excludes demonstrably invalid rows from a derived view.

WITH filtered AS (
    SELECT *
    FROM read_csv_auto(
        'data/raw/noaa_storm_events/details/year=2024/StormEvents_details-ftp_v1.0_d2024_c20260728.csv'
    ) AS details
    WHERE details.STATE = 'OKLAHOMA'
      AND details.YEAR = 2024
      AND details.EVENT_TYPE IN (
          'Heavy Rain',
          'Flash Flood',
          'Flood',
          'Strong Wind',
          'High Wind',
          'Thunderstorm Wind',
          'Excessive Heat',
          'Heat',
          'Cold/Wind Chill',
          'Extreme Cold/Wind Chill',
          'Heavy Snow',
          'Ice Storm',
          'Winter Storm',
          'Winter Weather'
      )
), ranked AS (
    SELECT
        filtered.*,
        row_number() OVER (
            PARTITION BY EVENT_TYPE
            ORDER BY BEGIN_YEARMONTH, BEGIN_DAY, BEGIN_TIME, EVENT_ID
        ) AS sample_rank
    FROM filtered
)
SELECT * EXCLUDE (sample_rank)
FROM ranked
ORDER BY
    CASE WHEN sample_rank <= 25 THEN 0 ELSE 1 END,
    BEGIN_YEARMONTH,
    BEGIN_DAY,
    BEGIN_TIME,
    EVENT_ID
LIMIT 250;

