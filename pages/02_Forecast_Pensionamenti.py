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
    df = load_pensionamenti_regione(regione, ente)
    df = df[(df["regione"] == regione) & (df["ente"] == ente)]

elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    df = load_pensionamenti_provincia(regione, provincia, ente)
    df = df[(df["regione"] == regione) & (df["provincia"] == provincia) & (df["ente"] == ente)]

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
            .agg({"probabilita_media": "mean"})
            .sort_values("probabilita_media", ascending=False),
            x="ente",
            y="probabilita_media",
            color="probabilita_media",
            color_continuous_scale=px.colors.sequential.Blues[2:],
            labels={"ente": "Ente", "probabilita_media": "Probabilità Media"}
        )
        st.plotly_chart(rifinisci_barre(fig1), use_container_width=True)

    with col2:
        st.subheader("Top 5 Enti a rischio")
        fig2 = px.bar(
            df.groupby("ente", as_index=False)
            .agg({"probabilita_media": "mean"})
            .sort_values("probabilita_media", ascending=True)
            .tail(5),
            x="probabilita_media",
            y="ente",
            orientation="h",
            color="probabilita_media",
            color_continuous_scale=px.colors.sequential.Reds[2:],
            labels={"ente": "Ente", "probabilita_media": "Probabilità Media"}
        )
        st.plotly_chart(rifinisci_barre(fig2), use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.subheader("Pensionamento medio per Qualifica")
        fig3 = px.bar(
            df.groupby("qualifica", as_index=False)
            .agg({"probabilita_media": "mean"})
            .sort_values("probabilita_media", ascending=False),
            x="qualifica",
            y="probabilita_media",
            color_discrete_sequence=["#29b5e8"],
            labels={"qualifica": "Qualifica Professionale", "probabilita_media": "Probabilità Media"}
        )
        st.plotly_chart(rifinisci_barre(fig3), use_container_width=True)

    with col4:
        st.subheader("Pensionamenti previsti per anno")
        fig4 = px.line(
            df_annuale,
            x="anno",
            y="count",
            markers=True,
            labels={"anno": "Anno di Riferimento", "count": "Numero Previsto"}
        )
        fig4.update_traces(line_color="#FF4B4B", marker=dict(size=8))
        fig4.update_layout(margin=dict(t=20, b=20, l=10, r=10))
        st.plotly_chart(fig4, use_container_width=True)


# ===========================================================
# VISTA REGIONALE (2 grafici affiancati)
# ===========================================================
elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        if "provincia" in df.columns:
            st.subheader(f"Pensionamenti per Provincia - {regione}")
            fig_geo = px.bar(
                df.groupby("provincia", as_index=False)
                .agg({"probabilita_media": "mean"})
                .sort_values("probabilita_media", ascending=False),
                x="provincia",
                y="probabilita_media",
                color="probabilita_media",
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={"provincia": "Provincia", "probabilita_media": "Probabilità Media"}
            )
            st.plotly_chart(rifinisci_barre(fig_geo), use_container_width=True)
        elif "anno" in df.columns:
            st.subheader(f"Andamento per Anno - {regione}")
            col_y = "numero_pensionamenti" if "numero_pensionamenti" in df.columns else "probabilita_media"
            fig_anno = px.line(
                df.groupby("anno", as_index=False).agg({col_y: "mean"}),
                x="anno",
                y=col_y,
                markers=True
            )
            st.plotly_chart(fig_anno, use_container_width=True)
        else:
            st.info(f"Colonne disponibili nel dataset regionale: {', '.join(df.columns)}")

    with col2:
        st.subheader("Qualifiche più esposte")
        fig_qual = px.bar(
            df.groupby("qualifica", as_index=False)
            .agg({"probabilita_media": "mean"})
            .sort_values("probabilita_media", ascending=False),
            x="qualifica",
            y="probabilita_media",
            color="probabilita_media",
            color_continuous_scale=px.colors.sequential.Teal[2:],
            labels={"qualifica": "Qualifica", "probabilita_media": "Probabilità Media"}
        )
        st.plotly_chart(rifinisci_barre(fig_qual), use_container_width=True)


# ===========================================================
# VISTA PROVINCIALE (KPI + 2 grafici affiancati)
# ===========================================================
elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric("Pensionamenti Previsti", int(df["numero_pensionamenti"].sum()))
    with kpi2:
        st.metric("Probabilità Media", f"{df['probabilita_media'].mean():.2f}%")

    st.divider()
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Probabilità Media per Qualifica")
        fig1 = px.bar(
            df.groupby("qualifica", as_index=False)
            .agg({"probabilita_media": "mean"})
            .sort_values("probabilita_media", ascending=False),
            x="qualifica",
            y="probabilita_media",
            color="probabilita_media",
            color_continuous_scale=px.colors.sequential.Purples[2:],
            labels={"qualifica": "Qualifica", "probabilita_media": "Probabilità Media"}
        )
        st.plotly_chart(rifinisci_barre(fig1), use_container_width=True)

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
            labels={"qualifica": "Qualifica", "numero_pensionamenti": "Pensionamenti Previsti"}
        )
        st.plotly_chart(rifinisci_barre(fig2), use_container_width=True)

st.divider()
tasto_torna_home()