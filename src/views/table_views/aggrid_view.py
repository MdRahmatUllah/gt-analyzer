import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd

def render_aggrid_table(df):
    """Render interactive table using Streamlit-AgGrid"""
    st.write("### AgGrid Interactive Table")
    st.write("📊 Feature-rich table with sorting and filtering")
    
    # Create a copy of the dataframe
    df_display = df.copy()
    
    # Format Share column
    df_display['Share'] = df_display['Share'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
    
    # Create GridOptionsBuilder
    gb = GridOptionsBuilder.from_dataframe(df_display)
    
    # Configure grid options
    gb.configure_default_column(
        filterable=True,
        sortable=True,
        resizable=True,
        editable=False
    )
    
    # Configure specific columns
    gb.configure_column(
        "Natural Person",
        filter=True,
        filterParams={
            "filterOptions": ["equals"],
            "suppressAndOrCondition": True
        }
    )
    
    gb.configure_column(
        "Country Code",
        filter=True,
        filterParams={
            "filterOptions": ["equals", "contains"],
            "suppressAndOrCondition": True
        }
    )
    
    gb.configure_column(
        "City",
        filter=True,
        filterParams={
            "filterOptions": ["equals", "contains"],
            "suppressAndOrCondition": True
        }
    )
    
    # Enable selection
    gb.configure_selection(
        selection_mode='multiple',
        use_checkbox=True
    )
    
    # Build grid options
    grid_options = gb.build()
    
    # Display controls
    st.sidebar.write("### Table Controls")
    st.sidebar.write("- 🔍 Filter any column")
    st.sidebar.write("- ↕️ Sort by clicking headers")
    st.sidebar.write("- ✅ Select rows with checkboxes")
    st.sidebar.write("- ↔️ Resize columns")
    
    # Create AgGrid
    grid_response = AgGrid(
        df_display,
        gridOptions=grid_options,
        height=600,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=False
    )
    
    # Display selection summary
    if grid_response['selected_rows']:
        st.write("### Selected Rows Summary")
        selected_df = pd.DataFrame(grid_response['selected_rows'])
        st.write(f"Number of selected rows: {len(selected_df)}")
        
        if len(selected_df) > 0:
            # Calculate statistics for selected rows
            natural_person_count = sum(selected_df['Natural Person'].str.lower() == 'yes')
            corporate_count = len(selected_df) - natural_person_count
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Natural Persons", natural_person_count)
            with col2:
                st.metric("Corporate Entities", corporate_count)
            
            # Show unique countries and cities
            st.write("#### Unique Countries")
            st.write(", ".join(sorted(selected_df['Country Code'].unique())))
            
            st.write("#### Unique Cities")
            st.write(", ".join(sorted(selected_df['City'].unique())))
