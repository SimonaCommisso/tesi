import streamlit as st
import plotly.express as px
import pandas as pd
from components import topbar, tasto_torna_home
from style import load_css_tasto_home
from utility.costanti import Ruolo
from database import (
    load_ai_impact,
    load_future_skills,
    load_skill_critiche,
    load_skill_loss,
    load_skill_loss_ente_reg,
    load_skill_loss_ente_prov
)

# ============================================================
# CONFIGURAZIONE PAGINA (sempre come prima istruzione Streamlit)
# ============================================================
st.set_page_config(page_title="Forecast Workforce Planning", layout="wide")

# ============================================================
# CONTROLLO LOGIN
# ============================================================
if not st.session_state.get("logged", False):
    st.switch_page("streamlit_app.py")

ruolo = st.session_state.get("ruolo")
regione = st.session_state.get("regione")
provincia = st.session_state.get("provincia")
ente = st.session_state.get("ente_nome")
ente_id = st.session_state.get("ente_id")

topbar()
load_css_tasto_home()

st.title("🧠 Strategic Workforce Planning")


def rifinisci_grafico(fig, is_bar=True):
    """Migliora leggibilità, margini e bordi delle barre."""
    if is_bar:
        fig.update_traces(marker_line_color="rgba(0,0,0,0.2)", marker_line_width=1)
    fig.update_layout(
        margin=dict(t=40, b=20, l=10, r=10),
        title_font_size=16,
        xaxis_title=None
    )
    return fig


# ============================================================
# VISTA ADMIN (Griglia 2x2)
# ============================================================
if ruolo == Ruolo.ADMIN:
    df_ai_impact = load_ai_impact()
    df_future_skills = load_future_skills()
    df_skill_critiche = load_skill_critiche()
    df_skill_loss = load_skill_loss()

    col1, col2 = st.columns(2, gap="large")

    # 1. Impatto AI per categoria (Barre orizzontali con media e scala contrastata)
    with col1:
        st.subheader("Impatto AI per Categoria Skill")
        df_ai_agg = (
            df_ai_impact.groupby("categoria_skill", as_index=False)
            .agg({"rischio_ai": "mean"})
            .sort_values("rischio_ai", ascending=True)
        )
        fig1 = px.bar(
            df_ai_agg,
            x="rischio_ai",
            y="categoria_skill",
            orientation="h",
            color="rischio_ai",
            color_continuous_scale=px.colors.sequential.OrRd[2:],
            text_auto=".1f",
            labels={"rischio_ai": "Rischio AI Medio", "categoria_skill": "Categoria"}
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(rifinisci_grafico(fig1), use_container_width=True)

    # 2. Competenze future con maggiore crescita
    with col2:
        st.subheader("Top 15 Competenze Future")
        df_fut_top = df_future_skills.sort_values("domanda_prevista", ascending=True).tail(15)
        fig2 = px.bar(
            df_fut_top,
            x="domanda_prevista",
            y="nome",
            orientation="h",
            color="domanda_prevista",
            color_continuous_scale=px.colors.sequential.Blues[2:],
            labels={"domanda_prevista": "Domanda Prevista", "nome": "Competenza"}
        )
        st.plotly_chart(rifinisci_grafico(fig2), use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2, gap="large")

    # 3. Competenze critiche
    with col3:
        st.subheader("Top 15 Competenze Critiche")
        df_crit_top = df_skill_critiche.sort_values("indice_criticita", ascending=True).tail(15)
        fig3 = px.bar(
            df_crit_top,
            x="indice_criticita",
            y="nome",
            orientation="h",
            color="strategica",
            color_discrete_map={True: "#d9534f", False: "#5bc0de", "Si": "#d9534f", "No": "#5bc0de"},
            labels={"indice_criticita": "Indice di Criticità", "nome": "Competenza", "strategica": "Strategica"}
        )
        st.plotly_chart(rifinisci_grafico(fig3), use_container_width=True)

    # 4. Perdita di competenze
    with col4:
        st.subheader("Top 15 Competenze a Rischio Perdita per Pensionamenti")
        df_loss_top = df_skill_loss.sort_values("percentuale_perdita", ascending=True).tail(15)
        fig4 = px.bar(
            df_loss_top,
            x="percentuale_perdita",
            y="nome",
            orientation="h",
            color="indice_criticita_sostituzione",
            color_continuous_scale=px.colors.sequential.Purples[2:],
            labels={
                "percentuale_perdita": "% Perdita Prevista",
                "nome": "Competenza",
                "indice_criticita_sostituzione": "Criticità Sost."
            }
        )
        st.plotly_chart(rifinisci_grafico(fig4), use_container_width=True)


# ============================================================
# VISTA REGIONALE (KPI + 2 grafici affiancati)
# ============================================================
elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    df_reg = load_skill_loss_ente_reg(regione, ente_id)
    df_reg = df_reg[df_reg["regione"] == regione]
    if ente_id is not None and "ente_id" in df_reg.columns:
        df_reg = df_reg[df_reg["ente_id"] == ente_id]
    elif ente:
        df_reg = df_reg[df_reg["ente"] == ente]

    if df_reg.empty:
        st.warning("Nessun dato disponibile per la regione e l'ente selezionati.")
    else:
        # KPI
        k1, k2, k3 = st.columns(3)
        k1.metric("Competenze a Rischio", int(df_reg["competenze_a_rischio"].sum()))
        k2.metric("Dipendenti in Uscita", int(df_reg["dipendenti_in_uscita"].sum()))
        k3.metric("Totale Competenze Mappate", int(df_reg["tot_competenze"].sum()))

        st.divider()
        col1, col2 = st.columns(2, gap="large")

        # Grafico 1: Top competenze a rischio (esplodendo la lista/array 'competenze')
        with col1:
            st.subheader(f"Competenze più a Rischio - {regione}")
            df_exp = df_reg.explode("competenze").dropna(subset=["competenze"])
            if not df_exp.empty:
                df_comp_counts = (
                    df_exp["competenze"]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"competenze": "competenza", "count": "frequenza"})
                    .head(12)
                    .sort_values("frequenza", ascending=True)
                )
                fig_r1 = px.bar(
                    df_comp_counts,
                    x="frequenza",
                    y="competenza",
                    orientation="h",
                    color="frequenza",
                    color_continuous_scale=px.colors.sequential.Teal[2:],
                    labels={"frequenza": "Occorrenze a Rischio", "competenza": "Competenza"}
                )
                st.plotly_chart(rifinisci_grafico(fig_r1), use_container_width=True)
            else:
                st.info("Nessun dettaglio competenze disponibile.")

        # Grafico 2: Confronto Competenze a Rischio vs Dipendenti in Uscita
        with col2:
            st.subheader("Impatto Uscite vs Competenze a Rischio")
            df_melt = df_reg.melt(
                id_vars=["ente"],
                value_vars=["competenze_a_rischio", "dipendenti_in_uscita"],
                var_name="Indicatore",
                value_name="Valore"
            )
            df_melt["Indicatore"] = df_melt["Indicatore"].replace({
                "competenze_a_rischio": "Competenze a Rischio",
                "dipendenti_in_uscita": "Dipendenti in Uscita"
            })
            fig_r2 = px.bar(
                df_melt,
                x="ente",
                y="Valore",
                color="Indicatore",
                barmode="group",
                text_auto=True,
                color_discrete_sequence=["#2b5c8f", "#e06d53"]
            )
            st.plotly_chart(rifinisci_grafico(fig_r2), use_container_width=True)


