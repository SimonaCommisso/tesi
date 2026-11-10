import streamlit as st
import requests
import pandas as pd

from database import load_last_refresh

# ============================================================
# CONFIGURAZIONE
# ============================================================

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

HOST = st.secrets["databricks"]["host"]
TOKEN = st.secrets["databricks"]["token"]
JOB_ID = st.secrets["databricks"]["job_id"]
HTTP_PATH = st.secrets["databricks"]["sql_warehouse_path"]

# ============================================================
# TITOLO
# ============================================================

st.title("🏛️ HR Analytics nella Pubblica Amministrazione")

# ============================================================
# ULTIMO AGGIORNAMENTO
# ============================================================

try:
    ultima_data = load_last_refresh()
    if ultima_data is not None:
        st.success(f"🕒 Ultimo aggiornamento modelli: {ultima_data}")
    else:
        st.warning("⚠️ Nessun aggiornamento disponibile")

except Exception as e:
    st.warning("⚠️ Impossibile recuperare la data di aggiornamento")

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