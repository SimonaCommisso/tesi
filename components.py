import streamlit as st

def topbar():

    # Nasconde sidebar e hamburger menu
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }

        button[kind="header"] {
            display: none;
        }

        .block-container {
            padding-top: 1rem;
        }
    </style>""", unsafe_allow_html=True)

    # Barra di navigazione
    col1, col2, col3, col4, col5, col6 = st.columns([4, 2, 2, 2, 2, 1])

    with col1:
        st.markdown("""
            <h6 style="
                margin-top:10px;
                color:#1d3673;
                font-weight:700;
            ">
            🏛️ HR Analytics Dashboard
            </h6>
            """, unsafe_allow_html=True)

    with col2:
        if st.link_button("🏠 Home", use_container_width=True):
            st.switch_page("pages/01_Home.py")

    with col3:
        if st.link_button("📈 Pensionamenti", use_container_width=True):
            st.switch_page("pages/02_Forecast_Pensionamenti.py")

    with col4:
        if st.link_button("🧠 Workforce", use_container_width=True):
            st.switch_page("pages/03_Strategic_Workforce_Planning.py")

    with col5:
        if st.link_button("🔥 Burnout", use_container_width=True):
            st.switch_page("pages/04_Burnout_Forecast.py")

    with col6:
        with st.popover("👤"):
            st.markdown("### Profilo")
            st.write(f"**Nome:** {st.session_state.nome}")
            st.write(f"**Cognome:** {st.session_state.cognome}")
            if st.session_state.ruolo == "Admin":
                st.write("**Ruolo:** Admin")
            else:
                st.write(f"**Ruolo:** {st.session_state.ruolo}")
                if "ente_nome" in st.session_state:
                    st.write(f"**Ente:** {st.session_state.ente_nome}")
            st.divider()
            if st.link_button("🚪 Logout", key="logout_btn"):
                st.session_state.clear()
                st.switch_page("streamlit_app.py")

    st.divider()