import streamlit as st
from pyvis.network import Network
import pandas as pd
import streamlit.components.v1 as components

def render_pyvis_network(df):
    """Render network graph using PyVis"""
    st.write("### PyVis Network Graph")
    st.write("🔍 Interactive network with physics simulation")
    
    # Initialize network
    net = Network(
        height='600px',
        width='100%',
        bgcolor='#ffffff',
        font_color='#333333'
    )
    
    # Configure physics
    net.force_atlas_2based()
    net.show_buttons(filter_=['physics'])
    
    # Add nodes
    for _, row in df.iterrows():
        is_person = row.get('Natural Person', 'no').lower() == 'yes'
        net.add_node(
            row['Name'],
            label=row['Name'],
            title=(
                f"Name: {row['Name']}<br>"
                f"Type: {'Natural Person' if is_person else 'Corporate Entity'}<br>"
                f"City: {row.get('City', 'N/A')}<br>"
                f"Country: {row.get('Country Code', 'N/A')}"
            ),
            color='#ff7f7f' if is_person else '#7f7fff',
            size=20
        )
    
    # Add edges
    for _, row in df.iterrows():
        if pd.notna(row.get('Parent Entity ID')) and row.get('Parent Entity ID') in df.index:
            parent = df.loc[row['Parent Entity ID']]['Name']
            net.add_edge(parent, row['Name'], color='#888888')
    
    # Generate HTML file
    net.save_graph('network.html')
    
    # Read the file
    with open('network.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Display controls
    st.sidebar.write("### Graph Controls")
    st.sidebar.write("- 🖱️ Drag nodes to reposition")
    st.sidebar.write("- 🔍 Scroll to zoom")
    st.sidebar.write("- 👆 Hover for details")
    st.sidebar.write("- 🎮 Use physics controls")
    
    # Display the graph
    components.html(html, height=600)
