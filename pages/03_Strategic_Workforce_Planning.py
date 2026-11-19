import ast
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
    load_skill_loss_ente,
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
ente_id = st.session_state.get("ente_id")

topbar()
load_css_tasto_home()

st.title("🧠 Strategic Workforce Planning")


def rifinisci_grafico(fig, is_bar=True):
    """Migliora leggibilità, margini e bordi delle barre."""
    if is_bar:
        fig.update_traces(
            marker_line_color="rgba(0,0,0,0.2)",
            marker_line_width=1,
            textposition="outside",
        )
    fig.update_layout(
        margin=dict(t=35, b=20, l=10, r=15),
        title_font_size=16,
        xaxis_title=None,
        yaxis_title=None,
    )
    return fig


def mostra_nessun_dato(dettaglio=""):
    """Mostra una schermata pulita quando non ci sono record per l'utente."""
    st.info(
        f"📭 **Non sono presenti dati per questa casistica.** {dettaglio}\n\n"
        "Non risultano competenze a rischio o uscite previste associate al tuo profilo.",
        icon="ℹ️",
    )


def normalizza_competenze(serie):
    """Converte eventuali stringhe array tipo '[\"A\", \"B\"]' in liste Python."""
    def _parse(val):
        if isinstance(val, (list, tuple, set)):
            return list(val)
        if isinstance(val, str):
            s = val.strip()
            if s.startswith("[") and s.endswith("]"):
                try:
                    parsed = ast.literal_eval(s)
                    return parsed if isinstance(parsed, list) else [s]
                except Exception:
                    return [s]
            return [s] if s else []
        return []

    return serie.apply(_parse)


def filtra_per_ruolo_territoriale(df_in, ruolo_utente, reg_utente, prov_utente, ente_utente):
    """Applica il filtro coerente con il ruolo (Regionale o Provinciale)."""
    if df_in is None or df_in.empty:
        return pd.DataFrame()

    out = df_in.copy()

    if reg_utente and "regione" in out.columns:
        out = out[out["regione"].astype(str).str.strip().str.lower() == str(reg_utente).strip().lower()]

    if ruolo_utente == Ruolo.VISUALIZZATORE_PROVINCIALE:
        if prov_utente and "provincia" in out.columns:
            out = out[
                out["provincia"].astype(str).str.strip().str.lower()
                == str(prov_utente).strip().lower()
            ]

    if ente_utente is not None and "ente_id" in out.columns:
        out = out[out["ente_id"].astype(str) == str(ente_utente)]

    return out


def render_vista_territoriale(df_terr, titolo_area, gruppo_col):
    """Renderizza KPI e 2 grafici chiari per vista Regionale o Provinciale."""
    k1, k2 = st.columns(2)
    k1.metric("Competenze a Rischio", int(pd.to_numeric(df_terr["competenze_a_rischio"], errors="coerce").fillna(0).sum()))
    k2.metric("Dipendenti in Uscita", int(pd.to_numeric(df_terr["dipendenti_in_uscita"], errors="coerce").fillna(0).sum()))

    st.divider()
    col1, col2 = st.columns(2, gap="large")

    # Grafico sinistra: Top competenze più ricorrenti tra quelle a rischio
    with col1:
        st.subheader(f"Competenze più a Rischio — {titolo_area}")
        if "competenze" in df_terr.columns:
            serie_comp = normalizza_competenze(df_terr["competenze"])
            df_exp = (
                df_terr.assign(_comp=serie_comp)
                .explode("_comp")
                .dropna(subset=["_comp"])
            )
            df_exp["_comp"] = df_exp["_comp"].astype(str).str.strip()
            df_exp = df_exp[df_exp["_comp"] != ""]

            if not df_exp.empty:
                df_comp_counts = (
                    df_exp.groupby("_comp", as_index=False)
                    .size()
                    .rename(columns={"_comp": "competenza", "size": "occorrenze"})
                    .sort_values("occorrenze", ascending=False)
                    .head(10)
                    .sort_values("occorrenze", ascending=True)
                )
                fig_left = px.bar(
                    df_comp_counts,
                    x="occorrenze",
                    y="competenza",
                    orientation="h",
                    color="occorrenze",
                    color_continuous_scale=px.colors.sequential.Teal[2:],
                    text_auto=True,
                    labels={"occorrenze": "Occorrenze", "competenza": "Competenza"},
                )
                st.plotly_chart(rifinisci_grafico(fig_left), width="stretch")
            else:
                st.info("Nessun dettaglio sulle singole competenze a rischio per il profilo selezionato.")
        else:
            st.info("Colonna 'competenze' non disponibile.")

    # Grafico destra: Confronto Competenze a Rischio vs Dipendenti in Uscita
    with col2:
        st.subheader(f"Uscite vs Competenze a Rischio — {titolo_area}")
        asse_x = gruppo_col if gruppo_col in df_terr.columns else ("ente" if "ente" in df_terr.columns else None)

        if asse_x:
            df_agg_area = (
                df_terr.groupby(asse_x, as_index=False)
                .agg(
                    competenze_a_rischio=("competenze_a_rischio", "sum"),
                    dipendenti_in_uscita=("dipendenti_in_uscita", "sum"),
                )
                .sort_values("dipendenti_in_uscita", ascending=False)
                .head(10)
            )
            df_melt = df_agg_area.melt(
                id_vars=[asse_x],
                value_vars=["competenze_a_rischio", "dipendenti_in_uscita"],
                var_name="Indicatore",
                value_name="Valore",
            )
            df_melt["Indicatore"] = df_melt["Indicatore"].replace({
                "competenze_a_rischio": "Competenze a Rischio",
                "dipendenti_in_uscita": "Dipendenti in Uscita",
            })
            fig_right = px.bar(
                df_melt,
                x=asse_x,
                y="Valore",
                color="Indicatore",
                barmode="group",
                text_auto=True,
                color_discrete_sequence=["#2b5c8f", "#e06d53"],
                labels={asse_x: asse_x.capitalize(), "Valore": "Conteggio"},
            )
            st.plotly_chart(rifinisci_grafico(fig_right), width="stretch")
        else:
            st.info("Dimensione territoriale non disponibile per il confronto.")


