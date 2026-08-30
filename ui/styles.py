import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        .stApp {
            background-color: #f4f7fb;
            color: #172033;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {
            background-color: #172033;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }


        /* =====================================================
           HEADER
        ===================================================== */

        .resoroute-header {
            background: white;
            padding: 25px 30px;
            border-radius: 18px;
            border: 1px solid #dfe5ef;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }

        .resoroute-title {
            font-size: 38px;
            font-weight: 800;
            color: #173f73;
            margin-bottom: 5px;
        }

        .resoroute-subtitle {
            font-size: 17px;
            color: #64748b;
        }


        /* =====================================================
           SECTION TITLES
           ===================================================== */

        .section-title {
            font-size: 26px;
            font-weight: 800;
            color: #173f73;
            margin-top: 15px;
            margin-bottom: 15px;
        }


        /* =====================================================
           METRICS
           ===================================================== */

        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #dfe5ef;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        }

        [data-testid="stMetricLabel"] {
            color: #526173 !important;
        }

        [data-testid="stMetricValue"] {
            color: #173f73 !important;
            font-weight: 800;
        }


        /* =====================================================
           ROUTE CARDS
           ===================================================== */

        .route-card {
            background: white;
            border: 1px solid #dfe5ef;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.04);
            color: #172033;
        }

        .route-name {
            font-size: 19px;
            font-weight: 800;
            color: #173f73;
        }


        /* =====================================================
           ALERT
           ===================================================== */

        .alert-danger {
            background: #fff1f1;
            border-left: 5px solid #dc2626;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 8px;
            color: #991b1b;
            font-weight: 600;
        }


        /* =====================================================
           FOOTER
           ===================================================== */

        .resoroute-footer {
            background: #172033;
            color: white;
            text-align: center;
            padding: 25px;
            border-radius: 15px;
            margin-top: 35px;
            font-size: 15px;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            border-radius: 9px;
            font-weight: 600;
        }


        /* =====================================================
           DATAFRAME
           ===================================================== */

        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
