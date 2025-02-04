from .pyvis_view import render_pyvis_hierarchy
from .d3_view import render_d3_hierarchy
from .graphviz_view import render_graphviz_hierarchy
from .pyecharts_view import render_pyecharts_hierarchy

def render_hierarchy_views(df):
    """
    Render all hierarchy visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Visualization Type",
        ["PyVis", "D3.js", "Graphviz", "PyEcharts"],
        help="Choose different visualization libraries to view the hierarchy"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "PyVis":
        render_pyvis_hierarchy(df)
    elif viz_type == "D3.js":
        render_d3_hierarchy(df)
    elif viz_type == "Graphviz":
        render_graphviz_hierarchy(df)
    else:  # PyEcharts
        render_pyecharts_hierarchy(df)
