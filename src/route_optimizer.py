import networkx as nx


def calculate_route_cost(distance, travel_time, risk):
    """
    Risk-aware route cost.
    Higher risk receives a strong penalty.
    """

    risk_penalty = risk * 5

    return (
        distance
        + travel_time
        + risk_penalty
    )


def build_graph(routes):

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


def find_best_route(routes, source, destination):

    graph = build_graph(routes)

    if graph.number_of_edges() == 0:
        return None

    try:

        # Dijkstra shortest path
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

        total_distance = 0
        total_time = 0
        total_risk = 0

        # Collect information for every road segment
        for i in range(len(path) - 1):

            edge = graph[
                path[i]
            ][
                path[i + 1]
            ]

            route_ids.append(
                edge["route_id"]
            )

            total_distance += edge["distance"]

            total_time += edge["travel_time"]

            total_risk += edge["risk"]

        # Average risk
        if route_ids:
            average_risk = (
                total_risk / len(route_ids)
            )
        else:
            average_risk = 0

        return {

            "path": path,

            "route_ids": route_ids,

            "total_cost": round(
                total_cost,
                2
            ),

            "total_distance": round(
                total_distance,
                2
            ),

            "total_time": round(
                total_time,
                2
            ),

            "average_risk": round(
                average_risk,
                2
            )
        }

    except nx.NetworkXNoPath:

        return None
