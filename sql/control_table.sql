-- =========================================================
-- Azure Spend Analytics
-- ADF Metadata / Watermark Control Table
-- =========================================================

CREATE TABLE dbo.pipeline_control
(
    source_name        VARCHAR(100),
    source_object      VARCHAR(100),
    source_path        VARCHAR(500),
    target_path        VARCHAR(500),
    load_type          VARCHAR(20),
    watermark_column   VARCHAR(100),
    last_watermark     DATETIME2,
    is_active          BIT,
    created_date       DATETIME2 DEFAULT GETDATE(),
    updated_date       DATETIME2 DEFAULT GETDATE()
);


-- =========================================================
-- Sample Configuration
-- =========================================================

INSERT INTO dbo.pipeline_control
(
    source_name,
    source_object,
    source_path,
    target_path,
    load_type,
    watermark_column,
    last_watermark,
    is_active
)
VALUES
(
    'SpendCSV',
    'transactions',
    '/landing/spend/',
    '/bronze/spend/',
    'INCREMENTAL',
    'modified_date',
    '2026-01-01 00:00:00',
    1
);


-- =========================================================
-- ADF Lookup Query
-- Returns active pipeline configurations
-- =========================================================

SELECT
    source_name,
    source_object,
    source_path,
    target_path,
    load_type,
    watermark_column,
    last_watermark
FROM dbo.pipeline_control
WHERE is_active = 1;


-- =========================================================
-- Example Incremental Source Query
-- =========================================================

SELECT *
FROM dbo.transactions
WHERE modified_date > @LastWatermark
  AND modified_date <= @CurrentWatermark;


-- =========================================================
-- Update Watermark After Successful Pipeline Execution
-- =========================================================

UPDATE dbo.pipeline_control
SET
    last_watermark = @CurrentWatermark,
    updated_date = GETDATE()
WHERE source_object = 'transactions';
