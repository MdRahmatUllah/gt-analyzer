import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd

def render_plotly_hierarchy(df):
    """
    Render ownership hierarchy using Networkx + Plotly
    """
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for _, row in df.iterrows():
        # Add node
        G.add_node(row['Entity ID'], 
                  name=row['Name'],
                  city=row.get('City', 'N/A'),
                  country=row.get('Country Code', 'N/A'),
                  is_person=row.get('Natural Person', 'no').lower() == 'yes')
        
        # Add edge if there's a parent
        if pd.notna(row.get('Parent Entity ID')):
            G.add_edge(row['Parent Entity ID'], row['Entity ID'], 
                      weight=row.get('Share', 0))

    # Use hierarchical layout
    pos = nx.spring_layout(G)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = []
    node_y = []
    node_colors = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Color based on type
        node_colors.append('#ff9999' if G.nodes[node]['is_person'] else '#99ccff')
        
        # Create hover text
        node_text.append(
            f"Name: {G.nodes[node]['name']}<br>"
            f"City: {G.nodes[node]['city']}<br>"
            f"Country: {G.nodes[node]['country']}"
        )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[node]['name'] for node in G.nodes()],
        textposition="bottom center",
        hovertext=node_text,
        marker=dict(
            showscale=False,
            color=node_colors,
            size=20,
            line_width=2))

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=0),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                   )

    st.write("### Plotly Hierarchy Visualization")
    st.write("🔍 Interactive features: Zoom, pan, hover for details")
    st.plotly_chart(fig, use_container_width=True)
