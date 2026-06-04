# IoT Environmental Monitoring System

## Overview

This project implements an IoT environmental monitoring system using MQTT, Python, MongoDB, MySQL, and Neo4j.

The system simulates IoT devices that publish environmental and network data through MQTT topics. A Python subscriber receives the messages, processes the data, generates alerts, validates measurements, and routes the information to different databases based on the topic and data type.

---

# Technologies Used

* Python 3
* MQTT
* Eclipse Mosquitto
* MongoDB
* MySQL
* Neo4j
* Docker

---

# System Architecture

Publishers
→ Mosquitto MQTT Broker
→ Python Subscriber
→ MongoDB / MySQL / Neo4j

---

# MQTT Topics

## sensors/environment

Used for:

* temperature
* humidity
* air quality

Routing:

* MongoDB
* MySQL

---

## sensors/network

Used for:

* gateway connections
* signal strength
* network topology

Routing:

* MongoDB
* Neo4j

---

# Installation

## Clone Repository

## Install Python Dependencies

```bash
pip install paho-mqtt
pip install pymongo
pip install mysql-connector-python
pip install neo4j
```

---

## Run MongoDB

```bash
docker run -d --name mongodb -p 27017:27017 mongo
```

---

## Run MySQL

```bash
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=iot_database -p 3306:3306 mysql
```

---

## Run Mosquitto MQTT Broker

```bash
docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto
```

---

## Neo4j Setup

1. Install Neo4j Desktop
2. Create a local database
3. Start the database

Connection URL:

```text
bolt://localhost:7687
```

---

# Create MySQL Table

```sql
CREATE TABLE sensor_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id VARCHAR(50),
    location VARCHAR(100),
    temperature FLOAT,
    humidity FLOAT,
    air_quality INT,
    timestamp VARCHAR(100)
);
```

---

# Running the System

## Terminal 1

Start Mosquitto:

```bash
docker start mosquitto
```

---

## Terminal 2

Run subscriber:

```bash
python .\subscriber\subscriber.py
```

---

## Terminal 3

Run environment publisher:

```bash
python .\publisher\publisher.py
```

---

## Terminal 4

Run network publisher:

```bash
python .\publisher\network_publisher.py
```

---

# Database Roles

## MongoDB

Stores:

* environment events
* network events
* alerts
* flexible event documents

---

## MySQL

Stores:

* validated environmental measurements

---

## Neo4j

Stores:

* sensor relationships
* gateway connections
* location topology



Author: Alex Demse

University of Messina - Data Analysis Program
