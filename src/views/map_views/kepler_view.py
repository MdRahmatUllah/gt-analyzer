import streamlit as st
import pandas as pd
from utils.geocoding import get_location_data
import keplergl

def render_kepler_map(df):
    """Render geographic distribution using Kepler.gl"""
    st.write("### Kepler.gl Map Visualization")
    st.write("🗺️ Advanced geospatial visualization with multiple layers")
    
    # Get location data
    location_df = get_location_data(df)
    
    if location_df.empty:
        st.warning("No valid location data found.")
        return
    
    # Create Kepler map configuration
    config = {
        "version": "v1",
        "config": {
            "visState": {
                "filters": [],
                "layers": [
                    {
                        "id": "points",
                        "type": "point",
                        "config": {
                            "dataId": "data",
                            "label": "Points",
                            "color": [255, 153, 153],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude",
                                "altitude": None
                            },
                            "isVisible": True,
                            "visConfig": {
                                "radius": 10,
                                "fixedRadius": False,
                                "opacity": 0.8,
                                "outline": True,
                                "thickness": 2,
                                "colorRange": {
                                    "name": "Custom",
                                    "type": "custom",
                                    "category": "Custom",
                                    "colors": ["#ff9999", "#99ccff"]
                                },
                                "radiusRange": [5, 20],
                                "filled": True
                            }
                        },
                        "visualChannels": {
                            "colorField": {
                                "name": "is_person",
                                "type": "boolean"
                            },
                            "colorScale": "ordinal",
                            "sizeField": None,
                            "sizeScale": "linear"
                        }
                    },
                    {
                        "id": "heat",
                        "type": "heatmap",
                        "config": {
                            "dataId": "data",
                            "label": "Heat",
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.8,
                                "colorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": ["#5A1846", "#900C3F", "#C70039", "#FF5733", "#FFC300"]
                                },
                                "radius": 20
                            }
                        }
                    }
                ]
            },
            "mapState": {
                "bearing": 0,
                "latitude": location_df['latitude'].mean(),
                "longitude": location_df['longitude'].mean(),
                "pitch": 0,
                "zoom": 3
            },
            "mapStyle": {
                "styleType": "dark",
                "topLayerGroups": {},
                "visibleLayerGroups": {
                    "label": True,
                    "road": True,
                    "border": False,
                    "building": True,
                    "water": True,
                    "land": True
                }
            }
        }
    }
    
    # Create Kepler map
    map_1 = keplergl.KeplerGl(height=600, data={"data": location_df}, config=config)
    
    # Display the map
    keplergl.KeplerGl.save_to_html(
        map_1,
        file_name='kepler_map.html',
        read_only=True
    )
    
    # Read the generated HTML and display it
    with open('kepler_map.html', 'r') as f:
        html_content = f.read()
    
    st.components.v1.html(html_content, height=600)