# ============================================================
# VISTA ADMIN (Griglia 2x2)
# ============================================================
if ruolo == Ruolo.ADMIN:
    df_ai_impact = load_ai_impact()
    df_future_skills = load_future_skills()
    df_skill_critiche = load_skill_critiche()
    df_skill_loss = load_skill_loss()

    col1, col2 = st.columns(2, gap="large")

    # 1. Top competenze esposte all'AI (al posto della categoria unica 'operativa')
    with col1:
        st.subheader("Top 12 Competenze più Esposte all'AI")
        if df_ai_impact is not None and not df_ai_impact.empty:
            df_ai_top = (
                df_ai_impact.dropna(subset=["competenza", "rischio_ai"])
                .groupby("competenza", as_index=False)
                .agg(
                    rischio_ai=("rischio_ai", "mean"),
                    qualifiche_coinvolte=("qualifica", "nunique") if "qualifica" in df_ai_impact.columns else ("competenza", "count"),
                )
                .sort_values("rischio_ai", ascending=False)
                .head(12)
                .sort_values("rischio_ai", ascending=True)
            )
            fig1 = px.bar(
                df_ai_top,
                x="rischio_ai",
                y="competenza",
                orientation="h",
                color="rischio_ai",
                color_continuous_scale=px.colors.sequential.OrRd[2:],
                text_auto=".2f",
                hover_data=["qualifiche_coinvolte"],
                labels={
                    "rischio_ai": "Rischio AI Medio",
                    "competenza": "Competenza",
                    "qualifiche_coinvolte": "Qualifiche",
                },
            )
            st.plotly_chart(rifinisci_grafico(fig1), width="stretch")
        else:
            st.info("Nessun dato disponibile sull'impatto AI.")

    # 2. Top 15 Competenze Future per domanda prevista
    with col2:
        st.subheader("Top 15 Competenze Future per Domanda Prevista")
        if df_future_skills is not None and not df_future_skills.empty:
            hover_fut = [c for c in ["categoria", "priorita_2030"] if c in df_future_skills.columns]
            col_fut_color = "priorita_2030" if "priorita_2030" in df_future_skills.columns else "domanda_prevista"
            df_fut_top = (
                df_future_skills.dropna(subset=["nome", "domanda_prevista"])
                .sort_values("domanda_prevista", ascending=False)
                .head(15)
                .sort_values("domanda_prevista", ascending=True)
            )
            fig2 = px.bar(
                df_fut_top,
                x="domanda_prevista",
                y="nome",
                orientation="h",
                color=col_fut_color,
                color_continuous_scale=px.colors.sequential.Blues[2:],
                text_auto=".0f",
                hover_data=hover_fut,
                labels={
                    "domanda_prevista": "Domanda Prevista",
                    "nome": "Competenza",
                    "priorita_2030": "Priorità 2030",
                    "categoria": "Categoria",
                },
            )
            st.plotly_chart(rifinisci_grafico(fig2), width="stretch")
        else:
            st.info("Nessun dato disponibile sulle competenze future.")

    st.divider()
    col3, col4 = st.columns(2, gap="large")

    # 3. Top 15 Competenze Critiche
    with col3:
        st.subheader("Top 15 Competenze Critiche")
        if df_skill_critiche is not None and not df_skill_critiche.empty:
            metrica_crit = (
                "indice_criticita"
                if "indice_criticita" in df_skill_critiche.columns
                else "criticita_pa"
            )
            hover_crit = [
                c
                for c in ["crescita_domanda", "rischio_ai", "difficolta_replacement", "criticita_pa"]
                if c in df_skill_critiche.columns and c != metrica_crit
            ]
            df_crit_top = (
                df_skill_critiche.dropna(subset=["nome", metrica_crit])
                .sort_values(metrica_crit, ascending=False)
                .head(15)
                .sort_values(metrica_crit, ascending=True)
            )
            fig3 = px.bar(
                df_crit_top,
                x=metrica_crit,
                y="nome",
                orientation="h",
                color=metrica_crit,
                color_continuous_scale=px.colors.sequential.Reds[2:],
                text_auto=".2f",
                hover_data=hover_crit,
                labels={
                    metrica_crit: "Indice di Criticità" if metrica_crit == "indice_criticita" else "Criticità PA",
                    "nome": "Competenza",
                    "crescita_domanda": "Crescita Domanda",
                    "rischio_ai": "Rischio AI",
                    "difficolta_replacement": "Diff. Replacement",
                    "criticita_pa": "Criticità PA",
                },
            )
            st.plotly_chart(rifinisci_grafico(fig3), width="stretch")
        else:
            st.info("Nessun dato disponibile sulle competenze critiche.")

    # 4. Top 15 Competenze a Rischio Perdita per Pensionamenti
    with col4:
        st.subheader("Top 15 Competenze a Rischio Perdita")
        if df_skill_loss is not None and not df_skill_loss.empty:
            col_loss_color = (
                "indice_criticita_sostituzione"
                if "indice_criticita_sostituzione" in df_skill_loss.columns
                else "criticita_pa"
            )
            hover_loss = [
                c
                for c in ["totale_possessori", "possessori_in_uscita", "criticita_pa"]
                if c in df_skill_loss.columns
            ]
            df_loss_top = (
                df_skill_loss.dropna(subset=["nome", "percentuale_perdita"])
                .sort_values("percentuale_perdita", ascending=False)
                .head(15)
                .sort_values("percentuale_perdita", ascending=True)
            )
            fig4 = px.bar(
                df_loss_top,
                x="percentuale_perdita",
                y="nome",
                orientation="h",
                color=col_loss_color,
                color_continuous_scale=px.colors.sequential.Purples[2:],
                text_auto=".1f",
                hover_data=hover_loss,
                labels={
                    "percentuale_perdita": "% Perdita Prevista",
                    "nome": "Competenza",
                    "indice_criticita_sostituzione": "Criticità Sost.",
                    "totale_possessori": "Possessori",
                    "possessori_in_uscita": "In Uscita",
                    "criticita_pa": "Criticità PA",
                },
            )
            st.plotly_chart(rifinisci_grafico(fig4), width="stretch")
        else:
            st.info("Nessun dato disponibile sul rischio perdita competenze.")


