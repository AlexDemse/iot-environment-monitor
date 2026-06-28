# Installation and Usage Guide

## Overview

This document describes how to install, configure, and run the IoT Environmental
Monitoring System.

---

## Required Software

| Software | Purpose |
|---|---|
| Python 3.x | Runs the publisher, subscriber, and CLI |
| Docker Desktop | Runs Mosquitto, MongoDB, MySQL, and Neo4j containers |
| MongoDB Compass (optional) | Visual inspection of MongoDB data |
| MySQL Workbench (optional) | Visual inspection of MySQL data |
| Neo4j Desktop / Neo4j Browser (optional) | Visual inspection of the graph |

Check Python and Docker are installed:

```bash
python --version
docker --version
```

---

## Python Dependencies

Install everything in one step:

```bash
pip install -r requirements.txt
```

This installs: paho-mqtt, pymongo, mysql-connector-python, neo4j.

---

## Docker Services

All four backend services run through Docker Compose.

Start them:

```bash
docker compose up -d
```

Verify they are running:

```bash
docker ps
```

Expected containers:

```text
mosquitto
mongodb
mysql-db
neo4j
```

Stop them (data is kept):

```bash
docker compose down
```

---

## MQTT Broker

```text
Broker: localhost
Port:   1883
```

Topics:

```text
sensors/environment   -> environmental readings
sensors/network       -> network / connectivity data
```

The subscriber listens to `sensors/#`, so it receives every sensor topic.

---

## Database Configuration

### MongoDB

```text
Connection: mongodb://localhost:27017
Database:   iot_database
Collections: sensor_data, performance
```

Stores environmental events, network events, generated alerts, and performance
timings.

### MySQL

```text
Host: localhost   Port: 3306
User: root        Password: root123
Database: iot_database   Table: sensor_readings
```

Stores validated environmental measurements.

Create the table (PowerShell):

```powershell
Get-Content database/schema.sql | docker exec -i mysql-db mysql -u root -proot123
```

Create the table (bash):

```bash
docker exec -i mysql-db mysql -u root -proot123 < database/schema.sql
```

### Neo4j

```text
Bolt URL: bolt://localhost:7687
Username: neo4j   Password: root12345
Browser:  http://localhost:7474
```

Stores the network graph with five node types: Sensor, Gateway, Room, Location,
Zone, and the relationships CONNECTED_TO, LOCATED_IN, PART_OF, IN_ZONE, SERVES.

If you use Neo4j Desktop instead of the Docker container, add a Remote connection
to `bolt://localhost:7687` (and stop any local Desktop database first to avoid a
port conflict).

---

## Running the System

Open separate terminals.

Start the subscriber (listens and stores):

```bash
python subscriber/subscriber.py
```

Start the publisher (simulates 5 sensors, both environment and network):

```bash
python publisher/simulator.py
```

Open the user terminal:

```bash
python cli.py
```

Menu options:

1. Aggregate readings - avg/min/max temperature, humidity, air quality by location and time
2. View alerts - recent alerts, filter by type
3. Network topology - sensor to gateway to room to location to zone
4. Live monitor - shows incoming readings and stores them at the same time
5. Performance metrics - average store time per database

---

## Expected Results

- MongoDB: environmental events, network events, alerts, performance timings
- MySQL: validated environmental rows
- Neo4j: Sensor / Gateway / Room / Location / Zone nodes and their relationships

---

## Troubleshooting

MQTT connection error: run `docker ps` and confirm the `mosquitto` container is up.

MySQL table missing: re-run the schema command above.

Neo4j connection error: confirm the `neo4j` container (or Neo4j Desktop) is running
and the Bolt URL, username, and password match `.env`.

PowerShell `<` error: PowerShell does not support input redirection; use the
`Get-Content ... | docker exec` form shown above.
