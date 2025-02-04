import streamlit as st
import streamlit.components.v1 as components
from pyecharts import options as opts
from pyecharts.charts import Tree
import pandas as pd

def render_pyecharts_hierarchy(df):
    """
    Render ownership hierarchy using PyEcharts
    """
    def build_tree(df):
        nodes = {}
        root = None
        
        # First pass: create all nodes
        for _, row in df.iterrows():
            node = {
                'name': row['Name'],
                'value': [
                    row.get('City', 'N/A'),
                    row.get('Country Code', 'N/A'),
                    'Natural Person' if row.get('Natural Person', 'no').lower() == 'yes' else 'Corporate Entity'
                ],
                'itemStyle': {
                    'color': '#ff9999' if row.get('Natural Person', 'no').lower() == 'yes' else '#99ccff'
                },
                'children': [],
                'collapsed': False
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

    # Build the tree data
    data = build_tree(df)
    
    # Calculate appropriate height based on number of nodes
    num_nodes = len(df)
    height = max(600, num_nodes * 50)
    
    # Create the tree chart
    tree = (
        Tree(init_opts=opts.InitOpts(width="100%", height=f"{height}px"))
        .add(
            series_name="",
            data=[data],
            pos_top="2%",
            pos_bottom="2%",
            pos_left="15%",
            pos_right="15%",
            layout="orthogonal",
            orient="TB",
            initial_tree_depth=-1,
            symbol_size=10,
            is_roam=True,
            label_opts=opts.LabelOpts(
                position="right",
                horizontal_align="left",
                vertical_align="middle",
                font_size=12,
                distance=15,
                rotate=0,
                font_weight="bold",
                padding=[5, 7, 5, 7],
                border_width=1,
                border_color="#ccc",
                border_radius=5,
                background_color="rgba(255,255,255,0.8)"
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Ownership Hierarchy",
                subtitle="Drag to pan, scroll to zoom",
                pos_left="center"
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                trigger_on="mousemove",
                formatter="""
                    Name: {b}<br/>
                    City: {c0}<br/>
                    Country: {c1}<br/>
                    Type: {c2}
                """
            )
        )
    )
    
    st.write("### PyEcharts Hierarchy Visualization")
    st.write("🔍 Interactive features: Drag to pan, scroll to zoom")
    
    # Add custom CSS to ensure the chart container is scrollable
    components.html(
        f"""
        <style>
        .chart-container {{
            width: 100%;
            height: {height}px;
            overflow: auto;
            border: 1px solid #eee;
            border-radius: 5px;
        }}
        </style>
        <div class="chart-container">
            {tree.render_embed()}
        </div>
        """,
        height=height
    )
