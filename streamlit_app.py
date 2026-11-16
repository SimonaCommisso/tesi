import streamlit as st
import hashlib
import pandas as pd
from database import load_users, load_ente_user
from style import load_css_login_page

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

# ============================================================
# LOGIN STATE
# ============================================================

if "logged" not in st.session_state:
    st.session_state.logged = False

# ============================================================
# PAGINA LOGIN
# ============================================================

if not st.session_state.logged:

    load_css_login_page()

    col_left, col_center, col_right = st.columns([1, 8, 1])

    with col_center:
        with st.container():

            col_form, col_img = st.columns([1, 1], gap="large")

            # --------------------------------------------------
            # FORM LOGIN
            # --------------------------------------------------

            with col_form:

                st.markdown("""
                <div class="login-title">
                    🏛️ HR Analytics
                </div>
                <div class="login-subtitle">
                    Dashboard di Workforce Analytics
                    per la Pubblica Amministrazione
                </div>
                """, unsafe_allow_html=True)

                with st.form("login_form"):

                    username = st.text_input("Username", placeholder="Inserisci username")

                    password = st.text_input("Password",
                        type="password", placeholder="••••••••")

                    st.write("")

                    submit_button = st.form_submit_button("Accedi",
                        use_container_width=True)

                if submit_button:
                    users = load_users()
                    password_hash = hashlib.sha256(password.encode()).hexdigest()

                    user = users[
                        (users["username"] == username)
                        &
                        (users["password"] == password_hash)
                    ]

                    if len(user) == 1:
                        user = user.iloc[0]
                        st.session_state.logged = True
                        st.session_state.nome = user["nome"]
                        st.session_state.cognome = user["cognome"]
                        st.session_state.ruolo = user["ruolo"]
                        st.session_state.ente_id = (None if pd.isna(user["ente_id"])
                            else int(user["ente_id"]))
                        st.session_state.regione = None
                        st.session_state.provincia = None
                        st.session_state.ente_nome = ""
                        if user["ruolo"] != "Admin":
                            st.session_state.regione = user["regione"]
                            st.session_state.provincia = user["provincia"]
                            if pd.notna(user["ente_id"]):
                                ente_nome = load_ente_user(st.session_state.ente_id)
                                if ente_nome.empty:
                                    st.session_state.clear()
                                    st.error("Ente associato non trovato.")
                                    st.stop()
                                st.session_state.ente_nome = (ente_nome.iloc[0]["ente_nome"])

                        st.switch_page("pages/01_Home.py")

                    else:
                        st.error("Credenziali non valide. Verificare username e password.")

            # --------------------------------------------------
            # IMMAGINE
            # --------------------------------------------------

            with col_img:
                st.markdown("""<div class="box-image">""",
                    unsafe_allow_html=True)
                st.image("./assets/img/HR Analytics Dashboard login.png", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
# ============================================================
# UTENTE GIÀ LOGGATO
# ============================================================

st.switch_page("pages/01_Home.py")