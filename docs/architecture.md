# System Architecture

## Project Overview

The system simulates IoT environmental sensors that send data through MQTT.

A Python processing application receives the data and stores it into multiple database systems depending on the data type and usage.

---

## Main Components

1. Simulated IoT Sensors
2. MQTT Broker (Mosquitto)
3. Python Processing Application
4. MySQL Database
5. MongoDB Database
6. Neo4j Graph Database

---

## Data Flow

Sensors → MQTT Broker → Python Processor → Databases

## commands used
- docker run -it -p 1883:1883 eclipse-mosquitto
