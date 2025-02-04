import streamlit as st

def render_sidebar_header():
    """Render the sidebar header with welcome message."""
    st.sidebar.title('📊 Dashboard Controls')
    st.sidebar.markdown("""
        Welcome! Use these controls to:
        - Upload your corporate structure data
        - Filter and customize the visualization
        - Export your filtered results
    """)

def render_file_upload():
    """Handle file upload in the sidebar."""
    return st.sidebar.file_uploader("Upload Excel/CSV file", type=["xlsx", "csv"])
