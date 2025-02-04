import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

def render_d3_hierarchy(df):
    """
    Render ownership hierarchy using D3.js
    """
    # Convert data to hierarchical structure
    def build_tree(df):
        nodes = {}
        root = None
        
        # First pass: create all nodes
        for _, row in df.iterrows():
            node = {
                'id': row['Entity ID'],
                'name': row['Name'],
                'city': row.get('City', 'N/A'),
                'country': row.get('Country Code', 'N/A'),
                'is_person': row.get('Natural Person', 'no').lower() == 'yes',
                'children': []
            }
            nodes[row['Entity ID']] = node
            
            if pd.isna(row.get('Parent Entity ID')):
                root = node
        
        # Second pass: build relationships
        for _, row in df.iterrows():
            if pd.notna(row.get('Parent Entity ID')):
                parent = nodes.get(row['Parent Entity ID'])
                if parent:
                    parent['children'].append(nodes[row['Entity ID']])
        
        return root if root else nodes[list(nodes.keys())[0]]

    # Convert data to hierarchical JSON
    tree_data = build_tree(df)
    
    # Calculate dimensions based on data size
    node_count = len(df)
    height = max(600, node_count * 40)
    width = max(800, node_count * 50)

    # D3.js visualization code
    d3_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            .node circle {{
                fill: #fff;
                stroke-width: 2px;
            }}
            .node text {{
                font: 12px sans-serif;
            }}
            .link {{
                fill: none;
                stroke: #ccc;
                stroke-width: 1px;
            }}
            .tooltip {{
                position: absolute;
                padding: 8px;
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd;
                border-radius: 4px;
                pointer-events: none;
                font-family: sans-serif;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div id="tree-container"></div>
        <script>
            // Data
            const data = {json.dumps(tree_data)};
            
            // Dimensions
            const width = {width};
            const height = {height};
            const margin = {{top: 20, right: 120, bottom: 20, left: 120}};
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;
            
            // Create the SVG container
            const svg = d3.select("#tree-container")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);
            
            // Create the tree layout
            const tree = d3.tree()
                .size([innerHeight, innerWidth]);
            
            // Create the root node
            const root = d3.hierarchy(data);
            
            // Generate the tree layout
            tree(root);
            
            // Create tooltip
            const tooltip = d3.select("body")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);
            
            // Add the links
            svg.selectAll(".link")
                .data(root.links())
                .join("path")
                .attr("class", "link")
                .attr("d", d3.linkHorizontal()
                    .x(d => d.y)
                    .y(d => d.x));
            
            // Add the nodes
            const nodes = svg.selectAll(".node")
                .data(root.descendants())
                .join("g")
                .attr("class", "node")
                .attr("transform", d => `translate(${{d.y}},${{d.x}})`);
            
            // Add circles to nodes
            nodes.append("circle")
                .attr("r", 6)
                .style("stroke", d => d.data.is_person ? "#ff9999" : "#99ccff")
                .style("fill", d => d.data.is_person ? "#ff9999" : "#99ccff")
                .on("mouseover", function(event, d) {{
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    tooltip.html(`Name: ${{d.data.name}}<br/>` +
                               `City: ${{d.data.city}}<br/>` +
                               `Country: ${{d.data.country}}`)
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 28) + "px");
                }})
                .on("mouseout", function(d) {{
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                }});
            
            // Add labels to nodes
            nodes.append("text")
                .attr("dy", ".35em")
                .attr("x", d => d.children ? -12 : 12)
                .style("text-anchor", d => d.children ? "end" : "start")
                .text(d => d.data.name)
                .each(function(d) {{
                    const bbox = this.getBBox();
                    d3.select(this.parentNode)
                        .insert("rect", "text")
                        .attr("x", bbox.x - 4)
                        .attr("y", bbox.y - 2)
                        .attr("width", bbox.width + 8)
                        .attr("height", bbox.height + 4)
                        .attr("rx", 4)
                        .attr("ry", 4)
                        .style("fill", "rgba(255, 255, 255, 0.9)")
                        .style("stroke", "#ddd");
                }});
            
            // Add zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.5, 2])
                .on("zoom", (event) => {{
                    svg.attr("transform", event.transform);
                }});
            
            d3.select("svg")
                .call(zoom)
                .call(zoom.translateTo, width / 2, height / 2);
        </script>
    </body>
    </html>
    """
    
    # Display the visualization
    st.write("### D3.js Hierarchy Visualization")
    st.write("🔍 Interactive features: Hover for details, zoom and pan")
    components.html(d3_code, height=height, width=width)
