"""
data_loader.py
Reads the CSV dummy datasets (data/) into plain Python structures used
by the rest of the engine. In a production build these reads would be
replaced by database queries / live API pulls (see README).
"""
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_edges():
    """Returns dict edge_id -> edge record (mutable at runtime for risk updates)."""
    edges = {}
    with open(os.path.join(DATA_DIR, "routes.csv"), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            edges[row["edge_id"]] = {
                "edge_id": row["edge_id"],
                "from": row["from_node"],
                "to": row["to_node"],
                "label": row["label"],
                "distance_km": float(row["distance_km"]),
                "time_min": float(row["time_min"]),
                "base_weather_risk": float(row["base_weather_risk"]),
                "base_traffic_risk": float(row["base_traffic_risk"]),
                # live/mutable fields, reset via reset_edge_state()
                "weather_risk": float(row["base_weather_risk"]),
                "incident_risk": 0.0,
                "traffic_risk": float(row["base_traffic_risk"]),
                "status": "open",
            }
    return edges


def load_vehicles():
    vehicles = {}
    with open(os.path.join(DATA_DIR, "vehicles.csv"), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vehicles[row["vehicle_id"]] = {
                "vehicle_id": row["vehicle_id"],
                "name": row["name"],
                "cargo": row["cargo"],
                "start_node": row["start_node"],
                "dest_node": row["dest_node"],
                "current_route": "A",
                "progress_pct": 32,
                "status": "En Route",
            }
    return vehicles


# Named human-friendly routes through the graph, matching the pitch deck's
# "Route A / Route B / Route C" framing. Real shortest-path selection is
# still computed by route_optimizer.dijkstra() over the full graph.
NAMED_ROUTES = {
    "A": ["GHY", "N1", "N2", "DEST"],
    "B": ["GHY", "N3", "DEST"],
    "C": ["GHY", "N1", "N3", "DEST"],
}

NODE_LABELS = {
    "GHY": "Guwahati",
    "N1": "Nalbari",
    "N2": "Baksa",
    "N3": "Rangia",
    "DEST": "Tawang",
}
