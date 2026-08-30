
import networkx as nx


def calculate_route_cost(distance, travel_time, risk):
    """
    Calculate weighted cost for a road segment.

    Lower cost = better route.
    """

    return (
        distance
        + travel_time
        + (risk * 0.5)
    )


def build_graph(routes):
    """
    Build a road network graph.

    Each row represents a road segment.
    Blocked roads are excluded.
    """

    graph = nx.DiGraph()

    for _, route in routes.iterrows():

        # Do not use blocked roads
        if int(route["blockage"]) == 1:
            continue

        cost = calculate_route_cost(
            route["distance_km"],
            route["travel_time_min"],
            route["risk"]
        )

        graph.add_edge(
            route["source"],
            route["destination"],
            weight=cost,
            route_id=route["route_id"],
            distance=route["distance_km"],
            travel_time=route["travel_time_min"],
            risk=route["risk"]
        )

    return graph


def find_best_route(
    routes,
    source=None,
    destination=None
):
    """
    Find the lowest-cost route using Dijkstra's algorithm.
    """

    graph = build_graph(routes)

    if graph.number_of_edges() == 0:
        return None

    if source is None:
        source = routes.iloc[0]["source"]

    if destination is None:
        destination = routes.iloc[0]["destination"]

    try:

        path = nx.shortest_path(
            graph,
            source=source,
            target=destination,
            weight="weight"
        )

        total_cost = nx.shortest_path_length(
            graph,
            source=source,
            target=destination,
            weight="weight"
        )

        route_ids = []

        for i in range(len(path) - 1):

            edge = graph[
                path[i]
            ][
                path[i + 1]
            ]

            route_ids.append(
                edge["route_id"]
            )

        return {
            "path": path,
            "route_ids": route_ids,
            "total_cost": round(total_cost, 2)
        }

    except nx.NetworkXNoPath:

        return None