# ============================================================
# VISTA PROVINCIALE (KPI + 2 grafici affiancati)
# ============================================================
elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    df_prov = load_skill_loss_ente_prov(regione, provincia, ente_id)
    df_prov = df_prov[(df_prov["regione"] == regione) & (df_prov["provincia"] == provincia)]
    if ente_id is not None and "ente_id" in df_prov.columns:
        df_prov = df_prov[df_prov["ente_id"] == ente_id]
    elif ente:
        df_prov = df_prov[df_prov["ente"] == ente]

    if df_prov.empty:
        st.warning("Nessun dato disponibile per la provincia selezionata.")
    else:
        # KPI
        k1, k2 = st.columns(2)
        k1.metric("Competenze a Rischio", int(df_prov["competenze_a_rischio"].sum()))
        k2.metric("Dipendenti in Uscita", int(df_prov["dipendenti_in_uscita"].sum()))

        st.divider()
        col1, col2 = st.columns(2, gap="large")

        # Grafico 1: Top competenze a rischio nella provincia
        with col1:
            st.subheader(f"Competenze più a Rischio - {provincia}")
            df_exp = df_prov.explode("competenze").dropna(subset=["competenze"])
            if not df_exp.empty:
                df_comp_counts = (
                    df_exp["competenze"]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"competenze": "competenza", "count": "frequenza"})
                    .head(12)
                    .sort_values("frequenza", ascending=True)
                )
                fig_p1 = px.bar(
                    df_comp_counts,
                    x="frequenza",
                    y="competenza",
                    orientation="h",
                    color="frequenza",
                    color_continuous_scale=px.colors.sequential.Purples[2:],
                    labels={"frequenza": "Occorrenze a Rischio", "competenza": "Competenza"}
                )
                st.plotly_chart(rifinisci_grafico(fig_p1), use_container_width=True)
            else:
                st.info("Nessun dettaglio competenze disponibile.")

        # Grafico 2: Confronto Dipendenti in Uscita vs Competenze a Rischio
        with col2:
            st.subheader("Dipendenti in Uscita vs Competenze a Rischio")
            df_melt = df_prov.melt(
                id_vars=["ente"],
                value_vars=["competenze_a_rischio", "dipendenti_in_uscita"],
                var_name="Indicatore",
                value_name="Valore"
            )
            df_melt["Indicatore"] = df_melt["Indicatore"].replace({
                "competenze_a_rischio": "Competenze a Rischio",
                "dipendenti_in_uscita": "Dipendenti in Uscita"
            })
            fig_p2 = px.bar(
                df_melt,
                x="ente",
                y="Valore",
                color="Indicatore",
                barmode="group",
                text_auto=True,
                color_discrete_sequence=["#5e3c99", "#e66101"]
            )
            st.plotly_chart(rifinisci_grafico(fig_p2), use_container_width=True)

else:
    st.error("Ruolo non riconosciuto.")
    st.stop()

st.divider()
tasto_torna_home()