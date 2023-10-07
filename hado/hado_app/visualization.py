# Functions for creating graphics and visualizations

# Modules and libraries
import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from sklearn.preprocessing import LabelEncoder
import plotly.express as px


def plot_selected_category(df, selected_column):
    """
    Plots the distribution of a selected categorical column from the dataframe.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    selected_column (str): The column to be plotted.
    
    Returns:
    A bar plot of the selected column's distribution displayed on Streamlit using st.pyplot(fig).
    """
    # Chart style
    plt.style.use('bmh')
    
    # Configuration of the displays
    fig, ax = plt.subplots(figsize=(12, 7))
    order = df[selected_column].value_counts().index
    sns.countplot(data=df, y=selected_column, order=order, ax=ax, palette='pastel')
    ax.set_title(f'Distribución de {selected_column}', fontsize=16)
    ax.set_ylabel(f'Categorías de {selected_column}', fontsize=14)
    ax.set_xlabel('Pacientes',fontsize=12)
    ax.grid(axis='x', linestyle='--')
     
    # Showing the quantities in each bar
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}', (p.get_width(), p.get_y() + p.get_height()/2.), 
                    ha='left', va='center', fontsize=10, color='black', xytext=(5,0), 
                    textcoords='offset points')
        
    ax.text(0.5, -0.1, f"Este gráfico muestra la distribución total de {selected_column} para todos los años.", ha='center', va='center', transform=ax.transAxes, fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)

@st.spinner("Cargando, por favor espera...")
def plot_classification_heatmap(df, classification_column, score_column):
    """
    Plots a heatmap showing the distribution of scores for each classification.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    classification_column (str): The column containing the classifications.
    score_column (str): The column containing the scores.
    
    Returns:
    A heatmap of the score distribution per classification displayed on Streamlit using st.pyplot(fig).
    """
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
    """
    Plots the total number of patients per year.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    
    Returns:
    A line plot showing the total number of patients per year displayed on Streamlit using st.pyplot(fig).
    """
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
    # ax.set_ylim(bottom=0)

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

@st.spinner("Cargando, por favor espera...")
def plot_time_trends(df, selected_column):
    """
    Plots the distribution of a selected categorical column over the years.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    selected_column (str): The column to be plotted.
    
    Returns:
    A bar plot showing the distribution of the selected column over the years displayed on Streamlit using st.pyplot(fig).
    """
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
    # ax.set_ylim(bottom=0)

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
            ha='center', va='center', transform=ax.transAxes, fontsize=14)
    # Design adjustment
    plt.tight_layout()

    # Show the graph in Streamlit
    st.pyplot(fig)

@st.spinner("Cargando, por favor espera...")
def plot_heatmap(df, selected_column, selected_column_2):
    """
    Plots two heatmaps showing the relationship between two selected columns, one in percentages and the other in absolute values.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    selected_column (str): The first column to be plotted.
    selected_column_2 (str): The second column to be plotted.
    
    Returns:
    Two heatmaps showing the relationship between the two selected columns displayed on Streamlit using st.pyplot(fig).
    """
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
    """
    Plots the evolution of a selected categorical column over the years.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    selected_column (str): The column to be plotted.
    
    Returns:
    A line plot showing the evolution of the selected column over the years displayed on Streamlit using st.pyplot(fig).
    """
    # Chart style
    plt.style.use('bmh')

    # Calculates counts by year and by the selected category
    count_data = df.groupby(['year', selected_column]).size().reset_index(name='count')

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.lineplot(data=count_data, x='year', y='count', hue=selected_column, palette='pastel', marker="o", ax=ax)

    ax.set_title(f'Evolución de {selected_column} por Año', fontsize=16)
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Número de Registros', fontsize=14)

    # Axis limits
    # ax.set_ylim(bottom=0)

    # Legend
    ax.legend(title=f'Valores {selected_column}', loc='best', fontsize='small', bbox_to_anchor=(1, 1))

    # Grid
    ax.grid(True, axis='y', linestyle='--')

    # Chart description
    ax.text(0.5, -0.1, f"Este gráfico muestra la evolución de {selected_column} a lo largo de los años.",
            ha='center', va='center', transform=ax.transAxes, fontsize=14)

    plt.tight_layout()
    st.pyplot(fig)
    
