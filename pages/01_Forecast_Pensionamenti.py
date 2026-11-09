import streamlit as st
import plotly.express as px

from database import load_pensionamenti

st.set_page_config(
    page_title="Forecast Pensionamenti",
    layout="wide"
)

st.title("📈 Forecast Pensionamenti")

df = load_pensionamenti()

#============================================================
# DASHBOARD PENSIONAMENTI
# ============================================================
st.subheader("Pensionamento medio per Regione")
fig = px.bar(
    df.groupby("regione", as_index=False)
      .agg({
          "probabilita_media_pensionamento":"mean"
      })
      .sort_values(
          "probabilita_media_pensionamento",
          ascending=False
      ),
    x="regione",
    y="probabilita_media_pensionamento",
    title="Probabilità media pensionamento per Regione"
)
st.divider()

# ===========================================================
# DASHBOARD TOP ENTI A RISCHIO
# ============================================================
st.subheader("Top Enti a rischio")
fig = px.bar(
    df.groupby("ente", as_index=False)
      .agg({
          "probabilita_media_pensionamento":"mean"
      })
      .sort_values(
          "probabilita_media_pensionamento",
          ascending=False
      )
      .head(10),
    x="ente",
    y="probabilita_media_pensionamento",
    title="Top 10 Enti a rischio pensionamento"
)
st.divider()

# ===========================================================
# DASHBOARD DISTRIBUZIONE RISCHIO
# ============================================================
st.subheader("Distribuzione livello rischio")
fig = px.pie(
    df.groupby(
        "livello_rischio"
    ).size().reset_index(name="totale"),
    names="livello_rischio",
    values="totale",
    title="Distribuzione rischio pensionamento"
)

st.divider()

st.subheader("Pensionamento per Qualifica")
fig = px.bar(
    df.groupby("qualifica", as_index=False)
      .agg({
          "probabilita_media_pensionamento":"mean"
      })
      .sort_values(
          "probabilita_media_pensionamento",
          ascending=False
      ),
    x="qualifica",
    y="probabilita_media_pensionamento",
    title="Probabilità pensionamento per qualifica"
)

st.page_link("streamlit_app.py", label="Torna alla Home", icon="🏠")


