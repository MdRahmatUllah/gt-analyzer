import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import pandas as pd
from utils.geocoding import get_location_data

def render_folium_map(df):
    """Render geographic distribution using Folium"""
    st.write("### Folium Map Visualization")
    st.write("🗺️ Interactive map with clustered markers")
    
    # Get location data
    location_df = get_location_data(df)
    
    if location_df.empty:
        st.warning("No valid location data found.")
        return
    
    # Create map centered on mean coordinates
    center_lat = location_df['lat'].mean()
    center_lon = location_df['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=3)
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers
    for _, row in location_df.iterrows():
        # Create popup content
        popup_content = f"""
        <div style='width: 200px'>
            <b>{row['name']}</b><br>
            City: {row['city']}<br>
            Country: {row['country']}<br>
            Type: {'Natural Person' if row['is_person'] else 'Corporate Entity'}
        </div>
        """
        
        # Add marker with custom icon
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(
                color='red' if row['is_person'] else 'blue',
                icon='info-sign'
            )
        ).add_to(marker_cluster)
    
    # Add fullscreen control
    folium.plugins.Fullscreen().add_to(m)
    
    # Display the map
    folium_static(m, width=800, height=600)
