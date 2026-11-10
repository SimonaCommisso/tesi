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
            padding-top: 1rem !important;
        }

        /* CONTENITORE COMPLETO */
        .st-key-topbar {
            background-color: #0f2454;
            border-radius: 10px;
            padding: 0 15px 12px 15px;
            margin-bottom: 20px;
        }

        /* TITOLO */
        .topbar-title {
            margin-top: 10px;
            min-height: 85px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff !important;
            font-size: 32px;
            font-weight: 700;
            text-align: center;
        }

        /* LINK DI NAVIGAZIONE */
        .st-key-topbar [data-testid="stPageLink"] a,
        .st-key-topbar [data-testid="stPageLink"] a *,
        .st-key-topbar [data-testid="stPageLink"] a p,
        .st-key-topbar [data-testid="stPageLink"] a span,
        .st-key-topbar [data-testid="stPageLink"] a div {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            text-decoration: none !important;
            font-weight: 600 !important;
        }

        /* SFONDO E DIMENSIONI */
        .st-key-topbar [data-testid="stPageLink"] a {
            background-color: #16336f !important;
            border-radius: 7px;
            padding: 12px 5px;
            justify-content: center;
        }

        /* HOVER */
        .st-key-topbar [data-testid="stPageLink"] a:hover,
        .st-key-topbar [data-testid="stPageLink"] a:hover * {
            background-color: #294d91 !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important; 
        }

        /* POPOVER UTENTE */
        .st-key-topbar button[data-testid="stPopoverButton"] {
            background-color: #16336f;
            color: #ffffff !important;
            border: 1px solid #52678e;
            border-radius: 7px;
            min-height: 52px;
        }
        
        .st-key-topbar button[data-testid="stPopoverButton"],
        .st-key-topbar button[data-testid="stPopoverButton"] * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        .st-key-topbar button[data-testid="stPopoverButton"]:hover {
            background-color: #294d91;
            color: #ffffff !important;
        }

    </style>
    """, unsafe_allow_html=True)

    # NAVBAR
    with st.container(key="topbar"):

        # RIGA 1 - TITOLO
        st.markdown(
            '<div class="topbar-title">🏛️ HR Analytics Dashboard</div>',
            unsafe_allow_html=True
        )

        # RIGA 2 - MENU
        col1, col2, col3, col4, col5 = st.columns(
            [2, 2, 2, 2, 0.6],
            vertical_alignment="center"
        )

        with col1:
            st.page_link(
                "pages/01_Home.py",
                label="Home",
                use_container_width=True
            )

        with col2:
            st.page_link(
                "pages/02_Forecast_Pensionamenti.py",
                label="Pensionamenti",
                use_container_width=True
            )

        with col3:
            st.page_link(
                "pages/03_Strategic_Workforce_Planning.py",
                label="Workforce Planning",
                use_container_width=True
            )

        with col4:
            st.page_link(
                "pages/04_Burnout_Forecast.py",
                label="Burnout Forecast",
                use_container_width=True
            )

        with col5:
            with st.popover("👤", use_container_width=True):

                st.write(
                    f"**Utente:** {st.session_state.nome} "
                    f"{st.session_state.cognome}"
                )

                if st.session_state.ruolo == "Admin":
                    st.write("**Ruolo:** Admin")
                else:
                    st.write(f"**Ente:** {st.session_state.ruolo}")

                st.divider()

                if st.button("Logout", key="logout_button"):
                    st.session_state.clear()
                    st.switch_page("streamlit_app.py")
