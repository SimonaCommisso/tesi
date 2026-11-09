import streamlit as st
import plotly.express as px

from database import load_ai_impact, load_future_skills, load_skill_critiche, load_skill_loss

st.set_page_config(
    page_title="Forecast Workforce Planning",
    layout="wide"
)

st.title("🧠 Strategic Workforce Planning")

## Caricamento dei dati dai modelli di Machine Learning
df_ai_impact = load_ai_impact()
df_future_skills = load_future_skills()
df_skill_critiche = load_skill_critiche()
df_skill_loss = load_skill_loss()

# ============================================================
# DASHBOARD IMPATTO AI
# ============================================================
st.subheader("Dashboard Impatto AI")
fig = px.box(
    df_ai_impact,
    x="categoria_skill",
    y="rischio_ai",
    color="categoria_skill",
    title="Impatto AI per categoria skill"
)
st.divider()

# ============================================================
# DASHBOARD COMPETENZE FUTURE
# ============================================================
st.subheader("Dashboard Competenze Future")
fig = px.bar(
    df_future_skills.sort_values(
        "domanda_prevista",
        ascending=False
    ).head(15),
    x="nome",
    y="domanda_prevista",
    color="domanda_prevista",
    title="Competenze future con maggiore crescita"
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

# ============================================================
# DASHBOARD COMPETENZE CRITICHE
# ============================================================
st.subheader("Dashboard Competenze Critiche")
fig = px.bar(
    df_skill_critiche.sort_values(
        "indice_criticita",
        ascending=False
    ).head(15),
    x="nome",
    y="indice_criticita",
    color="strategica",
    title="Indice di criticità delle competenze"
)
st.divider()

# ============================================================
# DASHBOARD PERDITA DI COMPETENZE
# ============================================================
st.subheader("Dashboard Perdita di Competenze")
fig = px.bar(
    df_skill_loss.sort_values(
        "percentuale_perdita",
        ascending=False
    ).head(15),
    x="nome",
    y="percentuale_perdita",
    color="indice_criticita_sostituzione",
    title="Competenze maggiormente a rischio perdita"
)
st.plotly_chart(fig, use_container_width=True)

    
st.page_link(
    "streamlit_app.py",
    label="Torna alla Home",
    icon="🏠"
)
