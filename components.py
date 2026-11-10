import streamlit as st

def topbar():

    st.markdown("""
    <style>

        /* Nasconde sidebar e header */
        section[data-testid="stSidebar"] {
            display: none;
        }

        button[kind="header"] {
            display: none;
        }

        .block-container {
            padding-top: 0.5rem;
        }

        /* Navbar principale */
        .navbar {
            background: #0f2454;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }

        /* Titolo */
        .navbar-title {
            color: white;
            text-align: center;
            padding: 18px;
            font-size: 32px;
            font-weight: 700;
        }

        /* Riga menu */
        .navbar-menu {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            background: #16336f;
            gap: 10px;
        }

        /* Link */
        .navbar-menu a {
            color: white !important;
            text-decoration: none !important;
            font-size: 15px;
            font-weight: 600;
            padding: 12px 15px;
            border-radius: 6px;
            text-align: center;
            flex: 1;
            white-space: nowrap;
            transition: background 0.2s;
        }

        .navbar-menu a:hover {
            background: #294d91;
        }

        /* Profilo utente */
        .navbar-menu .user-link {
            flex: 0;
            margin-left: auto;
            border: 1px solid #ffffff55;
            border-radius: 50%;
            min-width: 42px;
        }

    </style>
    """, unsafe_allow_html=True)

    nome = st.session_state.nome
    cognome = st.session_state.cognome

    st.markdown(f"""
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
    """, unsafe_allow_html=True)