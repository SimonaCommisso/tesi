import streamlit as st

def topbar():
    st.markdown("""
    <style>
        /* Nasconde sidebar e header nativo */
        section[data-testid="stSidebar"] { display: none; }
        button[kind="header"] { display: none; }
        .block-container { padding-top: 1rem; max-width: 100%; }

        /* Barra superiore unificata */
        .topbar-wrapper {
            background-color: #0f2454;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        /* Titolo centrato all'interno della barra */
        .topbar-title {
            color: #ffffff !important;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 20px;
        }

        /* Stile dei link di navigazione (st.page_link) dentro la barra */
        div[data-testid="stPageLink"] a {
            background-color: #1a366e !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            text-align: center !important;
            font-weight: 600 !important;
            width: 100% !important;
            padding: 10px 8px !important;
            box-sizing: border-box;
            text-decoration: none !important;
        }
        
        div[data-testid="stPageLink"] a:hover {
            background-color: #27498c !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
        }

        /* Allineamento a destra del blocco utente */
        .user-col {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            height: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

    # Apriamo il contenitore visivo con lo sfondo blu
    st.markdown('<div class="topbar-wrapper">', unsafe_allow_html=True)
    
    # Titolo
    st.markdown('<div class="topbar-title">🏛️ HR Analytics Dashboard</div>', unsafe_allow_html=True)

    # Colonne per i link e il menu utente
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1], gap="small")

    with col1:
        st.page_link("pages/01_Home.py", label="🏠 Home")

    with col2:
        st.page_link("pages/02_Forecast_Pensionamenti.py", label="⏳ Pensionamenti")

    with col3:
        st.page_link("pages/03_Strategic_Workforce_Planning.py", label="📊 Workforce Planning")

    with col4:
        st.page_link("pages/04_Burnout_Forecast.py", label="🔥 Burnout Forecast")

    with col5:
        st.markdown('<div class="user-col">', unsafe_allow_html=True)
        with st.popover("👤"):
            nome = st.session_state.get("nome", "")
            cognome = st.session_state.get("cognome", "")
            ruolo = st.session_state.get("ruolo", "Utente")
            
            st.write(f"**Utente:** {nome} {cognome}")
            if ruolo == "Admin":
                st.write("**Ruolo:** Admin")
            else:
                st.write(f"**Ente:** {ruolo}")
            st.divider()

            if st.button("Logout", key="logout_button_topbar"):
                st.session_state.clear()
                st.switch_page("streamlit_app.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chiudiamo il contenitore blu
    st.markdown('</div>', unsafe_allow_html=True)