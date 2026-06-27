# core/router.py
# Decides where each message goes, based on its MQTT topic.
# This is the one place that ties the databases together.

from core import alerts
from core import validation
from db import mongo_store
from db import mysql_store
from db import neo4j_store


def handle_message(topic, data):
    """Process one decoded message and store it in the right database(s).
    Returns a short text summary of what happened (handy for printing).
    """
    if topic == "sensors/environment":
        return _handle_environment(data)
    elif topic == "sensors/network":
        return _handle_network(data)
    else:
        return "Unknown topic: " + str(topic)


def _handle_environment(data):
    # Keep location spelling consistent across all databases.
    data["location"] = validation.normalize_location(data["location"])

    # MongoDB: full enriched event with alerts.
    found_alerts = alerts.generate_alerts(data)
    document = {
        "sensor_id": data["sensor_id"],
        "location": data["location"],
        "readings": {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "air_quality": data["air_quality"],
        },
        "alerts": found_alerts,
        "has_alert": len(found_alerts) > 0,
        "timestamp": data["timestamp"],
        "source_topic": "sensors/environment",
    }
    mongo_store.insert_event(document)

    # MySQL: only clean, valid readings.
    if validation.is_valid_for_mysql(data):
        mysql_store.insert_reading(data)
        mysql_note = "MySQL: saved"
    else:
        mysql_note = "MySQL: skipped (invalid)"

    alert_note = str(len(found_alerts)) + " alert(s)"
    return ("environment @ " + data["location"] +
            " -> MongoDB ok, " + mysql_note + ", " + alert_note)


def _handle_network(data):
    data["location"] = validation.normalize_location(data["location"])

    # MongoDB: keep a copy of the raw network event.
    document = {
        "event_type": "network",
        "sensor_id": data["sensor_id"],
        "zone": data["zone"],
        "location": data["location"],
        "room": data["room"],
        "connected_to": data["connected_to"],
        "signal_strength": data["signal_strength"],
        "has_alert": False,
        "source_topic": "sensors/network",
    }
    mongo_store.insert_event(document)

    # Neo4j: build the graph relationships.
    neo4j_store.insert_network(data)

    return ("network    @ " + data["location"] +
            " -> MongoDB ok, Neo4j graph updated")
