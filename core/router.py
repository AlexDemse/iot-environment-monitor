import time

from core import alerts
from core import validation
from db import mongo_store
from db import mysql_store
from db import neo4j_store


def _timed(database, store_function, payload):
    """Run a store function, measure how long it took."""
    start = time.perf_counter()
    store_function(payload)
    seconds = time.perf_counter() - start
    mongo_store.record_timing(database, seconds)
    return seconds


def handle_message(topic, data):
    if topic == "sensors/environment":
        return _handle_environment(data)
    elif topic == "sensors/network":
        return _handle_network(data)
    else:
        return "Unknown topic: " + str(topic)


def _handle_environment(data):
    # spelling consistent.
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
    mongo_seconds = _timed("MongoDB", mongo_store.insert_event, document)

    # MySQL: only clean, valid readings.
    if validation.is_valid_for_mysql(data):
        mysql_seconds = _timed("MySQL", mysql_store.insert_reading, data)
        mysql_note = "MySQL %.4fs" % mysql_seconds
    else:
        mysql_note = "MySQL skipped (invalid)"

    alert_note = str(len(found_alerts)) + " alert(s)"
    return ("environment @ " + data["location"] +
            " -> MongoDB %.4fs, " % mongo_seconds + mysql_note + ", " + alert_note)


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
    mongo_seconds = _timed("MongoDB", mongo_store.insert_event, document)

    # Neo4j: build the graph relationships.
    neo4j_seconds = _timed("Neo4j", neo4j_store.insert_network, data)

    return ("network    @ " + data["location"] +
            " -> MongoDB %.4fs, Neo4j %.4fs" % (mongo_seconds, neo4j_seconds))
