# Database Design

## Overview

The project uses a polyglot persistence architecture, where different databases are used for different types of data.

The system integrates:

- MongoDB
- MySQL
- Neo4j

Each database has a specialized role.

---

# MongoDB Design

## Purpose

MongoDB stores flexible enriched event documents and acts as the central event archive.

## Stored Data

MongoDB stores:

- environmental events
- network events
- generated alerts
- nested readings
- raw MQTT event information

## Example Use Cases

- storing flexible JSON structures
- storing alert metadata
- preserving historical event data
- handling varying event structures

## Example Document Types

### Environment Event

- readings
- alerts
- alert thresholds
- timestamps

### Network Event

- connected gateway
- signal strength
- sensor metadata

---

# MySQL Design

## Purpose

MySQL stores validated structured environmental measurements.

## Stored Data

- sensor_id
- location
- temperature
- humidity
- air_quality
- timestamp

## Validation Rules

Only data that:
- contains required fields
- falls within acceptable ranges

is inserted into MySQL.

## Purpose of Validation

Validation prevents:
- corrupted readings
- impossible values
- malformed data

from affecting analytics and reports.

---

# Neo4j Design

## Purpose

Neo4j stores graph relationships and network topology information.

## Stored Nodes

- Sensor
- Gateway
- Location

## Stored Relationships

- CONNECTED_TO
- LOCATED_IN

---

# Polyglot Persistence

The project uses different databases for different strengths:

| Database | Strength |
|---|---|
| MongoDB | flexible document storage |
| MySQL | structured relational analysis |
| Neo4j | relationship and graph modeling |

This architecture improves:
- scalability
- flexibility
- data organization
- analytical capabilities