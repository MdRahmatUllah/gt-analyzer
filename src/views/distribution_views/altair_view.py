import streamlit as st
import altair as alt
import pandas as pd

def render_altair_distribution(df):
    """Render entity type distribution using Altair"""
    st.write("### Altair Distribution Plot")
    st.write("📊 Declarative visualization with interactive features")
    
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
        # If 'All' is selected, sum up counts across countries
        display_df = type_counts.groupby('Entity Type')['Count'].sum().reset_index()
        total = display_df['Count'].sum()
        display_df['Percentage'] = (display_df['Count'] / total * 100).round(1)
        display_df['Country'] = 'All Countries'
    
    # Add percentage text to display
    display_df['PercentageLabel'] = display_df['Percentage'].apply(lambda x: f'{x:.1f}%')
    
    # Create base chart
    chart = alt.Chart(display_df).encode(
        x=alt.X('Entity Type:N', 
                axis=alt.Axis(title='Entity Type'),
                sort='-y'),
        y=alt.Y('Count:Q',
                axis=alt.Axis(title='Count')),
        tooltip=[
            alt.Tooltip('Entity Type:N', title='Type'),
            alt.Tooltip('Count:Q', title='Count', format=','),
            alt.Tooltip('Percentage:Q', title='Percentage', format='.1f'),
            alt.Tooltip('Country:N', title='Country')
        ],
        color=alt.Color('Entity Type:N',
                       scale=alt.Scale(
                           domain=['Natural Person', 'Corporate Entity'],
                           range=['#ff7f7f', '#7f7fff']
                       ),
                       legend=None)
    )
    
    # Create bars
    bars = chart.mark_bar()
    
    # Create text labels for counts
    text_count = chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5
    ).encode(
        text=alt.Text('Count:Q', format=',')
    )
    
    # Create text labels for percentages
    text_percentage = chart.mark_text(
        align='center',
        baseline='middle',
        color='white',
        fontSize=14
    ).encode(
        y=alt.Y('Count:Q', stack=None),
        text='PercentageLabel:N'
    )
    
    # Combine the visualizations
    final_chart = (bars + text_count + text_percentage).properties(
        width=600,
        height=400,
        title=alt.Title(
            text=f'Entity Type Distribution {f"in {selected_country}" if selected_country != "All" else ""}',
            fontSize=16,
            anchor='middle'
        )
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    
    # Display controls
    st.sidebar.write("### Visualization Controls")
    st.sidebar.write("- 🌍 Filter by country")
    st.sidebar.write("- 📊 Shows count and percentage")
    st.sidebar.write("- 🔍 Interactive tooltips")
    st.sidebar.write("- 📏 Sorted by count")
    
    # Display the plot
    st.altair_chart(final_chart, use_container_width=True)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    summary_df = display_df[['Entity Type', 'Count', 'Percentage']].copy()
    st.write(summary_df.style.format({
        'Count': '{:,}',
        'Percentage': '{:.1f}%'
    }))
