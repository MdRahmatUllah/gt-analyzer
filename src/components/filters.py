import streamlit as st

def render_filters(df):
    # Filters
    countries = sorted(df['Country Code'].unique())
    selected_countries = st.sidebar.multiselect(
        'Filter by Country',
        countries,
        default=countries
    )
    
    min_share = st.sidebar.slider('Minimum Share %', 0, 100, 0)
    show_persons = st.sidebar.checkbox('Show Natural Persons', value=True)
    
    return selected_countries, min_share, show_persons

def apply_filters(df, selected_countries, min_share, show_persons):
    # Filter data
    filtered_df = df[df['Country Code'].isin(selected_countries)]
    filtered_df = filtered_df[filtered_df['Share'] >= min_share]
    if not show_persons:
        filtered_df = filtered_df[filtered_df['Natural Person'] != 'yes']
    
    return filtered_df