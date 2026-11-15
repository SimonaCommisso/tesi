import streamlit as st

def load_css():

    st.markdown("""
    <style>
    
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
    
    [data-testid="column"] {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #dce1ea;
        box-shadow: 0px 4px 12px rgba(15,36,84,0.08);
    }

    </style>
    """, unsafe_allow_html=True)