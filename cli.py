# cli.py
# Simple text menu for the end user.
# Run with:  python cli.py

import json

import paho.mqtt.client as mqtt

import config
from core import router
from db import mongo_store
from db import mysql_store
from db import neo4j_store


def fmt(value):
    """Format a number to 2 decimals, or '-' if it is missing."""
    if value is None:
        return "-"
    return "%.2f" % float(value)


# ---------- 1) Aggregate readings (MySQL) ----------
def menu_aggregate():
    print("\n--- Aggregate readings ---")

    locations = mysql_store.list_locations()
    if len(locations) == 0:
        print("No readings stored yet.")
        return

    print("Locations:")
    print("  0) All locations")
    i = 1
    for loc in locations:
        print("  " + str(i) + ") " + loc)
        i = i + 1

    choice = input("Pick a location number: ").strip()
    location = None
    if choice != "0":
        if choice.isdigit() and 1 <= int(choice) <= len(locations):
            location = locations[int(choice) - 1]
        else:
            print("Invalid choice.")
            return

    hours_input = input("Last how many hours? (blank = all time): ").strip()
    hours = None
    if hours_input != "":
        if hours_input.isdigit():
            hours = int(hours_input)
        else:
            print("Invalid number.")
            return

    rows = mysql_store.aggregate_readings(location=location, hours=hours)
    if len(rows) == 0:
        print("No data for that filter.")
        return

    print("")
    header = "%-18s %6s | %-21s | %-21s | %-21s" % (
        "Location", "Count", "Temp (avg/min/max)",
        "Humidity (avg/min/max)", "Air (avg/min/max)")
    print(header)
    print("-" * len(header))
    for r in rows:
        loc = r[0]
        count = r[1]
        temp = fmt(r[2]) + "/" + fmt(r[3]) + "/" + fmt(r[4])
        hum = fmt(r[5]) + "/" + fmt(r[6]) + "/" + fmt(r[7])
        air = fmt(r[8]) + "/" + fmt(r[9]) + "/" + fmt(r[10])
        print("%-18s %6s | %-21s | %-21s | %-21s" % (loc, count, temp, hum, air))


# ---------- 2) View alerts (MongoDB) ----------
def menu_alerts():
    print("\n--- View alerts ---")
    print("Alert types: 0) all  1) temperature  2) humidity  3) air_quality")
    choice = input("Pick a type: ").strip()
    types = {"1": "temperature", "2": "humidity", "3": "air_quality"}
    alert_type = types.get(choice)  # None means all

    events = mongo_store.find_alerts(alert_type=alert_type, limit=20)
    if len(events) == 0:
        print("No alerts found.")
        return

    print("")
    for event in events:
        time_str = str(event.get("timestamp", "-"))
        location = event.get("location", "-")
        print(time_str + "  @ " + location)
        for a in event.get("alerts", []):
            print("    [" + a["level"] + "] " + a["type"] +
                  " = " + str(a["value"]) +
                  " (threshold " + str(a["threshold"]) + ") - " + a["message"])


# ---------- 3) Network topology (Neo4j) ----------
def menu_topology():
    print("\n--- Network topology ---")
    rows = neo4j_store.get_topology()
    if len(rows) == 0:
        print("No network data stored yet.")
        return

    print("")
    header = "%-8s %-10s %-12s %-18s %-12s %6s" % (
        "Sensor", "Gateway", "Room", "Location", "Zone", "Signal")
    print(header)
    print("-" * len(header))
    for r in rows:
        print("%-8s %-10s %-12s %-18s %-12s %6s" % (
            r.get("sensor") or "-",
            r.get("gateway") or "-",
            r.get("room") or "-",
            r.get("location") or "-",
            r.get("zone") or "-",
            str(r.get("signal")) if r.get("signal") is not None else "-"))


# ---------- 4) Live monitor (writes to DB while showing) ----------
def _on_connect(client, userdata, flags, rc):
    client.subscribe("sensors/#")


def _on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        summary = router.handle_message(msg.topic, data)
        print(summary)
    except Exception as error:
        print("Error:", error)


def menu_live():
    print("\n--- Live monitor (storing data as it arrives) ---")
    print("Press Ctrl-C to stop and return to the menu.\n")

    client = mqtt.Client()
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.connect(config.MQTT_BROKER, config.MQTT_PORT)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nStopped live monitor.")
    finally:
        client.disconnect()


# ---------- main menu ----------
def main():
    while True:
        print("\n=== IoT Environment Monitor ===")
        print(" 1) Aggregate readings")
        print(" 2) View alerts")
        print(" 3) Network topology")
        print(" 4) Live monitor (stores + shows)")
        print(" 0) Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            menu_aggregate()
        elif choice == "2":
            menu_alerts()
        elif choice == "3":
            menu_topology()
        elif choice == "4":
            menu_live()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
