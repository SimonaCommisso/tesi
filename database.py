import pandas as pd
import streamlit as st
from databricks import sql

# Caricamento della connessione al database Databricks
def get_connection():
    return sql.connect(
        server_hostname=st.secrets["databricks"]["host"],
        http_path=st.secrets["databricks"]["sql_warehouse_path"],
        access_token=st.secrets["databricks"]["token"]
    )
    
# Caricamento dei dati degli utenti
def load_users():
    conn = get_connection()
    query = """
    SELECT * FROM tesi.pubblica_amministrazione_tesi.app_users """
    return pd.read_sql(query, conn)



# ============================================================
# FILTRO RUOLO
# ============================================================
def apply_role_filter(df):

    ruolo = st.session_state.get("ruolo", "Admin")

    # ADMIN: accesso completo
    if ruolo == "Admin":
        return df

    ente_id = st.session_state.get("ente_id")

    # Recupero informazioni dell'ente dalla tabella dimensionale
    conn = get_connection()

    query = """
        SELECT ente_nome, regione, provincia
        FROM tesi.pubblica_amministrazione_tesi.dim_ente
        WHERE ente_id = ?
    """

    ente = pd.read_sql(query, conn, params=[ente_id])

    if ente.empty:
        return df.iloc[0:0]

    ente_nome = ente.iloc[0]["ente_nome"]
    regione = ente.iloc[0]["regione"]
    provincia = ente.iloc[0]["provincia"]

    # VISUALIZZATORE REGIONALE
    if ruolo == "Visualizzatore Regionale":

        if "regione" in df.columns:
            return df[df["regione"] == regione]

        return df.iloc[0:0]

    # VISUALIZZATORE PROVINCIALE
    elif ruolo == "Visualizzatore Provinciale":

        if "provincia" in df.columns:
            return df[
                (df["regione"] == regione) &
                (df["provincia"] == provincia)
            ]

        return df.iloc[0:0]

    # ALTRI RUOLI: filtro per ente
    if "ente_id" in df.columns:
        return df[df["ente_id"] == ente_id]

    if "ente" in df.columns:
        return df[df["ente"] == ente_nome]

    return df.iloc[0:0]


# ============================================================
# PAGE: 01_Home
# ============================================================
# Lettura dell'ultimo aggiornamento dei modelli di Machine Learning
def load_last_refresh():
    conn = get_connection()
    query = """SELECT timestamp_refresh FROM tesi.pubblica_amministrazione_tesi.ml_refresh_log"""
    df = pd.read_sql(query, conn)
    conn.close()
    if len(df) == 0:
        return None
    return df.iloc[0]["timestamp_refresh"]

def load_enti_visibili():
    conn = get_connection()
    query = """SELECT DISTINCT ente_id, ente FROM tesi.pubblica_amministrazione_tesi.dim_ente"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)

# ============================================================
# PAGE: 02_Forecast_Pensionamenti
# ============================================================
# Caricamento dei dati dal modello di Forecast Pensionamenti
def load_pensionamenti():
    conn = get_connection()
    query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml1_forecast_pensionamenti"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)

# ============================================================
# PAGE: 02_Forecast_Pensionamenti
# ============================================================
# Caricamento dei dati dal modello per l'analisi dell'impatto dell'Intelligenza Artificiale sulle competenze
def load_ai_impact():
    conn = get_connection()
    query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_ai_impact_analysis"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)

# Caricamento dei dati dal modello per l'analisi delle competenze future
def load_future_skills():
    conn = get_connection()
    query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_future_skills_forecast"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)

# Caricamento dei dati dal modello per l'analisi delle competenze critiche
def load_skill_critiche():
    conn = get_connection()
    query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_critiche"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)

# Caricamento dei dati dal modello per l'analisi della perdita di competenze
def load_skill_loss():
    conn = get_connection()
    query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_loss_forecast"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)

# ============================================================
# PAGE: 04_Burnout_Forecast
# ============================================================
# Caricamento dei dati dal modello per l'analisi del rischio di burnout
def load_burnout():
    conn = get_connection()
    query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml3_predictions_burnout"""
    df = pd.read_sql(query, conn)
    conn.close()
    return apply_role_filter(df)