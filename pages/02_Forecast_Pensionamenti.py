import streamlit as st
import plotly.express as px
from database import (
    load_pensionamenti_nazionali, 
    load_pensionamenti_regione, 
    load_pensionamenti_provincia, 
    load_pensionamenti_annuali
)
from components import topbar, tasto_torna_home
from style import load_css_tasto_home
from utility.costanti import Ruolo

#===========================================================
# CONTROLLO LOGIN
#===========================================================
if not st.session_state.get("logged", False):
    st.switch_page("streamlit_app.py")
    
#===========================================================
# CONFIGURAZIONE PAGINA
#===========================================================
st.set_page_config(page_title="Forecast Pensionamenti", layout="wide")
ruolo = st.session_state.get("ruolo")
regione = st.session_state.get("regione")
provincia = st.session_state.get("provincia")
ente = st.session_state.get("ente_nome")

# Caricamento topbar
topbar()
load_css_tasto_home()

st.title("📈 Forecast Pensionamenti")

# Carico i dati dai modelli di Machine Learning
if ruolo == Ruolo.ADMIN:
    df = load_pensionamenti_nazionali()
    df_annuale = load_pensionamenti_annuali()

elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    df = load_pensionamenti_regione(regione, ente)
    df = df[(df["regione"] == regione) & (df["ente"] == ente)]

elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    df = load_pensionamenti_provincia(regione, provincia, ente)
    df = df[(df["regione"] == regione) & (df["provincia"] == provincia) & (df["ente"] == ente)]
    

if ruolo == Ruolo.ADMIN:
    # 1. Pensionamento medio per Ente (con colore personalizzato e alias)
    st.subheader("Pensionamento medio per Ente")
    fig = px.bar(
        df.groupby("ente", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="ente",
        y="probabilita_media",
        color="probabilita_media",
        color_continuous_scale="Blues",
        labels={"ente": "Ente", "probabilita_media": "Probabilità Media"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # 2. Top 5 Enti a rischio (Barre orizzontali, orientate con scala di rosso)
    st.subheader("Top 5 Enti a rischio")
    fig = px.bar(
        df.groupby("ente", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=True).tail(5), # .tail(5) con ascending=True mette i più alti in alto
        x="probabilita_media",
        y="ente",
        orientation="h",
        color="probabilita_media",
        color_continuous_scale="Reds",
        labels={"ente": "Ente", "probabilita_media": "Probabilità Media"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # 3. Pensionamento medio per Qualifica (con colore fisso personalizzato)
    st.subheader("Pensionamento medio per Qualifica")
    fig = px.bar(
        df.groupby("qualifica", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="qualifica",
        y="probabilita_media",
        color_discrete_sequence=["#29b5e8"],
        labels={"qualifica": "Qualifica Professionale", "probabilita_media": "Probabilità Media"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    
    # 4. Pensionamenti previsti per anno (Linea con colore personalizzato)
    st.subheader("Pensionamenti previsti per anno")
    fig = px.line(
        df_annuale, 
        x="anno", 
        y="count", 
        markers=True,
        labels={"anno": "Anno di Riferimento", "count": "Numero Previsto"}
    )
    fig.update_traces(line_color="#FF4B4B", marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)
        
       
elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    st.subheader(f"Pensionamenti per Provincia - {regione}")
    fig = px.bar(
        df.groupby("provincia", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="provincia",
        y="probabilita_media",
        color="probabilita_media",
        color_continuous_scale="Viridis",
        labels={"provincia": "Provincia", "probabilita_media": "Probabilità Media"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Qualifiche più esposte")
    fig = px.bar(
        df.groupby("qualifica", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="qualifica",
        y="probabilita_media",
        color="probabilita_media",
        color_continuous_scale="Teal",
        labels={"qualifica": "Qualifica", "probabilita_media": "Probabilità Media"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pensionamenti Previsti", int(df["numero_pensionamenti"].sum()))
    with col2:
        st.metric("Probabilità Media", round(df["probabilita_media"].mean(), 2))
        
    fig = px.bar(
        df.groupby("qualifica", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="qualifica",
        y="probabilita_media",
        color="probabilita_media",
        color_continuous_scale="Purples",
        labels={"qualifica": "Qualifica", "probabilita_media": "Probabilità Media"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
st.divider()

tasto_torna_home()