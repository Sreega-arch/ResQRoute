import streamlit as st
import matplotlib.pyplot as plt

from src.data_loader import (
    load_routes,
    load_weather,
    load_incidents,
    load_vehicles,
    load_road_conditions
)

from src.risk_engine import (
    calculate_risk,
    get_risk_level
)

from src.route_optimizer import (
    find_best_route
)

from src.weather_engine import (
    process_weather_data
)

from src.traffic_engine import (
    process_traffic_data
)

from src.incident_engine import (
    create_incident,
    add_incident
)

from src.vehicle_tracker import (
    load_vehicle_data,
    get_vehicle
)

from src.simulator import (
    simulate_flood,
    simulate_landslide,
    simulate_road_blockage,
    reset_simulation
)

from ui.styles import load_css


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ResORoute",
    page_icon="🚚",
    layout="wide"
)

load_css()


# ============================================================
# SESSION STATE
# ============================================================

if "routes" not in st.session_state:
    st.session_state.routes = load_routes()

if "incidents" not in st.session_state:
    st.session_state.incidents = load_incidents()

if "vehicles" not in st.session_state:
    st.session_state.vehicles = load_vehicles()

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "simulation" not in st.session_state:
    st.session_state.simulation = "Normal"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="resoroute-header">

        <div class="resoroute-title">
            🚚 ResORoute
        </div>

        <div class="resoroute-subtitle">
            AI-Powered Smart Routing & Risk Intelligence
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚚 ResORoute")

st.sidebar.caption(
    "NER Logistics Intelligence Platform"
)

st.sidebar.divider()

st.sidebar.subheader("📍 Delivery")

origin = st.sidebar.selectbox(
    "Origin",
    ["Rangpo"]
)

destination = st.sidebar.selectbox(
    "Destination",
    ["Gangtok"]
)

vehicle_id = st.sidebar.selectbox(
    "Vehicle",
    st.session_state.vehicles[
        "vehicle_id"
    ].tolist()
)

st.sidebar.divider()

st.sidebar.subheader(
    "🌧️ Disaster Simulation"
)


if st.sidebar.button(
    "🌊 Simulate Flood",
    use_container_width=True
):

    st.session_state.routes = (
        simulate_flood(
            st.session_state.routes
        )
    )

    st.session_state.simulation = (
        "Flood"
    )

    st.session_state.alerts.insert(
        0,
        "🔴 Flood detected — "
        "Singtam → Ranipool blocked"
    )

    st.rerun()


if st.sidebar.button(
    "⛰️ Simulate Landslide",
    use_container_width=True
):

    st.session_state.routes = (
        simulate_landslide(
            st.session_state.routes
        )
    )

    st.session_state.simulation = (
        "Landslide"
    )

    st.session_state.alerts.insert(
        0,
        "🔴 Landslide detected — "
        "Singtam → Ranipool blocked"
    )

    st.rerun()


if st.sidebar.button(
    "🚧 Simulate Road Blockage",
    use_container_width=True
):

    st.session_state.routes = (
        simulate_road_blockage(
            st.session_state.routes
        )
    )

    st.session_state.simulation = (
        "Road Blockage"
    )

    st.session_state.alerts.insert(
        0,
        "🚧 Road blockage detected — "
        "Route A segment unavailable"
    )

    st.rerun()


if st.sidebar.button(
    "🔄 Reset Simulation",
    use_container_width=True
):

    st.session_state.routes = (
        reset_simulation(
            st.session_state.routes
        )
    )

    st.session_state.simulation = (
        "Normal"
    )

    st.session_state.alerts = []

    st.rerun()


st.sidebar.divider()

st.sidebar.info(
    "Prototype Mode\n\n"
    "Synthetic NER logistics data"
)


# ============================================================
# RISK CALCULATION
# ============================================================

routes = st.session_state.routes.copy()

routes["risk"] = routes.apply(
    lambda row: calculate_risk(
        rainfall=row["rainfall"],
        traffic=row["traffic"],
        road_condition=row["road_condition"],
        flood_risk=row["flood_risk"],
        blockage=row["blockage"]
    ),
    axis=1
)

routes["risk_level"] = (
    routes["risk"]
    .apply(get_risk_level)
)


# ============================================================
# DIJKSTRA
# ============================================================

route_result = find_best_route(
    routes,
    source=origin,
    destination=destination
)


