import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np

def render_plotly_network(df):
    """Render network graph using Plotly"""
    st.write("### Plotly Network Graph")
    st.write("🔍 Interactive force-directed graph with hover information")
    
    # Create graph
    G = nx.DiGraph()
    
    # Add nodes
    for _, row in df.iterrows():
        G.add_node(
            row['Name'],
            is_person=row.get('Natural Person', 'no').lower() == 'yes',
            city=row.get('City', 'N/A'),
            country=row.get('Country Code', 'N/A')
        )
    
    # Add edges
    for _, row in df.iterrows():
        if pd.notna(row.get('Parent Entity ID')) and row.get('Parent Entity ID') in df.index:
            parent = df.loc[row['Parent Entity ID']]['Name']
            G.add_edge(parent, row['Name'])
    
    # Get node positions using spring layout
    pos = nx.spring_layout(G, k=1/np.sqrt(len(G.nodes())), iterations=50)
    
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
        mode='lines'
    )
    
    # Create node trace
    node_x = []
    node_y = []
    node_colors = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_colors.append('#ff7f7f' if G.nodes[node]['is_person'] else '#7f7fff')
        node_text.append(
            f"Name: {node}<br>"
            f"Type: {'Natural Person' if G.nodes[node]['is_person'] else 'Corporate Entity'}<br>"
            f"City: {G.nodes[node]['city']}<br>"
            f"Country: {G.nodes[node]['country']}"
        )
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=node_colors,
            size=15,
            line_width=2
        )
    )
    
    # Create figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title='Entity Network Graph',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[
                dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=800,
            height=600
        )
    )
    
    # Add legend
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=15, color='#ff7f7f'),
        name='Natural Person'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=15, color='#7f7fff'),
        name='Corporate Entity'
    ))
    
    # Display the graph
    st.plotly_chart(fig, use_container_width=True)
    
    # Add controls
    st.sidebar.write("### Graph Controls")
    st.sidebar.write("- 🖱️ Drag nodes to reposition")
    st.sidebar.write("- 🔍 Scroll to zoom")
    st.sidebar.write("- 👆 Hover for details")
    st.sidebar.write("- 📱 Double click to reset view")
