
def simulate_flood(routes):
    """
    Simulate a flood affecting Route A.
    """

    routes = routes.copy()

    mask = routes["route_id"] == "A"

    routes.loc[mask, "rainfall"] = 85
    routes.loc[mask, "flood_risk"] = 85
    routes.loc[mask, "blockage"] = 1

    return routes


def simulate_landslide(routes):
    """
    Simulate a landslide affecting Route A.
    """

    routes = routes.copy()

    mask = routes["route_id"] == "A"

    routes.loc[mask, "rainfall"] = 75
    routes.loc[mask, "landslide_risk"] = 90
    routes.loc[mask, "blockage"] = 1

    return routes


def simulate_road_blockage(routes):
    """
    Simulate a complete road blockage.
    """

    routes = routes.copy()

    mask = routes["route_id"] == "A"

    routes.loc[mask, "blockage"] = 1

    return routes


def reset_simulation(routes):
    """
    Reset the simulation to normal conditions.
    """

    routes = routes.copy()

    mask = routes["route_id"] == "A"

    routes.loc[mask, "rainfall"] = 20
    routes.loc[mask, "flood_risk"] = 15
    routes.loc[mask, "landslide_risk"] = 10
    routes.loc[mask, "blockage"] = 0

    return routes
