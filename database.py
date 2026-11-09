import pandas as pd
import streamlit as st

from databricks import sql


def get_connection():

    return sql.connect(

        server_hostname=st.secrets["databricks"]["host"],

        http_path=st.secrets["databricks"]["sql_warehouse_path"],

        access_token=st.secrets["databricks"]["token"]

    )


def load_burnout():

    conn = get_connection()

    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.burnout_forecast
    """

    return pd.read_sql(query, conn)


def load_pensionamenti():

    conn = get_connection()

    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.workforce_forecast_dettaglio
    """

    return pd.read_sql(query, conn)


def load_workforce():

    conn = get_connection()

    query = """
    SELECT *
    FROM tesi.pubblica_amministrazione_tesi.skill_loss_forecast
    """

    return pd.read_sql(query, conn)