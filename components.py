import streamlit as st

def topbar():

    st.markdown("""
    <style>

        section[data-testid="stSidebar"] {
            display:none;
        }

        button[kind="header"] {
            display:none;
        }

        .block-container {
            padding-top:0.5rem;
        }

        .navbar-title {
            background:#0f2454;
            color:white;
            text-align:center;
            padding:18px;
            font-size:32px;
            font-weight:700;
            border-radius:10px 10px 0 0;
        }

    </style>
    """, unsafe_allow_html=True)

    # RIGA 1 - TITOLO
    st.markdown("""<div class="navbar-title">
                    🏛️ HR Analytics Dashboard
                </div>""", unsafe_allow_html=True)

    # RIGA 2 - MENU
    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])

    with col1:
        if st.button("Home", use_container_width=True):
            st.switch_page("pages/01_Home.py")

    with col2:
        if st.button("Pensionamenti", use_container_width=True):
            st.switch_page("pages/02_Forecast_Pensionamenti.py")

    with col3:
        if st.button("Workforce Planning", use_container_width=True):
            st.switch_page("pages/03_Strategic_Workforce_Planning.py")

    with col4:
        if st.button("Burnout Forecast", use_container_width=True):
            st.switch_page("pages/04_Burnout_Forecast.py")

    with col5:
        with st.popover("👤"):
            st.write(f"**Utente:** {st.session_state.nome} {st.session_state.cognome}")
            if st.session_state.ruolo == "Admin":
                st.write("**Ruolo:** Admin")
            else:
                st.write(f"**Ente:** {st.session_state.ruolo}")
            st.divider()

            if st.button("Logout", key="logout_button"):
                st.session_state.clear()
                st.switch_page("streamlit_app.py")

    st.markdown("<hr>", unsafe_allow_html=True)