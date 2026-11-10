import streamlit as st
import plotly.express as px
import pandas as pd
from database import load_burnout
from components import topbar

# ============================================================
# CONTROLLO LOGIN
# ============================================================
if not st.session_state.get("logged",False):
    st.switch_page("streamlit_app.py")

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================
st.set_page_config(page_title="Forecast Workforce Planning",layout="wide")

# Caricamento topbar
topbar()

st.title("🔥 Burnout Forecast")

# Carico i dati dai modelli di Machine Learning
df = load_burnout()

# ============================================================
# DASHBOARD RISCHIO BURNOUT
# ============================================================
st.subheader("Dashboard Rischio Burnout")
fig = px.pie(
    df.groupby(
        "livello_burnout"
    ).size().reset_index(name="totale"),
    names="livello_burnout",
    values="totale",
    title="Distribuzione rischio burnout"
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

#============================================================
# DASHBOARD BURNOUT PER FASCIA D'ETA'
# ============================================================
st.subheader("Burnout medio per fascia d'età")
df["fascia_eta"] = pd.cut(
    df["eta_calcolata"],
    bins=[20,30,40,50,60,70],
    labels=[
        "20-30",
        "31-40",
        "41-50",
        "51-60",
        "60+"
    ]
)

fig = px.bar(
    df.groupby(
        "fascia_eta",
        as_index=False
    )["probabilita_burnout"].mean(),
    x="fascia_eta",
    y="probabilita_burnout",
    title="Burnout medio per fascia d'età"
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

# ===========================================================
# DASHBOARD BURNOUT vs STRAORDINARI
# ============================================================
st.subheader("Straordinari Vs Burnout")
fig = px.scatter(
    df,
    x="ore_straordinario_2025",
    y="probabilita_burnout",
    color="livello_burnout",
    title="Straordinari e rischio burnout"
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

# ==========================================================
# DASHBOARD BURNOUT vs PERFORMANCE
# ============================================================
st.subheader("Performance Vs Burnout")
fig = px.scatter(
    df,
    x="performance_2025",
    y="probabilita_burnout",
    color="livello_burnout",
    title="Performance e rischio burnout"
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

st.page_link("pages/01_Home.py", label="Torna alla Home", icon="🏠")
