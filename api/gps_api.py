
from datetime import datetime


def create_gps_update(
    vehicle_id,
    latitude,
    longitude,
    speed_kmph=0,
    status="En Route"
):
    """
    Create a GPS location update for a vehicle.
    """

    return {
        "vehicle_id": vehicle_id,
        "latitude": latitude,
        "longitude": longitude,
        "speed_kmph": speed_kmph,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }


def validate_coordinates(latitude, longitude):
    """
    Validate GPS coordinates.
    """

    if not -90 <= latitude <= 90:
        return False

    if not -180 <= longitude <= 180:
        return False

    return True


def get_vehicle_location(vehicle):
    """
    Get the current location of a vehicle
    from the vehicle data.
    """

    latitude = float(vehicle["latitude"])
    longitude = float(vehicle["longitude"])

    if not validate_coordinates(
        latitude,
        longitude
    ):
        return None

    return {
        "vehicle_id": vehicle["vehicle_id"],
        "latitude": latitude,
        "longitude": longitude,
        "status": vehicle["status"],
        "progress": float(vehicle["progress"])
    }
