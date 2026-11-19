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
    try: 
        query = """
        SELECT * FROM tesi.pubblica_amministrazione_tesi.app_users """
        return pd.read_sql(query, conn)
    finally:
        conn.close()

# Caricamento dell'ente
def load_ente_user(ente):
    conn = get_connection()
    try:
        query = """SELECT nome AS ente_nome FROM tesi.pubblica_amministrazione_tesi.dim_ente
                    WHERE ente_id = ? """
        return pd.read_sql(query, conn, params=(ente,))
    finally:
        conn.close()

# ============================================================
# FILTRO RUOLO
# ============================================================

def apply_role_filter(df):

    ruolo = st.session_state.get("ruolo")

    # ADMIN: accesso completo
    if ruolo == "Admin":
        return df

    ente_id = st.session_state.get("ente_id")

    if ente_id is None:
        return df.iloc[0:0]

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

        if "regione" not in df.columns or pd.isna(regione):
            return df.iloc[0:0]

        return df[df["regione"] == regione]

    # VISUALIZZATORE PROVINCIALE
    elif ruolo == "Visualizzatore Provinciale":

        if ("regione" not in df.columns
            or "provincia" not in df.columns
            or pd.isna(regione)
            or pd.isna(provincia)):
            return df.iloc[0:0]

        return df[
            (df["regione"] == regione) &
            (df["provincia"] == provincia)
        ]

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
# Caricamento dei dati livello Nazionale
def load_pensionamenti_nazionali():
    conn = get_connection()
    try: 
        query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml1_forecast_pensionamenti_nazionale"""
        return pd.read_sql(query, conn)
    finally:
        conn.close()

# Caricamento dei dati livello Regione e Provincia
def load_pensionamenti(regione=None, provincia=None, ente=None):
    conn = get_connection()
    try:
        query = "SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml1_forecast_pensionamenti WHERE 1=1"
        params = []

        if pd.notna(regione) and str(regione).strip() != "":
            query += " AND regione = ?"
            params.append(str(regione).strip())

        if pd.notna(provincia) and str(provincia).strip() != "":
            query += " AND provincia = ?"
            params.append(str(provincia).strip())

        if pd.notna(ente) and str(ente).strip() != "":
            query += " AND ente = ?"
            params.append(str(ente).strip())

        with conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()
        
# Caricamento dei dati annuali
def load_pensionamenti_annuali(): 
    conn = get_connection()
    try:
        query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml1_forecast_pensionamenti_anno"""
        return pd.read_sql(query, conn)
    finally:
            conn.close()


# ============================================================
# PAGE: 02_Forecast_Pensionamenti
# ============================================================
# Caricamento dei dati dal modello per l'analisi dell'impatto dell'Intelligenza Artificiale sulle competenze
def load_ai_impact():
    conn = get_connection()
    try:
        query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_ai_impact_analysis"""
        return pd.read_sql(query, conn)
    finally:
            conn.close()
  
# Caricamento dei dati dal modello per l'analisi delle competenze future
def load_future_skills():
    conn = get_connection()
    try:
        query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_future_skills_forecast"""
        return pd.read_sql(query, conn)
    finally:
            conn.close()

# Caricamento dei dati dal modello per l'analisi delle competenze critiche
def load_skill_critiche():
    conn = get_connection()
    try:
        query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_critiche"""
        return pd.read_sql(query, conn)
    finally:
            conn.close()

# Caricamento dei dati dal modello per l'analisi della perdita di competenze
def load_skill_loss():
    conn = get_connection()
    try:
        query = """SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_loss_forecast"""
        return pd.read_sql(query, conn)
    finally:
            conn.close()

# Caricamento dei dati dal modello per l'analisi della perdita di competenze
def load_skill_loss_ente(regione=None, provincia=None, ente_id=None):
    conn = get_connection()
    try: 
        query = "SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml2_skill_loss_ente WHERE 1=1"
        params = []

        if pd.notna(regione) and str(regione).strip() != "":
            query += " AND regione =?"
            params.append(regione)

        if pd.notna(provincia) and str(provincia).strip() != "":
            query += " AND provincia =?"
            params.append(provincia)

        if pd.notna(ente_id) and str(ente_id).strip() != "":
            query += " AND ente_id =?"
            params.append(ente_id)

        if params:
            return pd.read_sql(query, conn, params=tuple(params))
        return pd.read_sql(query, conn)
    finally:
            conn.close()
            

# ============================================================
# PAGE: 04_Burnout_Forecast
# ============================================================
# Caricamento dei dati dal modello per l'analisi del rischio di burnout
def load_burnout(regione=None, provincia=None, ente_id=None):
    conn = get_connection()
    try:
        query = "SELECT * FROM tesi.pubblica_amministrazione_tesi.result_ml3_predictions_burnout WHERE 1=1"
        params = []

        if pd.notna(regione) and str(regione).strip() != "":
            query += " AND regione =?"
            params.append(regione)

        if pd.notna(provincia) and str(provincia).strip() != "":
            query += " AND provincia =?"
            params.append(provincia)

        if pd.notna(ente_id) and str(ente_id).strip() != "":
            query += " AND ente_id =?"
            params.append(ente_id)

        if params:
            return pd.read_sql(query, conn, params=tuple(params))
        return pd.read_sql(query, conn)
    finally:
        conn.close()

        
def load_ente_name(ente_id):
    conn = get_connection()
    try:
        query = "SELECT nome FROM tesi.pubblica_amministrazione_tesi.dim_ente WHERE ente_id=?"
        return pd.read_sql(query, conn, params=[ente_id])
    finally:
        conn.close()
