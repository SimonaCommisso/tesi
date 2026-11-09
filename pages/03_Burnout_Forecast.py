import streamlit as st
import plotly.express as px

from database import load_burnout

st.title("🔥 Burnout Forecast")

df = load_burnout()

st.dataframe(df)

st.write(df.columns.tolist())

if "livello_burnout" in df.columns:

    burnout = (

        df

        .groupby(
            "livello_burnout"
        )

        .size()

        .reset_index(
            name="totale"
        )

    )

    fig = px.pie(

        burnout,

        names="livello_burnout",

        values="totale",

        title="Distribuzione rischio burnout"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )