import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Import modular components
from components.layout import init_page_layout, close_page_layout
from components.sidebar import render_sidebar_header, render_file_upload
from components.footer import render_footer
from components.main_content import render_main_content
from styles.main import load_styles
from components.filters import render_filters, apply_filters
from logic.data_processor import load_data, build_graph

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

def main():
    # Initialize page layout
    init_page_layout()
    
    # Load styles
    load_styles()
    
    # Render sidebar components
    render_sidebar_header()
    uploaded_file = render_file_upload()
    
    if uploaded_file is not None:
        # Load and process data
        df = load_data(uploaded_file)
        
        if df is not None:
            # Get and apply filters
            selected_countries, min_share, show_persons = render_filters(df)
            filtered_df = apply_filters(df, selected_countries, min_share, show_persons)
            
            # Render main content
            render_main_content(filtered_df)
            
            # Export options
            st.sidebar.download_button(
                "Download Filtered Data",
                filtered_df.to_csv(index=False),
                "filtered_data.csv",
                "text/csv"
            )
    else:
        render_main_content()
    
    # Close layout and render footer
    close_page_layout()
    render_footer()

if __name__ == "__main__":
    main()