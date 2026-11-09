import streamlit as st
import requests

HOST = st.secrets["databricks"]["host"]
TOKEN = st.secrets["databricks"]["token"]
JOB_ID = st.secrets["databricks"]["job_id"]
st.title("HR Analytics Dashboard")

if st.button("🔄 Aggiorna Modelli"):
    url = f"https://{HOST}/api/2.1/jobs/run-now"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"job_id": JOB_ID}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        st.success("Job avviato correttamente")
        st.json(response.json())
    else:
        st.error(f"Errore: {response.text}")
