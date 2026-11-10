import streamlit as st
import requests
import pandas as pd
from components import topbar
from database import load_last_refresh

# ============================================================
# CONFIGURAZIONE
# ============================================================

if not st.session_state.get("logged",False):
    st.switch_page("streamlit_app.py")

# ===========================================================
## DATI DI CONNESSIONE A DATABRICKS
# ============================================================ 
HOST = st.secrets["databricks"]["host"]
TOKEN = st.secrets["databricks"]["token"]
JOB_ID = st.secrets["databricks"]["job_id"]
HTTP_PATH = st.secrets["databricks"]["sql_warehouse_path"]

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

topbar()

if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("streamlit_app.py")

st.title("🏛️ Home")

#===========================================================
# DATI UTENTE LOGGATO
#===========================================================
st.success(f"""Benvenuto {st.session_state.nome} {st.session_state.cognome} - Ente di provenienza: {st.session_state.ruolo}""")


# ============================================================
# ULTIMO AGGIORNAMENTO
# ============================================================

try:
    ultima_data = load_last_refresh()
    if ultima_data is not None:
        ultima_data = pd.to_datetime(ultima_data).strftime("%d/%m/%Y %H:%M:%S")
        st.success(f"🕒 Ultimo aggiornamento modelli: {ultima_data}")
    else:
        st.warning("⚠️ Nessun aggiornamento disponibile")
except Exception as e:
    st.error(f"Errore nel caricamento della data: {e}")

# ============================================================
# DESCRIZIONE
# ============================================================

st.markdown("""
### 🎯 Obiettivo della Dashboard

Questa piattaforma di **HR Analytics per la Pubblica Amministrazione**
supporta i processi decisionali relativi alla gestione strategica del
capitale umano attraverso tecniche di Business Intelligence,
Machine Learning e Workforce Analytics.

### 📊 Aree di Analisi

#### 📈 Forecast Pensionamenti
Previsione delle uscite future del personale e supporto alla
pianificazione del turnover.

#### 🧠 Strategic Workforce Planning
Analisi delle competenze, individuazione degli skill gap,
valutazione del rischio di perdita delle competenze e impatto
dell'Intelligenza Artificiale sui profili professionali.

#### 🔥 Burnout Risk Forecast
Valutazione del benessere organizzativo e identificazione dei
dipendenti e delle strutture maggiormente esposte al rischio
burnout.

---

Utilizzare il pulsante **Aggiorna i Dati** per avviare
l'esecuzione dei modelli analitici su Databricks.
""")

# ============================================================
# AGGIORNA MODELLI
# ============================================================

if st.button("🔄 Aggiorna i Dati"):
    url = f"https://{HOST}/api/2.1/jobs/run-now"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"job_id": JOB_ID}

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        run_id = response.json()["run_id"]
        st.success(f"✅ Dati caricati correttamente")
    else:
        st.error(f"Errore nel caricamento dei dati: {response.text}")