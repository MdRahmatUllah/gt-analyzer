import streamlit as st
from bokeh.plotting import figure, from_networkx
from bokeh.models import (
    Circle, MultiLine, HoverTool, ResetTool,
    NodesAndLinkedEdges, EdgesAndLinkedNodes
)
import networkx as nx
import pandas as pd
import numpy as np
from bokeh.embed import file_html
from bokeh.resources import CDN
import streamlit.components.v1 as components

def render_bokeh_network(df):
    """Render network graph using Bokeh"""
    st.write("### Bokeh Network Graph")
    st.write(" Web-ready network graph with advanced interactions")
    
    # Create graph
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for _, row in df.iterrows():
        is_person = row.get('Natural Person', 'no').lower() == 'yes'
        G.add_node(
            row['Name'],
            is_person=is_person,
            city=row.get('City', 'N/A'),
            country=row.get('Country Code', 'N/A'),
            node_color='#ff7f7f' if is_person else '#7f7fff'
        )
    
    # Add edges
    for _, row in df.iterrows():
        if pd.notna(row.get('Parent Entity ID')) and row.get('Parent Entity ID') in df.index:
            parent = df.loc[row['Parent Entity ID']]['Name']
            G.add_edge(parent, row['Name'])
    
    # Create plot
    plot = figure(
        width=800,
        height=600,
        x_range=(-1.1, 1.1),
        y_range=(-1.1, 1.1),
        tools=['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'],
        active_scroll='wheel_zoom',
        title='Entity Network Graph'
    )
    
    # Remove grid and axes
    plot.grid.visible = False
    plot.axis.visible = False
    
    # Create network graph renderer
    graph_layout = nx.spring_layout(G, k=1/np.sqrt(len(G.nodes())), iterations=50)
    graph_renderer = from_networkx(G, graph_layout)
    
    # Configure node appearance
    graph_renderer.node_renderer.glyph = Circle(
        radius=8,
        fill_color='node_color',
        fill_alpha=0.8,
        line_color='white',
        line_width=1
    )
    
    # Configure edge appearance
    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color='#888888',
        line_alpha=0.6,
        line_width=1
    )
    
    # Add hover tool
    node_hover_tool = HoverTool(
        tooltips=[
            ('Name', '@index'),
            ('Type', '@is_person{Natural Person if True else Corporate Entity}'),
            ('City', '@city'),
            ('Country', '@country')
        ],
        renderers=[graph_renderer.node_renderer]
    )
    plot.add_tools(node_hover_tool)
    
    # Configure hover behavior
    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()
    
    # Add graph to plot
    plot.renderers.append(graph_renderer)
    
    # Display controls
    st.sidebar.write("### Graph Controls")
    st.sidebar.write("- Pan by dragging")
    st.sidebar.write("- Scroll to zoom")
    st.sidebar.write("- Box zoom available")
    st.sidebar.write("- Hover for details")
    st.sidebar.write("- Save plot as PNG")
    
    # Generate HTML
    html = file_html(plot, CDN, "Entity Network Graph")
    
    # Display the plot
    components.html(html, height=600)
