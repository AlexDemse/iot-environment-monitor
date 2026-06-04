import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pymongo import MongoClient
import mysql.connector
from neo4j import GraphDatabase

#connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_database"]
collection = db["sensor_data"]

#connection to MySQL
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="iot_database"
)
mysql_cursor = mysql_connection.cursor()

#connection to Neo4j
NEO4J_URL = "bolt://localhost:7687" 
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "root12345"

neo4j_driver = GraphDatabase.driver(
    NEO4J_URL,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


#connection to MQTT broker
BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/#"

#called on connection successful
def on_connect(client, userdata, flags, rc):
    print("connected to MQTT!")
    client.subscribe(TOPIC)

#define functions
def generate_alerts(data):
    alerts = []

    if data["temperature"] > 35:
        alerts.append({
            "type": "temperature",
            "level": "high",
            "value": data["temperature"],
            "threshold": 35,
            "message": "High temperature detected"
        })

    if data["humidity"] > 70:
        alerts.append({
            "type": "humidity",
            "level": "high",
            "value": data["humidity"],
            "threshold": 70,
            "message": "High humidity detected"
        })

    if data["air_quality"] > 150:
        alerts.append({
            "type": "air_quality",
            "level": "danger",
            "value": data["air_quality"],
            "threshold": 150,
            "message": "Poor air quality detected"
        })

    return alerts

def is_valid_for_mysql(data):
    required_fields = [
        "sensor_id",
        "location",
        "temperature",
        "humidity",
        "air_quality",
        "timestamp"
    ]
    has_required_fields = all(field in data for field in required_fields)
    if not has_required_fields:
        return False

    return (
        -50 <= data["temperature"] <= 60 and
        0 <= data["humidity"] <= 100 and
        data["air_quality"] >= 0
    )

#called when message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    data = json.loads(payload)

    if topic == "sensors/environment":
        #insertion into mongoDB
        alerts = generate_alerts(data)
        mongo_document = {
            "sensor_id": data["sensor_id"],
            "location": data["location"],
            "readings": {
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "air_quality": data["air_quality"]
            },
            "alerts": alerts,
            "has_alert": len(alerts) > 0,
            "timestamp": data["timestamp"],
            "source_topic": topic
        }
        collection.insert_one(mongo_document)
        print("\nEvent inserted into MongoDB")

        #insertion into MySQL
        if is_valid_for_mysql(data):
            sql = """
            INSERT INTO sensor_readings
            (sensor_id, location, temperature, humidity, air_quality, timestamp)
            VALUES(%s,%s,%s,%s,%s,%s)
            """
            values = (
                data["sensor_id"],
                data["location"],
                data["temperature"],
                data["humidity"],
                data["air_quality"],
                data["timestamp"]
            )
            mysql_cursor.execute(sql, values)
            mysql_connection.commit()
            print("Valid data inserted into MySQL")
        else:
            print("Invalid data no insert into MySQL")

    elif topic == "sensors/network":
        #insertion to MongoDB
        network_document = {
            "event_type": "network",
            "sensor_id": data["sensor_id"],
            "location": data["location"],
            "connected_to": data["connected_to"],
            "signal_strength": data["signal_strength"],
            "source_topic": topic
        }

        collection.insert_one(network_document)
        print("Network event stored in MongoDB")

        #insertion into neo4j
        with neo4j_driver.session() as session:
            session.run(
                """
                MERGE (s:Sensor {sensor_id: $sensor_id})
                MERGE (g:Gateway {name: $gateway})
                MERGE (l:Location {name: $location})

                MERGE (s)-[c:CONNECTED_TO]->(g)
                SET c.signal_strength = $signal_strength

                MERGE (s)-[:LOCATED_IN]->(l)
                MERGE (g)-[:LOCATED_IN]->(l)
                """,
                sensor_id=data["sensor_id"],
                gateway=data["connected_to"],
                location=data["location"],
                signal_strength=data["signal_strength"]
            )

        print("Network relationship inserted into Neo4j")
    
    else:
        print("unknown topic", topic)
    
    

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("waiting for messagges..")

client.loop_forever()
