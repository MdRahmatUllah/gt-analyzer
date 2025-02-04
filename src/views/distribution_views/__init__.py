from .seaborn_view import render_seaborn_distribution
from .plotly_view import render_plotly_distribution
from .altair_view import render_altair_distribution
from .bokeh_view import render_bokeh_distribution
from .matplotlib_view import render_matplotlib_distribution

def render_distribution_views(df):
    """
    Render all distribution visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Distribution Visualization Type",
        ["Seaborn", "Plotly", "Altair", "Bokeh", "Matplotlib"],
        help="Choose different visualization libraries to view entity type distribution"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "Seaborn":
        render_seaborn_distribution(df)
    elif viz_type == "Plotly":
        render_plotly_distribution(df)
    elif viz_type == "Altair":
        render_altair_distribution(df)
    elif viz_type == "Bokeh":
        render_bokeh_distribution(df)
    else:  # Matplotlib
        render_matplotlib_distribution(df)
