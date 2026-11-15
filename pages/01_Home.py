import streamlit as st
import requests
import pandas as pd
from style import load_css
from components import topbar
from database import load_last_refresh, load_pensionamenti_nazionali, load_pensionamenti_regione, load_pensionamenti_provincia
from streamlit_folium import st_folium
import folium
from utility.coordinate import get_coordinate_regione, get_coordinate_provincia


# ============================================================
# CONFIGURAZIONE
# ============================================================

if not st.session_state.get("logged",False):
    st.switch_page("streamlit_app.py")
    
load_css()

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

with col_mappa:

    with st.container(border=True):

        st.markdown('<div class="dashboard-title">🗺️ Ambito Territoriale</div>', unsafe_allow_html=True)
        regione = st.session_state.get("regione")
        provincia = st.session_state.get("provincia")

        if regione is None:
            st.info("🌍 Visualizzazione Nazionale")
            m = folium.Map(
                location=[42.5, 12.5],
                zoom_start=5,
                tiles="OpenStreetMap"
            )

        elif provincia is None:

            st.success(f"📍 Regione: {regione}")
            lat, lon = get_coordinate_regione(regione)

            m = folium.Map(
                location=[lat, lon],
                zoom_start=8,
                tiles="OpenStreetMap"
            )

            folium.Marker(
                [lat, lon],
                popup=regione
            ).add_to(m)

        else:

            st.success(f"📍 Provincia: {provincia}")

            lat, lon = get_coordinate_provincia(provincia)

            m = folium.Map(
                location=[lat, lon],
                zoom_start=10,
                tiles="OpenStreetMap"
            )

            folium.CircleMarker(
                [lat, lon],
                radius=10,
                color="#0f2454",
                fill=True
            ).add_to(m)

        st_folium(
            m,
            use_container_width=True,
            height=450
        )

with col_kpi:
    with st.container(border=True):
        st.markdown(
            '<div class="dashboard-title">📈 Forecast Pensionamenti</div>',
            unsafe_allow_html=True)
        regione = st.session_state.get("regione")
        provincia = st.session_state.get("provincia")
        ente_id = st.session_state.get("ente_id")

        if regione is None and provincia is None:
            df = load_pensionamenti_nazionali()
            df_view = df

        elif provincia is None:
            df = load_pensionamenti_regione(regione, ente_id)
            df_view = df[(df["regione"] == regione) & (df["ente_id"] == ente_id)]

        else:
            df = load_pensionamenti_provincia(regione, provincia, ente_id)
            df_view = df[(df["regione"] == regione) & (df["provincia"] == provincia) & (df["ente_id"] == ente_id)]

        totale = int(df_view["numero_dipendenti"].sum())

        if len(df_view) > 0:
            rischio = round(
                df_view["probabilita_media_pensionamento"].mean(), 2)
        else:
            rischio = 0

        st.metric("Pensionamenti Previsti", f"{totale:,}")
        st.metric( "Probabilità Media Pensionamento", f"{rischio}%")
    

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