import streamlit as st
from dash import Dash, dash_table
import pandas as pd
from dash import html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

def render_dash_table(df):
    """Render interactive table using Dash DataTable"""
    st.write("### Dash Interactive Table")
    st.write("📊 Highly customizable table with advanced filtering")
    
    # Create a copy of the dataframe
    df_display = df.copy()
    
    # Format Share column
    df_display['Share'] = df_display['Share'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
    
    # Create table using Plotly's Figure
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df_display.columns),
                    fill_color='paleturquoise',
                    align='left',
                    font=dict(size=12, color='black'),
                    height=40
                ),
                cells=dict(
                    values=[df_display[col] for col in df_display.columns],
                    fill_color='lavender',
                    align='left',
                    font=dict(size=11, color='black'),
                    height=30
                )
            )
        ]
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Arial")
    )
    
    # Display controls
    st.sidebar.write("### Table Controls")
    st.sidebar.write("- 🔍 Filter by multiple criteria")
    st.sidebar.write("- 📱 Responsive design")
    st.sidebar.write("- 📸 Download as PNG")
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Country filter
        countries = ['All'] + sorted(df_display['Country Code'].unique().tolist())
        selected_country = st.selectbox('Country', countries)
        
        # Entity type filter
        entity_types = ['All', 'Natural Person', 'Corporate Entity']
        selected_type = st.selectbox('Entity Type', entity_types)
    
    with col2:
        # City filter
        cities = ['All'] + sorted(df_display['City'].unique().tolist())
        selected_city = st.selectbox('City', cities)
        
        # Share range filter
        share_values = df['Share'].dropna()
        min_share = share_values.min()
        max_share = share_values.max()
        share_range = st.slider('Share Range (%)', 
                              float(min_share), 
                              float(max_share),
                              (float(min_share), float(max_share)))
    
    # Apply filters
    filtered_df = df_display.copy()
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    if selected_type != 'All':
        is_person = selected_type == 'Natural Person'
        filtered_df = filtered_df[filtered_df['Natural Person'].str.lower() == ('yes' if is_person else 'no')]
    
    # Update table with filtered data
    fig.update_traces(
        cells=dict(values=[filtered_df[col] for col in filtered_df.columns])
    )
    
    # Display the table
    st.plotly_chart(fig, use_container_width=True)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    
    # Calculate statistics
    total_filtered = len(filtered_df)
    natural_persons = sum(filtered_df['Natural Person'].str.lower() == 'yes')
    corporate_entities = total_filtered - natural_persons
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Filtered Entities",
            f"{total_filtered:,}",
            f"{total_filtered/len(df)*100:.1f}% of total"
        )
    
    with col2:
        st.metric(
            "Natural Persons",
            f"{natural_persons:,}",
            f"{natural_persons/total_filtered*100:.1f}% of filtered" if total_filtered > 0 else "N/A"
        )
    
    with col3:
        st.metric(
            "Corporate Entities",
            f"{corporate_entities:,}",
            f"{corporate_entities/total_filtered*100:.1f}% of filtered" if total_filtered > 0 else "N/A"
        )
