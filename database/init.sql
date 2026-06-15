CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) NOT NULL,
    temperature NUMERIC(6, 2) NOT NULL,
    rpm NUMERIC(8, 2) NOT NULL,
    vibration NUMERIC(6, 4) NOT NULL,
    pressure NUMERIC(6, 2) NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) NOT NULL,
    alert_type VARCHAR(100) NOT NULL,
    metric VARCHAR(50) NOT NULL,
    value NUMERIC(10, 4) NOT NULL,
    threshold NUMERIC(10, 4) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    triggered_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sensor_machine_id ON sensor_readings(machine_id);
CREATE INDEX IF NOT EXISTS idx_sensor_recorded_at ON sensor_readings(recorded_at);
CREATE INDEX IF NOT EXISTS idx_alerts_machine_id ON alerts(machine_id);
CREATE INDEX IF NOT EXISTS idx_alerts_triggered_at ON alerts(triggered_at);