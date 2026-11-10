import streamlit as st

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
        user = users[
            (users["username"] == username)
            &
            (users["password_hash"] == password)
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