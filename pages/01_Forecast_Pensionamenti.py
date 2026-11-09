import streamlit as st
import plotly.express as px

from database import load_pensionamenti

st.title("📈 Forecast Pensionamenti")

df = load_pensionamenti()

st.dataframe(df)
st.write(df.columns.tolist())

# esempio se hai una colonna anno

if "anno" in df.columns:

    fig = px.line(

        df,

        x="anno",

        y="dipendenti_previsti",

        markers=True,

        title="Forecast Pensionamenti"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    st.divider()
    
    st.page_link(
    "home.py",
    label="Torna alla Home",
    icon="🏠")


