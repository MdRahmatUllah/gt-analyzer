import streamlit as st

def init_page_layout():
    """Initialize the main page layout and configuration."""
    st.set_page_config(page_title="Corporate Structure Visualization", layout="wide")
    st.markdown('''
        <div class="main-container">
            <div class="content-wrapper">
    ''', unsafe_allow_html=True)

def close_page_layout():
    """Close the main page layout containers."""
    st.markdown('</div>', unsafe_allow_html=True)
