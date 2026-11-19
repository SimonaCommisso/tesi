import streamlit as st
import plotly.express as px
from database import (
    load_pensionamenti_nazionali,
    load_pensionamenti,
    load_pensionamenti_annuali,
)
from components import topbar, tasto_torna_home
from style import load_css_tasto_home
from utility.costanti import Ruolo

# ===========================================================
# CONFIGURAZIONE PAGINA (sempre come prima istruzione Streamlit)
# ===========================================================
st.set_page_config(page_title="Forecast Pensionamenti", layout="wide")

# ===========================================================
# CONTROLLO LOGIN
# ===========================================================
if not st.session_state.get("logged", False):
    st.switch_page("streamlit_app.py")

ruolo = st.session_state.get("ruolo")
regione = st.session_state.get("regione")
provincia = st.session_state.get("provincia")
ente = st.session_state.get("ente_nome")

topbar()
load_css_tasto_home()

st.title("📈 Forecast Pensionamenti")

# ===========================================================
# CARICAMENTO DATI
# ===========================================================
if ruolo == Ruolo.ADMIN:
    df = load_pensionamenti_nazionali()
    df_annuale = load_pensionamenti_annuali()

elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    df = load_pensionamenti(regione, provincia, ente)
    df = df[(df["regione"] == regione) & (df["ente"] == ente)]

elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    df = load_pensionamenti(regione, provincia, ente)
    df = df[
        (df["regione"] == regione)
        & (df["provincia"] == provincia)
        & (df["ente"] == ente)
    ]

else:
    st.error("Ruolo non riconosciuto.")
    st.stop()


def rifinisci_barre(fig):
    """Evita barre bianche invisibili aggiungendo un bordo leggero."""
    fig.update_traces(marker_line_color="rgba(0,0,0,0.2)", marker_line_width=1)
    fig.update_layout(margin=dict(t=20, b=20, l=10, r=10))
    return fig


# ===========================================================
# VISTA ADMIN (Griglia 2x2)
# ===========================================================
if ruolo == Ruolo.ADMIN:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Pensionamento medio per Ente")
        fig1 = px.bar(
            df.groupby("ente", as_index=False)
            .agg({"affinita_storica_media": "mean"})
            .sort_values("affinita_storica_media", ascending=False),
            x="ente",
            y="affinita_storica_media",
            color="affinita_storica_media",
            color_continuous_scale=px.colors.sequential.Blues[2:],
            labels={"ente": "Ente", "affinita_storica_media": "Affinità Media (%)"},
        )
        st.plotly_chart(rifinisci_barre(fig1), width="stretch")

    with col2:
        st.subheader("Top 5 Enti a rischio")
        fig2 = px.bar(
            df.groupby("ente", as_index=False)
            .agg({"affinita_storica_media": "mean"})
            .sort_values("affinita_storica_media", ascending=True)
            .tail(5),
            x="affinita_storica_media",
            y="ente",
            orientation="h",
            color="affinita_storica_media",
            color_continuous_scale=px.colors.sequential.Reds[2:],
            labels={"ente": "Ente", "affinita_storica_media": "Affinità Media (%)"},
        )
        st.plotly_chart(rifinisci_barre(fig2), width="stretch")

    st.divider()
    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.subheader("Pensionamento medio per Qualifica")
        df_qual_admin = (
            df.groupby("qualifica", as_index=False)
            .agg({"affinita_storica_media": "mean"})
            .sort_values("affinita_storica_media", ascending=False)
        )
        fig3 = px.bar(
            df_qual_admin,
            x="qualifica",
            y="affinita_storica_media",
            color="affinita_storica_media",
            color_continuous_scale=px.colors.sequential.Greens[2:],
            labels={
                "qualifica": "Qualifica Professionale",
                "affinita_storica_media": "Affinità Media (%)",
            },
        )
        st.plotly_chart(rifinisci_barre(fig3), width="stretch")

    with col4:
        st.subheader("Pensionamenti previsti per anno")
        col_anno = (
            "anno_pensione_stimato"
            if "anno_pensione_stimato" in df_annuale.columns
            else "anno"
        )
        col_valore = (
            "numero_dipendenti_stimati"
            if "numero_dipendenti_stimati" in df_annuale.columns
            else "count"
        )

        df_annuale_plot = (
            df_annuale.dropna(subset=[col_anno, col_valore])
            .groupby(col_anno, as_index=False)[col_valore]
            .sum()
            .sort_values(col_anno)
        )

        fig4 = px.line(
            df_annuale_plot,
            x=col_anno,
            y=col_valore,
            markers=True,
            labels={
                col_anno: "Anno di Riferimento",
                col_valore: "Numero Previsto",
            },
        )
        fig4.update_traces(line_color="#FF4B4B", marker=dict(size=8))
        fig4.update_layout(margin=dict(t=20, b=20, l=10, r=10))
        st.plotly_chart(fig4, width="stretch")


