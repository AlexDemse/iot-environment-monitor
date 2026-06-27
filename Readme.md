# IoT Environment Monitoring System

## Overview

Sensors publish data over MQTT. A subscriber receives it, classifies it by topic,
and stores it across three databases. A simple terminal menu lets you read the data
back (averages, alerts, network map).

- **MongoDB** - all events + generated alerts
- **MySQL** - clean, validated environmental readings (for averages/reports)
- **Neo4j** - network graph: Sensor -> Gateway, and Sensor -> Room -> Location -> Zone

## Project structure

```text
config.py            all settings, read from .env (one place for credentials)
.env / .env.example  connection settings and alert thresholds
requirements.txt     Python dependencies

db/                  one module per database
  mongo_store.py     insert events + read alerts
  mysql_store.py     insert readings + aggregate queries
  neo4j_store.py     build graph + read topology

core/                logic only (no database connections)
  validation.py      required-field + range checks, location normalization
  alerts.py          threshold-based alert generation
  router.py          decides which database each topic goes to

publisher/simulator.py   one publisher simulating 5 sensors (env + network)
subscriber/subscriber.py thin: MQTT -> router -> stores

cli.py               interactive menu for the end user

database/schema.sql  MySQL table + index
docker-compose.yml   Mosquitto, MongoDB, MySQL, Neo4j
```

## Setup

Install Python packages:

```bash
pip install -r requirements.txt
```

Start the services:

```bash
docker compose up -d
```

Create the MySQL table:

```bash
docker exec -i mysql-db mysql -u root -proot123 < database/schema.sql
```

## Run

In separate terminals:

```bash
python subscriber/subscriber.py     # listen and store
python publisher/simulator.py       # generate sensor data
```

Then open the user terminal:

```bash
python cli.py
```

Menu options:

1. **Aggregate readings** - avg/min/max temperature, humidity, air quality by location and time window
2. **View alerts** - recent alerts, filter by type
3. **Network topology** - sensor -> gateway -> room -> location -> zone
4. **Live monitor** - shows incoming readings and stores them at the same time

## Configuration

All credentials and thresholds live in `.env`.
Change a password or an alert threshold there - no need to edit the code.

## Author

Alex Demse - University of Messina
