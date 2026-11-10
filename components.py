
import streamlit as st
import textwrap
import html

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
            padding-top: 0 !important;
        }

        /* CONTENITORE NAVBAR */
        .navbar {
            width: 100%;
            background: #0f2454;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }

        /* TITOLO */
        .navbar-title {
            width: 100%;
            min-height: 85px;
            display: flex;
            align-items: center;
            justify-content: center;

            color: white;
            font-size: 32px;
            font-weight: 700;
            text-align: center;

            box-sizing: border-box;
            padding: 15px;
        }

        /* MENU */
        .navbar-menu {
            display: flex;
            align-items: center;
            justify-content: space-between;

            width: 100%;
            min-height: 65px;
            box-sizing: border-box;

            padding: 8px 15px;
            background: #16336f;
            gap: 8px;
        }

        /* LINK */
        .navbar-menu a {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;

            color: white !important;
            text-decoration: none !important;

            font-size: 15px;
            font-weight: 600;

            padding: 12px 8px;
            border-radius: 6px;
            white-space: nowrap;

            transition: background 0.2s;
        }

        .navbar-menu a:hover {
            background: #294d91;
        }

        /* UTENTE */
        .navbar-menu .user-link {
            flex: 0 0 45px;
            margin-left: 10px;
            border: 1px solid #ffffff55;
        }

        @media (max-width: 800px) {
            .navbar-menu {
                flex-wrap: wrap;
            }

            .navbar-menu a {
                white-space: normal;
                font-size: 12px;
            }
        }

    </style>
    """, unsafe_allow_html=True)

    nome = html.escape(str(st.session_state.nome))
    cognome = html.escape(str(st.session_state.cognome))

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

    # Rimuove l'indentazione che Markdown interpreta come codice
    navbar_html = textwrap.dedent(navbar_html).strip()

    st.markdown(navbar_html, unsafe_allow_html=True)
