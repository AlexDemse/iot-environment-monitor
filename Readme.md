# IoT Environment Monitoring System

## Project Overview

This project demonstrates the integration of MQTT and Python for real-time IoT data collection, analysis, and storage using multiple database technologies.

The system receives environmental and network sensor data through MQTT topics and stores the data in different databases according to its purpose:

* MongoDB: Stores raw sensor readings and alerts.
* MySQL: Stores validated environmental data.
* Neo4j: Stores network relationships between sensors and gateways.

---

## Technologies Used

* Python
* MQTT (Mosquitto Broker)
* MongoDB
* MySQL
* Neo4j
* Docker Compose

---

## Project Structure

```text
iot-environment-monitor/
│
├── publisher/
│   ├── publisher.py
│   └── network_publisher.py
│
├── subscriber/
│   └── subscriber.py
│
├── database/
│   └── schema.sql
│
├── docker-compose.yml
│
└── README.md
```

---

## Docker Setup

Start all required services:

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

## MySQL Setup

Create the database structure:

```bash
docker exec -i mysql-db mysql -u root -proot123 < database/schema.sql
```

---

## Neo4j Setup

This project uses Neo4j Desktop.

1. Install Neo4j Desktop.
2. Create a local database.
3. Set:

```text
Username: neo4j
Password: root12345
```

4. Start the database.

---

## Running the System

### Start the Subscriber

```bash
python subscriber/subscriber.py
```

### Start the Environmental Publisher

```bash
python publisher/publisher.py
```

### Start the Network Publisher

```bash
python publisher/network_publisher.py
```

---

## MQTT Topics

### Environmental Data

```text
sensors/enviroment
```

Contains:

* Temperature
* Humidity
* Air Quality

### Network Data

```text
sensors/network
```

Contains:

* Sensor ID
* Gateway Connection
* Signal Strength

---

## Alert Generation

Alerts are generated when:

* Temperature > 35°C
* Humidity > 70%
* Air Quality > 150

Generated alerts are stored in MongoDB.

---

## Database Usage

### MongoDB

Stores:

* Environmental sensor readings
* Generated alerts
* Network events

### MySQL

Stores:

* Validated environmental readings

Validation rules:

* Temperature between -50 and 60
* Humidity between 0 and 100
* Air Quality ≥ 0

### Neo4j

Stores:

* Sensors
* Gateways
* Locations
* CONNECTED_TO relationships

---

## Expected Results

After running the publishers:

### MongoDB

* Sensor readings inserted
* Alerts generated when thresholds are exceeded

### MySQL

* Valid environmental data inserted into sensor_readings

### Neo4j

* Sensor-to-Gateway relationships created
* Location relationships stored

---

## Author

Alex Demse

University of Messina

Data Analysis Program
