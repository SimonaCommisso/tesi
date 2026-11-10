import streamlit as st

def topbar():

    st.markdown("""
    <style>

    .top-bar {
        background-color: #1d3673;
        padding: 15px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid #6982ba;
    }

    .title-project {
        color: white;
        font-size: 28px;
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([8, 1])

    with col1:
        st.markdown('<div class="title-project">🏛️ HR Analytics Dashboard</div>',
            unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("streamlit_app.py")
    st.divider()