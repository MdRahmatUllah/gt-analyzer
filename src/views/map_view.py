import streamlit as st
import pydeck as pdk

def render_map_view(filtered_df, get_coordinates):
    # Prepare data for map
    map_data = filtered_df.copy()
    map_data['coordinates'] = map_data['Country Code'].apply(get_coordinates)
    map_data['lat'] = map_data['coordinates'].apply(lambda x: x[0] if x else None)
    map_data['lon'] = map_data['coordinates'].apply(lambda x: x[1] if x else None)
    map_data = map_data.dropna(subset=['lat', 'lon'])
    
    if not map_data.empty:
        # Create map layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            map_data,
            get_position=["lon", "lat"],
            get_color=["255 if Natural Person == 'yes' else 0", "255 if Natural Person == 'yes' else 0", "255 if Natural Person != 'yes' else 0"],
            get_radius=100000,
            pickable=True
        )
        
        # Set the initial view state
        view_state = pdk.ViewState(
            latitude=map_data['lat'].mean(),
            longitude=map_data['lon'].mean(),
            zoom=3
        )
        
        # Create and display the deck
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    else:
        st.warning("No valid coordinates available for the selected entities.")