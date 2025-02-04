import streamlit as st
from views.statistics_view import render_statistics_view
from views.hierarchy_views import render_hierarchy_views
from views.map_views import render_map_views
from views.network_views import render_network_views
from views.distribution_views import render_distribution_views
from views.table_views import render_table_views

def render_main_content(filtered_df=None):
    """Render the main content area with all visualization tabs."""
    st.title('Corporate Structure Visualization Tool')
    
    if filtered_df is not None:
        # Display raw data in expander
        with st.expander("View Raw Data"):
            st.dataframe(filtered_df)
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Network Graph", 
            "Hierarchy View", 
            "Geographic View", 
            "Statistics", 
            "Distribution", 
            "Table View"
        ])
        
        with tab1:
            render_network_views(filtered_df)
        with tab2:
            render_hierarchy_views(filtered_df)
        with tab3:
            render_map_views(filtered_df)
        with tab4:
            render_statistics_view(filtered_df)
        with tab5:
            render_distribution_views(filtered_df)
        with tab6:
            render_table_views(filtered_df)
    else:
        st.info('Please upload a file to begin.')
