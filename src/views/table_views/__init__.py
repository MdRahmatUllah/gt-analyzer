from .ipywidgets_view import render_ipywidgets_table

def render_table_views(df):
    """
    Render all table visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Table Visualization Type",
        ["IPyWidgets"],
        help="Choose different libraries for interactive data tables"
    )
    
    st.write("---")
    
    # Render selected visualization
    # IPyWidgets
    render_ipywidgets_table(df)
