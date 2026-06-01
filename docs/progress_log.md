# Progress Log

## SETUP
- Initialized Git repository
- Created GitHub repository
- Installed Paho MQTT library
- Successfully ran Mosquitto using Docker
- Implemented MQTT publisher and subscriber
- Verified successful message transmission

## MQTT Communication Successful

- Installed Paho MQTT library
- Ran Eclipse Mosquitto using Docker
- Created MQTT publisher application
- Created MQTT subscriber application
- Successfully transmitted JSON sensor data through MQTT topics
- Verified communication between publisher and subscriber

## MongoDB Integration Started

- Installed the `pymongo` Python library.
- Started a MongoDB container using Docker.
- Tested Python connection to MongoDB.
- Created `iot_database` database.
- Created `sensor_data` collection.
- Updated the MQTT subscriber to decode incoming JSON messages.
- Inserted received sensor readings into MongoDB.
- Verified that MQTT data is now being stored persistently instead of only being printed.
- Installed MongoDB Compass to visually see the data 

Current flow:

Publisher → Mosquitto MQTT Broker → Subscriber → MongoDB

## MySQL Integration Started

- Started a MySQL container using Docker.
- Created a MySQL Workbench connection named `iot_DB`.
- Created the `iot_database` database.
- Created the `sensor_readings` table for structured environmental data.
- Installed the `mysql-connector-python` library.
- Prepared to connect the Python subscriber to MySQL.

Current system flow:

Publisher → Mosquitto MQTT Broker → Subscriber → MongoDB  
Next target:

Publisher → Mosquitto MQTT Broker → Subscriber → MongoDB + MySQL