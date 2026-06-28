# webapp/streamlit_app.py
# A PURE-PYTHON web dashboard built with Streamlit. No JavaScript or HTML to write.
# It reuses the existing db/ modules and provides every CLI feature plus trend charts.
#
# Run with:  streamlit run webapp/streamlit_app.py
# It opens in your browser automatically (usually http://localhost:8501).

import sys
import os
import time

import pandas as pd
import streamlit as st

# Allow importing config and db from the project root.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import mongo_store
from db import mysql_store
from db import neo4j_store

st.set_page_config(page_title="IoT Environment Dashboard", layout="wide")
st.title("IoT Environment Dashboard")
st.caption("MQTT · MySQL · MongoDB · Neo4j — pure Python (Streamlit)")


def safe(fn, default):
    """Run a function that touches a database; show an error instead of crashing."""
    try:
        return fn()
    except Exception as e:
        st.error("Database error: " + str(e))
        return default


# ---------- sidebar ----------
st.sidebar.header("Controls")
if st.sidebar.button("↻ Refresh now"):
    st.rerun()
auto = st.sidebar.checkbox("Auto-refresh every 10s", value=False)


# ---------- top metrics ----------
locations = safe(mysql_store.list_locations, [])
sensors = safe(mongo_store.list_sensors, [])
alert_counts = safe(mongo_store.get_alert_counts, [])
readings_rows = safe(lambda: mysql_store.aggregate_readings(), [])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Locations", len(locations))
c2.metric("Sensors", len(sensors))
c3.metric("Alerts", sum(c["count"] for c in alert_counts))
c4.metric("Readings (rows)", sum(r[1] for r in readings_rows))

tab_read, tab_alert, tab_topo, tab_live, tab_perf, tab_manage = st.tabs(
    ["Readings", "Alerts", "Topology", "Live feed", "Performance", "Manage"])


# ---------- 1) Aggregate readings ----------
with tab_read:
    st.subheader("Aggregate readings")
    col_a, col_b = st.columns(2)
    loc = col_a.selectbox("Location", ["All locations"] + locations)
    hours = col_b.number_input("Last hours (0 = all time)", min_value=0, value=0, step=1)
    loc_arg = None if loc == "All locations" else loc
    hours_arg = None if hours == 0 else int(hours)

    rows = safe(lambda: mysql_store.aggregate_readings(loc_arg, hours_arg), [])
    if not rows:
        st.info("No readings for this filter yet.")
    else:
        df = pd.DataFrame([{
            "Location": r[0], "Count": r[1],
            "Temp avg": r[2], "Temp min": r[3], "Temp max": r[4],
            "Humidity avg": r[5], "Humidity min": r[6], "Humidity max": r[7],
            "Air avg": r[8], "Air min": r[9], "Air max": r[10],
        } for r in rows])
        chart = df.set_index("Location")[["Temp avg", "Humidity avg", "Air avg"]]
        st.bar_chart(chart)
        st.dataframe(df, use_container_width=True, hide_index=True)


# ---------- 2) Alerts ----------
with tab_alert:
    st.subheader("Alerts")
    atype = st.selectbox("Type", ["All", "temperature", "humidity", "air_quality"])
    type_arg = None if atype == "All" else atype

    if alert_counts:
        cdf = pd.DataFrame([{"Type": c["_id"], "Count": c["count"]} for c in alert_counts])
        st.bar_chart(cdf.set_index("Type"))
    else:
        st.info("No alerts recorded yet.")

    events = safe(lambda: mongo_store.find_alerts(alert_type=type_arg, limit=20), [])
    recent = []
    for ev in events:
        for a in ev.get("alerts", []):
            if type_arg and a["type"] != type_arg:
                continue
            recent.append({
                "Time": str(ev.get("timestamp", "")), "Location": ev.get("location", ""),
                "Type": a["type"], "Level": a["level"],
                "Value": a["value"], "Threshold": a["threshold"],
            })
    if recent:
        st.dataframe(pd.DataFrame(recent), use_container_width=True, hide_index=True)
    else:
        st.caption("No recent alerts to show.")


