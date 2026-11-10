import streamlit as st
import hashlib
import pandas as pd
from database import load_users, get_connection

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

# ============================================================
# LOGIN
# ============================================================

if "logged" not in st.session_state:
    st.session_state.logged = False

# ============================================================
# PAGINA LOGIN
# ============================================================

if not st.session_state.logged:
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        display:none;
    }

    button[kind="header"] {
        display:none;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("🔐 Login")
    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("Accedi"):
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
            st.session_state.ente_id = user["ente_id"]
            
            # Recupero informazioni dell'ente
            if user["ruolo"] != "Admin":

                conn = get_connection()

                query = """
                    SELECT ente_nome, regione, provincia
                    FROM tesi.pubblica_amministrazione_tesi.dim_ente
                    WHERE ente_id = ?
                """

                ente = pd.read_sql(
                    query,
                    conn,
                    params=[user["ente_id"]]
                )

                if ente.empty:
                    st.session_state.clear()
                    st.error("Ente associato all'utente non trovato.")
                    st.stop()

                st.session_state.ente = ente.iloc[0]["ente_nome"]
                st.session_state.regione = ente.iloc[0]["regione"]
                st.session_state.provincia = ente.iloc[0]["provincia"]

                st.switch_page("pages/01_Home.py")

            else:
                st.error("Credenziali non valide")

    st.stop()

# ============================================================
# UTENTE GIÀ LOGGATO
# ============================================================

st.switch_page("pages/01_Home.py")