# ============================================================
# VISTA REGIONALE (Ente della propria regione)
# ============================================================
elif ruolo == Ruolo.VISUALIZZATORE_REGIONALE:
    if not regione or ente_id is None:
        mostra_nessun_dato("(Parametri regione o ente mancanti nel profilo)")
    else:
        df_raw_reg = load_skill_loss_ente(regione, provincia, ente_id)
        df_reg = filtra_per_ruolo_territoriale(
            df_raw_reg, ruolo, regione, provincia, ente_id
        )

        if df_reg.empty:
            mostra_nessun_dato(f"(Regione: {regione})")
        else:
            render_vista_territoriale(df_reg, f"Regione {regione}", gruppo_col="provincia")


# ============================================================
# VISTA PROVINCIALE (Proprio ente nella propria provincia)
# ============================================================
elif ruolo == Ruolo.VISUALIZZATORE_PROVINCIALE:
    if not regione or not provincia or ente_id is None:
        mostra_nessun_dato("(Parametri regione, provincia o ente mancanti nel profilo)")
    else:
        df_raw_prov = load_skill_loss_ente(regione, provincia, ente_id)
        df_prov = filtra_per_ruolo_territoriale(
            df_raw_prov, ruolo, regione, provincia, ente_id
        )

        if df_prov.empty:
            mostra_nessun_dato(f"(Regione: {regione} — Provincia: {provincia})")
        else:
            render_vista_territoriale(
                df_prov, f"{provincia} ({regione})", gruppo_col="ente"
            )

else:
    st.error("Ruolo non riconosciuto.")
    st.stop()

st.divider()
tasto_torna_home()