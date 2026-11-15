import streamlit as st
import hashlib
import pandas as pd
from database import load_users, get_connection

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
    # Nasconde sidebar e header di Streamlit nella schermata di login
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        button[kind="header"] {
            display: none;
        }
        /* Centratura e stile generale del blocco di login */
        .login-container {
            padding: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Creazione di uno spazio vuoto verticale per centrare meglio il box verticalmente
    st.write("")
    st.write("")

    # Centriamo la card principale usando tre colonne (la centrale conterrà il box diviso a metà)
    _, main_col, _ = st.columns([1, 8, 1])

    with main_col:
        # Usiamo un container con bordo per simulare il box unificato della card
        with st.container(border=True):
            col_form, col_img = st.columns(2, gap="large")

            # --- COLONNA SINISTRA: FORM DI LOGIN ---
            with col_form:
                st.markdown("### **LOGIN**")
                st.caption("Accedi alla HR Analytics Dashboard")
                
                # Form di Streamlit per gestire l'invio con il tasto Invio o bottone
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Inserisci il tuo username")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    
                    st.write("")
                    submit_button = st.form_submit_button("Accedi Ora", use_container_width=True)

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
                        st.session_state.ente_id = user["ente_id"]

                        # Inizializzazione delle informazioni territoriali
                        st.session_state.regione = None
                        st.session_state.provincia = None
                        st.session_state.ente_nome = None

                        # ADMIN
                        if user["ruolo"] == "Admin":
                            pass
                        else:
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
                                ente_nome = pd.read_sql(
                                    query,
                                    conn,
                                    params=[user["ente_id"]]
                                )

                                if ente_nome.empty:
                                    st.session_state.clear()
                                    st.error("Ente associato all'utente non trovato.")
                                    st.stop()

                                st.session_state.ente_nome = ente_nome.iloc[0]["ente_nome"]

                        st.switch_page("pages/01_Home.py")

                    else:
                        st.error("Credenziali non valide")

            # --- COLONNA DESTRA: IMMAGINE ILLUSTRATIVA ---
            with col_img:
                # Puoi sostituire questo URL con un'immagine locale (es. "assets/login_img.png")
                st.image("./assets/img/HR Analytics Dashboard login.png", 
                    use_container_width=True
                )

    st.stop()

# ============================================================
# UTENTE GIÀ LOGGATO
# ============================================================

st.switch_page("pages/01_Home.py")