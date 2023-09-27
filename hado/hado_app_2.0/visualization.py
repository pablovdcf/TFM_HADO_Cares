# Functions for creating graphics and visualizations

# Modules and libraries
import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def plot_selected_category(df, selected_column):
    # Chart style
    plt.style.use('bmh')
    
    # Configuration of the displays
    fig, ax = plt.subplots(figsize=(12, 7))
    order = df[selected_column].value_counts().index
    sns.countplot(data=df, y=selected_column, order=order, ax=ax, palette='viridis')
    ax.set_title(f'Distribución de {selected_column}', fontsize=16)
    ax.set_ylabel(f'Categorías de {selected_column}', fontsize=14)
    ax.set_xlabel('Número de Registros',fontsize=14)
    ax.grid(axis='x', linestyle='--')
        
    # Showing the quantities in each bar
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height()/2.), 
                    ha='left', va='center', fontsize=10, color='black', xytext=(5,0), 
                    textcoords='offset points')
        
    plt.tight_layout()
    st.pyplot(fig)

def plot_classification_heatmap(df, classification_column, score_column):
    # Chart style
    plt.style.use('bmh')
    
    # Group by the rating column and count the values in the score column.
    classification_group = df.groupby(classification_column)[score_column].value_counts().unstack().fillna(0)
    
    # Sort the columns
    classification_group_sorted = classification_group[sorted(classification_group.columns, key=int)]
    
    # Create a figure object and axes
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Create heatmap
    sns.heatmap(classification_group_sorted, annot=True, cmap="YlGnBu", fmt=".0f", cbar_kws={'label': 'Count'})
    
    # Configure titles and labels
    ax.set_title(f'Classification of {score_column} Scores', fontsize=20)
    ax.set_xlabel(f'{score_column} Score', fontsize=15)
    ax.set_ylabel('Classification', fontsize=15)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12, rotation=0)
    
    # Show the graph in Streamlit
    st.pyplot(fig)


def plot_total_patients(df):
    # Chart style
    plt.style.use('bmh')
    
    fig, ax = plt.subplots(1, 1, figsize=(12,7))
    
    # Data to be plotted
    data_to_plot = df['year'].value_counts().sort_index()
    ax.plot(data_to_plot.index, data_to_plot.values, marker='o', linestyle='-', color='royalblue', linewidth=2)

    # Configure titles and labels
    ax.set_title('Número de Pacientes por Año', fontsize=16)
    ax.set_xlabel('Año', fontsize=14)
    ax.set_ylabel('Número de Pacientes', fontsize=14)

    # Axis limits
    ax.set_ylim(bottom=0)

    # Grid
    ax.grid(True, which='both')

    # Annotations for each point
    for x, y in zip(data_to_plot.index, data_to_plot.values):
        ax.text(x, y + 10, str(y), ha='center', va='bottom')

    # Design adjustment
    plt.tight_layout()

    # Show the graph in Streamlit
    st.pyplot(fig)
    
def plot_time_trends(df, selected_column):
    # Chart style
    plt.style.use('bmh')
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))

    # Bar chart
    count_plot = sns.countplot(data=df, x='year', hue=selected_column, palette='pastel', ax=ax)

    # Configure titles and labels
    ax.set_title(f'Distribución de {selected_column} por Año', fontsize=16)
    ax.set_xlabel('Año', fontsize=14)
    ax.set_ylabel('Número de Registros', fontsize=14)

    # Axis limits
    ax.set_ylim(bottom=0)

    # Legend
    ax.legend(title=f'Categoría de {selected_column}', loc='upper right', fontsize='small', bbox_to_anchor=(1, 1))

    # Grid
    ax.grid(True, axis='y', linestyle='--')
    
    # Add data labels on each bar
    for p in count_plot.patches:
        count_plot.annotate(f'{int(p.get_height())}', 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='center', 
                            xytext=(0, 9), 
                            textcoords='offset points')

    # Design adjustment
    plt.tight_layout()

    # Show the graph in Streamlit
    st.pyplot(fig)


def plot_heatmap(df, selected_column, selected_column_2):
    # Chart style
    plt.style.use('bmh')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

    # First heatmap with percentages
    df_ct = pd.crosstab(df[selected_column], df[selected_column_2], normalize='all') * 100
    sns.heatmap(df_ct, annot=True, cmap='Blues', fmt='.2f', linewidths=0.5, 
                cbar_kws={'label': 'Porcentaje (%)'}, ax=ax1)

    # Titles and labels of the first heatmap
    ax1.set_title(f'Relación en Porcentajes de {selected_column} y {selected_column_2}', fontsize=16)
    ax1.set_xlabel(f'{selected_column_2}', fontsize=12)
    ax1.set_ylabel(f'{selected_column}', fontsize=12)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    
    # Second heatmap with absolute values
    df_ct_2 = pd.crosstab(df[selected_column], df[selected_column_2])
    sns.heatmap(df_ct_2, annot=True, cmap='Blues', fmt='g', ax=ax2)

    # Titles and labels of the second heatmap
    ax2.set_title(f'Relación Absoluta de {selected_column} y {selected_column_2}', fontsize=16)
    ax2.set_xlabel(f'{selected_column_2}', fontsize=12)
    ax2.set_ylabel(f'{selected_column}', fontsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=10)

    # Design adjustment
    plt.tight_layout(pad=5.0)  # Space between heatmaps

    # Show the graph in Streamlit
    st.pyplot(fig)