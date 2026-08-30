
import requests


def get_route_from_osrm(
    start_lon,
    start_lat,
    end_lon,
    end_lat
):
    """
    Get a route from the OSRM routing service.

    Coordinates must be provided as:
    longitude, latitude
    """

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            return None

        route = data["routes"][0]

        return {
            "distance_km": round(
                route["distance"] / 1000,
                2
            ),
            "travel_time_min": round(
                route["duration"] / 60,
                2
            ),
            "geometry": route[
                "geometry"
            ]
        }

    except requests.RequestException:
        return None
