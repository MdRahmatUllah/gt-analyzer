import streamlit as st
import graph_tool.all as gt
import pandas as pd
import numpy as np
import tempfile
import os

def render_graphtool_network(df):
    """Render network visualization using graph-tool"""
    st.write("### Graph-tool Network Visualization")
    st.write("📊 Interactive network visualization with community detection")
    
    # Create a new graph
    g = gt.Graph(directed=False)
    
    # Add vertex properties
    v_name = g.new_vertex_property("string")
    v_type = g.new_vertex_property("string")
    v_country = g.new_vertex_property("string")
    v_city = g.new_vertex_property("string")
    v_size = g.new_vertex_property("double")
    
    # Create vertices and store mapping
    vertex_map = {}
    for _, row in df.iterrows():
        # Add vertices for both source and target if they don't exist
        for entity in [row['Source'], row['Target']]:
            if entity not in vertex_map:
                v = g.add_vertex()
                vertex_map[entity] = v
                v_name[v] = entity
                # Set vertex properties
                v_type[v] = 'Natural Person' if row['Natural Person'].lower() == 'yes' else 'Corporate Entity'
                v_country[v] = row['Country Code']
                v_city[v] = row['City']
                v_size[v] = float(row['Share']) if pd.notna(row['Share']) else 1.0
    
    # Add edges
    for _, row in df.iterrows():
        source_v = vertex_map[row['Source']]
        target_v = vertex_map[row['Target']]
        g.add_edge(source_v, target_v)
    
    # Add properties to graph
    g.vertex_properties["name"] = v_name
    g.vertex_properties["type"] = v_type
    g.vertex_properties["country"] = v_country
    g.vertex_properties["city"] = v_city
    g.vertex_properties["size"] = v_size
    
    # Community detection using stochastic block model
    state = gt.minimize_nested_blockmodel_dl(g)
    
    # Get community assignments
    communities = state.get_bs()[0]
    v_community = g.new_vertex_property("int")
    for v in g.vertices():
        v_community[v] = communities[int(v)]
    g.vertex_properties["community"] = v_community
    
    # Layout
    pos = gt.sfdp_layout(g)
    
    # Color map for communities
    colors = plt.cm.get_cmap('Set3')(np.linspace(0, 1, max(communities) + 1))
    
    # Draw graph
    st.write("#### Network Graph")
    
    # Controls
    st.sidebar.write("### Network Controls")
    
    # Filtering options
    selected_country = st.sidebar.selectbox(
        "Filter by Country",
        ["All"] + sorted(list(set(v_country[v] for v in g.vertices())))
    )
    
    selected_type = st.sidebar.selectbox(
        "Filter by Entity Type",
        ["All", "Natural Person", "Corporate Entity"]
    )
    
    # Apply filters to create a filtered graph view
    filtered_vertices = g.new_vertex_property("bool")
    for v in g.vertices():
        show_vertex = True
        if selected_country != "All" and v_country[v] != selected_country:
            show_vertex = False
        if selected_type != "All" and v_type[v] != selected_type:
            show_vertex = False
        filtered_vertices[v] = show_vertex
    
    # Create a temporary file for the image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Draw the graph
        gt.graph_draw(
            g,
            pos=pos,
            vertex_fill_color=v_community,
            vertex_size=gt.prop_to_size(v_size, mi=15, ma=30),
            vertex_text=v_name,
            vertex_font_size=8,
            vertex_filter=filtered_vertices,
            edge_pen_width=1,
            output_size=(800, 600),
            output=tmp_file.name
        )
        
        # Display the image
        st.image(tmp_file.name)
        
        # Clean up
        os.unlink(tmp_file.name)
    
    # Display statistics
    st.write("#### Network Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Nodes", g.num_vertices())
        st.metric("Communities", max(communities) + 1)
    
    with col2:
        st.metric("Total Edges", g.num_edges())
        st.metric("Average Degree", f"{2 * g.num_edges() / g.num_vertices():.2f}")
    
    with col3:
        # Calculate network density
        density = (2 * g.num_edges()) / (g.num_vertices() * (g.num_vertices() - 1))
        st.metric("Network Density", f"{density:.3f}")
        
        # Calculate clustering coefficient
        clustering = gt.global_clustering(g)[0]
        st.metric("Clustering Coefficient", f"{clustering:.3f}")
    
    # Display community information
    st.write("#### Community Analysis")
    
    community_sizes = {}
    for v in g.vertices():
        comm = v_community[v]
        if comm not in community_sizes:
            community_sizes[comm] = 0
        community_sizes[comm] += 1
    
    # Create community summary
    community_data = []
    for comm, size in community_sizes.items():
        # Get countries in community
        countries = set(v_country[v] for v in g.vertices() if v_community[v] == comm)
        # Get entity types in community
        types = set(v_type[v] for v in g.vertices() if v_community[v] == comm)
        
        community_data.append({
            'Community': comm,
            'Size': size,
            'Countries': ', '.join(sorted(countries)),
            'Entity Types': ', '.join(sorted(types))
        })
    
    # Display community summary
    st.dataframe(pd.DataFrame(community_data))
