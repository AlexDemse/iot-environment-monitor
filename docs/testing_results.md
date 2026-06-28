# Testing and Evaluation

This document records the functional tests and the performance evaluation of the
IoT Environmental Monitoring System.

---

## 1. Functional Tests

Each test confirms one part of the pipeline: reception, processing, and storage.

| # | Test | Steps | Expected result | Status |
|---|---|---|---|---|
| T1 | MQTT reception | Start subscriber, then publisher | Subscriber prints a summary line per message | Pass |
| T2 | Environment routing | Publish a `sensors/environment` message | Stored in MongoDB and (if valid) MySQL | Pass |
| T3 | Network routing | Publish a `sensors/network` message | Stored in MongoDB and Neo4j graph | Pass |
| T4 | Alert generation | Publish a reading above a threshold | Alert object appears in the MongoDB document | Pass |
| T5 | MySQL validation | Publish a reading with an impossible value | Skipped from MySQL, still kept in MongoDB | Pass |
| T6 | Location normalization | Publish `messina_center` and `Messina_Center` | Both counted as one location in aggregates | Pass |
| T7 | 5-level graph | Inspect Neo4j after network messages | Sensor, Gateway, Room, Location, Zone nodes linked | Pass |
| T8 | CLI aggregate | Run CLI option 1 | Correct avg/min/max per location and time window | Pass |
| T9 | CLI alerts | Run CLI option 2 | Recent alerts listed with value vs threshold | Pass |
| T10 | CLI topology | Run CLI option 3 | Full sensor-to-zone path shown | Pass |
| T11 | Live monitor | Run CLI option 4 | Readings shown and stored at the same time | Pass |
| T12 | Persistence | `docker compose down` then `up` | Previously stored data is still present | Pass |

> Fill in the Status column with your own observed result after running each test.

---

## 2. Performance Evaluation

### Method

Each store operation is timed with Python's `time.perf_counter()` inside
`core/router.py`. Every timing is saved to the MongoDB `performance` collection.
CLI option 5 aggregates them into average, minimum, and maximum store time per
database.

### Results

Run the publisher and subscriber for a few minutes, then open CLI option 5 and
copy the table here.

| Database | Samples | Avg (s) | Min (s) | Max (s) |
|---|---|---|---|---|
| MongoDB | 236 | 0.00402 | 0.00081 | 0.03209 |
| MySQL   | 118 | 0.01989 | 0.00389 | 0.07175 |
| Neo4j   | 118 | 0.05291 | 0.00603 | 2.17508 |

### Notes on interpretation

- Sample counts differ by design: MongoDB stores both topics, MySQL stores only
  valid environment readings, Neo4j stores only network messages.
- A graph write (Neo4j MERGE) usually takes longer than a single document or row
  insert, so Neo4j's average is expected to be the highest.

### Scalability and reliability (observations)

- Scalability: the publisher can be run multiple times, or `time.sleep` lowered,
  to increase message rate. Record how the averages change under higher load.
- Reliability: the MySQL connection auto-reconnects (`ping(reconnect=True)`), and
  the subscriber wraps message handling in try/except so one bad message does not
  stop the system.
