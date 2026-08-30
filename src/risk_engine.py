"""
risk_engine.py
Transparent, rule-based risk scoring (no ML model needed for the prototype -
per the team's decision to keep decision-making explainable for the demo).

  edge total risk       = weather_risk + incident_risk + traffic_risk   (0-100, capped)
  route risk score       = 0.5 * (distance-weighted average edge risk)
                          + 0.5 * (highest single edge risk on the route)

The "highest edge risk" term makes one severely hazardous segment dominate
the score even if the rest of the route is fine - a flooded 5km stretch
should not get diluted into irrelevance by 200km of clear highway.
"""

RISK_WEIGHTS = {"avg": 0.5, "peak": 0.5}
LOW_THRESHOLD = 40
MEDIUM_THRESHOLD = 70


def edge_total_risk(edge):
    return min(100.0, edge["weather_risk"] + edge["incident_risk"] + edge["traffic_risk"])


def classify(risk_score):
    if risk_score < LOW_THRESHOLD:
        return "Low Risk"
    if risk_score < MEDIUM_THRESHOLD:
        return "Medium Risk"
    return "High Risk"


def route_risk_score(edges, path_edge_ids):
    """path_edge_ids: ordered list of edge_id along a route."""
    total_distance = 0.0
    weighted_risk_sum = 0.0
    peak_risk = 0.0
    for eid in path_edge_ids:
        edge = edges[eid]
        risk = edge_total_risk(edge)
        dist = edge["distance_km"]
        total_distance += dist
        weighted_risk_sum += risk * dist
        peak_risk = max(peak_risk, risk)

    avg_risk = (weighted_risk_sum / total_distance) if total_distance else 0.0
    score = RISK_WEIGHTS["avg"] * avg_risk + RISK_WEIGHTS["peak"] * peak_risk
    return round(min(100.0, score), 1)
