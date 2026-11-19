import streamlit as st
import plotly.express as px
import pandas as pd
from database import load_burnout
from components import topbar, tasto_torna_home
from style import load_css_tasto_home
from utility.costanti import Ruolo

# ============================================================
# CONFIGURAZIONE PAGINA (sempre come prima istruzione Streamlit)
# ============================================================
st.set_page_config(page_title="Burnout Forecast", layout="wide")

# ============================================================
# CONTROLLO LOGIN
# ============================================================
if not st.session_state.get("logged", False):
    st.switch_page("streamlit_app.py")

ruolo = st.session_state.get("ruolo")
regione = st.session_state.get("regione")
provincia = st.session_state.get("provincia")
ente_id = st.session_state.get("ente_id")

topbar()
load_css_tasto_home()

st.title("🔥 Burnout Forecast")

# ============================================================
# CARICAMENTO DATI IN BASE AL RUOLO
# ============================================================
if ruolo == Ruolo.ADMIN:
    df = load_burnout()

elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    if not regione or ente_id is None:
        df = pd.DataFrame()
    else:
        df = load_burnout(regione=regione, ente_id=ente_id)

elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    if not regione or not provincia or ente_id is None:
        df = pd.DataFrame()
    else:
        df = load_burnout(regione=regione, provincia=provincia, ente_id=ente_id)

else:
    st.error("Ruolo non riconosciuto.")
    st.stop()


# ============================================================
# CONTROLLO ASSENZA DATI
# ============================================================
if df is None or df.empty:
    st.info(
        "📭 **Non sono presenti dati per questa casistica.**\n\n"
        "Non risultano previsioni di burnout associate al tuo profilo territoriale.",
        icon="ℹ️",
    )
    st.divider()
    tasto_torna_home()
    st.stop()


# ============================================================
# KPI SINTETICI IN ALTO
# ============================================================
k1, k2, k3 = st.columns(3)
k1.metric("Dipendenti Analizzati", f"{len(df):,}")
k2.metric("Probabilità Media Burnout", f"{df['probabilita_burnout'].mean():.1f}%")
alto_rischio = (df["livello_burnout"].str.lower() == "alto").sum()
k3.metric("Dipendenti a Rischio Alto", f"{alto_rischio:,}")

st.divider()

# Palette coerente per i livelli di burnout
mappa_colori_burnout = {
    "Alto": "#d9534f",
    "alto": "#d9534f",
    "Medio": "#f0ad4e",
    "medio": "#f0ad4e",
    "Basso": "#5cb85c",
    "basso": "#5cb85c",
}

# ============================================================
# RIGA 1: DISTRIBUZIONE BURNOUT + BURNOUT PER FASCIA D'ETÀ
# ============================================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Distribuzione Rischio Burnout")
    df_pie = (
        df.groupby("livello_burnout", as_index=False)
        .size()
        .rename(columns={"size": "totale"})
    )
    fig1 = px.pie(
        df_pie,
        names="livello_burnout",
        values="totale",
        hole=0.45,
        color="livello_burnout",
        color_discrete_map=mappa_colori_burnout,
    )
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    fig1.update_layout(margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig1, width="stretch")

with col2:
    st.subheader("Burnout Medio per Fascia d'Età")
    df["fascia_eta"] = pd.cut(
        df["eta_calcolata"],
        bins=[18, 30, 40, 50, 60, 75],
        labels=["18-30", "31-40", "41-50", "51-60", "60+"],
    )
    df_eta = (
        df.groupby("fascia_eta", as_index=False, observed=False)["probabilita_burnout"]
        .mean()
        .dropna()
    )
    fig2 = px.bar(
        df_eta,
        x="fascia_eta",
        y="probabilita_burnout",
        color="probabilita_burnout",
        color_continuous_scale=px.colors.sequential.OrRd[2:],
        text_auto=".1f",
        labels={
            "fascia_eta": "Fascia d'Età",
            "probabilita_burnout": "Probabilità Media (%)",
        },
    )
    fig2.update_traces(
        marker_line_color="rgba(0,0,0,0.2)",
        marker_line_width=1,
        textposition="outside",
    )
    fig2.update_layout(margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig2, width="stretch")

st.divider()

# ============================================================
# RIGA 2: BURNOUT PER FASCE DI STRAORDINARI + QUOTA RISCHIO PER PERFORMANCE
# ============================================================
col3, col4 = st.columns(2, gap="large")

with col3:
    st.subheader("Probabilità Media Burnout per Fasce di Straordinario")
    df["fascia_straordinari"] = pd.cut(
        df["ore_straordinario_2025"],
        bins=[-1, 50, 100, 150, 200, 1000],
        labels=["0-50h", "51-100h", "101-150h", "151-200h", "200h+"],
    )
    df_straord = (
        df.groupby("fascia_straordinari", as_index=False, observed=False)
        .agg(
            prob_media=("probabilita_burnout", "mean"),
            dipendenti=("probabilita_burnout", "count"),
        )
        .dropna()
    )
    fig3 = px.bar(
        df_straord,
        x="fascia_straordinari",
        y="prob_media",
        color="prob_media",
        color_continuous_scale=px.colors.sequential.Reds[2:],
        text_auto=".1f",
        hover_data=["dipendenti"],
        labels={
            "fascia_straordinari": "Ore Straordinario (2025)",
            "prob_media": "Probabilità Media (%)",
            "dipendenti": "Dipendenti",
        },
    )
    fig3.update_traces(
        marker_line_color="rgba(0,0,0,0.2)",
        marker_line_width=1,
        textposition="outside",
    )
    fig3.update_layout(margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig3, width="stretch")

with col4:
    st.subheader("Distribuzione Livello Burnout per Fascia di Performance")
    df["fascia_performance"] = pd.cut(
        df["performance_2025"],
        bins=[0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.5],
        labels=["<=2.5", "2.6-3.0", "3.1-3.5", "3.6-4.0", "4.1-4.5", "4.6-5.0"],
    )
    df_perf_liv = (
        df.groupby(["fascia_performance", "livello_burnout"], as_index=False, observed=False)
        .size()
        .rename(columns={"size": "dipendenti"})
    )
    fig4 = px.bar(
        df_perf_liv,
        x="fascia_performance",
        y="dipendenti",
        color="livello_burnout",
        barmode="stack",
        color_discrete_map=mappa_colori_burnout,
        labels={
            "fascia_performance": "Fascia Performance (2025)",
            "dipendenti": "Numero Dipendenti",
            "livello_burnout": "Livello Burnout",
        },
    )
    fig4.update_traces(marker_line_color="rgba(0,0,0,0.2)", marker_line_width=1)
    fig4.update_layout(margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig4, width="stretch")

st.divider()
tasto_torna_home()