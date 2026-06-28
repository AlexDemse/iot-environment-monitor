import mysql.connector
import config

_connection = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DB,
)


def _cursor():
    _connection.ping(reconnect=True, attempts=3, delay=2)
    return _connection.cursor()


def insert_reading(data):
    """Insert one validated environmental reading."""
    sql = """
        INSERT INTO sensor_readings
        (sensor_id, location, temperature, humidity, air_quality, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        data["sensor_id"],
        data["location"],
        data["temperature"],
        data["humidity"],
        data["air_quality"],
        data["timestamp"],
    )
    cursor = _cursor()
    cursor.execute(sql, values)
    _connection.commit()
    cursor.close()


def list_locations():
    """Return all distinct locations that have readings."""
    cursor = _cursor()
    cursor.execute("SELECT DISTINCT location FROM sensor_readings ORDER BY location")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]


def aggregate_readings(location=None, hours=None):
    """Return avg/min/max temperature, humidity, air quality grouped by location.
    """
    sql = """
        SELECT
            location,
            COUNT(*) AS count,
            AVG(temperature), MIN(temperature), MAX(temperature),
            AVG(humidity), MIN(humidity), MAX(humidity),
            AVG(air_quality), MIN(air_quality), MAX(air_quality)
        FROM sensor_readings
    """
    where = []
    values = []

    if location is not None:
        where.append("location = %s")
        values.append(location)
    if hours is not None:
        where.append("timestamp >= NOW() - INTERVAL %s HOUR")
        values.append(hours)

    if where:
        sql = sql + " WHERE " + " AND ".join(where)

    sql = sql + " GROUP BY location ORDER BY location"

    cursor = _cursor()
    cursor.execute(sql, values)
    rows = cursor.fetchall()
    cursor.close()
    return rows



def delete_sensor_readings(sensor_id):
    """Delete all stored readings for one sensor."""
    cursor = _cursor()
    cursor.execute("DELETE FROM sensor_readings WHERE sensor_id = %s", (sensor_id,))
    _connection.commit()
    cursor.close()
