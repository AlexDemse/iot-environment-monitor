# core/alerts.py
# Builds alert objects when readings cross the thresholds set in config.

import config


def generate_alerts(data):
    """Return a list of alert dictionaries for one environmental reading."""
    alerts = []

    if data["temperature"] > config.TEMP_THRESHOLD:
        alerts.append({
            "type": "temperature",
            "level": "high",
            "value": data["temperature"],
            "threshold": config.TEMP_THRESHOLD,
            "message": "High temperature detected",
        })

    if data["humidity"] > config.HUMIDITY_THRESHOLD:
        alerts.append({
            "type": "humidity",
            "level": "high",
            "value": data["humidity"],
            "threshold": config.HUMIDITY_THRESHOLD,
            "message": "High humidity detected",
        })

    if data["air_quality"] > config.AIR_QUALITY_THRESHOLD:
        alerts.append({
            "type": "air_quality",
            "level": "danger",
            "value": data["air_quality"],
            "threshold": config.AIR_QUALITY_THRESHOLD,
            "message": "Poor air quality detected",
        })

    return alerts
