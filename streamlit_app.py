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

            # Inizializzazione delle informazioni territoriali
            st.session_state.regione = None
            st.session_state.provincia = None
            st.session_state.ente = None

            # ADMIN
            if user["ruolo"] == "Admin":
                pass

            else:
                # Regione e provincia da app_user
                st.session_state.regione = user["regione"]
                st.session_state.provincia = user["provincia"]

                # Recupero nome ente da dim_ente
                if pd.notna(user["ente_id"]):

                    conn = get_connection()

                    query = """
                        SELECT nome AS ente_nome
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

            st.switch_page("pages/01_Home.py")

        else:
            st.error("Credenziali non valide")

    st.stop()

# ============================================================
# UTENTE GIÀ LOGGATO
# ============================================================

st.switch_page("pages/01_Home.py")