# ---------- 3) Topology ----------
with tab_topo:
    st.subheader("Network topology")
    topo = safe(neo4j_store.get_topology, [])
    if topo:
        df = pd.DataFrame(topo)[["sensor", "gateway", "room", "location", "zone", "signal"]]
        df.columns = ["Sensor", "Gateway", "Room", "Location", "Zone", "Signal"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No network data yet.")


# ---------- 4) Live feed ----------
with tab_live:
    st.subheader("Live feed")
    st.caption("Most recent stored events. Keep the subscriber running so data is saved.")
    feed = safe(lambda: mongo_store.recent_events(limit=15), [])
    rows = []
    for d in feed:
        if d.get("source_topic") == "sensors/environment":
            rd = d.get("readings", {})
            rows.append({
                "Kind": "ENV", "Time": str(d.get("timestamp", "")),
                "Sensor": d.get("sensor_id", ""), "Location": d.get("location", ""),
                "Detail": f"{rd.get('temperature')}°C · {rd.get('humidity')}% · air {rd.get('air_quality')}",
                "Alerts": len(d.get("alerts", [])),
            })
        else:
            rows.append({
                "Kind": "NET", "Time": "",
                "Sensor": d.get("sensor_id", ""), "Location": d.get("location", ""),
                "Detail": f"→ {d.get('connected_to', '')} · signal {d.get('signal_strength')}",
                "Alerts": "",
            })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Waiting for data…")


# ---------- 5) Performance ----------
with tab_perf:
    st.subheader("Performance metrics (store time per database)")
    stats = safe(mongo_store.get_timing_stats, [])
    if stats:
        df = pd.DataFrame([{
            "Database": s["_id"], "Samples": s["samples"],
            "Avg (s)": s["avg"], "Min (s)": s["min"], "Max (s)": s["max"],
        } for s in stats])
        st.bar_chart(df.set_index("Database")[["Avg (s)"]])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No timings recorded yet.")


# ---------- Manage (add sensors / locations) ----------
with tab_manage:
    st.subheader("Add sensors & locations")
    col_s, col_l = st.columns(2)

    with col_s:
        st.markdown("**New sensor**")
        with st.form("sensor_form"):
            sid = st.text_input("Sensor ID", placeholder="S006")
            zone = st.text_input("Zone", placeholder="North_Zone")
            location = st.text_input("Location", placeholder="Messina_Center")
            room = st.text_input("Room", placeholder="Room_201")
            gateway = st.text_input("Gateway", placeholder="Gateway_F")
            if st.form_submit_button("Add sensor"):
                fields = {"sensor_id": sid, "zone": zone, "location": location,
                          "room": room, "gateway": gateway}
                missing = [k for k, v in fields.items() if not v.strip()]
                if missing:
                    st.error("Missing: " + ", ".join(missing))
                else:
                    safe(lambda: mongo_store.add_sensor({k: v.strip() for k, v in fields.items()}), None)
                    st.success("Sensor added — it will start sending data shortly.")

    with col_l:
        st.markdown("**New location**")
        with st.form("location_form"):
            lname = st.text_input("Location name", placeholder="Messina_Mall")
            lzone = st.text_input("Zone", placeholder="East_Zone")
            if st.form_submit_button("Add location"):
                if not lname.strip() or not lzone.strip():
                    st.error("Name and zone are required.")
                else:
                    safe(lambda: mongo_store.add_location({"name": lname.strip(), "zone": lzone.strip()}), None)
                    st.success("Location added.")
        st.caption("New sensors start generating data automatically "
                   "(the simulator reads this registry).")

    st.markdown("---")
    st.markdown("**Registered sensors**")
    reg = safe(mongo_store.list_sensors, [])
    if reg:
        st.dataframe(
            pd.DataFrame(reg)[["sensor_id", "zone", "location", "room", "gateway"]],
            use_container_width=True, hide_index=True)
        with st.form("delete_sensor_form"):
            target = st.selectbox("Remove a sensor", [r["sensor_id"] for r in reg])
            if st.form_submit_button("Delete sensor"):
                # Remove the sensor everywhere so the views stay consistent:
                # registry + its MongoDB events + MySQL rows + Neo4j graph nodes.
                safe(lambda: mongo_store.delete_sensor(target), None)
                safe(lambda: mongo_store.delete_sensor_events(target), None)
                safe(lambda: mysql_store.delete_sensor_readings(target), None)
                safe(lambda: neo4j_store.delete_sensor(target), None)
                st.success("Deleted sensor " + target + " and all its data.")
                st.rerun()
    else:
        st.caption("No sensors registered yet.")

    st.markdown("**Registered locations**")
    locs = safe(mongo_store.list_location_registry, [])
    if locs:
        st.dataframe(pd.DataFrame(locs)[["name", "zone"]],
                     use_container_width=True, hide_index=True)
        with st.form("delete_location_form"):
            ltarget = st.selectbox("Remove a location", [l["name"] for l in locs])
            if st.form_submit_button("Delete location"):
                safe(lambda: mongo_store.delete_location(ltarget), None)
                st.success("Deleted location " + ltarget + ".")
                st.rerun()
    else:
        st.caption("No locations registered yet.")

    st.markdown("---")
    st.markdown("**Maintenance**")
    st.caption("Removes data for any sensor that is in the databases but no longer "
               "in the registry (e.g. a sensor deleted before this cleanup existed).")
    if st.button("Clean up orphaned data"):
        reg_ids = {r["sensor_id"] for r in safe(mongo_store.list_sensors, [])}
        graph_ids = {g["sensor"] for g in safe(neo4j_store.get_topology, [])}
        orphan_ids = sorted(graph_ids - reg_ids)
        for sid in orphan_ids:
            safe(lambda sid=sid: mongo_store.delete_sensor_events(sid), None)
            safe(lambda sid=sid: mysql_store.delete_sensor_readings(sid), None)
            safe(lambda sid=sid: neo4j_store.delete_sensor(sid), None)
        if orphan_ids:
            st.success("Removed orphaned sensor(s): " + ", ".join(orphan_ids))
        else:
            st.info("Nothing to clean up — everything is consistent.")
        st.rerun()


# ---------- auto-refresh ----------
if auto:
    time.sleep(10)
    st.rerun()
