
def calculate_risk(
    rainfall,
    traffic,
    road_condition,
    flood_risk,
    blockage
):
    """
    Calculate the overall route risk score.

    Risk factors:
    - Rainfall
    - Traffic
    - Road condition
    - Flood risk
    - Road blockage
    """

    risk_score = (
        (rainfall * 0.10)
        + (traffic * 0.08)
        + ((10 - road_condition) * 2)
        + (flood_risk * 2.5)
        + (blockage * 20)
    )

    # Keep score between 0 and 100
    risk_score = max(0, min(risk_score, 100))

    return round(risk_score, 2)


def get_risk_level(risk_score):
    """Convert risk score into a risk category."""

    if risk_score < 30:
        return "LOW"

    elif risk_score < 60:
        return "MEDIUM"

    else:
        return "HIGH"


def get_risk_status(risk_score):
    """Return a display-friendly risk status."""

    level = get_risk_level(risk_score)

    if level == "LOW":
        return "🟢 LOW RISK"

    elif level == "MEDIUM":
        return "🟡 MEDIUM RISK"

    return "🔴 HIGH RISK"
