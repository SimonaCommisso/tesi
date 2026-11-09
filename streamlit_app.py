import streamlit as st
import requests

HOST = st.secrets["databricks"]["host"]
TOKEN = st.secrets["databricks"]["token"]
JOB_ID = st.secrets["databricks"]["job_id"]

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

st.title("🏛️ HR Analytics Dashboard")

st.markdown("""
Questa dashboard supporta l'analisi strategica delle risorse umane
della Pubblica Amministrazione attraverso:

- 📈 Forecast Pensionamenti
- 🧠 Strategic Workforce Planning
- 🔥 Burnout Risk Forecast
""")

st.divider()

if st.button("🔄 Aggiorna Modelli"):

    url = f"https://{HOST}/api/2.1/jobs/run-now"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"job_id": JOB_ID}
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        st.success("Job avviato correttamente")
        st.json(response.json())
    else:
        st.error(f"Errore: {response.text}")