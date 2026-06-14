# Installation Guide

## Overview

This document describes how to install and configure all software required to run the IoT Environmental Monitoring System.

---

# Required Software

## Cursor IDE

Purpose:

Used as the primary development environment for writing and managing project code.

---

## Python 3.14

Purpose:

Used to implement MQTT publishers, subscriber processing logic, alert generation, and database integration.

Verification:

```bash
python --version
```

---

## Docker Desktop

Purpose:

Used to run containerized services required by the project.

Verification:

```bash
docker --version
```

---

## MySQL Workbench

Purpose:

Used to inspect and manage MySQL databases and tables.

---

## Neo4j Desktop

Purpose:

Used to create, manage, and visualize the Neo4j graph database.

---

# Python Dependencies

Install required Python libraries:

```bash
pip install paho-mqtt
pip install pymongo
pip install mysql-connector-python
pip install neo4j
```

---

# Docker Services

The project uses Docker Compose to automatically start required services.

Services:

* Mosquitto MQTT Broker
* MongoDB
* MySQL

Start all services:

```bash
docker compose up -d
```

Verify services are running:

```bash
docker ps
```

Expected containers:

```text
mosquitto
mongodb
mysql-db
```

Stop services:

```bash
docker compose down
```

---

# MQTT Broker Configuration

## Mosquitto MQTT Broker

Purpose:

Receives messages from publishers and forwards them to subscribers.

Connection Information:

```text
Broker: localhost
Port: 1883
```

Topic Structure:

```text
sensors/enviroment
sensors/network
```

The subscriber listens to:

```text
sensors/#
```

which allows it to receive messages from all sensor topics.

---

# MongoDB Configuration

Purpose:

Stores:

* Environmental sensor events
* Network events
* Generated alerts
* Historical event data

Connection String:

```text
mongodb://localhost:27017
```

Database:

```text
iot_database
```

Collection:

```text
sensor_data
```

Optional Tool:

MongoDB Compass

Connection:

```text
mongodb://localhost:27017
```

---

# MySQL Configuration

Purpose:

Stores validated environmental measurements.

Container:

```text
mysql-db
```

Connection:

```text
Host: localhost
Port: 3306
User: root
Password: root123
```

Database:

```text
iot_database
```

## Database Initialization

Create required tables:

```bash
docker exec -i mysql-db mysql -u root -proot123 < database/schema.sql
```

Verification:

```sql
USE iot_database;
SHOW TABLES;
```

Expected table:

```text
sensor_readings
```

---

# Neo4j Configuration

Purpose:

Stores graph relationships between:

* Sensors
* Gateways
* Locations

Database Type:

```text
Neo4j Desktop
```

Connection:

```text
Bolt URL: bolt://localhost:7687
Username: neo4j
Password: root12345
```

Verification:

Open Neo4j Browser and run:

```cypher
MATCH (n)
RETURN n
LIMIT 10;
```

---

# Running the System

## Start Docker Services

```bash
docker compose up -d
```

---

## Start Subscriber

```bash
python subscriber/subscriber.py
```

---

## Start Environmental Publisher

```bash
python publisher/publisher.py
```

---

## Start Network Publisher

```bash
python publisher/network_publisher.py
```

---

# Expected Results

MongoDB:

* Stores environmental events
* Stores network events
* Stores generated alerts

MySQL:

* Stores validated environmental measurements

Neo4j:

* Creates Sensor nodes
* Creates Gateway nodes
* Creates Location nodes
* Creates CONNECTED_TO relationships
* Creates LOCATED_IN relationships

---

# Troubleshooting

## MQTT Connection Error

Verify:

```bash
docker ps
```

and ensure the Mosquitto container is running.

---

## MySQL Table Missing

Initialize schema:

```bash
docker exec -i mysql-db mysql -u root -proot123 < database/schema.sql
```

---

## Neo4j Connection Error

Verify:

* Neo4j Desktop is running
* Bolt service is enabled
* Username and password match subscriber configuration
