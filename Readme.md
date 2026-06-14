# IoT Environment Monitoring System

## Overview

This project demonstrates the integration of MQTT and Python for real-time IoT data collection, analysis, and storage across multiple database technologies.

The system classifies incoming sensor data and stores it in:

* MongoDB (sensor readings and alerts)
* MySQL (validated environmental data)
* Neo4j (network relationships)

---

## Technologies

* Python
* MQTT (Mosquitto)
* MongoDB
* MySQL
* Neo4j
* Docker Compose

---

## Quick Start

Start required services:

```bash
docker compose up -d
```

Create MySQL schema:

```bash
docker exec -i mysql-db mysql -u root -proot123 < database/schema.sql
```

Run subscriber:

```bash
python subscriber/subscriber.py
```

Run publishers:

```bash
python publisher/publisher.py
python publisher/network_publisher.py
```

---

## Project Structure

```text
publisher/
subscriber/
database/
docs/
docker-compose.yml
README.md
```

---

## Documentation

Detailed documentation is available in the docs folder:

* architecture.md
* database_design.md
* installation.md
* mqtt_setup.md
* progress_log.md
* testing_results.md

---

## Author

Alex Demse

University of Messina
