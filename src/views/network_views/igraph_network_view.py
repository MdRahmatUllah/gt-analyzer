import streamlit as st
import igraph as ig
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def render_igraph_network(df):
    """Render network visualization using igraph"""
    # Create a graph
    g = ig.Graph(directed=True)
    
    # Add vertices (nodes)
    unique_entities = set(df['Entity ID'].unique()) | set(df['Parent Entity ID'].dropna().unique())
    entity_to_idx = {entity: idx for idx, entity in enumerate(unique_entities)}
    g.add_vertices(len(unique_entities))
    
    # Set vertex properties
    entity_names = {}
    for _, row in df.iterrows():
        entity_names[row['Entity ID']] = row['Name']
        if pd.notna(row['Parent Entity ID']) and row['Parent Entity ID'] not in entity_names:
            # For parent entities not in the main dataset
            entity_names[row['Parent Entity ID']] = f"Entity {row['Parent Entity ID']}"
    
    g.vs['label'] = [entity_names.get(entity, f"Entity {entity}") for entity in unique_entities]
    g.vs['is_person'] = [df[df['Entity ID'] == entity]['Natural Person'].iloc[0] == 'yes' 
                        if entity in df['Entity ID'].values else False 
                        for entity in unique_entities]
    
    # Add edges
    edges = [(entity_to_idx[row['Parent Entity ID']], entity_to_idx[row['Entity ID']]) 
            for _, row in df.iterrows() if pd.notna(row['Parent Entity ID'])]
    g.add_edges(edges)
    
    # Set edge properties (ownership percentages)
    g.es['weight'] = [row['Share'] for _, row in df.iterrows() if pd.notna(row['Parent Entity ID'])]
    
    # Calculate layout
    layout = g.layout_fruchterman_reingold()
    
    # Convert layout to x, y coordinates
    Xn = [coord[0] for coord in layout]
    Yn = [coord[1] for coord in layout]
    
    # Create edges as scatter traces
    edge_traces = []
    for edge in g.es:
        x0, y0 = layout[edge.source]
        x1, y1 = layout[edge.target]
        
        # Create arrow shape
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=1, color='gray'),
            hoverinfo='text',
            text=f'Ownership: {edge["weight"]}%',
            mode='lines+text',
        )
        edge_traces.append(edge_trace)
    
    # Create nodes trace with different colors for persons and companies
    node_colors = ['lightgreen' if is_person else 'lightblue' for is_person in g.vs['is_person']]
    node_trace = go.Scatter(
        x=Xn,
        y=Yn,
        mode='markers+text',
        text=g.vs['label'],
        textposition="bottom center",
        marker=dict(
            size=20,
            color=node_colors,
            line=dict(width=2, color='darkblue')
        ),
        hoverinfo='text'
    )
    
    # Create figure
    fig = go.Figure(data=[*edge_traces, node_trace],
                   layout=go.Layout(
                       title="Corporate Network Structure",
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       plot_bgcolor='white'
                   ))
    
    # Add legend for node types
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=20, color='lightblue'),
        name='Company'
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=20, color='lightgreen'),
        name='Natural Person'
    ))
    fig.update_layout(showlegend=True)
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
