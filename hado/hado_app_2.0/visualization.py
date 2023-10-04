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
    sns.countplot(data=df, y=selected_column, order=order, ax=ax, palette='pastel')
    ax.set_title(f'Distribución de {selected_column}', fontsize=16)
    ax.set_ylabel(f'Categorías de {selected_column}', fontsize=14)
    ax.set_xlabel('Número de Pacientes',fontsize=12)
    ax.grid(axis='x', linestyle='--')
     
    # Showing the quantities in each bar
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height()/2.), 
                    ha='left', va='center', fontsize=10, color='black', xytext=(5,0), 
                    textcoords='offset points')
        
    ax.text(0.5, -0.1, f"Este gráfico muestra la distribución total de {selected_column} para todos los años.", ha='center', va='center', transform=ax.transAxes, fontsize=14)
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
    sns.heatmap(classification_group_sorted, annot=True, cmap="YlGnBu", fmt=".5g", cbar_kws={'label': 'Count'})
    
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
    # ax.set_xlabel('Año', fontsize=14)
    ax.set_ylabel('Número de Pacientes', fontsize=14)

    # Axis limits
    ax.set_ylim(bottom=0)

    # Grid
    ax.grid(True, which='both')

    # Annotations for each point
    for x, y in zip(data_to_plot.index, data_to_plot.values):
        ax.text(x, y + 10, str(y), ha='center', va='bottom')

    ax.text(0.5, -0.1, f"Este gráfico muestra el registro de pacientes a lo largo de los años.", ha='center', va='center', transform=ax.transAxes, fontsize=14)
    # Design adjustment
    plt.tight_layout()

    # Show the graph in Streamlit
    st.pyplot(fig)
    
def plot_time_trends(df, selected_column):
    # Chart style
    plt.style.use('bmh')
    
    # Calculate the order of the bars based on the count of the 'selected_column'
    order = sorted(df['year'].unique())
    hue_order = df[selected_column].value_counts().index
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    
    # Bar chart
    count_plot = sns.countplot(data=df, x='year', hue=selected_column, palette='pastel', ax=ax, order=order, hue_order=hue_order)

    # Configure titles and labels
    ax.set_title(f'Distribución de {selected_column} por Año', fontsize=16)
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Número de Registros', fontsize=14)
    
    # Axis limits
    ax.set_ylim(bottom=0)

    # Legend
    ax.legend(title=f'Valores {selected_column}', loc='best', fontsize='small', bbox_to_anchor=(1, 1))

    # Grid
    ax.grid(True, axis='y', linestyle='--')
    
    # Add data labels on each bar
    for p in count_plot.patches:
        count_plot.annotate(f'{int(p.get_height())}', 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='center', 
                            xytext=(0, 9), 
                            textcoords='offset points')
        
    # Add description inside the graphic
    ax.text(0.5, -0.1, f"Este gráfico muestra la distribución de {selected_column} a lo largo de los años.",
            ha='center', va='center', transform=ax.transAxes)
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
    
    st.markdown(f"""
    ##### Este conjunto de mapas de calor visualiza la relación entre *{selected_column}* y *{selected_column_2}*. El primer mapa de calor muestra los porcentajes normalizados de las ocurrencias combinadas de cada par de valores, representando la proporción de todas las observaciones que caen en cada combinación de categorías. Mientras que el segundo mapa de calor muestra la cantidad absoluta de registros para cada combinación de categorías, brindando una perspectiva más directa sobre la distribución real de los datos en el conjunto de datos. Las celdas más oscuras indican una mayor frecuencia o un porcentaje más alto de observaciones, mientras que las celdas más claras indican lo contrario, ayudando a identificar rápidamente las combinaciones de categorías más y menos comunes.
""")
    
def plot_time_trends_line(df, selected_column):
    # Estilo del gráfico
    plt.style.use('bmh')

    # Calcula los conteos por año y por la categoría seleccionada
    count_data = df.groupby(['year', selected_column]).size().reset_index(name='count')

    # Crea el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.lineplot(data=count_data, x='year', y='count', hue=selected_column, palette='pastel', marker="o", ax=ax)

    # Configura los títulos y etiquetas
    ax.set_title(f'Evolución de {selected_column} por Año', fontsize=16)
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Número de Registros', fontsize=14)

    # Límites de los ejes
    ax.set_ylim(bottom=0)

    # Leyenda
    ax.legend(title=f'Valores {selected_column}', loc='best', fontsize='small', bbox_to_anchor=(1, 1))

    # Cuadrícula
    ax.grid(True, axis='y', linestyle='--')

    # Descripción dentro del gráfico
    ax.text(0.5, -0.1, f"Este gráfico muestra la evolución de {selected_column} a lo largo de los años.",
            ha='center', va='center', transform=ax.transAxes)

    # Ajuste del diseño
    plt.tight_layout()

    # Muestra el gráfico en Streamlit
    st.pyplot(fig)