# ===========================================================
# VISTA REGIONALE (2 grafici affiancati)
# ===========================================================
elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader(f"Pensionamenti per Provincia - {regione}")
        fig_geo = px.bar(
            df.groupby("provincia", as_index=False)
            .agg({"affinita_storica_media": "mean"})
            .sort_values("affinita_storica_media", ascending=False),
            x="provincia",
            y="affinita_storica_media",
            color="affinita_storica_media",
            color_continuous_scale=px.colors.sequential.Viridis,
            labels={"provincia": "Provincia", "affinita_storica_media": "Affinità Media (%)"},
        )
        st.plotly_chart(rifinisci_barre(fig_geo), width="stretch")

    with col2:
        st.subheader("Qualifiche più esposte")
        fig_qual = px.bar(
            df.groupby("qualifica", as_index=False)
            .agg({"affinita_storica_media": "mean"})
            .sort_values("affinita_storica_media", ascending=False),
            x="qualifica",
            y="affinita_storica_media",
            color="affinita_storica_media",
            color_continuous_scale=px.colors.sequential.Teal[2:],
            labels={"qualifica": "Qualifica", "affinita_storica_media": "Affinità Media (%)"},
        )
        st.plotly_chart(rifinisci_barre(fig_qual), width="stretch")


# ===========================================================
# VISTA PROVINCIALE (KPI + 2 grafici affiancati)
# ===========================================================
elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric("Pensionamenti Previsti", int(df["numero_pensionamenti"].sum()))
    with kpi2:
        st.metric("Affinità Media", f"{df['affinita_storica_media'].mean():.2f}%")

    st.divider()
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Affinità Media per Qualifica")
        fig1 = px.bar(
            df.groupby("qualifica", as_index=False)
            .agg({"affinita_storica_media": "mean"})
            .sort_values("affinita_storica_media", ascending=False),
            x="qualifica",
            y="affinita_storica_media",
            color="affinita_storica_media",
            color_continuous_scale=px.colors.sequential.Purples[2:],
            labels={"qualifica": "Qualifica", "affinita_storica_media": "Affinità Media (%)"},
        )
        st.plotly_chart(rifinisci_barre(fig1), width="stretch")

    with col2:
        st.subheader("Pensionamenti Previsti per Qualifica")
        fig2 = px.bar(
            df.groupby("qualifica", as_index=False)
            .agg({"numero_pensionamenti": "sum"})
            .sort_values("numero_pensionamenti", ascending=False),
            x="qualifica",
            y="numero_pensionamenti",
            color="numero_pensionamenti",
            color_continuous_scale=px.colors.sequential.Blues[2:],
            labels={"qualifica": "Qualifica", "numero_pensionamenti": "Pensionamenti Previsti"},
        )
        st.plotly_chart(rifinisci_barre(fig2), width="stretch")

st.divider()
tasto_torna_home()