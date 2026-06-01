# MQTT Setup Documentation

## MQTT Overview

MQTT (Message Queuing Telemetry Transport) is a lightweight publish/subscribe communication protocol commonly used in IoT systems.

The project uses MQTT to transmit sensor data from simulated IoT devices to the central processing application.

---

## MQTT Broker

Broker Used:
Eclipse Mosquitto

Reason for Selection:
- lightweight
- easy to configure
- Docker support
- suitable for educational projects

---

## Mosquitto Setup

Docker Command:
docker run -it -p 1883:1883 eclipse-mosquitto

Port 1883 is the default MQTT communication port.

---

## MQTT Architecture

Publisher → Mosquitto Broker → Subscriber

Publisher:
Simulated sensor sending temperature data.

Subscriber:
Python application receiving and processing messages.