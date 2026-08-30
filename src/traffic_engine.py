def calculate_traffic_risk(traffic_level):
    """
    Convert traffic level (0–100)
    into a traffic-risk score.
    """

    traffic_level = max(0, min(traffic_level, 100))

    return round(traffic_level, 2)


def get_traffic_status(traffic_level):
    """
    Convert traffic level into a readable status.
    """

    if traffic_level < 30:
        return "🟢 Low Traffic"

    elif traffic_level < 60:
        return "🟡 Moderate Traffic"

    elif traffic_level < 80:
        return "🟠 Heavy Traffic"

    else:
        return "🔴 Severe Traffic"


def process_traffic_data(routes):
    """
    Add traffic risk and traffic status
    to the route DataFrame.
    """

    routes = routes.copy()

    routes["traffic_risk"] = routes[
        "traffic"
    ].apply(calculate_traffic_risk)

    routes["traffic_status"] = routes[
        "traffic"
    ].apply(get_traffic_status)

    return routes
