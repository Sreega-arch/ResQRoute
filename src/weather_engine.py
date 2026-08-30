def calculate_weather_risk(rainfall_mm):
    """
    Convert rainfall into a simple weather-risk score.
    Score range: 0–100.
    """

    if rainfall_mm < 20:
        return 10

    elif rainfall_mm < 40:
        return 30

    elif rainfall_mm < 60:
        return 50

    elif rainfall_mm < 80:
        return 70

    else:
        return 90


def get_weather_status(rainfall_mm):
    """
    Convert rainfall into a readable weather status.
    """

    if rainfall_mm < 20:
        return "🟢 Normal"

    elif rainfall_mm < 40:
        return "🟡 Light Rain"

    elif rainfall_mm < 60:
        return "🟠 Moderate Rain"

    elif rainfall_mm < 80:
        return "🔴 Heavy Rain"

    else:
        return "🚨 Extreme Rain"


def process_weather_data(weather_df):
    """
    Add weather risk and status columns
    to the weather DataFrame.
    """

    weather_df = weather_df.copy()

    weather_df["weather_risk"] = weather_df[
        "rainfall_mm"
    ].apply(calculate_weather_risk)

    weather_df["weather_status"] = weather_df[
        "rainfall_mm"
    ].apply(get_weather_status)

    return weather_df
