import streamlit as st
import plotly.express as px
import pandas as pd
from utils.geocoding import get_location_data

def render_plotly_map(df):
    """Render geographic distribution using Plotly Express"""
    st.write("### Plotly Express Map Visualization")
    st.write("🗺️ Interactive map with entity type filtering")
    
    # Get location data
    location_df = get_location_data(df)
    
    if location_df.empty:
        st.warning("No valid location data found.")
        return
    
    # Create color map
    color_map = {'Natural Person': '#ff9999', 'Corporate Entity': '#99ccff'}
    
    # Create the map
    fig = px.scatter_mapbox(
        location_df,
        lat='lat',
        lon='lon',
        hover_name='name',
        hover_data=['city', 'country'],
        color='is_person',
        size='size',
        size_max=15,
        zoom=2,
        color_discrete_map=color_map,
        title='Entity Geographic Distribution',
        mapbox_style='carto-positron'
    )
    
    # Update layout
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        height=600,
        legend_title_text='Entity Type',
        mapbox=dict(
            center=dict(
                lat=location_df['lat'].mean(),
                lon=location_df['lon'].mean()
            )
        )
    )
    
    # Add entity type filter
    entity_types = st.multiselect(
        'Filter by Entity Type',
        options=location_df['is_person'].unique(),
        default=location_df['is_person'].unique()
    )
    
    # Filter data based on selection
    filtered_df = location_df[location_df['is_person'].isin(entity_types)]
    
    if filtered_df.empty:
        st.warning("No entities match the selected filters.")
        return
    
    # Update figure data
    fig.data = []
    for entity_type in entity_types:
        df_type = filtered_df[filtered_df['is_person'] == entity_type]
        fig.add_trace(
            px.scatter_mapbox(
                df_type,
                lat='lat',
                lon='lon',
                hover_name='name',
                hover_data=['city', 'country'],
                color='is_person',
                size='size',
                size_max=15,
                color_discrete_map=color_map
            ).data[0]
        )
    
    # Display the map
    st.plotly_chart(fig, use_container_width=True)
