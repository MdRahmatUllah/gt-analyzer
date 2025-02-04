from .aggrid_view import render_aggrid_table
from .dash_view import render_dash_table
from .plotly_view import render_plotly_table
from .ipywidgets_view import render_ipywidgets_table

def render_table_views(df):
    """
    Render all table visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Table Visualization Type",
        ["AgGrid", "Dash", "Plotly", "IPyWidgets"],
        help="Choose different libraries for interactive data tables"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "AgGrid":
        render_aggrid_table(df)
    elif viz_type == "Dash":
        render_dash_table(df)
    elif viz_type == "Plotly":
        render_plotly_table(df)
    else:  # IPyWidgets
        render_ipywidgets_table(df)
