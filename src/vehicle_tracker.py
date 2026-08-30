
import pandas as pd


def load_vehicle_data(vehicles):
    """
    Prepare vehicle tracking data.
    """

    vehicles = vehicles.copy()

    vehicles["progress"] = pd.to_numeric(
        vehicles["progress"],
        errors="coerce"
    ).fillna(0)

    vehicles["progress"] = vehicles["progress"].clip(0, 100)

    return vehicles


def get_vehicle(vehicle_data, vehicle_id):
    """
    Get information for a specific vehicle.
    """

    vehicle = vehicle_data[
        vehicle_data["vehicle_id"] == vehicle_id
    ]

    if vehicle.empty:
        return None

    return vehicle.iloc[0]


def get_vehicle_status(progress):
    """
    Determine delivery status from progress.
    """

    if progress <= 0:
        return "Not Started"

    elif progress < 100:
        return "🚚 En Route"

    return "✅ Delivered"


def update_vehicle_progress(
    vehicle_data,
    vehicle_id,
    progress
):
    """
    Update the simulated progress
    of a vehicle.
    """

    vehicle_data = vehicle_data.copy()

    progress = max(0, min(progress, 100))

    vehicle_data.loc[
        vehicle_data["vehicle_id"] == vehicle_id,
        "progress"
    ] = progress

    vehicle_data.loc[
        vehicle_data["vehicle_id"] == vehicle_id,
        "status"
    ] = get_vehicle_status(progress)

    return vehicle_data


def get_active_vehicles(vehicle_data):
    """
    Return vehicles that are currently
    travelling.
    """

    return vehicle_data[
        vehicle_data["progress"] < 100
    ].copy()


def get_delivery_summary(vehicle):
    """
    Create a simple vehicle/delivery summary.
    """

    return {
        "vehicle_id": vehicle["vehicle_id"],
        "cargo": vehicle["cargo"],
        "origin": vehicle["source"],
        "destination": vehicle["destination"],
        "status": get_vehicle_status(
            vehicle["progress"]
        ),
        "progress": vehicle["progress"]
    }
