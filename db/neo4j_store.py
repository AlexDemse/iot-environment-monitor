from neo4j import GraphDatabase
import config

_driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
)


def insert_network(data):
    """Create or update the graph for one network message."""
    query = """
        MERGE (s:Sensor {sensor_id: $sensor_id})
        MERGE (g:Gateway {name: $gateway})
        MERGE (r:Room {name: $room})
        MERGE (l:Location {name: $location})
        MERGE (z:Zone {name: $zone})

        MERGE (s)-[c:CONNECTED_TO]->(g)
        SET c.signal_strength = $signal_strength

        MERGE (s)-[:LOCATED_IN]->(r)
        MERGE (r)-[:PART_OF]->(l)
        MERGE (l)-[:IN_ZONE]->(z)
        MERGE (g)-[:SERVES]->(l)
    """
    session = _driver.session()
    session.run(
        query,
        sensor_id=data["sensor_id"],
        gateway=data["connected_to"],
        room=data["room"],
        location=data["location"],
        zone=data["zone"],
        signal_strength=data["signal_strength"],
    )
    session.close()


def get_topology():
    """Return one row per sensor describing its full path:
    sensor, gateway, room, location, zone, signal strength.
    """
    query = """
        MATCH (s:Sensor)-[c:CONNECTED_TO]->(g:Gateway)
        OPTIONAL MATCH (s)-[:LOCATED_IN]->(r:Room)
        OPTIONAL MATCH (r)-[:PART_OF]->(l:Location)
        OPTIONAL MATCH (l)-[:IN_ZONE]->(z:Zone)
        RETURN s.sensor_id AS sensor,
               g.name AS gateway,
               r.name AS room,
               l.name AS location,
               z.name AS zone,
               c.signal_strength AS signal
        ORDER BY zone, location, room, sensor
    """
    session = _driver.session()
    result = session.run(query)
    rows = []
    for record in result:
        rows.append(dict(record))
    session.close()
    return rows


def delete_sensor(sensor_id):
    """Remove a sensor from the graph, then clean up any nodes that are left
    with no sensor attached (orphaned gateway/room/location/zone).
    Shared nodes used by other sensors are kept.
    """
    cleanup = """
        MATCH (s:Sensor {sensor_id: $sensor_id}) DETACH DELETE s
    """
    orphans = [
        "MATCH (g:Gateway) WHERE NOT (g)<-[:CONNECTED_TO]-(:Sensor) DETACH DELETE g",
        "MATCH (r:Room) WHERE NOT (r)<-[:LOCATED_IN]-(:Sensor) DETACH DELETE r",
        "MATCH (l:Location) WHERE NOT (l)<-[:PART_OF]-(:Room) "
        "AND NOT (l)<-[:SERVES]-(:Gateway) DETACH DELETE l",
        "MATCH (z:Zone) WHERE NOT (z)<-[:IN_ZONE]-(:Location) DETACH DELETE z",
    ]
    session = _driver.session()
    session.run(cleanup, sensor_id=sensor_id)
    for q in orphans:
        session.run(q)
    session.close()
