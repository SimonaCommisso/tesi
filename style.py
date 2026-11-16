import streamlit as st

# CSS PAGINA LOGIN
def load_css_login_page():
    st.markdown("""
        <style>
    
        .stApp {
            background-color: #004678;
        }
    
        section[data-testid="stSidebar"] {
            display: none;
        }
    
        button[kind="header"] {
            display: none;
        }
    
        .main .block-container {
            padding-top: 6rem;
            max-width: 1400px;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white !important;
            border-radius: 24px !important;
            padding: 30px !important;
            border: none !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.18) !important;
        }
        
        [data-testid="stForm"] {
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
        }
            
        .box-image {
            background: linear-gradient(135deg, #004678, #1d79b8);
            padding:20px;
            border-radius:20px;
        }
    
        .login-title {
            font-size: 44px;
            font-weight: 800;
            color: #002b4f;
            letter-spacing: 0.5px;
            text-align: center;
        }
    
        .login-subtitle {
            font-size: 20px;
            color: #56606b;
            text-align: center;
            line-height: 1.5;
            margin-bottom: 35px;
        }
    
        div[data-baseweb="input"] {
            background: #f4f6f9 !important;
            border: 1px solid #e3e6ea !important;
            border-radius: 12px !important;
        }
    
        div[data-testid="stFormSubmitButton"] button {
            background-color: #004678 !important;
            color: white !important;
            border-radius: 12px !important;
            height: 54px !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            border: 0 !important;
        }
    
        div[data-testid="stFormSubmitButton"] button:hover {
            background-color: #005f9e;
            color: white;
        }
        
        [data-testid="stVerticalBlock"] > div:has(.login-title){
            background-color:white;
            border-radius:24px;
            padding:35px;
        }
    
        </style>""", unsafe_allow_html=True)
    

# CSS GENERICO
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
    

# CSS TASTO TORNA ALLA HOME 
def load_css_tasto_home():
    st.markdown("""
    <style>
        div[data-testid="stPageLink"] > a {
            background-color: #f0f2f6 !important;
            border: 1px solid #d6d9dc !important;
            border-radius: 8px !important;
            padding: 6px 14px !important;
            width: fit-content !important;
            color: #31333F !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            transition: all 0.2s ease;
        }
        div[data-testid="stPageLink"] > a:hover {
            background-color: #e2e8f0 !important;
            border-color: #b0c4de !important;
        }
    </style>
    """, unsafe_allow_html=True)
    