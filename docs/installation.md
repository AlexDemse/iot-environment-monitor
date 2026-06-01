# Installation Documentation

## Tools Installed

### Cursor IDE
Purpose:
Used as the main development environment for coding the project.

---

### Python 3.14
Purpose:
Used for MQTT communication, data processing, and database integration.

Verification Command:
python --version

---

### Docker Desktop
Purpose:
Used to run containerized services such as Mosquitto MQTT broker, MongoDB, and databases.

Verification Command:
docker --version

---

### MySQL Workbench
Purpose:
Used for SQL database management and visualization.

---

### Neo4j Desktop
Purpose:
Used for graph database creation and visualization.

---

### Paho MQTT Python Library
Installation Command:
pip install paho-mqtt

Purpose:
Allows Python applications to communicate using the MQTT protocol.

### MongoDB
Purpose:
Used to store raw IoT sensor messages as flexible JSON-like documents.

Run Command:
docker run -d --name mongodb -p 27017:27017 mongo

Connection String:
mongodb://localhost:27017

Python Library:
pymongo

Install Command:
pip install pymongo

---

### MongoDB Compass
Purpose:
Used as a graphical interface to inspect MongoDB databases, collections, and documents.

Connection String:
mongodb://localhost:27017

---

### MySQL Docker Container
Purpose:
Used to store structured environmental sensor readings in relational table format.

Run Command:
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=root123 -p 3306:3306 -d mysql:latest

Workbench Connection:
Host: localhost
Port: 3306
User: root
Password: root123

---

### MySQL Python Connector
Purpose:
Allows the Python subscriber application to connect to MySQL and insert structured sensor readings.

Install Command:
pip install mysql-connector-python
