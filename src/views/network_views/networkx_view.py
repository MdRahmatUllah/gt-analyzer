import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from community import community_louvain
import io

def render_networkx_network(df):
    """Render network visualization using NetworkX"""
    st.write("### NetworkX Network Visualization")
    st.write("📊 Interactive network visualization with community detection")
    
    # Create a new graph
    G = nx.Graph()
    
    # Add nodes with attributes
    for _, row in df.iterrows():
        entity_id = row['Entity ID']
        parent_id = row['Parent Entity ID']
        
        # Add entity node
        if not G.has_node(entity_id):
            G.add_node(entity_id, 
                      name=row['Name'],
                      type='Natural Person' if str(row['Natural Person']).lower() == 'yes' else 'Corporate Entity',
                      country=row['Country Code'],
                      size=float(row['Share']) if pd.notna(row['Share']) else 1.0)
        
        # Add parent node and edge if parent exists
        if pd.notna(parent_id):
            if not G.has_node(parent_id):
                parent_data = df[df['Entity ID'] == parent_id]
                if not parent_data.empty:
                    parent_row = parent_data.iloc[0]
                    G.add_node(parent_id,
                              name=parent_row['Name'],
                              type='Natural Person' if str(parent_row['Natural Person']).lower() == 'yes' else 'Corporate Entity',
                              country=parent_row['Country Code'],
                              size=float(parent_row['Share']) if pd.notna(parent_row['Share']) else 1.0)
                else:
                    G.add_node(parent_id,
                              name=f'Entity {parent_id}',
                              type='Corporate Entity',
                              country='Unknown',
                              size=1.0)
            
            # Add edge
            G.add_edge(parent_id, entity_id)
    
    if len(G.nodes()) == 0:
        st.error("No valid nodes found in the data. Please check the data structure.")
        return
    
    # Community detection using Louvain method
    communities = community_louvain.best_partition(G)
    
    # Controls
    st.sidebar.write("### Network Controls")
    
    # Filtering options
    selected_country = st.sidebar.selectbox(
        "Filter by Country",
        ["All"] + sorted(list(set(data['country'] for _, data in G.nodes(data=True))))
    )
    
    selected_type = st.sidebar.selectbox(
        "Filter by Entity Type",
        ["All", "Natural Person", "Corporate Entity"]
    )
    
    # Create a subgraph based on filters
    nodes_to_keep = []
    for node, data in G.nodes(data=True):
        if (selected_country == "All" or data['country'] == selected_country) and \
           (selected_type == "All" or data['type'] == selected_type):
            nodes_to_keep.append(node)
    
    filtered_G = G.subgraph(nodes_to_keep)
    
    if len(filtered_G.nodes()) == 0:
        st.warning("No nodes match the selected filters.")
        return
    
    # Layout
    pos = nx.spring_layout(filtered_G, k=1/np.sqrt(len(filtered_G)), iterations=50)
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Draw network
    node_sizes = [data['size'] * 100 for _, data in filtered_G.nodes(data=True)]
    node_colors = [communities[node] for node in filtered_G.nodes()]
    
    # Draw edges first
    nx.draw_networkx_edges(filtered_G, pos,
                          edge_color='gray',
                          alpha=0.3)
    
    # Draw nodes
    nx.draw_networkx_nodes(filtered_G, pos,
                          node_color=node_colors,
                          node_size=node_sizes,
                          cmap=plt.cm.Set3,
                          alpha=0.7)
    
    # Draw labels using entity names instead of IDs
    labels = {node: data['name'] for node, data in filtered_G.nodes(data=True)}
    nx.draw_networkx_labels(filtered_G, pos,
                           labels=labels,
                           font_size=8)
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    plt.close()
    
    # Display the plot
    st.image(buf)
    
    # Display statistics
    st.write("#### Network Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Nodes", len(filtered_G))
        st.metric("Communities", len(set(communities.values())))
    
    with col2:
        st.metric("Total Edges", filtered_G.number_of_edges())
        avg_degree = 2 * filtered_G.number_of_edges() / len(filtered_G) if len(filtered_G) > 0 else 0
        st.metric("Average Degree", f"{avg_degree:.2f}")
    
    with col3:
        # Calculate network density
        density = nx.density(filtered_G)
        st.metric("Network Density", f"{density:.3f}")
        
        # Calculate average clustering coefficient
        clustering = nx.average_clustering(filtered_G) if len(filtered_G) > 2 else 0
        st.metric("Clustering Coefficient", f"{clustering:.3f}")
    
    # Display community information
    st.write("#### Community Analysis")
    
    # Create community summary
    community_data = []
    for comm in set(communities.values()):
        # Get nodes in community
        comm_nodes = [node for node, comm_id in communities.items() if comm_id == comm and node in filtered_G]
        
        if comm_nodes:  # Only include communities that have nodes in the filtered graph
            # Get countries and types in community
            countries = set(filtered_G.nodes[node]['country'] for node in comm_nodes)
            types = set(filtered_G.nodes[node]['type'] for node in comm_nodes)
            
            community_data.append({
                'Community': comm,
                'Size': len(comm_nodes),
                'Countries': ', '.join(sorted(countries)),
                'Entity Types': ', '.join(sorted(types))
            })
    
    # Display community summary
    if community_data:
        st.dataframe(pd.DataFrame(community_data))
