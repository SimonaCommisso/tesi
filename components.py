import streamlit as st

def topbar():
    st.markdown("""
    <style>
        /* Nasconde la sidebar e l'header di Streamlit */
        section[data-testid="stSidebar"] {
            display: none;
        }
        button[kind="header"] {
            display: none;
        }
        .block-container {
            padding-top: 0.5rem;
        }

        /* Titolo della navbar con angoli superiori arrotondati */
        .navbar-title {
            background: #0f2454;
            color: white;
            text-align: center;
            padding: 18px;
            font-size: 32px;
            font-weight: 700;
            border-radius: 10px 10px 0 0;
        }

        /* Container per la riga dei bottoni/menu con sfondo coordinato e angoli inferiori arrotondati */
        .navbar-menu {
            background: #0f2454;
            padding: 10px 15px 15px 15px;
            border-radius: 0 0 10px 10px;
            display: flex;
            align-items: center;
        }

        /* Stile personalizzato per i link di pagina di Streamlit per farli occupare lo spazio uniformemente */
        div[data-testid="stPageLink"] a {
            background-color: #1a366e !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 6px !important;
            text-align: center !important;
            font-weight: 600 !important;
            width: 100% !important;
            padding: 8px 12px !important;
            box-sizing: border-box;
            text-decoration: none !important;
        }
        
        div[data-testid="stPageLink"] a:hover {
            background-color: #27498c !important;
            border-color: rgba(255, 255, 255, 0.4) !important;
        }

        /* Allineamento del popover utente */
        .user-popover-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # RIGA 1 - TITOLO
    st.markdown("""<div class="navbar-title">
                    🏛️ HR Analytics Dashboard
                </div>""", unsafe_allow_html=True)

    # RIGA 2 - MENU UNIFICATO CON SFONDO BLU
    # Utilizziamo un container visivo per chiudere il blocco
    with st.container():
        st.markdown('<div class="navbar-menu">', unsafe_allow_html=True)
        
        # Suddividiamo lo spazio: 4 colonne larghe per le pagine, 1 più stretta a destra per l'utente
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

        with col1:
            st.page_link("pages/01_Home.py", label="🏠 Home")

        with col2:
            st.page_link("pages/02_Forecast_Pensionamenti.py", label="⏳ Pensionamenti")

        with col3:
            st.page_link("pages/03_Strategic_Workforce_Planning.py", label="📊 Workforce Planning")

        with col4:
            st.page_link("pages/04_Burnout_Forecast.py", label="🔥 Burnout Forecast")

        with col5:
            # Contenitore per allineare a destra il popover utente
            st.markdown('<div class="user-popover-container">', unsafe_allow_html=True)
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

                if st.button("Logout", key="logout_button"):
                    st.session_state.clear()
                    st.switch_page("streamlit_app.py")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 10px;'>", unsafe_allow_html=True)