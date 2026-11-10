
import streamlit as st

def topbar():

    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }

        button[kind="header"] {
            display: none;
        }

        .block-container {
            padding-top: 0.5rem;
        }

        .navbar {
            background: #0f2454;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }

        .navbar-title {
            color: white;
            text-align: center;
            padding: 18px;
            font-size: 32px;
            font-weight: 700;
        }

        .navbar-menu {
            display: flex;
            align-items: center;
            width: 100%;
            box-sizing: border-box;
            padding: 10px 15px;
            background: #16336f;
            gap: 8px;
        }

        .navbar-menu a {
            color: white !important;
            text-decoration: none !important;
            font-size: 15px;
            font-weight: 600;
            padding: 12px 10px;
            border-radius: 6px;
            text-align: center;
            flex: 1;
            white-space: nowrap;
        }

        .navbar-menu a:hover {
            background: #294d91;
        }

        .navbar-menu .user-link {
            flex: 0 0 45px;
            margin-left: auto;
            border: 1px solid #ffffff55;
            border-radius: 6px;
        }
    </style>
    """, unsafe_allow_html=True)

    nome = st.session_state.nome
    cognome = st.session_state.cognome

    navbar_html = f"""
    <div class="navbar">
        <div class="navbar-title">
            🏛️ HR Analytics Dashboard
        </div>

        <div class="navbar-menu">
            <a href="/" target="_self">Home</a>

            <a href="/Forecast_Pensionamenti" target="_self">
                Pensionamenti
            </a>

            <a href="/Strategic_Workforce_Planning" target="_self">
                Workforce Planning
            </a>

            <a href="/Burnout_Forecast" target="_self">
                Burnout Forecast
            </a>

            <a href="#" class="user-link" title="{nome} {cognome}">
                👤
            </a>
        </div>
    </div>
    """

    st.markdown(navbar_html, unsafe_allow_html=True)
