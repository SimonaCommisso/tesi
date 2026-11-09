import streamlit as st
import plotly.express as px

from database import load_ai_impact, load_future_skills, load_skill_critiche, load_skill_loss

st.title("🧠 Strategic Workforce Planning")

st.subheader("📊 Dashboard Impatto AI")
df_ai_impact = load_ai_impact()
st.dataframe(df_ai_impact)
st.write(df_ai_impact.columns.tolist())
st.divider

st.subheader("📊 Dashboard Competenze Future")
df_future_skills = load_future_skills()
st.dataframe(df_future_skills)
st.write(df_future_skills.columns.tolist())
st.divider()

st.subheader("📊 Dashboard Competenze Critiche")
df_skill_critiche = load_skill_critiche()
st.dataframe(df_skill_critiche)
st.write(df_skill_critiche.columns.tolist())
st.divider()

st.subheader("📊 Dashboard Perdita di Competenze")
df_skill_loss = load_skill_loss()
st.dataframe(df_skill_loss)
st.write(df_skill_loss.columns.tolist())
st.divider()


# fig = px.bar(
#     df_ai_impact.head(10),
#     x="nome",
#     y="indice_criticita_sostituzione",
#     title="Competenze più critiche"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

st.divider()
    
st.page_link(
"streamlit_app.py",
label="Torna alla Home",
icon="🏠")
