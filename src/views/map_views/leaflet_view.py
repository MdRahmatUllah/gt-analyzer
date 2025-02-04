import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, HeatMap, MiniMap
from utils.geocoding import get_location_data

def render_leaflet_map(df):
    """Render geographic distribution using Leaflet"""
    st.write("### Leaflet Map Visualization")
    st.write("🗺️ Interactive map with multiple visualization layers")
    
    # Get location data
    location_df = get_location_data(df)
    
    if location_df.empty:
        st.warning("No valid location data found.")
        return
    
    # Create base map
    center_lat = location_df['lat'].mean()
    center_lon = location_df['lon'].mean()
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=3,
        tiles="OpenStreetMap"
    )
    
    # Add tile layer control with proper attributions
    folium.TileLayer(
        'cartodbpositron',
        name='Light Map',
        attr='© CartoDB'
    ).add_to(m)
    
    folium.TileLayer(
        'cartodbdark_matter',
        name='Dark Map',
        attr='© CartoDB'
    ).add_to(m)
    
    folium.TileLayer(
        'Stamen Terrain',
        name='Terrain Map',
        attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL'
    ).add_to(m)
    
    # Create separate marker clusters for persons and entities
    person_cluster = MarkerCluster(name='Natural Persons').add_to(m)
    entity_cluster = MarkerCluster(name='Corporate Entities').add_to(m)
    
    # Add markers to appropriate clusters
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
        
        # Create marker
        marker = folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(
                color='red' if row['is_person'] else 'blue',
                icon='info-sign'
            )
        )
        
        # Add to appropriate cluster
        if row['is_person']:
            marker.add_to(person_cluster)
        else:
            marker.add_to(entity_cluster)
    
    # Add heatmap layer
    heat_data = [[row['lat'], row['lon']] for _, row in location_df.iterrows()]
    HeatMap(heat_data, name='Heat Map').add_to(m)
    
    # Add minimap
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add fullscreen control
    folium.plugins.Fullscreen().add_to(m)
    
    # Add search control
    m.add_child(folium.plugins.Search(
        layer=person_cluster,
        search_label='name',
        position='topright'
    ))
    
    # Display map options
    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Map Features")
        st.write("- 🔍 Clustered markers")
        st.write("- 🌡️ Heat map layer")
        st.write("- 🔎 Search functionality")
    with col2:
        st.write("##### Layer Types")
        st.write("- 🔴 Natural Persons")
        st.write("- 🔵 Corporate Entities")
        st.write("- 🗺️ Multiple base maps")
    
    # Display the map
    folium_static(m, width=800, height=600)
