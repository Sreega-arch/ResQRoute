"""
incident_engine.py
Handles field-officer incident reports (blocked roads, floods, accidents
spotted on the ground) and folds them into the affected road segment's risk.
"""
import time
import uuid

INCIDENT_TYPES = ["Road Blockage", "Flood", "Landslide", "Accident", "Bridge Damage"]

_log = []  # in-memory report log, mirrors data/incidents.csv


def submit_incident(edges, edge_id, incident_type, severity, description=""):
    if edge_id not in edges:
        raise ValueError(f"Unknown edge_id: {edge_id}")
    if incident_type not in INCIDENT_TYPES:
        raise ValueError(f"Unknown incident_type: {incident_type}")

    edge = edges[edge_id]
    edge["incident_risk"] = min(100.0, edge["incident_risk"] + float(severity))
    if incident_type in ("Road Blockage", "Bridge Damage") and severity >= 60:
        edge["status"] = "blocked"
    elif edge["incident_risk"] >= 40:
        edge["status"] = "risky"

    report = {
        "incident_id": str(uuid.uuid4())[:8],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "edge_id": edge_id,
        "incident_type": incident_type,
        "severity": severity,
        "description": description,
    }
    _log.append(report)
    return report


def get_log():
    return list(reversed(_log))


def reset(edges):
    for edge in edges.values():
        edge["incident_risk"] = 0.0
    _log.clear()
