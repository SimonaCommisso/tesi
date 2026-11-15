import streamlit as st
import requests
import pandas as pd
from components import topbar
from database import load_last_refresh, load_pensionamenti

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

st.title("🏛️ Home")

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
# DASHBOARD OVERVIEW
# ============================================================

st.markdown("""### Home""")

col_mappa, col_kpi = st.columns([2,1])
st.session_state.regione
st.session_state.provincia
df_pensionamenti = load_pensionamenti()

with col_mappa:

    st.subheader("🗺️ Ambito Territoriale")

    regione = st.session_state.get("regione")
    provincia = st.session_state.get("provincia")

    if regione is None:

        st.info("🌍 Visualizzazione Nazionale")

        st.image("https://upload.wikimedia.org/wikipedia/commons/0/03/Italy_regions_map.png",
            use_container_width=True)

    elif provincia is None:
        st.success(f"📍 Regione: {regione}")
        st.write("Visualizzazione limitata alla regione assegnata.")

    else:
        st.success(f"📍 Provincia: {provincia}")
        st.write(f"Visualizzazione limitata alla provincia di {provincia}.")

with col_kpi:
    st.subheader("📈 Forecast Pensionamenti")
    df = load_pensionamenti()
    
    if (st.session_state.get("regione") is None and
        st.session_state.get("provincia") is None):
        totale = df["numero_dipendenti"].sum()
        
    elif (st.session_state.get("regione") is not None and
        st.session_state.get("provincia") is None):
        totale = (df[df["regione"] == st.session_state["regione"]]
            ["numero_dipendenti"].sum())
    else:
        totale = (df[df["provincia"] == st.session_state["provincia"]]
            ["numero_dipendenti"].sum())
    
    st.metric(label="Pensionamenti Previsti", value=f"{int(totale):,}")
    rischio = round(df["probabilita_media_pensionamento"].mean(), 2)
    st.metric("Probabilità Media Pensionamento", f"{rischio}%")
    

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