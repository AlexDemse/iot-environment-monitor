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
## Problem Description

The rapid growth of IoT devices has caused an exponential increase in the volume
of data they generate. Environmental sensors continuously produce readings such as
temperature, humidity, and air quality, alongside network information about how the
devices connect. Handling this big data efficiently requires a system that can
receive it in real time, process and validate it, and store it in a way that suits
the shape of each data type. A single database type is rarely ideal for every kind
of data, which motivates a polyglot approach.

## Project Objective

Build an integrated system that uses an MQTT broker and Python to receive, process,
and store IoT sensor data in different database platforms (SQL, MongoDB, and Neo4j),
choosing the storage destination based on the topic of each MQTT message, and to
provide a simple way for an end user to query the stored data.

## MQTT Broker Selection

Several MQTT brokers were considered:

| Broker | Notes |
|---|---|
| Eclipse Mosquitto | Lightweight, open source, very easy to run in Docker, ideal for development and small to medium projects |
| EMQX | Highly scalable and clustered, aimed at very large production deployments; heavier to set up |
| HiveMQ | Enterprise focused with strong tooling; commercial features |
| VerneMQ | Distributed and scalable; more operational overhead |

Eclipse Mosquitto was chosen because it is lightweight, free, well documented, and
runs with a single Docker image. These qualities match the needs of this project,
where the priority is a reliable broker that is quick to set up and simple to
operate, rather than large-scale clustering.
