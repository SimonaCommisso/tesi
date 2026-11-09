import streamlit as st
import plotly.express as px

from database import load_workforce

st.title("🧠 Strategic Workforce Planning")

df = load_workforce()

st.dataframe(df)
st.write(df.columns.tolist())

fig = px.bar(

    df.head(10),

    x="nome",

    y="indice_criticita_sostituzione",

    title="Competenze più critiche"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
    
st.page_link(
"app.py",
label="Torna alla Home",
icon="🏠")