if route_result:

    route_path = route_result[
        "path"
    ]

    best_route_ids = route_result[
        "route_ids"
    ]

    route_cost = route_result[
        "total_cost"
    ]

    total_distance = route_result[
        "total_distance"
    ]

    total_time = route_result[
        "total_time"
    ]

    average_risk = route_result[
        "average_risk"
    ]

else:

    route_path = []
    best_route_ids = []
    route_cost = None
    total_distance = 0
    total_time = 0
    average_risk = 0


# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🚨 Active Alerts",
        len(st.session_state.alerts)
    )

with col2:

    if route_path:

        route_display = (
            " → ".join(route_path)
        )

    else:

        route_display = "Unavailable"

    st.metric(
        "🛣️ Recommended Path",
        route_display
    )

with col3:

    st.metric(
        "⚠️ Average Risk",
        f"{average_risk:.0f}%"
    )

with col4:

    st.metric(
        "⏱️ Estimated Time",
        f"{total_time:.0f} min"
    )


st.divider()


# ============================================================
# MAP + ROUTE RECOMMENDATION
# ============================================================

map_col, route_col = st.columns(
    [1.6, 1]
)


# ============================================================
# SYNTHETIC MAP
# ============================================================

with map_col:

    st.markdown(
        '<div class="section-title">'
        '🗺️ NER Logistics Network'
        '</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    # Route A
    route_a_x = [
        1,
        2.5,
        4,
        5.5,
        7
    ]

    route_a_y = [
        4,
        3.7,
        3.2,
        2.2,
        1
    ]

    route_a_ids = [
        "A1",
        "A2",
        "A3"
    ]

    for i in range(3):

        segment = routes[
            routes["route_id"]
            == route_a_ids[i]
        ].iloc[0]

        x = [
            route_a_x[i],
            route_a_x[i + 1]
        ]

        y = [
            route_a_y[i],
            route_a_y[i + 1]
        ]

        if segment["blockage"] == 1:

            ax.plot(
                x,
                y,
                linestyle="--",
                linewidth=4,
                label=(
                    "Blocked Segment"
                    if i == 1
                    else None
                )
            )

        else:

            ax.plot(
                x,
                y,
                linewidth=3,
                label=(
                    "Route A"
                    if i == 0
                    else None
                )
            )


    # Route B
    route_b_x = [
        1,
        2.2,
        3.5,
        5,
        7
    ]

    route_b_y = [
        4,
        4.8,
        4.6,
        3.5,
        1
    ]

    route_b_ids = [
        "B1",
        "B2",
        "B3"
    ]

    for i in range(3):

        segment = routes[
            routes["route_id"]
            == route_b_ids[i]
        ].iloc[0]

        x = [
            route_b_x[i],
            route_b_x[i + 1]
        ]

        y = [
            route_b_y[i],
            route_b_y[i + 1]
        ]

        ax.plot(
            x,
            y,
            linestyle="--",
            linewidth=3,
            label=(
                "Route B"
                if i == 0
                else None
            )
        )


    # Locations

    ax.scatter(
        1,
        4,
        s=130,
        marker="o"
    )

    ax.scatter(
        7,
        1,
        s=130,
        marker="o"
    )

    ax.text(
        0.75,
        4.25,
        "Rangpo"
    )

    ax.text(
        6.7,
        0.75,
        "Gangtok"
    )


    # Vehicle

    vehicle_data = (
        load_vehicle_data(
            st.session_state.vehicles
        )
    )

    vehicle = get_vehicle(
        vehicle_data,
        vehicle_id
    )

    if vehicle is not None:

        ax.scatter(
            3.5,
            3.3,
            s=180,
            marker="o",
            label="Vehicle"
        )


    ax.set_title(
        "Synthetic NER Transportation Network"
    )

    ax.legend()

    ax.axis("off")

    st.pyplot(
        fig,
        use_container_width=True
    )


# ============================================================
# ROUTE RECOMMENDATION
# ============================================================

with route_col:

    st.markdown(
        '<div class="section-title">'
        '🧭 Route Recommendation'
        '</div>',
        unsafe_allow_html=True
    )

    if route_result:

        st.success(
            "✓ Safest available route selected"
        )

        st.info(
            " → ".join(route_path)
        )

        st.write(
            f"**Distance:** "
            f"{total_distance:.1f} km"
        )

        st.write(
            f"**Travel Time:** "
            f"{total_time:.0f} min"
        )

        st.write(
            f"**Average Risk:** "
            f"{average_risk:.0f}%"
        )

        st.write(
            f"**Route Cost:** "
            f"{route_cost:.2f}"
        )

    else:

        st.error(
            "🚨 No safe route available."
        )

    st.divider()

    for _, route in routes.iterrows():

        risk = route["risk"]

        level = route["risk_level"]

        if level == "LOW":
            status = "🟢 LOW RISK"

        elif level == "MEDIUM":
            status = "🟡 MEDIUM RISK"

        else:
            status = "🔴 HIGH RISK"

        st.markdown(
            f"""
            <div class="route-card">

            <div class="route-name">
                {route['route_id']} —
                {route['route_name']}
            </div>

            <br>

            <b>Risk:</b> {risk:.0f}%<br>
            <b>Status:</b> {status}<br>
            <b>Distance:</b>
            {route['distance_km']} km<br>
            <b>Travel Time:</b>
            {route['travel_time_min']} min

            </div>
            """,
            unsafe_allow_html=True
        )

        if route["route_id"] in best_route_ids:

            st.success(
                "✓ Part of recommended path"
            )

        if route["blockage"] == 1:

            st.error(
                "🚧 ROAD BLOCKED"
            )


# ============================================================
# WEATHER
# ============================================================

st.divider()

weather_col, traffic_col = st.columns(2)


with weather_col:

    st.markdown(
        '<div class="section-title">'
        '🌧️ Weather Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    weather = process_weather_data(
        load_weather()
    )

    st.dataframe(
        weather[
            [
                "location",
                "rainfall_mm",
                "weather_condition",
                "weather_risk",
                "weather_status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TRAFFIC
# ============================================================

with traffic_col:

    st.markdown(
        '<div class="section-title">'
        '🚦 Traffic Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    traffic = process_traffic_data(
        routes
    )

    st.dataframe(
        traffic[
            [
                "route_id",
                "traffic",
                "traffic_status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ALERTS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🚨 Recent Alerts'
    '</div>',
    unsafe_allow_html=True
)

if st.session_state.alerts:

    for alert in (
        st.session_state.alerts[:5]
    ):

        st.markdown(
            f"""
            <div class="alert-danger">
                {alert}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success(
        "✓ No active disruptions detected."
    )


# ============================================================
# VEHICLE TRACKING
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🚚 Vehicle Tracking'
    '</div>',
    unsafe_allow_html=True
)

if vehicle is not None:

    v1, v2, v3, v4 = st.columns(4)

    v1.metric(
        "Vehicle",
        vehicle["vehicle_id"]
    )

    v2.metric(
        "Cargo",
        vehicle["cargo"]
    )

    v3.metric(
        "Progress",
        f"{vehicle['progress']:.0f}%"
    )

    v4.metric(
        "Status",
        vehicle["status"]
    )


# ============================================================
# INCIDENT REPORTING
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '📍 Field Incident Reporting'
    '</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    incident_type = st.selectbox(
        "Incident Type",
        [
            "Flood",
            "Landslide",
            "Road Damage",
            "Bridge Damage",
            "Heavy Rainfall"
        ]
    )

with c2:

    incident_location = st.text_input(
        "Location",
        "Rangpo"
    )

with c3:

    severity = st.selectbox(
        "Severity",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )


description = st.text_input(
    "Description",
    "Road condition update"
)


if st.button(
    "📤 Submit Incident",
    type="primary"
):

    incident_id = (
        f"INC"
        f"{len(st.session_state.incidents) + 1:03d}"
    )

    new_incident = create_incident(
        incident_id,
        incident_type,
        incident_location,
        severity
    )

    st.session_state.incidents = (
        add_incident(
            st.session_state.incidents,
            new_incident
        )
    )

    st.session_state.alerts.insert(
        0,
        f"📍 {incident_type} reported at "
        f"{incident_location} — "
        f"{severity} severity"
    )

    st.success(
        "Incident successfully recorded."
    )

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="resoroute-footer">

        ResORoute • AI-Powered Smart Routing &
        Risk Intelligence

        <br>

        SIH26002 • Prototype using Synthetic Data

    </div>
    """,
    unsafe_allow_html=True
)
