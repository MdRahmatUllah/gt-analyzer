import streamlit as st

def render_footer():
    """Render the application footer with social links and copyright information."""
    footer_html = """
    <footer>
        <div class="footer-content">
            <div class="social-links">
                <a href="https://github.com/yourusername" target="_blank">
                    <i class="fab fa-github"></i> GitHub
                </a>
                <a href="https://linkedin.com/in/yourusername" target="_blank">
                    <i class="fab fa-linkedin"></i> LinkedIn
                </a>
                <a href="mailto:contact@example.com">
                    <i class="fas fa-envelope"></i> Contact
                </a>
            </div>
            <div class="copyright">
                © 2025 Corporate Structure Visualization Tool. All rights reserved.
            </div>
        </div>
    </footer>
    """
    # Add Font Awesome for social icons
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)
    st.markdown(footer_html, unsafe_allow_html=True)
