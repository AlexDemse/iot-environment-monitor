# config.py
# All settings for the project.
# Values are read from a .env file if it exists, otherwise the defaults below are used.

import os


# --- tiny .env reader  ---
def load_env():
    here = os.path.dirname(__file__)
    env_path = os.path.join(here, ".env")
    if not os.path.exists(env_path):
        return
    f = open(env_path)
    for line in f:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()
    f.close()


load_env()


# --- MQTT ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

# --- MongoDB ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "iot_database")

# --- MySQL ---
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root123")
MYSQL_DB = os.getenv("MYSQL_DB", "iot_database")

# --- Neo4j ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "root12345")

# --- Alert thresholds ---
TEMP_THRESHOLD = float(os.getenv("TEMP_THRESHOLD", "35"))
HUMIDITY_THRESHOLD = float(os.getenv("HUMIDITY_THRESHOLD", "70"))
AIR_QUALITY_THRESHOLD = float(os.getenv("AIR_QUALITY_THRESHOLD", "150"))
