# Testing and Results

## Objective

The system was tested to verify:

- MQTT communication
- topic-based routing
- MongoDB storage
- MySQL validation and insertion
- Neo4j graph updates
- alert generation

---

# MQTT Communication Test

## Test

The publisher applications sent MQTT messages to the Mosquitto broker.

## Result

The subscriber successfully received and processed MQTT messages using topic subscriptions.

---

# Environment Topic Test

## Topic

sensors/environment

## Expected Behavior

- MongoDB stores enriched event documents
- MySQL stores validated readings
- alerts generated for abnormal readings

## Result

The system successfully:
- inserted environmental documents into MongoDB
- inserted validated rows into MySQL
- generated alerts for high temperature, humidity, and air quality

---

# Network Topic Test

## Topic

sensors/network

## Expected Behavior

- MongoDB stores network event documents
- Neo4j updates graph relationships

## Result

The system successfully:
- stored network events in MongoDB
- created Sensor, Gateway, and Location nodes
- created CONNECTED_TO and LOCATED_IN relationships

---

# MongoDB Validation

## Result

MongoDB successfully stored:
- nested readings
- alerts arrays
- event metadata
- flexible event structures

---

# MySQL Validation

## Result

MySQL validation correctly:
- rejected invalid values
- rejected incomplete data
- stored only clean structured readings

---

# Neo4j Validation

## Result

Neo4j successfully represented:
- sensor topology
- gateway connections
- location relationships

Graph relationships were verified visually in Neo4j Browser.

---

# Final Result

The final system successfully demonstrated:

- MQTT-based IoT communication
- event-driven processing
- topic-based routing
- polyglot persistence
- multi-database integration
- real-time alert generation
- graph relationship modeling