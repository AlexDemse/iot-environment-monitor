# Conclusions

## Summary of Results

The project delivered a working system that integrates an MQTT broker with Python
to collect, process, and store IoT environmental data across three different
database platforms, with the destination chosen by the MQTT topic.

What was achieved:

- A Mosquitto MQTT broker receives data from simulated sensors and forwards it to
  a Python subscriber.
- The subscriber uses the Paho MQTT library, decodes each JSON message, validates
  and enriches it, and routes it based on its topic.
- Topic-based polyglot storage works as designed:
  - `sensors/environment` is stored in MongoDB (enriched events plus alerts) and,
    when valid, in MySQL (clean structured rows).
  - `sensors/network` is stored in MongoDB and in Neo4j as a five-level graph
    (Sensor, Gateway, Room, Location, Zone).
- Real-time processing includes range validation, location normalization, and
  threshold-based alert generation.
- A user-facing command-line interface answers practical questions: average
  temperature by location, recent alerts, network topology, a live monitor, and
  performance metrics.
- Performance is measured automatically: every store operation is timed and the
  results are aggregated per database.
- Data persists across restarts through Docker volumes.

The system therefore satisfies the core technical goals of the brief: MQTT
integration, Python processing with Paho, and topic-driven storage in SQL,
MongoDB, and Neo4j.

## Possible Future Developments

- Replace the simulator with real hardware sensors (for example ESP32 or Raspberry
  Pi devices) publishing to the same topics.
- Add authentication and TLS to the MQTT broker for secure transport.
- Add a web dashboard with live charts on top of the existing query layer.
- Introduce batch or bulk inserts to improve throughput under high message rates.
- Add automated unit and integration tests so the test suite runs on its own.
- Extend the analytics layer with trend detection and predictive alerts.
- Scale horizontally with multiple subscribers and a clustered broker for higher
  data volumes.
