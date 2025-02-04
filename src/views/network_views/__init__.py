from .networkx_view import render_networkx_network
from .igraph_network_view import render_igraph_network

def render_network_views(df):
    """Render all available network views"""
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Network Visualization Type",
        ["NetworkX", "iGraph"],
        help="Choose different visualization libraries to view the entity network"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "NetworkX":
        render_networkx_network(df)
    else:  # iGraph
        render_igraph_network(df)
