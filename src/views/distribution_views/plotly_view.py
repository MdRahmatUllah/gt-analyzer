import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_plotly_distribution(df):
    """Render entity type distribution using Plotly"""
    st.write("### Plotly Distribution Plot")
    st.write("📊 Interactive bar chart with filtering options")
    
    # Prepare data
    entity_types = df['Natural Person'].apply(lambda x: 'Natural Person' if str(x).lower() == 'yes' else 'Corporate Entity')
    country_codes = df['Country Code'].fillna('Unknown')
    
    # Create DataFrame for visualization
    plot_df = pd.DataFrame({
        'Entity Type': entity_types,
        'Country': country_codes
    })
    
    # Add country filter
    countries = ['All'] + sorted(plot_df['Country'].unique().tolist())
    selected_country = st.selectbox('Select Country', countries)
    
    # Filter data based on selection
    if selected_country != 'All':
        plot_df = plot_df[plot_df['Country'] == selected_country]
    
    # Calculate counts
    type_counts = plot_df['Entity Type'].value_counts().reset_index()
    type_counts.columns = ['Entity Type', 'Count']
    
    # Create bar chart
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(
        go.Bar(
            x=type_counts['Entity Type'],
            y=type_counts['Count'],
            marker_color=['#ff7f7f' if t == 'Natural Person' else '#7f7fff' for t in type_counts['Entity Type']],
            text=type_counts['Count'],
            textposition='auto',
            hovertemplate='%{x}<br>Count: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>',
            customdata=[(count/type_counts['Count'].sum()*100) for count in type_counts['Count']]
        )
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'Distribution of Entity Types {f"in {selected_country}" if selected_country != "All" else ""}',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Entity Type',
        yaxis_title='Count',
        showlegend=False,
        height=500
    )
    
    # Add percentage text
    total = type_counts['Count'].sum()
    for i, row in type_counts.iterrows():
        percentage = (row['Count'] / total) * 100
        fig.add_annotation(
            x=row['Entity Type'],
            y=row['Count']/2,
            text=f'{percentage:.1f}%',
            showarrow=False,
            font=dict(color='white')
        )
    
    # Display controls
    st.sidebar.write("### Visualization Controls")
    st.sidebar.write("- 🌍 Filter by country")
    st.sidebar.write("- 📊 Shows count and percentage")
    st.sidebar.write("- 🔍 Hover for details")
    st.sidebar.write("- 📸 Download as PNG")
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    summary_df = type_counts.copy()
    summary_df['Percentage'] = summary_df['Count'] / summary_df['Count'].sum() * 100
    st.write(summary_df.style.format({
        'Count': '{:,}',
        'Percentage': '{:.1f}%'
    }))
