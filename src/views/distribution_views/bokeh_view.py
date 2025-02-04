import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Label, LabelSet
from bokeh.palettes import Spectral6
import pandas as pd
import streamlit.components.v1 as components
from bokeh.embed import file_html
from bokeh.resources import CDN

def render_bokeh_distribution(df):
    """Render entity type distribution using Bokeh"""
    st.write("### Bokeh Distribution Plot")
    st.write("📊 Interactive bar chart with tooltips")
    
    # Prepare data
    entity_types = df['Natural Person'].apply(lambda x: 'Natural Person' if str(x).lower() == 'yes' else 'Corporate Entity')
    country_codes = df['Country Code'].fillna('Unknown')
    
    # Create DataFrame for visualization
    plot_df = pd.DataFrame({
        'Entity Type': entity_types,
        'Country': country_codes
    })
    
    # Calculate counts and percentages
    type_counts = plot_df.groupby(['Entity Type', 'Country']).size().reset_index(name='Count')
    total_by_country = type_counts.groupby('Country')['Count'].sum().reset_index()
    type_counts = type_counts.merge(total_by_country, on='Country', suffixes=('', '_total'))
    type_counts['Percentage'] = (type_counts['Count'] / type_counts['Count_total'] * 100).round(1)
    
    # Add country filter
    countries = ['All'] + sorted(type_counts['Country'].unique().tolist())
    selected_country = st.selectbox('Select Country', countries)
    
    # Filter data based on selection
    if selected_country != 'All':
        display_df = type_counts[type_counts['Country'] == selected_country]
    else:
        display_df = type_counts.groupby('Entity Type')['Count'].sum().reset_index()
        total = display_df['Count'].sum()
        display_df['Percentage'] = (display_df['Count'] / total * 100).round(1)
        display_df['Country'] = 'All Countries'
    
    # Create color map
    colors = {'Natural Person': '#ff7f7f', 'Corporate Entity': '#7f7fff'}
    display_df['color'] = display_df['Entity Type'].map(colors)
    
    # Add label text
    display_df['count_label'] = display_df['Count'].apply(lambda x: f'{x:,}')
    display_df['percentage_label'] = display_df['Percentage'].apply(lambda x: f'{x:.1f}%')
    
    # Create ColumnDataSource
    source = ColumnDataSource(display_df)
    
    # Create figure
    p = figure(
        height=500,
        title=f'Distribution of Entity Types {f"in {selected_country}" if selected_country != "All" else ""}',
        toolbar_location='above',
        tools='pan,box_zoom,reset,save',
        x_range=display_df['Entity Type'].tolist(),
        sizing_mode='stretch_width'
    )
    
    # Add bars
    bars = p.vbar(
        x='Entity Type',
        top='Count',
        width=0.5,
        source=source,
        color='color',
        line_color='white',
        line_width=1
    )
    
    # Add count labels
    count_labels = LabelSet(
        x='Entity Type',
        y='Count',
        text='count_label',
        source=source,
        text_align='center',
        text_baseline='bottom',
        y_offset=5
    )
    p.add_layout(count_labels)
    
    # Add percentage labels
    percentage_labels = LabelSet(
        x='Entity Type',
        y='Count',
        text='percentage_label',
        source=source,
        text_align='center',
        text_baseline='middle',
        text_color='white',
        y_offset=-15
    )
    p.add_layout(percentage_labels)
    
    # Customize plot
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = 'Entity Type'
    p.yaxis.axis_label = 'Count'
    p.title.text_font_size = '16pt'
    p.title.align = 'center'
    
    # Customize axis
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'
    p.xaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_size = '14pt'
    
    # Add hover tool
    hover = HoverTool(
        renderers=[bars],
        tooltips=[
            ('Entity Type', '@{Entity Type}'),
            ('Count', '@count_label'),
            ('Percentage', '@percentage_label'),
            ('Country', '@Country')
        ]
    )
    p.add_tools(hover)
    
    # Generate HTML
    html = file_html(p, CDN, "Entity Distribution")
    
    # Display controls
    st.sidebar.write("### Visualization Controls")
    st.sidebar.write("- 🌍 Filter by country")
    st.sidebar.write("- 📊 Shows count and percentage")
    st.sidebar.write("- 🔍 Hover for details")
    st.sidebar.write("- 📸 Download as PNG")
    
    # Display the plot
    components.html(html, height=600)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    summary_df = display_df[['Entity Type', 'Count', 'Percentage']].copy()
    st.write(summary_df.style.format({
        'Count': '{:,}',
        'Percentage': '{:.1f}%'
    }))
