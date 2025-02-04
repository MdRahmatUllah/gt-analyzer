from .matplotlib_view import render_matplotlib_distribution

def render_distribution_views(df):
    """
    Render all distribution visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Distribution Visualization Type",
        ["Matplotlib"],
        help="Choose different visualization libraries to view entity type distribution"
    )
    
    st.write("---")
    
    # Render selected visualization
    render_matplotlib_distribution(df)
