import pandas as pd
import networkx as nx
import streamlit as st

@st.cache_data
def load_data(uploaded_file):
    # Load the data based on file type
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        df = pd.read_csv(uploaded_file)
    
    # Ensure required columns exist
    required_columns = ['Entity ID', 'Name', 'Country Code', 'Natural Person', 'Parent Entity ID', 'Share']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None
    
    # Fill missing values with appropriate defaults
    df['Name'] = df['Name'].fillna('Unnamed Entity')
    df['Country Code'] = df['Country Code'].fillna('Unknown')
    df['Natural Person'] = df['Natural Person'].fillna('no')
    df['Share'] = df['Share'].fillna(0)
    
    return df

def build_graph(df):
    G = nx.DiGraph()
    
    # First pass: add all nodes
    entities = set(df['Entity ID'])
    parent_entities = set(df['Parent Entity ID'].dropna())
    all_entities = entities.union(parent_entities)
    
    for entity_id in all_entities:
        # Find entity data if it exists in the dataframe
        entity_data = df[df['Entity ID'] == entity_id].iloc[0] if entity_id in entities else None
        
        G.add_node(entity_id,
                   name=entity_data['Name'] if entity_data is not None else f'Entity {entity_id}',
                   country=entity_data['Country Code'] if entity_data is not None else 'Unknown',
                   is_person=entity_data['Natural Person'] == 'yes' if entity_data is not None else False)
    
    # Second pass: add edges
    for _, row in df.iterrows():
        if pd.notna(row['Parent Entity ID']):
            G.add_edge(row['Parent Entity ID'], row['Entity ID'], share=row['Share'])
    
    return G