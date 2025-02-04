from .folium_view import render_folium_map
from .leaflet_view import render_leaflet_map

def render_map_views(df):
    """
    Render all map visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Map Visualization Type",
        ["Folium", "Leaflet"],
        help="Choose different visualization libraries to view the geographic distribution"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "Folium":
        render_folium_map(df)
    else:  # Leaflet
        render_leaflet_map(df)
