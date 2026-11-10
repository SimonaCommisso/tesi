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

    </style>
    """, unsafe_allow_html=True)