import streamlit as st

def render_statistics_view(filtered_df):
    # Add statistical visualizations
    st.subheader("Ownership Statistics")
    
    # Ownership distribution by country
    st.write("### Ownership Distribution by Country")
    country_ownership = filtered_df.groupby('Country Code')['Share'].sum()
    st.bar_chart(country_ownership)
    
    # Entity type distribution
    st.write("### Entity Type Distribution")
    entity_types = filtered_df['Natural Person'].value_counts()
    st.bar_chart(entity_types)
    
    # Average ownership by entity type
    st.write("### Average Ownership by Entity Type")
    avg_ownership = filtered_df.groupby('Natural Person')['Share'].mean()
    st.bar_chart(avg_ownership)