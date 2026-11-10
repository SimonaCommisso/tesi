import pandas as pd
import streamlit as st

from databricks import sql


def get_connection():
    return sql.connect(
        server_hostname=st.secrets["databricks"]["host"],
        http_path=st.secrets["databricks"]["sql_warehouse_path"],
        access_token=st.secrets["databricks"]["token"]
    )


# ============================================================
# Caricamento dei dati dai modelli di Machine Learning
# ============================================================

# Caricamento dei dati dal modello di Forecast Pensionamenti
def load_pensionamenti():
    conn = get_connection()
    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.result_ml1_forecast_pensionamenti
    """
    return pd.read_sql(query, conn)

# Caricamento dei dati dal modello per l'analisi dell'impatto dell'Intelligenza Artificiale sulle competenze
def load_ai_impact():
    conn = get_connection()
    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.result_ml2_ai_impact_analysis
    """
    return pd.read_sql(query, conn)

# Caricamento dei dati dal modello per l'analisi delle competenze future
def load_future_skills():
    conn = get_connection()
    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.result_ml2_future_skills_forecast
    """
    return pd.read_sql(query, conn)

# Caricamento dei dati dal modello per l'analisi delle competenze critiche
def load_skill_critiche():
    conn = get_connection()
    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_critiche
    """
    return pd.read_sql(query, conn)

# Caricamento dei dati dal modello per l'analisi della perdita di competenze
def load_skill_loss():
    conn = get_connection()
    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_loss_forecast
    """
    return pd.read_sql(query, conn)

# Caricamento dei dati dal modello per l'analisi del rischio di burnout
def load_burnout():
    conn = get_connection()
    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.result_ml3_predictions_burnout
    """
    return pd.read_sql(query, conn)

# Lettura dell'ultimo aggiornamento dei modelli di Machine Learning
def load_last_refresh():
    conn = get_connection()
    query = """
    SELECT timestamp_refresh
    FROM tesi.pubblica_amministrazione_tesi.ml_refresh_log
    """
    return pd.read_sql(query, conn)
