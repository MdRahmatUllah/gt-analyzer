import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
import time
import pandas as pd

@st.cache_data
def get_coordinates(location):
    """
    Get coordinates for a location using geopy with retry logic
    """
    if pd.isna(location) or location.strip() == '':
        return None

    geolocator = Nominatim(
        user_agent="corporate_structure_app",
        timeout=10
    )
    # Create rate-limited geocoding function
    geocode = RateLimiter(
        geolocator.geocode,
        min_delay_seconds=1,
        max_retries=3,
        error_wait_seconds=2.0
    )
    
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            location_data = geocode(location)
            if location_data:
                return location_data.latitude, location_data.longitude
            return None
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_retries - 1:  # Last attempt
                st.warning(f"Could not geocode location: {location}. Error: {str(e)}")
                return None
            time.sleep(retry_delay)
    
    return None

@st.cache_data
def get_location_data(df):
    """
    Get location data for all entities with progress bar and error handling
    """
    locations = []
    total_rows = len(df)
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, row in df.iterrows():
        # Update progress
        progress = (idx + 1) / total_rows
        progress_bar.progress(progress)
        status_text.text(f"Processing {idx + 1}/{total_rows} entities...")
        
        location_str = f"{row.get('City', '')}, {row.get('Country Code', '')}"
        coords = get_coordinates(location_str)
        
        if coords:
            locations.append({
                'name': row['Name'],
                'city': row.get('City', 'N/A'),
                'country': row.get('Country Code', 'N/A'),
                'is_person': row.get('Natural Person', 'no').lower() == 'yes',
                'lat': coords[0],
                'lon': coords[1],
                'latitude': coords[0],  # For compatibility with different libraries
                'longitude': coords[1],
                'size': 20,  # For plotly visualization
                'elevation': 1000 if row.get('Natural Person', 'no').lower() == 'yes' else 2000  # For pydeck
            })
    
    # Clear progress bar and status text
    progress_bar.empty()
    status_text.empty()
    
    result_df = pd.DataFrame(locations)
    
    if result_df.empty:
        st.error("No valid location data found. Please check if the City and Country Code columns contain valid data.")
        return pd.DataFrame()
    
    st.success(f"Successfully geocoded {len(result_df)} out of {total_rows} entities.")
    return result_df
