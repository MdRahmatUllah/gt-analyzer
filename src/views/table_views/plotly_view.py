import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_plotly_table(df):
    """Render interactive table using Plotly Table"""
    st.write("### Plotly Interactive Table")
    st.write("📊 Interactive table with filtering and selection")
    
    # Create a copy of the dataframe
    df_display = df.copy()
    
    # Format Share column
    df_display['Share'] = df_display['Share'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
    
    # Add filters
    st.sidebar.write("### Filters")
    
    # Country filter
    countries = ['All'] + sorted(df_display['Country Code'].unique().tolist())
    selected_country = st.sidebar.selectbox('Country', countries)
    
    # City filter
    cities = ['All'] + sorted(df_display['City'].unique().tolist())
    selected_city = st.sidebar.selectbox('City', cities)
    
    # Entity type filter
    entity_types = ['All', 'Natural Person', 'Corporate Entity']
    selected_type = st.sidebar.selectbox('Entity Type', entity_types)
    
    # Apply filters
    if selected_country != 'All':
        df_display = df_display[df_display['Country Code'] == selected_country]
    if selected_city != 'All':
        df_display = df_display[df_display['City'] == selected_city]
    if selected_type != 'All':
        is_person = selected_type == 'Natural Person'
        df_display = df_display[df_display['Natural Person'].str.lower() == ('yes' if is_person else 'no')]
    
    # Create table
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
    
    # Display the table
    st.plotly_chart(fig, use_container_width=True)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    
    # Calculate statistics
    total_filtered = len(df_display)
    natural_persons = sum(df_display['Natural Person'].str.lower() == 'yes')
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
    
    # Display unique values
    st.write("#### Unique Values in Filtered Data")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Countries:", ", ".join(sorted(df_display['Country Code'].unique())))
    
    with col2:
        st.write("Cities:", ", ".join(sorted(df_display['City'].unique())))
