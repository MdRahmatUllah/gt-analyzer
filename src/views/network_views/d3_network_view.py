import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

def render_d3_network(df):
    """Render network graph using D3.js"""
    st.write("### D3.js Network Graph")
    st.write("🔍 Customizable force-directed graph with smooth animations")
    
    # Prepare data
    nodes = []
    links = []
    
    # Add nodes
    for _, row in df.iterrows():
        is_person = row.get('Natural Person', 'no').lower() == 'yes'
        nodes.append({
            'id': row['Name'],
            'group': 1 if is_person else 2,
            'city': row.get('City', 'N/A'),
            'country': row.get('Country Code', 'N/A'),
            'type': 'Natural Person' if is_person else 'Corporate Entity'
        })
    
    # Add links
    for _, row in df.iterrows():
        if pd.notna(row.get('Parent Entity ID')) and row.get('Parent Entity ID') in df.index:
            parent = df.loc[row['Parent Entity ID']]['Name']
            links.append({
                'source': parent,
                'target': row['Name'],
                'value': 1
            })
    
    # Create D3.js visualization
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            .node {{
                stroke: #fff;
                stroke-width: 1.5px;
            }}
            .link {{
                stroke: #999;
                stroke-opacity: 0.6;
            }}
            .tooltip {{
                position: absolute;
                padding: 10px;
                background: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                pointer-events: none;
                font-family: sans-serif;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <script>
            const data = {json.dumps({'nodes': nodes, 'links': links})};
            
            const width = 800;
            const height = 600;
            
            const color = d3.scaleOrdinal()
                .domain([1, 2])
                .range(['#ff7f7f', '#7f7fff']);
            
            const simulation = d3.forceSimulation(data.nodes)
                .force('link', d3.forceLink(data.links).id(d => d.id))
                .force('charge', d3.forceManyBody().strength(-100))
                .force('center', d3.forceCenter(width / 2, height / 2));
            
            const svg = d3.create('svg')
                .attr('viewBox', [0, 0, width, height]);
            
            const link = svg.append('g')
                .selectAll('line')
                .data(data.links)
                .join('line')
                .attr('class', 'link');
            
            const tooltip = d3.select('body').append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);
            
            const node = svg.append('g')
                .selectAll('circle')
                .data(data.nodes)
                .join('circle')
                .attr('class', 'node')
                .attr('r', 5)
                .attr('fill', d => color(d.group))
                .call(drag(simulation))
                .on('mouseover', function(event, d) {{
                    tooltip.transition()
                        .duration(200)
                        .style('opacity', .9);
                    tooltip.html(
                        `<strong>Name:</strong> ${{d.id}}<br>` +
                        `<strong>Type:</strong> ${{d.type}}<br>` +
                        `<strong>City:</strong> ${{d.city}}<br>` +
                        `<strong>Country:</strong> ${{d.country}}`
                    )
                        .style('left', (event.pageX + 10) + 'px')
                        .style('top', (event.pageY - 28) + 'px');
                }})
                .on('mouseout', function(d) {{
                    tooltip.transition()
                        .duration(500)
                        .style('opacity', 0);
                }});
            
            simulation.on('tick', () => {{
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
            }});
            
            function drag(simulation) {{
                function dragstarted(event) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    event.subject.fx = event.subject.x;
                    event.subject.fy = event.subject.y;
                }}
                
                function dragged(event) {{
                    event.subject.fx = event.x;
                    event.subject.fy = event.y;
                }}
                
                function dragended(event) {{
                    if (!event.active) simulation.alphaTarget(0);
                    event.subject.fx = null;
                    event.subject.fy = null;
                }}
                
                return d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended);
            }}
            
            document.body.appendChild(svg.node());
        </script>
    </body>
    </html>
    """
    
    # Display controls
    st.sidebar.write("### Graph Controls")
    st.sidebar.write("- 🖱️ Drag nodes to reposition")
    st.sidebar.write("- 👆 Hover for details")
    st.sidebar.write("- 🎨 Smooth force-directed layout")
    
    # Display the graph
    components.html(html, height=600, width=800)
