
import streamlit as st


def load_css():
    """Apply ResORoute dashboard styling."""

    st.markdown(
        """
        <style>

        /* ---------- Main Page ---------- */

        .stApp {
            background-color: #f5f7fa;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }


        /* ---------- Header ---------- */

        .resoroute-header {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px 26px;
            margin-bottom: 20px;
        }

        .resoroute-title {
            font-size: 32px;
            font-weight: 700;
            color: #163b65;
            margin: 0;
        }

        .resoroute-subtitle {
            font-size: 14px;
            color: #64748b;
            margin-top: 4px;
        }


        /* ---------- Section Titles ---------- */

        .section-title {
            font-size: 19px;
            font-weight: 700;
            color: #163b65;
            margin-top: 10px;
            margin-bottom: 12px;
        }


        /* ---------- Route Cards ---------- */

        .route-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }

        .route-name {
            font-size: 18px;
            font-weight: 700;
            color: #163b65;
        }


        /* ---------- Alerts ---------- */

        .alert-danger {
            background: #fff5f5;
            border-left: 5px solid #dc2626;
            border-radius: 8px;
            padding: 12px 15px;
            margin-bottom: 8px;
            color: #7f1d1d;
        }

        .alert-warning {
            background: #fffbeb;
            border-left: 5px solid #f59e0b;
            border-radius: 8px;
            padding: 12px 15px;
            margin-bottom: 8px;
            color: #78350f;
        }

        .alert-success {
            background: #f0fdf4;
            border-left: 5px solid #16a34a;
            border-radius: 8px;
            padding: 12px 15px;
            margin-bottom: 8px;
            color: #14532d;
        }


        /* ---------- Information Cards ---------- */

        .info-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px;
        }


        /* ---------- Footer ---------- */

        .resoroute-footer {
            text-align: center;
            color: #94a3b8;
            font-size: 12px;
            padding-top: 25px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
