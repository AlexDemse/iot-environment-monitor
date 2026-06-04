# IoT Environmental Monitoring System

## Overview

This project implements an IoT environmental monitoring system using MQTT, Python, MongoDB, MySQL, and Neo4j.

The system simulates IoT sensors that publish environmental and network data through MQTT topics. A Python subscriber receives the messages, processes the data, generates alerts, validates measurements, and routes the information to different databases based on the message topic and data type.

The project demonstrates:

* MQTT-based communication
* event-driven processing
* topic-based routing
* polyglot persistence
* real-time alert generation
* graph relationship modeling

---

# Technologies Used

## Programming Language

* Python 3

## Communication Protocol

* MQTT

## MQTT Broker

* Eclipse Mosquitto

## Databases

* MongoDB
* MySQL
* Neo4j

## Python Libraries

* paho-mqtt
* pymongo
* mysql-connector-python
* neo4j

## Containerization

* Docker

---

# System Architecture

The system architecture consists of:

1. Sensor publishers
2. Mosquitto MQTT broker
3. Python subscriber processing engine
4. MongoDB
5. MySQL
6. Neo4j

## Data Flow

Publishers
→ Mosquitto MQTT Broker
→ Python Subscriber
→ MongoDB / MySQL / Neo4j

---

# MQTT Topics

## Environment Topic

```text
sensors/environment
```

Purpose:

* environmental sensor readings
* temperature
* humidity
* air quality

Routing:

* MongoDB
* MySQL

---

## Network Topic

```text
sensors/network
```

Purpose:

* network topology data
* sensor connections
* gateway relationships
* signal strength

Routing:

* MongoDB
* Neo4j

```
```
# Installation and Setup

## Clone the Repository

```bash
git clone https://github.com/AlexDemse/iot_enviroment-monitor.git
cd iot_enviroment-monitor
```

---

# Install Python Dependencies

Install the required Python libraries:

```bash
pip install paho-mqtt
pip install pymongo
pip install mysql-connector-python
pip install neo4j
```

---

# Install Docker

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

After installation, start Docker Desktop.

---

# Run MongoDB Container

```bash
docker run -d --name mongodb -p 27017:27017 mongo
```

---

# Run MySQL Container

```bash
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=iot_database -p 3306:3306 mysql
```

---

# Run Mosquitto MQTT Broker

```bash
docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto
```

---

# Neo4j Setup

1. Install Neo4j Desktop
2. Create a local database
3. Start the database
4. Set username and password

Default connection:

```text
bolt://localhost:7687
```

---

# Create MySQL Table

Open MySQL Workbench and run:

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
# Running the System

Open multiple terminals and run the components in the following order.

---

# Terminal 1 — Start Mosquitto

```bash id="7qu0c2"
docker start mosquitto
```

---

# Terminal 2 — Start Subscriber

```bash id="hpkj8m"
python .\subscriber\subscriber.py
```

Expected output:

```text id="qv6k91"
connected to MQTT!
waiting for messages..
```

---

# Terminal 3 — Start Environment Publisher

```bash id="6b4bwb"
python .\publisher\publisher.py
```

This publisher sends environmental sensor data using the topic:

```text id="7d2fsh"
sensors/environment
```

---

# Terminal 4 — Start Network Publisher

```bash id="x1m8yl"
python .\publisher\network_publisher.py
```

This publisher sends network topology data using the topic:

```text id="8q1nft"
sensors/network
```

---

# Verifying MongoDB

Open MongoDB Compass and connect to:

```text id="1mztku"
mongodb://localhost:27017
```

Check:

```text id="lxyh7u"
iot_database
→ sensor_data
```

MongoDB stores:

* environment events
* network events
* alerts
* enriched documents

---

# Verifying MySQL

Open MySQL Workbench and run:

```sql id="1ypf6o"
USE iot_database;

SELECT * FROM sensor_readings;
```

MySQL stores:

* validated environmental measurements

---

# Verifying Neo4j

Open Neo4j Browser and run:

```cypher id="bhvk2q"
MATCH (n)-[r]->(m)
RETURN n,r,m;
```

Neo4j stores:

* Sensor nodes
* Gateway nodes
* Location nodes
* CONNECTED_TO relationships
* LOCATED_IN relationships

```
