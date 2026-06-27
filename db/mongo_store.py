# db/mongo_store.py
# Handles all MongoDB work: storing events and reading back alerts.

from pymongo import MongoClient
import config

# We connect once and reuse the same collection.
_client = MongoClient(config.MONGO_URI)
_db = _client[config.MONGO_DB]
collection = _db["sensor_data"]


def insert_event(document):
    """Save one event document (environment or network) into MongoDB."""
    collection.insert_one(document)


def find_alerts(alert_type=None, level=None, limit=20):
    """Return recent events that contain alerts.
    Optional filters: alert_type ('temperature'/'humidity'/'air_quality')
    and level ('high'/'danger').
    """
    query = {"has_alert": True}

    if alert_type is not None:
        query["alerts.type"] = alert_type
    if level is not None:
        query["alerts.level"] = level

    results = collection.find(query).sort("timestamp", -1).limit(limit)
    return list(results)
