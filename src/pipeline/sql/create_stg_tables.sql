IF OBJECT_ID('stg.machine_events_clean','U') IS NOT NULL
BEGIN
    DROP TABLE stg.machine_events_clean;
END;

CREATE TABLE stg.machine_events_clean (
    stg_event_id INT IDENTITY(1,1) PRIMARY KEY,
    raw_event_id INT NOT NULL,
    source_file_name VARCHAR(255) NULL,
    event_id VARCHAR(100) NULL,
    machine_id VARCHAR(100) NULL,
    production_line VARCHAR(100) NULL,
    event_timestamp DATETIME2 NULL,
    signal_name VARCHAR(100) NULL,
    signal_value FLOAT NULL,
    status VARCHAR(100) NULL,
    batch_id VARCHAR(100) NULL,
    created_at DATETIME2 NULL,
    loaded_at DATETIME2 NULL,
    transformed_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);