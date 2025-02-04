from .folium_view import render_folium_map
from .plotly_map_view import render_plotly_map
from .pydeck_view import render_pydeck_map
from .leaflet_view import render_leaflet_map
from .kepler_view import render_kepler_map

def render_map_views(df):
    """
    Render all map visualizations
    """
    import streamlit as st
    
    # Create tabs for different visualizations
    viz_type = st.radio(
        "Select Map Visualization Type",
        ["Folium", "Plotly", "PyDeck", "Leaflet", "Kepler.gl"],
        help="Choose different visualization libraries to view the geographic distribution"
    )
    
    st.write("---")
    
    # Render selected visualization
    if viz_type == "Folium":
        render_folium_map(df)
    elif viz_type == "Plotly":
        render_plotly_map(df)
    elif viz_type == "PyDeck":
        render_pydeck_map(df)
    elif viz_type == "Leaflet":
        render_leaflet_map(df)
    else:  # Kepler.gl
        render_kepler_map(df)
