def simulate_flood(routes):
    """
    Simulate flooding on a specific road segment.
    """

    routes = routes.copy()

    # Flood affects Singtam → Ranipool
    mask = routes["route_id"] == "A2"

    routes.loc[mask, "rainfall"] = 85
    routes.loc[mask, "flood_risk"] = 90
    routes.loc[mask, "blockage"] = 1

    return routes


def simulate_landslide(routes):
    """
    Simulate a landslide on a specific road segment.
    """

    routes = routes.copy()

    # Landslide affects Singtam → Ranipool
    mask = routes["route_id"] == "A2"

    routes.loc[mask, "rainfall"] = 75
    routes.loc[mask, "landslide_risk"] = 95
    routes.loc[mask, "blockage"] = 1

    return routes


def simulate_road_blockage(routes):
    """
    Simulate a complete blockage of a road segment.
    """

    routes = routes.copy()

    # Road blockage affects Singtam → Ranipool
    mask = routes["route_id"] == "A2"

    routes.loc[mask, "blockage"] = 1

    return routes


def reset_simulation(routes):
    """
    Reset all simulated conditions.
    """

    routes = routes.copy()

    # Reset affected segment
    mask = routes["route_id"] == "A2"

    routes.loc[mask, "rainfall"] = 20
    routes.loc[mask, "flood_risk"] = 20
    routes.loc[mask, "landslide_risk"] = 15
    routes.loc[mask, "blockage"] = 0

    return routes
