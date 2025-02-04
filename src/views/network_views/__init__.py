from .bokeh_network_view import render_bokeh_network
from .cytoscape_network_view import render_cytoscape_network
from .d3_network_view import render_d3_network
from .plotly_network_view import render_plotly_network
from .pyvis_network_view import render_pyvis_network
from .networkx_view import render_networkx_network

def render_network_views(df):
    """Render all available network views"""
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Network Visualization Type",
        ["Plotly", "PyVis", "Cytoscape", "D3.js", "Bokeh", "NetworkX"],
        help="Choose different visualization libraries to view the entity network"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "Plotly":
        render_plotly_network(df)
    elif viz_type == "PyVis":
        render_pyvis_network(df)
    elif viz_type == "Cytoscape":
        render_cytoscape_network(df)
    elif viz_type == "D3.js":
        render_d3_network(df)
    elif viz_type == "Bokeh":
        render_bokeh_network(df)
    else:  # NetworkX
        render_networkx_network(df)
