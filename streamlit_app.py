import streamlit as st
import requests

HOST = st.secrets["databricks"]["host"]
TOKEN = st.secrets["databricks"]["token"]
JOB_ID = st.secrets["databricks"]["job_id"]

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

st.title("🏛️ HR Analytics nella Pubblica Amministrazione")

st.markdown("""
Questa dashboard supporta l'analisi strategica delle risorse umane
della Pubblica Amministrazione attraverso:

- 📈 Forecast Pensionamenti
- 🧠 Strategic Workforce Planning
- 🔥 Burnout Risk Forecast
""")

st.divider()

# ============================================================
# AGGIORNA MODELLI
# ============================================================

if st.button("🔄 Aggiorna Modelli"):

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

st.divider()

# ============================================================
# NAVIGAZIONE
# ============================================================

st.subheader("📊 Dashboard Analitiche")

st.write("Test")

# col1, col2, col3 = st.columns(3)

# with col1:

#     st.page_link(
#         "pages/01_Forecast_Pensionamenti.py",
#         label="📈 Forecast Pensionamenti",
#         icon="📈"
#     )

#     st.caption(
#         "Analisi delle uscite previste e del turnover."
#     )

# with col2:

#     st.page_link(
#         "pages/02_Strategic_Workforce_Planning.py",
#         label="🧠 Workforce Planning",
#         icon="🧠"
#     )

#     st.caption(
#         "Skill gap, skill loss e competenze future."
#     )

# with col3:

#     st.page_link(
#         "pages/03_Burnout_Forecast.py",
#         label="🔥 Burnout Forecast",
#         icon="🔥"
#     )

#     st.caption(
#         "Rischio burnout e benessere organizzativo."
#     )

st.divider()

st.info(
    "Seleziona una dashboard per visualizzare i risultati dei modelli HR Analytics."
)