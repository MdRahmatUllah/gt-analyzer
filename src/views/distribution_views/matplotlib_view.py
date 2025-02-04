import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def render_matplotlib_distribution(df):
    """Render entity type distribution using Matplotlib"""
    st.write("### Matplotlib Distribution Plot")
    st.write("📊 Basic bar chart with customizations")
    
    # Prepare data
    entity_types = df['Natural Person'].apply(lambda x: 'Natural Person' if str(x).lower() == 'yes' else 'Corporate Entity')
    type_counts = entity_types.value_counts()
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    bars = ax.bar(
        range(len(type_counts)),
        type_counts.values,
        color=['#ff7f7f', '#7f7fff'],
        tick_label=type_counts.index
    )
    
    # Customize plot
    ax.set_title('Distribution of Entity Types', pad=20)
    ax.set_xlabel('Entity Type')
    ax.set_ylabel('Count')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom'
        )
        # Add percentage label
        percentage = (height / type_counts.sum()) * 100
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height/2,
            f'{percentage:.1f}%',
            ha='center',
            va='center',
            color='white',
            fontweight='bold'
        )
    
    # Adjust layout
    plt.tight_layout()
    
    # Display controls
    st.sidebar.write("### Visualization Controls")
    st.sidebar.write("- 📊 Shows count and percentage")
    st.sidebar.write("- 🎨 Custom color palette")
    st.sidebar.write("- 📏 Y-axis grid lines")
    
    # Display the plot
    st.pyplot(fig)
    
    # Display summary statistics
    st.write("### Summary Statistics")
    summary_df = pd.DataFrame({
        'Entity Type': type_counts.index,
        'Count': type_counts.values,
        'Percentage': (type_counts.values / type_counts.sum() * 100).round(1)
    })
    st.write(summary_df.style.format({
        'Count': '{:,}',
        'Percentage': '{:.1f}%'
    }))
