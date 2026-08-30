import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import (
    load_routes,
    load_weather,
    load_incidents,
    load_vehicles
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
# PAGE CONFIGURATION
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


# Vehicle list
vehicle_list = (
    st.session_state.vehicles["vehicle_id"]
    .astype(str)
    .tolist()
)

vehicle_id = st.sidebar.selectbox(
    "Vehicle",
    vehicle_list
)


# ============================================================
# DISASTER SIMULATION
# ============================================================

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

    st.session_state.simulation = "Flood"

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

    st.session_state.simulation = "Landslide"

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

    st.session_state.simulation = "Road Blockage"

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

    st.session_state.simulation = "Normal"

    st.session_state.alerts = []

    st.rerun()


st.sidebar.divider()

st.sidebar.info(
    "Prototype Mode\n\n"
    "Synthetic NER logistics data"
)


# ============================================================
# LOAD ROUTES
# ============================================================

routes = st.session_state.routes.copy()


# Make sure important numeric columns are numeric

numeric_columns = [
    "distance_km",
    "travel_time_min",
    "rainfall",
    "traffic",
    "road_condition",
    "flood_risk",
    "landslide_risk",
    "blockage"
]

for column in numeric_columns:

    if column in routes.columns:

        routes[column] = pd.to_numeric(
            routes[column],
            errors="coerce"
        ).fillna(0)


# ============================================================
# RISK CALCULATION
# ============================================================

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
# DIJKSTRA ROUTE OPTIMIZATION
# ============================================================

route_result = find_best_route(
    routes,
    source=origin,
    destination=destination
)


if route_result:

    route_path = route_result.get(
        "path",
        []
    )

    best_route_ids = route_result.get(
        "route_ids",
        []
    )

    route_cost = route_result.get(
        "total_cost",
        0
    )

    total_distance = route_result.get(
        "total_distance",
        0
    )

    total_time = route_result.get(
        "total_time",
        0
    )

    average_risk = route_result.get(
        "average_risk",
        0
    )

else:

    route_path = []

    best_route_ids = []

    route_cost = 0

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

        if len(route_path) > 3:

            route_display = (
                f"{route_path[0]} → "
                f"... → "
                f"{route_path[-1]}"
            )

        else:

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


# ============================================================
# SIMULATION STATUS
# ============================================================

if st.session_state.simulation != "Normal":

    st.warning(
        f"⚠️ Active Simulation: "
        f"{st.session_state.simulation}"
    )


st.divider()


# ============================================================
# MAP + ROUTE RECOMMENDATION
# ============================================================

map_col, route_col = st.columns(
    [1.6, 1]
)


# ============================================================
# MAP
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


    # --------------------------------------------------------
    # ROUTE A
    # --------------------------------------------------------

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


    for i, route_id in enumerate(
        route_a_ids
    ):

        segment = routes[
            routes["route_id"]
            .astype(str)
            .str.strip()
            == route_id
        ]


        x = [
            route_a_x[i],
            route_a_x[i + 1]
        ]

        y = [
            route_a_y[i],
            route_a_y[i + 1]
        ]


        # ----------------------------------------------------
        # If route exists
        # ----------------------------------------------------

        if not segment.empty:

            row = segment.iloc[0]

            blocked = (
                int(row["blockage"]) == 1
            )


            if blocked:

                ax.plot(
                    x,
                    y,
                    linestyle="--",
                    linewidth=4
                )

            elif route_id in best_route_ids:

                ax.plot(
                    x,
                    y,
                    linewidth=5
                )

            else:

                ax.plot(
                    x,
                    y,
                    linewidth=3
                )


        # ----------------------------------------------------
        # If route does not exist
        # ----------------------------------------------------

        else:

            ax.plot(
                x,
                y,
                linewidth=3
            )


    # ========================================================
    # ROUTE B
    # ========================================================

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


    for i, route_id in enumerate(
        route_b_ids
    ):

        segment = routes[
            routes["route_id"]
            .astype(str)
            .str.strip()
            == route_id
        ]


        x = [
            route_b_x[i],
            route_b_x[i + 1]
        ]

        y = [
            route_b_y[i],
            route_b_y[i + 1]
        ]


        if not segment.empty:

            row = segment.iloc[0]

            blocked = (
                int(row["blockage"]) == 1
            )


            if blocked:

                ax.plot(
                    x,
                    y,
                    linestyle="--",
                    linewidth=4
                )

            elif route_id in best_route_ids:

                ax.plot(
                    x,
                    y,
                    linewidth=5
                )

            else:

                ax.plot(
                    x,
                    y,
                    linewidth=3
                )

        else:

            ax.plot(
                x,
                y,
                linewidth=3
            )


    # ========================================================
    # LOCATION MARKERS
    # ========================================================

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
        0.65,
        4.25,
        "Rangpo",
        fontsize=11,
        fontweight="bold"
    )

    ax.text(
        6.55,
        0.7,
        "Gangtok",
        fontsize=11,
        fontweight="bold"
    )


    # ========================================================
    # INTERMEDIATE LOCATIONS
    # ========================================================

    ax.text(
        2.15,
        3.45,
        "Singtam",
        fontsize=9
    )

    ax.text(
        3.65,
        2.95,
        "Ranipool",
        fontsize=9
    )

    ax.text(
        2.0,
        4.95,
        "Melli",
        fontsize=9
    )

    ax.text(
        4.75,
        3.65,
        "Namchi",
        fontsize=9
    )


    # ========================================================
    # VEHICLE
    # ========================================================

    vehicle_data = load_vehicle_data(
        st.session_state.vehicles
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
            marker="o"
        )

        ax.text(
            3.6,
            3.4,
            "🚚",
            fontsize=14
        )


    # ========================================================
    # MAP TITLE
    # ========================================================

    ax.set_title(
        "NER Transportation Network",
        fontsize=14,
        fontweight="bold"
    )

    ax.axis("off")


    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


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


        if route_path:

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
            "🚨 No safe route is currently available."
        )


    st.divider()


    # ========================================================
    # ROUTE CARDS
    # ========================================================

    for _, route in routes.iterrows():

        route_id = str(
            route["route_id"]
        )

        risk = float(
            route["risk"]
        )

        level = str(
            route["risk_level"]
        )


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
                    {route_id} —
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


        if route_id in best_route_ids:

            st.success(
                "✓ Part of recommended path"
            )


        if int(route["blockage"]) == 1:

            st.error(
                "🚧 ROAD BLOCKED"
            )


# ============================================================
# WEATHER INTELLIGENCE
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


    weather = load_weather()

    weather = process_weather_data(
        weather
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
# TRAFFIC INTELLIGENCE
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


    with v1:

        st.metric(
            "Vehicle",
            str(vehicle["vehicle_id"])
        )


    with v2:

        st.metric(
            "Cargo",
            str(vehicle["cargo"])
        )


    with v3:

        st.metric(
            "Progress",
            f"{float(vehicle['progress']):.0f}%"
        )


    with v4:

        st.metric(
            "Status",
            str(vehicle["status"])
        )


# ============================================================
# FIELD INCIDENT REPORTING
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
        "✓ Incident successfully recorded."
    )


    st.rerun()


# ============================================================
# INCIDENT TABLE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📋 Incident Log'
    '</div>',
    unsafe_allow_html=True
)


if not st.session_state.incidents.empty:

    st.dataframe(
        st.session_state.incidents,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="resoroute-footer">

        ResORoute • AI-Powered Smart Routing &
        Risk Intelligence

        <br><br>

        SIH26002 • Prototype using Synthetic Data

    </div>
    """,
    unsafe_allow_html=True
)
