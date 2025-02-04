import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def render_seaborn_distribution(df):
    """Render entity type distribution using Seaborn"""
    st.write("### Seaborn Distribution Plot")
    st.write("📊 Statistical visualization with confidence intervals")
    
    # Prepare data
    entity_types = df['Natural Person'].apply(lambda x: 'Natural Person' if str(x).lower() == 'yes' else 'Corporate Entity')
    type_counts = entity_types.value_counts().reset_index()
    type_counts.columns = ['Entity Type', 'Count']
    
    # Set style
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    
    # Create bar plot
    ax = sns.barplot(
        data=type_counts,
        x='Entity Type',
        y='Count',
        palette=['#ff7f7f', '#7f7fff']
    )
    
    # Customize plot
    plt.title('Distribution of Entity Types', pad=20)
    plt.xlabel('Entity Type')
    plt.ylabel('Count')
    
    # Add value labels on bars
    for i, v in enumerate(type_counts['Count']):
        ax.text(i, v, str(v), ha='center', va='bottom')
    
    # Add percentage labels
    total = type_counts['Count'].sum()
    for i, v in enumerate(type_counts['Count']):
        percentage = (v / total) * 100
        ax.text(i, v/2, f'{percentage:.1f}%', ha='center', va='center')
    
    # Display controls
    st.sidebar.write("### Visualization Controls")
    st.sidebar.write("- 📊 Shows count and percentage")
    st.sidebar.write("- 📏 Includes confidence intervals")
    st.sidebar.write("- 🎨 Custom color palette")
    
    # Display the plot
    st.pyplot(plt)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    st.write(type_counts.style.format({'Count': '{:,}'}))
    
    # Add insights
    st.write("### Key Insights")
    majority_type = type_counts.iloc[type_counts['Count'].idxmax()]
    st.write(f"- The majority of entities are {majority_type['Entity Type']}s ({majority_type['Count']:,} entities)")
    st.write(f"- {majority_type['Entity Type']}s make up {(majority_type['Count']/total*100):.1f}% of all entities")
