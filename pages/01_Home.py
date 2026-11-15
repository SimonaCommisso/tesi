import streamlit as st
import requests
import pandas as pd
import style
from components import topbar
from database import load_last_refresh, load_pensionamenti
from streamlit_folium import st_folium
import folium


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

    st.markdown("""
    <div class="dashboard-card">
        <div class="dashboard-title">
            🗺️ Ambito Territoriale
        </div>
    </div>
    """,
    unsafe_allow_html=True)

    regione = st.session_state.get("regione")
    provincia = st.session_state.get("provincia")

    # ADMIN
    if regione is None:
        st.info("🌍 Visualizzazione Nazionale")
        m = folium.Map(location=[42.5, 12.5], zoom_start=5, tiles="OpenStreetMap")

    # UTENTE REGIONALE
    elif provincia is None:

        st.success(f"📍 Regione: {regione}")
        coordinate_regioni = {
            "Abruzzo": [42.3500, 13.4000],
            "Basilicata": [40.5000, 16.0833],
            "Calabria": [38.9100, 16.5900],
            "Campania": [40.8399, 14.2525],
            "Emilia-Romagna": [44.4949, 11.3426],
            "Friuli Venezia Giulia": [45.6495, 13.7768],
            "Lazio": [41.9028, 12.4964],
            "Liguria": [44.4056, 8.9463],
            "Lombardia": [45.4642, 9.1900],
            "Marche": [43.6158, 13.5189],
            "Molise": [41.5600, 14.6600],
            "Piemonte": [45.0703, 7.6869],
            "Provincia Autonoma Bolzano": [46.4983, 11.3548],
            "Provincia Autonoma Trento": [46.0748, 11.1217],
            "Puglia": [41.1171, 16.8719],
            "Sardegna": [39.2238, 9.1217],
            "Sicilia": [38.1157, 13.3615],
            "Toscana": [43.7696, 11.2558],
            "Umbria": [43.1107, 12.3908],
            "Valle d'Aosta": [45.7370, 7.3201],
            "Veneto": [45.4408, 12.3155]
        }

        lat, lon = coordinate_regioni.get(regione, [42.5, 12.5])

        m = folium.Map(location=[lat, lon], zoom_start=8, tiles="CartoDB positron")

        folium.Marker([lat, lon],
            popup=regione,
            tooltip=regione).add_to(m)

    # UTENTE PROVINCIALE
    else:

        st.success(f"📍 Provincia: {provincia}")

        coordinate_province = {
             "Chieti": [42.3512, 14.1675],
            "L'Aquila": [42.3500, 13.3995],
            "Pescara": [42.4618, 14.2161],
            "Teramo": [42.6589, 13.7044],

            "Matera": [40.6663, 16.6043],
            "Potenza": [40.6400, 15.8050],

            "Catanzaro": [38.9098, 16.5877],
            "Cosenza": [39.2983, 16.2537],
            "Crotone": [39.0808, 17.1271],
            "Reggio Calabria": [38.1113, 15.6473],
            "Vibo Valentia": [38.6750, 16.1000],

            "Avellino": [40.9149, 14.7920],
            "Benevento": [41.1298, 14.7826],
            "Caserta": [41.0740, 14.3330],
            "Napoli": [40.8518, 14.2681],
            "Salerno": [40.6824, 14.7681],

            "Bologna": [44.4949, 11.3426],
            "Ferrara": [44.8381, 11.6198],
            "Forli-Cesena": [44.2227, 12.0400],
            "Modena": [44.6471, 10.9252],
            "Parma": [44.8015, 10.3279],
            "Piacenza": [45.0526, 9.6930],
            "Ravenna": [44.4184, 12.2035],
            "Reggio Emilia": [44.6982, 10.6313],
            "Rimini": [44.0678, 12.5695],

            "Gorizia": [45.9410, 13.6217],
            "Pordenone": [45.9564, 12.6600],
            "Trieste": [45.6495, 13.7768],
            "Udine": [46.0711, 13.2346],

            "Frosinone": [41.6396, 13.3417],
            "Latina": [41.4676, 12.9036],
            "Rieti": [42.4044, 12.8567],
            "Roma": [41.9028, 12.4964],
            "Viterbo": [42.4207, 12.1077],

            "Genova": [44.4056, 8.9463],
            "Imperia": [43.8896, 8.0392],
            "La Spezia": [44.1078, 9.8231],
            "Savona": [44.3072, 8.4810],

            "Bergamo": [45.6983, 9.6773],
            "Brescia": [45.5416, 10.2118],
            "Como": [45.8081, 9.0852],
            "Cremona": [45.1332, 10.0227],
            "Lecco": [45.8566, 9.3977],
            "Lodi": [45.3141, 9.5036],
            "Mantova": [45.1564, 10.7914],
            "Milano": [45.4642, 9.1900],
            "Monza e Brianza": [45.5845, 9.2744],
            "Pavia": [45.1847, 9.1582],
            "Sondrio": [46.1699, 9.8782],
            "Varese": [45.8206, 8.8251],

            "Ancona": [43.6158, 13.5189],
            "Ascoli Piceno": [42.8530, 13.5749],
            "Fermo": [43.1600, 13.7186],
            "Macerata": [43.3008, 13.4534],
            "Pesaro e Urbino": [43.9097, 12.9133],

            "Campobasso": [41.5600, 14.6600],
            "Isernia": [41.5960, 14.2330],

            "Alessandria": [44.9128, 8.6157],
            "Asti": [44.9000, 8.2060],
            "Biella": [45.5628, 8.0583],
            "Cuneo": [44.3845, 7.5427],
            "Novara": [45.4469, 8.6212],
            "Torino": [45.0703, 7.6869],
            "Verbano Cusio Ossola": [45.9214, 8.5512],
            "Vercelli": [45.3217, 8.4236],

            "Bolzano": [46.4983, 11.3548],
            "Trento": [46.0748, 11.1217],

            "Bari": [41.1171, 16.8719],
            "Barletta-Andria-Trani": [41.2000, 16.0833],
            "Brindisi": [40.6327, 17.9418],
            "Foggia": [41.4622, 15.5446],
            "Lecce": [40.3515, 18.1750],
            "Taranto": [40.4644, 17.2470],

            "Cagliari": [39.2238, 9.1217],
            "Nuoro": [40.3219, 9.3300],
            "Oristano": [39.9036, 8.5920],
            "Sassari": [40.7259, 8.5557],

            "Agrigento": [37.3111, 13.5765],
            "Caltanissetta": [37.4901, 14.0629],
            "Catania": [37.5079, 15.0830],
            "Enna": [37.5676, 14.2794],
            "Messina": [38.1938, 15.5540],
            "Palermo": [38.1157, 13.3615],
            "Ragusa": [36.9269, 14.7255],
            "Siracusa": [37.0755, 15.2866],
            "Trapani": [38.0176, 12.5365],

            "Arezzo": [43.4633, 11.8781],
            "Firenze": [43.7696, 11.2558],
            "Grosseto": [42.7635, 11.1124],
            "Livorno": [43.5485, 10.3106],
            "Lucca": [43.8429, 10.5027],
            "Massa Carrara": [44.0354, 10.1393],
            "Pisa": [43.7228, 10.4017],
            "Pistoia": [43.9333, 10.9167],
            "Prato": [43.8777, 11.1022],
            "Siena": [43.3188, 11.3308],

            "Perugia": [43.1107, 12.3908],
            "Terni": [42.5636, 12.6427],

            "Aosta": [45.7370, 7.3201],

            "Belluno": [46.1426, 12.2156],
            "Padova": [45.4064, 11.8768],
            "Rovigo": [45.0703, 11.7901],
            "Treviso": [45.6669, 12.2430],
            "Venezia": [45.4408, 12.3155],
            "Verona": [45.4384, 10.9916],
            "Vicenza": [45.5455, 11.5354]
        }

        lat, lon = coordinate_province.get(provincia, [42.5, 12.5])

        m = folium.Map(location=[lat, lon], zoom_start=10, tiles="CartoDB positron")

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color="#0f2454",
            fill=True,
            fill_opacity=0.8
        ).add_to(m)

    st_folium(
        m,
        width=None,
        height=450
    )

with col_kpi:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="dashboard-title">
                📈 Forecast Pensionamenti
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
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