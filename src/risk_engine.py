"""
route_optimizer.py
Runs Dijkstra's Algorithm over the road-segment graph to find the safest
fastest route. Each road's cost is a weighted combination of distance,
travel time, and its current risk score - so the algorithm naturally
reroutes around a segment the moment its risk spikes.

    edge_cost = (distance_km * DIST_WEIGHT)
              + (time_min   * TIME_WEIGHT)
              + (risk_score * RISK_WEIGHT)
"""
import heapq

from src import risk_engine, data_loader

DIST_WEIGHT = 1.0
TIME_WEIGHT = 0.5
RISK_KM_WEIGHT = 6.0  # scales risk exposure by the distance travelled through it,
                       # so a hazard's cost impact is proportional to km affected -
                       # not to how many hops the route happens to have


def _adjacency(edges):
    """Build an undirected adjacency list: node -> [(neighbor, edge_id), ...]"""
    adj = {}
    for edge in edges.values():
        adj.setdefault(edge["from"], []).append((edge["to"], edge["edge_id"]))
        adj.setdefault(edge["to"], []).append((edge["from"], edge["edge_id"]))
    return adj


def edge_cost(edges, edge_id):
    edge = edges[edge_id]
    risk = risk_engine.edge_total_risk(edge)  # 0-100
    risk_exposure = (risk / 100.0) * edge["distance_km"] * RISK_KM_WEIGHT
    return (edge["distance_km"] * DIST_WEIGHT) + (edge["time_min"] * TIME_WEIGHT) + risk_exposure


def dijkstra(edges, source, target):
    """Classic Dijkstra's algorithm. Returns (path_nodes, path_edge_ids, total_cost)."""
    adj = _adjacency(edges)
    dist = {source: 0.0}
    prev = {}
    visited = set()
    pq = [(0.0, source)]

    while pq:
        d, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            break
        for neighbor, edge_id in adj.get(node, []):
            if neighbor in visited:
                continue
            new_dist = d + edge_cost(edges, edge_id)
            if new_dist < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_dist
                prev[neighbor] = (node, edge_id)
                heapq.heappush(pq, (new_dist, neighbor))

    if target not in dist:
        return None, None, None

    # reconstruct path
    path_nodes = [target]
    path_edges = []
    cur = target
    while cur != source:
        p_node, p_edge = prev[cur]
        path_edges.append(p_edge)
        path_nodes.append(p_node)
        cur = p_node
    path_nodes.reverse()
    path_edges.reverse()
    return path_nodes, path_edges, round(dist[target], 1)


def route_metrics(edges, path_edge_ids):
    distance = sum(edges[e]["distance_km"] for e in path_edge_ids)
    time_min = sum(edges[e]["time_min"] for e in path_edge_ids)
    risk_score = risk_engine.route_risk_score(edges, path_edge_ids)
    cost = sum(edge_cost(edges, e) for e in path_edge_ids)
    return {
        "distance_km": distance,
        "time_min": time_min,
        "eta": f"{int(time_min // 60)}h {int(time_min % 60)}m",
        "risk_score": risk_score,
        "risk_class": risk_engine.classify(risk_score),
        "cost": round(cost, 1),
        "segments": [edges[e]["label"] for e in path_edge_ids],
        "segment_ids": list(path_edge_ids),
    }


def get_all_routes(edges, source="GHY", target="DEST"):
    """
    Returns metrics for the three named demo routes (A/B/C) PLUS runs real
    Dijkstra over the whole graph to determine which one is actually optimal
    right now. The 'recommended' flag marks whichever route Dijkstra's
    shortest path matches.
    """
    _, dijkstra_edges, _ = dijkstra(edges, source, target)

    results = {}
    for name, node_path in data_loader.NAMED_ROUTES.items():
        edge_ids = _edges_for_node_path(edges, node_path)
        metrics = route_metrics(edges, edge_ids)
        metrics["route_name"] = f"Route {name}"
        metrics["is_recommended"] = (edge_ids == dijkstra_edges)
        results[name] = metrics

    return results


def _edges_for_node_path(edges, node_path):
    """Given an ordered list of node ids, find the connecting edge_id for each hop."""
    edge_ids = []
    for a, b in zip(node_path, node_path[1:]):
        match = next(
            e["edge_id"] for e in edges.values()
            if {e["from"], e["to"]} == {a, b}
        )
        edge_ids.append(match)
    return edge_ids
