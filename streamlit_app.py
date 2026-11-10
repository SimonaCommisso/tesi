import streamlit as st
import hashlib
from database import load_users

# ============================================================
# LOGIN
# ============================================================

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("Accedi"):
        users = load_users()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = users[
            (users["username"] == username)
            &
            (users["password_hash"] == password_hash)
        ]

        if len(user) == 1:
            user = user.iloc[0]
            st.session_state.logged = True
            st.session_state.nome = user["nome"]
            st.session_state.cognome = user["cognome"]
            st.session_state.ruolo = user["ruolo"]
            st.session_state.ente_id = user["ente_id"]
            st.rerun()

        else:
            st.error("Credenziali non valide")

    st.stop()