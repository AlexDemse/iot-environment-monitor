CREATE DATABASE IF NOT EXISTS iot_database;

USE iot_database;

CREATE TABLE IF NOT EXISTS sensor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id VARCHAR(50),
    location VARCHAR(100),
    temperature FLOAT,
    humidity FLOAT,
    air_quality FLOAT,
    timestamp DATETIME
);

-- Speeds up the CLI "aggregate by location / time" queries.
CREATE INDEX idx_location_time ON sensor_readings (location, timestamp);