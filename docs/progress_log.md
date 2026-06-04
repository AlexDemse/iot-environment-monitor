# Progress Log

## SETUP
- Initialized Git repository
- Created GitHub repository
- Installed Paho MQTT library
- Successfully ran Mosquitto using Docker
- Implemented MQTT publisher and subscriber
- First successful message transmission
- Message(data) is not persistant(not being saved)


## MQTT Integration

- Installed Paho MQTT library
- Ran Eclipse Mosquitto using Docker
- Created MQTT publisher application
- Created MQTT subscriber application
- Successfully transmitted JSON sensor data through MQTT topics
- Verified communication between publisher and subscriber
- Message(data) not persistant(not being saved)

Flow :
Publisher -> Mosquitto MQTT Broker -> Subscriber 

## MongoDB Integration 

- Installed the `pymongo` Python library
- Started a MongoDB container using Docker
- Tested Python connection to MongoDB
- Created `iot_database` database
- Created `sensor_data` collection
- Updated the MQTT subscriber to decode incoming JSON messages
- Inserted received sensor readings into MongoDB
- Verified that MQTT message(data) is persistant (saved)
- Installed MongoDB Compass to visually see the data 

Flow:
Publisher -> Mosquitto MQTT Broker -> Subscriber -> MongoDB

## MySQL Integration 

- Started a MySQL container using Docker
- Created a MySQL Workbench connection named `iot_DB`
- Created the `iot_database` database
- Created the `sensor_readings` table for structured environmental data
- Installed the `mysql-connector-python` library
- Integrated Python subscriber into MySQL and MongoDB

Flow:
Publisher -> Mosquitto MQTT Broker -> Subscriber -> MongoDB + MySQL 

## Neo4j Integration and Topic-Based Routing

- Installed and tested the official Neo4j Python driver.
- Connected the Python subscriber application to Neo4j using the Bolt protocol.
- Created graph nodes for sensors and locations.
- Created `LOCATED_IN` relationships between sensors and their locations.
- Verified the graph visually in Neo4j Browser.
- Refactored the subscriber to use topic-based routing.
- Updated the MQTT subscriber topic to `sensors/#` so it can receive multiple sensor topics.
- Routed `sensors/environment` messages to MongoDB and MySQL.
- Routed `sensors/network` messages to Neo4j.
- Fixed topic handling using `msg.topic`.
- Confirmed that data is now stored according to message type instead of being sent blindly to every database.

Flow:
- `sensors/environment` -> MongoDB + MySQL
- `sensors/network` -> Neo4j

## MongoDB
- Update MongoDB to include enriched enviromental events and alerts in subscriber
- MongoDB give alerts on temps, air_quality and humidity 

## Event Enrichment and Neo4j Network Topology

- Refactored the system to use topic-based routing instead of sending every message to all databases.
- Updated the subscriber to subscribe to `sensors/#`.
- Implemented routing logic using `msg.topic`.

### Environment Topic
- `sensors/environment` messages are now routed to:
  - MongoDB
  - MySQL

### MongoDB Improvements
- Refactored MongoDB storage into enriched event documents.
- Added nested `readings` objects.
- Added `alerts` arrays.
- Added `has_alert` status field.
- Implemented alert generation logic inside the subscriber.
- Alerts are generated based on environmental thresholds:
  - High temperature
  - High humidity
  - Poor air quality

### MySQL Role
- MySQL now stores clean structured environmental measurements for reporting and analysis.

### Neo4j Improvements
- Refactored Neo4j to focus on graph relationships instead of telemetry storage.
- Added support for `sensors/network` topic.
- Created a dedicated `network_publisher.py`.
- Added graph modeling for:
  - Sensor nodes
  - Gateway nodes
  - Location nodes
- Created graph relationships:
  - `CONNECTED_TO`
  - `LOCATED_IN`

Current routing architecture:

- `sensors/environment` → MongoDB + MySQL
- `sensors/network` → Neo4j

Current architecture:

Publisher(s)
    ↓
Mosquitto MQTT Broker
    ↓
Subscriber Processing Engine
    ↓
MongoDB / MySQL / Neo4j