import streamlit as st
import requests

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

HOST = st.secrets["databricks"]["host"]
TOKEN = st.secrets["databricks"]["token"]
JOB_ID = st.secrets["databricks"]["job_id"]

st.title("🏛️ HR Analytics nella Pubblica Amministrazione")

st.markdown("""
### 🎯 Obiettivo della Dashboard

Questa piattaforma di **HR Analytics per la Pubblica Amministrazione** supporta i processi 
decisionali relativi alla gestione strategica del capitale umano, integrando tecniche di 
**Business Intelligence**, **Machine Learning** e **Workforce Analytics**.

Attraverso l'elaborazione dei dati del personale, la dashboard fornisce strumenti per monitorare 
le dinamiche della forza lavoro, individuare rischi organizzativi e pianificare interventi di 
sviluppo delle competenze.

### 📊 Aree di Analisi

#### 📈 Forecast Pensionamenti
Analisi predittiva finalizzata a stimare le uscite future del personale per pensionamento, 
supportando la pianificazione del turnover, il ricambio generazionale e le strategie di recruitment.

#### 🧠 Strategic Workforce Planning
Valutazione delle competenze presenti e future dell'organizzazione attraverso l'identificazione di:
- competenze critiche;
- skill gap organizzativi;
- rischio di perdita delle competenze chiave;
- impatto dell'Intelligenza Artificiale sui profili professionali;
- competenze emergenti da sviluppare nel medio e lungo periodo.

#### 🔥 Burnout Risk Forecast
Analisi del benessere organizzativo mediante modelli predittivi in grado di individuare 
dipendenti, strutture e profili professionali maggiormente esposti a fenomeni di stress 
lavorativo e rischio burnout.

---

Utilizzare il pulsante **"Aggiorna i Dati"** per eseguire nuovamente i modelli analitici e aggiornare i risultati in base ai dati più recenti disponibili nel Data Warehouse Databricks.
""")

# ============================================================
# NAVIGAZIONE
# ============================================================

st.subheader("📊 Dashboard Analitiche")

st.info(
    "Seleziona una dashboard per visualizzare i risultati dei modelli HR Analytics."
)

col1, col2, col3 = st.columns(3)

with col1:

    st.page_link(
        "pages/01_Forecast_Pensionamenti.py",
        label="Forecast Pensionamenti",
        icon="📈"
    )

    st.caption(
        "Analisi delle uscite previste e del turnover."
    )

with col2:

    st.page_link(
        "pages/02_Strategic_Workforce_Planning.py",
        label="Workforce Planning",
        icon="🧠"
    )

    st.caption(
        "Skill gap, skill loss e competenze future."
    )

with col3:

    st.page_link(
        "pages/03_Burnout_Forecast.py",
        label="Burnout Forecast",
        icon="🔥"
    )

    st.caption(
        "Rischio burnout e benessere organizzativo."
    )

st.divider()

# ============================================================
# AGGIORNA MODELLI
# ============================================================

if st.button("🔄 Aggiorna i Dati"):

    url = f"https://{HOST}/api/2.1/jobs/run-now"

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    payload = {
        "job_id": JOB_ID
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code == 200:

        st.success("Job avviato correttamente")

    else:

        st.error(
            f"Errore: {response.text}"
        )


