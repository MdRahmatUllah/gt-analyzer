import streamlit as st
import graphviz
import pandas as pd

def render_graphviz_hierarchy(df):
    """
    Render ownership hierarchy using Graphviz
    """
    # Create a new directed graph
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')  # Top to bottom layout
    
    # Add nodes and edges
    for _, row in df.iterrows():
        # Node attributes
        node_attrs = {
            'label': f"{row['Name']}\n{row.get('City', 'N/A')}\n{row.get('Country Code', 'N/A')}",
            'shape': 'box',
            'style': 'filled',
            'fillcolor': '#ff9999' if row.get('Natural Person', 'no').lower() == 'yes' else '#99ccff',
            'tooltip': f"Name: {row['Name']}\nCity: {row.get('City', 'N/A')}\nCountry: {row.get('Country Code', 'N/A')}"
        }
        
        # Add node
        dot.node(str(row['Entity ID']), **node_attrs)
        
        # Add edge if there's a parent
        if pd.notna(row.get('Parent Entity ID')):
            edge_attrs = {
                'label': f" {row.get('Share', '?')}%",
                'tooltip': f"Ownership: {row.get('Share', '?')}%"
            }
            dot.edge(str(row['Parent Entity ID']), str(row['Entity ID']), **edge_attrs)
    
    st.write("### Graphviz Hierarchy Visualization")
    st.write("📊 Clean hierarchical layout with ownership percentages")
    st.graphviz_chart(dot)
