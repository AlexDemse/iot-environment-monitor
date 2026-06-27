# core/validation.py
# Checks and cleans environmental data before it goes into MySQL.

REQUIRED_FIELDS = [
    "sensor_id",
    "location",
    "temperature",
    "humidity",
    "air_quality",
    "timestamp",
]


def normalize_location(name):
    """Make location spelling consistent so 'Messina_center' and
    'Messina_Center' are treated as the same place.
    """
    if name is None:
        return name
    # Capitalize each word split by underscore, e.g. messina_center -> Messina_Center
    parts = name.split("_")
    fixed = []
    for part in parts:
        if part == "":
            fixed.append(part)
        else:
            fixed.append(part[0].upper() + part[1:].lower())
    return "_".join(fixed)


def is_valid_for_mysql(data):
    """Return True only if all required fields exist and values are realistic."""
    for field in REQUIRED_FIELDS:
        if field not in data:
            return False

    if not (-50 <= data["temperature"] <= 60):
        return False
    if not (0 <= data["humidity"] <= 100):
        return False
    if not (data["air_quality"] >= 0):
        return False

    return True
