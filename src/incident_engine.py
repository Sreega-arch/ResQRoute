
import pandas as pd


def get_incident_risk(severity):
    """
    Convert incident severity into a risk value.
    """

    severity = str(severity).lower()

    if severity == "low":
        return 20

    elif severity == "medium":
        return 50

    elif severity == "high":
        return 80

    elif severity == "critical":
        return 100

    return 0


def get_incident_icon(incident_type):
    """
    Return an icon based on incident type.
    """

    incident_type = str(incident_type).lower()

    if "flood" in incident_type:
        return "🌊"

    elif "landslide" in incident_type:
        return "⛰️"

    elif "road" in incident_type:
        return "🛣️"

    elif "bridge" in incident_type:
        return "🌉"

    elif "rain" in incident_type:
        return "🌧️"

    return "⚠️"


def process_incidents(incidents):
    """
    Process incident data and add
    risk and display information.
    """

    incidents = incidents.copy()

    incidents["incident_risk"] = incidents[
        "severity"
    ].apply(get_incident_risk)

    incidents["icon"] = incidents[
        "type"
    ].apply(get_incident_icon)

    return incidents


def get_active_incidents(incidents):
    """
    Return only currently active incidents.
    """

    return incidents[
        incidents["status"].str.lower() == "active"
    ].copy()


def create_incident(
    incident_id,
    incident_type,
    location,
    severity,
    status="Active"
):
    """
    Create a new field incident report.
    """

    return {
        "incident_id": incident_id,
        "type": incident_type,
        "location": location,
        "severity": severity,
        "status": status
    }


def add_incident(incidents, incident):
    """
    Add a new incident to the incident DataFrame.
    """

    new_incident = pd.DataFrame([incident])

    return pd.concat(
        [incidents, new_incident],
        ignore_index=True
    )
