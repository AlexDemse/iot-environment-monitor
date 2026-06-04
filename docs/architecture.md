# System Architecture

## Project Title

IoT Environmental Monitoring System using MQTT, Python, MySQL, MongoDB, and Neo4j

## Overview

This project simulates an IoT environmental monitoring system. Sensor data is published through MQTT, received by a Python subscriber, processed, and then routed to different database platforms based on the MQTT topic and the type of data.


## Main Components

1. Sensor Publishers  
   Simulate IoT devices that generate environmental and network data. 

2. Mosquitto MQTT Broker  
   Receives messages from publishers and forwards them to subscribers based on topics.

3. Python Subscriber / Processing Engine  
   Subscribes to MQTT topics, processes incoming JSON messages, generates alerts, and routes data to the appropriate database.

4. MongoDB  
   Stores enriched environmental event documents, including nested readings and alerts.

5. MySQL  
   Stores clean structured environmental readings for reporting and analysis.

6. Neo4j  
   Stores graph relationships between sensors, gateways, and locations.

## Data Flow

Sensor Publishers
        ↓
Mosquitto MQTT Broker
        ↓
Python Subscriber / Processing Engine
        ↓
MongoDB + MySQL + Neo4j