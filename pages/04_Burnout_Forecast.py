import streamlit as st
import plotly.express as px
import pandas as pd
from database import load_burnout, load_ente_name
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

df = df.copy()

# Normalizzazione coerente livello_burnout: Basso -> Medio -> Alto
ordine_livelli = ["Basso", "Medio", "Alto"]
mappa_colori_burnout = {
    "Basso": "#5cb85c",
    "Medio": "#f0ad4e",
    "Alto": "#d9534f",
}

if "livello_burnout" in df.columns:
    df["livello_burnout"] = (
        df["livello_burnout"]
        .astype(str)
        .str.strip()
        .str.capitalize()
        .where(
            df["livello_burnout"].astype(str).str.strip().str.capitalize().isin(ordine_livelli),
            "Basso",
        )
    )
    df["livello_burnout"] = pd.Categorical(
        df["livello_burnout"],
        categories=ordine_livelli,
        ordered=True,
    )


def applica_stile_grafico(fig, is_bar=True):
    if is_bar:
        fig.update_traces(
            marker_line_color="rgba(0,0,0,0.2)",
            marker_line_width=1,
        )
    fig.update_layout(
        margin=dict(t=25, b=20, l=10, r=10),
        legend=dict(
            traceorder="normal",
            title=dict(text="Livello Burnout"),
        ),
    )
    return fig


def grafico_burnout_per_sesso(dati):
    st.subheader("Rischio Burnout per Sesso")
    if "sesso" not in dati.columns or dati["sesso"].dropna().empty:
        st.info("Colonna 'sesso' non disponibile.")
        return

    df_sesso = (
        dati.dropna(subset=["sesso"])
        .assign(
            sesso_label=lambda d: d["sesso"]
            .astype(str)
            .str.strip()
            .str.upper()
            .replace({"M": "Maschile", "F": "Femminile"})
        )
        .groupby("sesso_label", as_index=False)
        .agg(
            prob_media=("probabilita_burnout", "mean"),
            dipendenti=("probabilita_burnout", "count"),
        )
        .sort_values("prob_media", ascending=False)
    )

    fig = px.bar(
        df_sesso,
        x="sesso_label",
        y="prob_media",
        color="prob_media",
        color_continuous_scale=px.colors.sequential.OrRd[2:],
        text_auto=".1f",
        hover_data=["dipendenti"],
        labels={
            "sesso_label": "Sesso",
            "prob_media": "Probabilità Media (%)",
            "dipendenti": "Dipendenti",
        },
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(applica_stile_grafico(fig), width="stretch")


def grafico_burnout_per_qualifica(dati):
    st.subheader("Rischio Burnout per Qualifica")
    if "qualifica" not in dati.columns or dati["qualifica"].dropna().empty:
        st.info("Colonna 'qualifica' non disponibile.")
        return

    df_qual = (
        dati.dropna(subset=["qualifica"])
        .groupby("qualifica", as_index=False)
        .agg(
            prob_media=("probabilita_burnout", "mean"),
            dipendenti=("probabilita_burnout", "count"),
        )
        .sort_values("prob_media", ascending=True)
        .tail(12)
    )

    fig = px.bar(
        df_qual,
        x="prob_media",
        y="qualifica",
        orientation="h",
        color="prob_media",
        color_continuous_scale=px.colors.sequential.Blues[2:],
        text_auto=".1f",
        hover_data=["dipendenti"],
        labels={
            "prob_media": "Probabilità Media (%)",
            "qualifica": "Qualifica",
            "dipendenti": "Dipendenti",
        },
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(applica_stile_grafico(fig), width="stretch")


# ============================================================
# KPI SINTETICI IN ALTO
# ============================================================
k1, k2, k3 = st.columns(3)
k1.metric("Dipendenti Analizzati", f"{len(df):,}")
k2.metric("Probabilità Media Burnout", f"{df['probabilita_burnout'].mean():.1f}%")
alto_rischio = (df["livello_burnout"] == "Alto").sum()
k3.metric("Dipendenti a Rischio Alto", f"{alto_rischio:,}")

st.divider()

# ============================================================
# VISTA ADMIN
# ============================================================
if ruolo == Ruolo.ADMIN:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        grafico_burnout_per_qualifica(df)

    with col2:
        st.subheader("Rischio Burnout per Ente")
        df_plot_ente = df.copy()

        if "ente" in df_plot_ente.columns and not df_plot_ente["ente"].dropna().empty:
            col_ente = "ente"
        elif "ente_id" in df_plot_ente.columns and not df_plot_ente["ente_id"].dropna().empty:
            ids_unici = df_plot_ente["ente_id"].dropna().unique().tolist()
            mappa_enti = {}
            for e_id in ids_unici:
                df_info_ente = load_ente_name(e_id)
                if df_info_ente is not None and not df_info_ente.empty:
                    for col_nome in ["nome", "denominazione", "ente"]:
                        if col_nome in df_info_ente.columns:
                            mappa_enti[e_id] = df_info_ente[col_nome].iloc[0]
                            break

            if mappa_enti:
                df_plot_ente["nome_ente"] = df_plot_ente["ente_id"].map(mappa_enti).fillna(
                    df_plot_ente["ente_id"].astype(str)
                )
                col_ente = "nome_ente"
            else:
                col_ente = "ente_id"
        else:
            col_ente = None

        if col_ente:
            df_ente = (
                df_plot_ente.dropna(subset=[col_ente])
                .groupby(col_ente, as_index=False)
                .agg(
                    prob_media=("probabilita_burnout", "mean"),
                    dipendenti=("probabilita_burnout", "count"),
                )
                .sort_values("prob_media", ascending=True)
                .tail(12)
            )
            fig3 = px.bar(
                df_ente,
                x="prob_media",
                y=col_ente,
                orientation="h",
                color="prob_media",
                color_continuous_scale=px.colors.sequential.Reds[2:],
                text_auto=".1f",
                hover_data=["dipendenti"],
                labels={
                    "prob_media": "Probabilità Media (%)",
                    col_ente: "Ente",
                    "dipendenti": "Dipendenti",
                },
            )
            fig3.update_traces(textposition="outside")
            fig3.update_yaxes(dtick=1)
            st.plotly_chart(applica_stile_grafico(fig3), width="stretch")
        else:
            st.info("Informazione sull'ente non disponibile nei dati.")

# ============================================================
# VISTA REGIONALE / PROVINCIALE (dati già filtrati per ruolo)
# ============================================================
else:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        grafico_burnout_per_sesso(df)

    with col2:
        grafico_burnout_per_qualifica(df)

st.divider()
tasto_torna_home()