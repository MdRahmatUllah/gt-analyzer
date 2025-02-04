import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
import tempfile

def render_pyvis_hierarchy(df):
    """
    Render ownership hierarchy using PyVis
    """
    # Create a PyVis network
    net = Network(height="600px", width="100%", bgcolor="#ffffff", 
                 font_color="black", directed=True)
    
    # Add nodes
    for _, row in df.iterrows():
        # Determine node color based on whether it's a natural person
        color = "#ff9999" if row.get('Natural Person', 'no').lower() == 'yes' else "#99ccff"
        
        # Create tooltip
        tooltip = f"""
        Name: {row['Name']}
        City: {row.get('City', 'N/A')}
        Country: {row.get('Country Code', 'N/A')}
        """
        
        # Add node
        net.add_node(row['Entity ID'], 
                    label=row['Name'], 
                    title=tooltip,
                    color=color)
        
        # Add edge if there's a parent
        if pd.notna(row.get('Parent Entity ID')):
            net.add_edge(row['Parent Entity ID'], 
                        row['Entity ID'],
                        title=f"Ownership: {row.get('Share', '?')}%")

    # Generate HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, 'r', encoding='utf-8') as f:
            html_data = f.read()

    # Display the network
    st.write("### PyVis Hierarchy Visualization")
    st.write("🔍 Interactive features: Zoom, drag nodes, hover for details")
    components.html(html_data, height=600)
