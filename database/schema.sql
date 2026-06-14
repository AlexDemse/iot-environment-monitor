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