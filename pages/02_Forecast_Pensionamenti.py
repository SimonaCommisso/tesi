import streamlit as st
import plotly.express as px
from database import (
    load_pensionamenti_nazionali, 
    load_pensionamenti_regione, 
    load_pensionamenti_provincia, 
    load_pensionamenti_annuali
)
from components import topbar

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
ente = st.session_state.get("ente_id")

# Caricamento topbar
topbar()

st.title("📈 Forecast Pensionamenti")

# Carico i dati dai modelli di Machine Learning
if ruolo == "Admin":
    df = load_pensionamenti_nazionali()
    df_annuale = load_pensionamenti_annuali()

elif ruolo == "Visualizzatore Regionale":
    df = load_pensionamenti_regione(regione)
    df = df[(df["regione"] == regione) & (df["ente_id"] == ente)]

elif ruolo == "Visualizzatore Provinciale":
    df = load_pensionamenti_provincia(regione, provincia)
    df = df[(df["regione"] == regione) & (df["provincia"] == provincia) & (df["ente_id"] == ente)]
    

if ruolo == "Admin":
    st.subheader("Pensionamento medio per Ente")

    fig = px.bar(df.groupby("ente", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="ente",
        y="probabilita_media")

    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    st.subheader("Top 10 Enti a rischio")
    fig = px.bar(df.groupby("ente", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False).head(10),
        x="ente",
        y="probabilita_media")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Pensionamento medio per Qualifica")
    fig = px.bar(df.groupby("qualifica", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="qualifica",
        y="probabilita_media")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("Pensionamienti previsti per anno")
    fig = px.line(df_annuale, x="anno", y="count", markers=True)
    st.plotly_chart(fig, use_container_width=True)
        
       
elif ruolo == "Visualizzatore Regionale":
    st.subheader(f"Pensionamenti per Provincia - {regione}")
    fig = px.bar(df.groupby("provincia", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="provincia",
        y="probabilita_media",
        color="probabilita_media"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Qualifiche più esposte")
    fig = px.bar(df.groupby("qualifica", as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="qualifica",
        y="probabilita_media"
    )
    st.plotly_chart(fig, use_container_width=True)
    
elif ruolo == "Visualizzatore Provinciale":
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pensionamenti Previsti", int(df["numero_pensionamenti"].sum()))
    with col2:
        st.metric("Probabilità Media", round(df["probabilita_media"].mean(),2))
        
    fig = px.bar(df.groupby("qualifica",as_index=False)
        .agg({"probabilita_media":"mean"})
        .sort_values("probabilita_media", ascending=False),
        x="qualifica",
        y="probabilita_media")
    st.plotly_chart(fig, use_container_width=True)
    
st.divider()

st.page_link("pages/01_Home.py", label="Torna alla Home", icon="🏠")