def wordcloud_or_hist_box_plot(df, selected_column):
    """
    Generates a word cloud for object type columns or a histogram and a boxplot for numeric columns of type int64.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    selected_column (str): The column to be plotted.
    
    Returns:
    A word cloud or a histogram and a boxplot based on the data type of the selected column displayed on Streamlit using st.pyplot(fig).
    """
    plt.style.use('bmh')
    # Checks the data type of the selected column
    column_dtype = df[selected_column].dtype

    if column_dtype == 'object':
        # Generates a word cloud for object type columns
        text = ' '.join(df[selected_column].astype(str))
        wordcloud = WordCloud(
            background_color='white',
            width=800, 
            height=400, 
            random_state=21, 
            max_font_size=110, 
            colormap='viridis_r'
        ).generate(text)
        
        fig_wordcloud = plt.figure(figsize=(15, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        plt.tight_layout()
        st.pyplot(fig_wordcloud)

    elif column_dtype == 'int64':
        
        # Generates a histogram and a boxplot for numeric columns of type int64
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))
        sns.histplot(data=df, x=selected_column, kde=True, ax=axs[0])
        sns.boxplot(y=df[selected_column], ax=axs[1])

        # Añade una explicación con ax.text
        axs[0].text(0.5, -0.2, f"Histograma de {selected_column} con densidad de Kernel",
                    ha='center', va='center', transform=axs[0].transAxes, fontsize=12)
        axs[1].text(0.5, -0.2, f"Boxplot de {selected_column}",
                    ha='center', va='center', transform=axs[1].transAxes, fontsize=12)
        
        plt.tight_layout()
        st.pyplot(fig)


def plot_bubble_chart(df, x_column, y_column, size_column, color_column=None):
    """
    Plots a bubble chart showing the relationship between three or four variables.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    x_column (str): The column for the x-axis.
    y_column (str): The column for the y-axis.
    size_column (str): The column for the size of the bubbles.
    color_column (str, optional): The column for the color of the bubbles.
    
    Returns:
    A bubble chart showing the relationship between the specified variables displayed on Streamlit using st.pyplot(fig).
    """
    plt.style.use('bmh')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if color_column:
        # If a color column is specified and is categorical, convert to numeric values
        if df[color_column].dtype == 'object':
            le = LabelEncoder()
            color_values = le.fit_transform(df[color_column])
            cmap = 'viridis_r'
        else:
            color_values = df[color_column]
            cmap = None
    else:
        color_values = None
        cmap = None
    
    bubble = ax.scatter(df[x_column], df[y_column], s=df[size_column]*10, c=color_values, cmap=cmap, alpha=0.6, edgecolors="w", linewidth=2)
    
    if color_column:
        # Adds a color bar if a color column is specified
        cbar = plt.colorbar(bubble)
        if df[color_column].dtype == 'object':
            cbar.set_ticks(range(len(le.classes_)))
            cbar.set_ticklabels(le.classes_)
            cbar.set_label(color_column)
            
    ax.set_title(f'Gráfico de Burbujas de {x_column} vs {y_column}')
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    ax.text(0.5, -0.25, f"Este gráfico muestra la relación entre {x_column}, {y_column} y {size_column}.",
            ha='center', va='center', transform=ax.transAxes, fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig)

def plot_animated_bubble_chart(df, x_column, y_column, size_column, color_column=None):
    """
    Plots an animated bubble chart showing the relationship between three or four variables over time.
    
    Parameters:
    df (pd.DataFrame): The data frame containing the data.
    x_column (str): The column for the x-axis.
    y_column (str): The column for the y-axis.
    size_column (str): The column for the size of the bubbles.
    color_column (str, optional): The column for the color of the bubbles.
    
    Returns:
    An animated bubble chart showing the relationship between the specified variables over time displayed on Streamlit using st.plotly_chart(fig).
    """
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        animation_frame='year',  # La columna de años debe llamarse 'year'
        range_x=[df[x_column].min(), df[x_column].max()],
        range_y=[df[y_column].min(), df[y_column].max()],
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        title=f'Animación de Burbujas de {x_column} vs {y_column} a lo largo del tiempo',
        xaxis_title=x_column,
        yaxis_title=y_column,
        template='plotly',
        margin=dict(l=40, r=40, t=40, b=40),
        height=800,
        width=1200  
    )
    
    st.plotly_chart(fig)