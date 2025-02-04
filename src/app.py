import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd

# Import modular components
from views.map_view import render_map_view
from views.statistics_view import render_statistics_view
from views.hierarchy_views import render_hierarchy_views
from views.map_views import render_map_views
from views.network_views import render_network_views
from views.distribution_views import render_distribution_views
from views.table_views import render_table_views
from components.filters import render_filters, apply_filters
from logic.data_processor import load_data, build_graph

# Set page config
st.set_page_config(page_title="Corporate Structure Visualization", layout="wide")

# Cache the geocoding function
@st.cache_data
def get_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="corporate_structure_app")
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        return None
    except GeocoderTimedOut:
        return None

# Main app
st.title('Corporate Structure Visualization Tool')

# Sidebar
st.sidebar.title('Controls')

# File upload
uploaded_file = st.sidebar.file_uploader("Upload Excel/CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Load and display data
    df = load_data(uploaded_file)
    
    if df is not None:
        # Display raw data in expander
        with st.expander("View Raw Data"):
            st.dataframe(df)
        
        # Get and apply filters
        selected_countries, min_share, show_persons = render_filters(df)
        filtered_df = apply_filters(df, selected_countries, min_share, show_persons)
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Network Graph", "Hierarchy View", "Geographic View", "Map View", "Statistics", "Distribution", "Table View"])

        
        with tab1:
            render_network_views(filtered_df)
            
        with tab2:
            render_hierarchy_views(filtered_df)
        
        with tab3:
            render_map_views(filtered_df)
            
        with tab4:
            render_map_view(filtered_df, get_coordinates)
        
        with tab5:
            render_statistics_view(filtered_df)
        
        with tab6:
            render_distribution_views(filtered_df)
        
        with tab7:
            render_table_views(filtered_df)
        
        # Export options
        st.sidebar.download_button(
            "Download Filtered Data",
            filtered_df.to_csv(index=False),
            "filtered_data.csv",
            "text/csv"
        )
else:
    st.info('Please upload a file to begin.')