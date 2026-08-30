
import pandas as pd


DATA_PATH = "data/"


def load_routes():
    """Load route information."""
    return pd.read_csv(
        f"{DATA_PATH}routes.csv"
    )


def load_weather():
    """Load weather information."""
    return pd.read_csv(
        f"{DATA_PATH}weather.csv"
    )


def load_incidents():
    """Load incident reports."""
    return pd.read_csv(
        f"{DATA_PATH}incidents.csv"
    )


def load_vehicles():
    """Load vehicle tracking data."""
    return pd.read_csv(
        f"{DATA_PATH}vehicles.csv"
    )


def load_road_conditions():
    """Load road condition information."""
    return pd.read_csv(
        f"{DATA_PATH}road_conditions.csv"
    )
