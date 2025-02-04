import streamlit as st

def load_styles():
    """Load all CSS styles for the application."""
    st.markdown("""
    <style>
        /* Main container styling */
        .main-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .content-wrapper {
            flex: 1 0 auto;
            padding-bottom: 6rem;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #6B46C1;
            padding: 2rem 1rem;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
        }
        [data-testid="stSidebar"] h1 {
            color: white;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 2rem;
        }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
            color: #E9D8FD;
        }
        [data-testid="stSidebar"] .stSelectbox, 
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stCheckbox {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        [data-testid="stSidebar"] .stButton > button {
            background-color: #9F7AEA;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #805AD5;
            transform: translateY(-2px);
        }
        [data-testid="stSidebar"] .stFileUploader {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Footer Styling */
        footer {
            flex-shrink: 0;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100vw;
            background-color: #f8f9fa;
            padding: 1rem 0;
            text-align: center;
            border-top: 1px solid #e9ecef;
            margin: 0;
            box-sizing: border-box;
            z-index: 999;
        }
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
            max-width: 100%;
            margin: 0 auto;
        }
        .social-links {
            display: flex;
            gap: 2rem;
        }
        .social-links a {
            color: #6B46C1;
            text-decoration: none;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .social-links a:hover {
            color: #805AD5;
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }
        .copyright {
            color: #6B7280;
            font-size: 0.9rem;
            padding: 0.5rem 0;
        }
        
        /* Fix any horizontal scroll issues */
        [data-testid="stAppViewContainer"] {
            overflow-x: hidden;
        }
    </style>
    """, unsafe_allow_html=True)
