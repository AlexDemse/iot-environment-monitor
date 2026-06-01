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

## Neo4j Integration


