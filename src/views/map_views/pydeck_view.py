import streamlit as st
import pydeck as pdk
import pandas as pd
from utils.geocoding import get_location_data

def render_pydeck_map(df):
    """Render geographic distribution using PyDeck"""
    st.write("### PyDeck Map Visualization")
    st.write("🗺️ 3D interactive map with elevated markers")
    
    # Get location data
    location_df = get_location_data(df)
    
    if location_df.empty:
        st.warning("No valid location data found.")
        return
    
    # Add controls in sidebar
    with st.sidebar:
        st.write("### Map Controls")
        pitch = st.slider("Pitch", 0, 89, 45)
        bearing = st.slider("Bearing", 0, 360, 0)
    
    # Define the column layer for entities
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=location_df,
        get_position=["longitude", "latitude"],
        get_elevation="elevation",
        elevation_scale=1,
        radius=20000,
        get_fill_color=["255 * (is_person == True)", "153", "255 * (is_person == False)", 180],
        pickable=True,
        auto_highlight=True,
    )
    
    # Define the text layer for labels
    text_layer = pdk.Layer(
        "TextLayer",
        data=location_df,
        get_position=["longitude", "latitude"],
        get_text="name",
        get_size=16,
        get_color=[0, 0, 0, 255],
        get_angle=0,
        text_anchor="middle",
        pickable=True,
        font_family="Arial",
        get_text_background=True,
        get_text_background_color=[255, 255, 255, 200],
        get_text_border_width=2,
        get_text_border_color=[0, 0, 0, 100],
    )
    
    # Create the view state with user-defined pitch and bearing
    view_state = pdk.ViewState(
        latitude=location_df["latitude"].mean(),
        longitude=location_df["longitude"].mean(),
        zoom=2,
        pitch=pitch,
        bearing=bearing
    )
    
    # Create tooltip
    tooltip = {
        "html": "<b>{name}</b><br/>"
                "City: {city}<br/>"
                "Country: {country}<br/>"
                "Type: {is_person}",
        "style": {
            "backgroundColor": "white",
            "color": "black"
        }
    }
    
    # Create the deck with updated view state
    deck = pdk.Deck(
        layers=[column_layer, text_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="light",
    )
    
    # Display the map
    st.pydeck_chart(deck)
