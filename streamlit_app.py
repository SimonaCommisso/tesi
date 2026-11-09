import streamlit as st

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

st.title("HR Analytics nella Pubblica Amministrazione")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pensionamenti Previsti", "1.245")

with col2:
    st.metric("Competenze Critiche", "37")

with col3:
    st.metric("Dipendenti ad Alto Rischio Burnout", "842")

st.markdown("---")