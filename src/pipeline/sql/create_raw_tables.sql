IF OBJECT_ID('raw.machine_events_raw', 'U') IS NOT NULL
BEGIN
    DROP TABLE raw.machine_events_raw;
END;

    CREATE TABLE raw.machine_events_raw (
        raw_event_id INT IDENTITY(1,1) PRIMARY KEY,
        source_file_name VARCHAR(255) NULL,
        event_id VARCHAR(100) NULL,
        machine_id VARCHAR(100) NULL,
        production_line VARCHAR(100) NULL,
        event_timestamp VARCHAR(100) NULL,
        signal_name VARCHAR(100) NULL,
        signal_value VARCHAR(100) NULL,
        status VARCHAR(100) NULL,
        batch_id VARCHAR(100) NULL,
        created_at VARCHAR(100) NULL,
        loaded_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
