import requests


def get_live_weather(latitude, longitude, api_key=None):
    """
    Fetch live weather data.

    If no API key is provided, return None so that
    the prototype can continue using synthetic data.
    """

    if not api_key:
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "temperature_c": data["main"]["temp"],
            "rainfall_mm": data.get(
                "rain",
                {}
            ).get(
                "1h",
                0
            ),
            "weather_condition": data[
                "weather"
            ][0]["main"]
        }

    except requests.RequestException:
        return None
