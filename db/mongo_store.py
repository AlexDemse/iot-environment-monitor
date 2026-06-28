from datetime import datetime
from pymongo import MongoClient
import config

# We connect once and reuse the same collections.
_client = MongoClient(config.MONGO_URI)
_db = _client[config.MONGO_DB]
collection = _db["sensor_data"]
metrics_collection = _db["performance"]


def insert_event(document):
    collection.insert_one(document)


def find_alerts(alert_type=None, level=None, limit=20):
    query = {"has_alert": True}

    if alert_type is not None:
        query["alerts.type"] = alert_type
    if level is not None:
        query["alerts.level"] = level

    results = collection.find(query).sort("timestamp", -1).limit(limit)
    return list(results)


def record_timing(database, seconds):
    """Save how long one store operation took (in seconds)."""
    metrics_collection.insert_one({
        "database": database,
        "seconds": seconds,
        "timestamp": datetime.now(),
    })


def get_timing_stats():
    """Return avg/min/max store time per database, plus number of samples."""
    pipeline = [
        {"$group": {
            "_id": "$database",
            "samples": {"$sum": 1},
            "avg": {"$avg": "$seconds"},
            "min": {"$min": "$seconds"},
            "max": {"$max": "$seconds"},
        }},
        {"$sort": {"_id": 1}},
    ]
    return list(metrics_collection.aggregate(pipeline))


# --- registry collections (sensors and locations added from the dashboard) ---
sensors_collection = _db["sensors"]
locations_collection = _db["locations"]


def get_alert_counts():
    """Return how many alerts of each type have"""
    pipeline = [
        {"$match": {"has_alert": True}},
        {"$unwind": "$alerts"},
        {"$group": {"_id": "$alerts.type", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    return list(collection.aggregate(pipeline))


def list_sensors():
    """Return all registered sensors."""
    return list(sensors_collection.find({}, {"_id": 0}))


def add_sensor(doc):
    """Add or update one sensor in the registry (keyed by sensor_id)."""
    sensors_collection.update_one(
        {"sensor_id": doc["sensor_id"]}, {"$set": doc}, upsert=True)


def seed_sensors(defaults):
    """Insert the default sensors only if the registry is empty."""
    if sensors_collection.count_documents({}) == 0:
        sensors_collection.insert_many([dict(d) for d in defaults])


def list_location_registry():
    """Return all registered locations."""
    return list(locations_collection.find({}, {"_id": 0}))


def add_location(doc):
    """Add or update one location in the registry (keyed by name)."""
    locations_collection.update_one(
        {"name": doc["name"]}, {"$set": doc}, upsert=True)


def recent_events(limit=15):
    """Return the most recently stored events (newest first) for the live feed."""
    cur = collection.find({}, {"_id": 0}).sort("_id", -1).limit(limit)
    return list(cur)


def delete_sensor(sensor_id):
    """Remove one sensor from the registry."""
    sensors_collection.delete_one({"sensor_id": sensor_id})


def delete_location(name):
    """Remove one location from the registry."""
    locations_collection.delete_one({"name": name})


def delete_sensor_events(sensor_id):
    """Delete all stored events (environment + network) for one sensor."""
    collection.delete_many({"sensor_id": sensor_id})
