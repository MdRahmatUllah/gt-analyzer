import streamlit as st
import pandas as pd

def render_ipywidgets_table(df):
    """Render interactive table using Streamlit widgets"""
    st.write("### Interactive Filtered Table")
    st.write("📊 Widget-based interactive filtering")
    
    # Create a copy of the dataframe
    df_display = df.copy()
    
    # Format Share column - convert to numeric first
    df_display['Share'] = pd.to_numeric(df_display['Share'], errors='coerce')
    df_display['Share'] = df_display['Share'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
    
    # Create filters
    st.sidebar.write("### Filters")
    
    # Create two columns for filters
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
        min_share = float(share_values.min())
        max_share = float(share_values.max())
        share_range = st.slider('Share Range (%)', 
                              min_value=min_share,
                              max_value=max_share,
                              value=(min_share, max_share))
    
    # Apply filters
    filtered_df = df_display.copy()
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country Code'] == selected_country]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    if selected_type != 'All':
        is_person = selected_type == 'Natural Person'
        filtered_df = filtered_df[filtered_df['Natural Person'].str.lower() == ('yes' if is_person else 'no')]
    
    # Display controls
    st.sidebar.write("### Table Controls")
    st.sidebar.write("- 🔍 Interactive filtering")
    st.sidebar.write("- 📊 Real-time updates")
    st.sidebar.write("- 📈 Summary statistics")
    
    # Add search functionality
    search_term = st.text_input("Search in any column", "")
    if search_term:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    # Display the filtered dataframe
    st.dataframe(filtered_df, height=400, use_container_width=True)
    
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
    
    # Display unique values
    st.write("#### Unique Values in Filtered Data")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Countries:", ", ".join(sorted(filtered_df['Country Code'].unique())))
    
    with col2:
        st.write("Cities:", ", ".join(sorted(filtered_df['City'].unique())))
