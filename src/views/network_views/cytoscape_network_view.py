import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def render_cytoscape_network(df):
    """Render network graph using Cytoscape"""
    st.write("### Cytoscape Network Graph")
    st.write("🔍 Highly interactive graph with advanced layout options")
    
    # Prepare data for cytoscape
    nodes = []
    edges = []
    
    # Add nodes
    for _, row in df.iterrows():
        is_person = row.get('Natural Person', 'no').lower() == 'yes'
        nodes.append({
            'id': row['Name'],
            'label': row['Name'],
            'type': 'person' if is_person else 'entity',
            'city': row.get('City', 'N/A'),
            'country': row.get('Country Code', 'N/A')
        })
    
    # Add edges
    for _, row in df.iterrows():
        if pd.notna(row.get('Parent Entity ID')) and row.get('Parent Entity ID') in df.index:
            parent = df.loc[row['Parent Entity ID']]['Name']
            edges.append({
                'source': parent,
                'target': row['Name']
            })
    
    # Create Cytoscape HTML
    cytoscape_html = f"""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.23.0/cytoscape.min.js"></script>
        <style>
            #cy {{
                width: 100%;
                height: 600px;
                display: block;
            }}
        </style>
    </head>
    <body>
        <div id="cy"></div>
        <script>
            var cy = cytoscape({{
                container: document.getElementById('cy'),
                elements: {{
                    nodes: {str([{
                        'data': {
                            'id': node['id'],
                            'label': node['label'],
                            'type': node['type'],
                            'city': node['city'],
                            'country': node['country']
                        }
                    } for node in nodes])},
                    edges: {str([{
                        'data': {
                            'source': edge['source'],
                            'target': edge['target']
                        }
                    } for edge in edges])}
                }},
                style: [
                    {{
                        selector: 'node',
                        style: {{
                            'content': 'data(label)',
                            'text-wrap': 'wrap',
                            'text-max-width': 100,
                            'font-size': '12px',
                            'text-valign': 'center',
                            'text-halign': 'center'
                        }}
                    }},
                    {{
                        selector: 'node[type = "person"]',
                        style: {{
                            'background-color': '#ff7f7f',
                            'shape': 'ellipse'
                        }}
                    }},
                    {{
                        selector: 'node[type = "entity"]',
                        style: {{
                            'background-color': '#7f7fff',
                            'shape': 'rectangle'
                        }}
                    }},
                    {{
                        selector: 'edge',
                        style: {{
                            'width': 1,
                            'line-color': '#888888',
                            'target-arrow-color': '#888888',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier'
                        }}
                    }}
                ],
                layout: {{
                    name: 'cose',
                    animate: true,
                    animationDuration: 500,
                    nodeDimensionsIncludeLabels: true
                }}
            }});
            
            // Add event listeners
            cy.on('tap', 'node', function(evt){{
                var node = evt.target;
                alert(
                    'Name: ' + node.data('label') + '\\n' +
                    'Type: ' + node.data('type') + '\\n' +
                    'City: ' + node.data('city') + '\\n' +
                    'Country: ' + node.data('country')
                );
            }});
        </script>
    </body>
    </html>
    """
    
    # Display controls
    st.sidebar.write("### Graph Controls")
    st.sidebar.write("- 🖱️ Drag nodes to reposition")
    st.sidebar.write("- 🔍 Scroll to zoom")
    st.sidebar.write("- 👆 Click for details")
    st.sidebar.write("- 🎮 Double-click to center")
    
    # Display the graph
    components.html(cytoscape_html, height=600)
