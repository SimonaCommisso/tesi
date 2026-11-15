import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .topbar {
        background-color:#0e1117;
        padding:12px;
        border-radius:10px;
        margin-bottom:20px;
    }
    
    .dashboard-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #d9d9d9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    .dashboard-title {
        color: #0f2454;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)