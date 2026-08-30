
import networkx as nx


def calculate_route_cost(distance, travel_time, risk):
    """
    Calculate the total cost of a route.

    Lower cost = better route.

    Cost =
        Distance × 1
        + Travel Time × 1
        + Risk × 0.5
    """

    return (
        (distance * 1)
        + (travel_time * 1)
        + (risk * 0.5)
    )


def build_graph(routes):
    """
    Build a weighted graph from route data.
    """

    graph = nx.DiGraph()

    for _, route in routes.iterrows():

        # Ignore blocked roads
        if route["blockage"] == 1:
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
            route_id=route["route_id"]
        )

    return graph


def find_best_route(routes):
    """
    Find the lowest-cost route using Dijkstra's algorithm.
    """

    graph = build_graph(routes)

    if graph.number_of_edges() == 0:
        return None

    source = routes.iloc[0]["source"]
    destination = routes.iloc[0]["destination"]

    try:

        path = nx.shortest_path(
            graph,
            source=source,
            target=destination,
            weight="weight"
        )

        route_id = graph[
            path[0]
        ][
            path[1]
        ]["route_id"]

        return route_id

    except nx.NetworkXNoPath:

        return None
