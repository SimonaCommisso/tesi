import streamlit as st

def load_css():

    st.markdown("""
    <style>
    
    .dashboard-card {
        background-color: white;
        padding: 20px;
        height: 605px;
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
    
    
    
def load_css_tasto_home():
    
    st.markdown("""
    <style>
    /* Stilizza il componente st.page_link facendolo sembrare un pulsante */
        .back-to-home-buttom [data-testid="stPageLink" ] {
            background-color: #f0f2f6;
            border: 1px solid #d6d9dc;
            border-radius: 8px;
            padding: 4px 12px;
            width: fit-content;
            transition: all 0.3s ease;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        
        /* Effetto hover al passaggio del mouse */
        .back-to-home-buttom [data-testid="stPageLink"]:hover {
            background-color: #e2e8f0;
            border-color: #b0c4de;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    
        /* Colore e stile del testo/icona all'interno del link */
        .back-to-home-buttom [data-testid="stPageLink"] a {
            color: #31333F !important;
            font-weight: 500;
            text-decoration: none !important;
        }
    </style>
        """, unsafe_allow_html=True)