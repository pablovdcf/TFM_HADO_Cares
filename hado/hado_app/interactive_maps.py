# Functions for generating interactive maps

# Modules and libraries
import streamlit as st
import streamlit.components.v1 as components
import folium
import folium.plugins
import matplotlib.pyplot as plt
import seaborn as sns

# The folium_static function is a function to display Folium maps in Streamlit.
def folium_static(m):
    """
    Render a folium map as a Streamlit component.
    
    Args:
    m (folium.Map): A folium map instance to display.
    
    """
    m.save("tmp_map.html")
    components.html(open("tmp_map.html", "r").read(), height=600)

@st.spinner("🧑‍💻Estamos cargando el mapa, por favor espera...")
def generate_interactive_maps(data, column, gdf, year, selected_value=None):
    """
    Generate an interactive map based on specified parameters.
    
    Args:
    data (pd.DataFrame): The data frame containing the data.
    column (str): The column based on which the data will be filtered.
    gdf (GeoDataFrame): The geospatial data frame containing the geometry of the locations.
    year (int): The year based on which the data will be filtered.
    selected_value (str, optional): The selected value based on which the data will be filtered.
    
    Returns:
    folium.Map: An interactive map generated based on specified parameters.
    """
    # Create interactive map with minimum and maximum zoom
    m = folium.Map(location=[42.7550000, -8.5000000], zoom_start=9, tiles="cartodb positron", min_zoom=8, max_zoom=11)
    
    # Map styles
    folium.TileLayer('openstreetmap').add_to(m)

    # Filters by year
    data_year = data[data['year'] == year]

    # Check if all values of 'ayuntamiento' are 'desconocido' in data_year
    if (data_year['ayuntamiento'] == 'desconocido').all():
        # Error message if 'ayuntamiento' are "desconocido"
        return f"No existen datos para ayuntamientos conocidos en el año {year}"
    
    if data[column].dtype in ['int64', 'float64']:  # Si la columna es numérica
        data_year = data_year.groupby('ayuntamiento')[column].agg(['count','mean', 'min', 'max', 'median']).reset_index()
        # Verificar si data_year está vacío
        if data_year.empty:
            # Error message if no data
            return f"No existen datos para este año {year} y esta categoría {column}"
        # Merge GeoDataFrame of Galicia
        merged_gdf_num = gdf.merge(data_year, left_on='NAME_4', right_on='ayuntamiento', how='left')
    
        # In the choropleth map, you can use any column of count_data_pivot
        
        choropleth = folium.Choropleth(
            geo_data=merged_gdf_num,
            name=f'choropleth_{year}',
            data=merged_gdf_num,
            columns=['NAME_4', 'mean'],
            key_on='feature.properties.NAME_4',
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'Distribución de {column} en {year}'
        ).add_to(m)
    
        # Function to add popups
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(fields=['NAME_4', 'count', 'mean', 'min', 'max', 'median'], 
                                            aliases=['Municipio:', 'Total de pacientes:', f'Media de {column}:', f'Mínimo de {column}:', f'Máximo de {column}:', f'Mediana de {column}:'], 
                                            localize=True)
                                    )
    else:  # If the column is not numeric
        if selected_value is not None:
            # Filters the data to include only the selected value
            data_year = data_year[data_year[column] == selected_value]

        # Group by 'city hall' and 'column' to get counts
        count_data = data_year.groupby(['ayuntamiento', column]).size().reset_index(name='count')

        # Reorganize the DataFrame to have a more user-friendly layout
        count_data_pivot = count_data.pivot(index='ayuntamiento', columns=column, values='count').reset_index().fillna(0)

        # Check if count_data_pivot is empty
        if count_data_pivot.empty:
            # Error message if no data
            return f"No existen datos para este año {year} y esta categoría {column}"
        
        # Merge GeoDataFrame of Galicia
        merged_gdf_cat = gdf.merge(count_data_pivot, left_on='NAME_4', right_on='ayuntamiento', how='left')

        choropleth = folium.Choropleth(
            geo_data=merged_gdf_cat,
            name=f'choropleth_{year}_{selected_value}',
            data=merged_gdf_cat,
            columns=['NAME_4', selected_value],
            key_on='feature.properties.NAME_4',
            fill_color='YlGnBu',
            fill_opacity=0.6,
            line_opacity=0.3,
            legend_name=f'Distribución de {selected_value} en {year}',
            highlight=True,
        ).add_to(m)

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(fields=['NAME_4', selected_value], 
                                            aliases=['Municipio:', f'Total de {selected_value}:'], 
                                            localize=True)
        )

    # Plugins
    folium.plugins.ScrollZoomToggler().add_to(m)
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(m)
    # Añadir control de capas
    folium.LayerControl().add_to(m)
    
    return m

@st.spinner("🧑‍💻Dibujando gráficas, por favor espera...")
def plot_patients_by_ayuntamiento(df_filtered, selected_year):
    """
    Plot the number of patients by municipality for a selected year.
    
    Args:
    df_filtered (pd.DataFrame): The data frame containing the filtered data.
    selected_year (int): The year based on which the data has been filtered.
    """
    plt.style.use('bmh')
    
    # Count the number of patients per municipality
    cases_by_ayuntamiento = df_filtered['ayuntamiento'].value_counts().reset_index()
    cases_by_ayuntamiento.columns = ['Ayuntamiento', 'Número de Pacientes']
    
    # Enable users to select municipalities
    ayuntamientos_options = sorted(cases_by_ayuntamiento['Ayuntamiento'].tolist())
    selected_ayuntamientos = st.multiselect("Seleccione Ayuntamientos:", ayuntamientos_options, default=ayuntamientos_options)
    
    # Filter data by the selected municipalities
    cases_by_ayuntamiento = cases_by_ayuntamiento[cases_by_ayuntamiento['Ayuntamiento'].isin(selected_ayuntamientos)]
    
    # Check if the values of 'ayuntamiento' are 'desconocido' in data_year
    if (df_filtered['ayuntamiento'] == 'desconocido').all():
        # Error message if all values from 'ayuntamiento' are "desconocido"
        return f"No existen datos para ayuntamientos conocidos en el año {selected_year}"
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    
    sns.barplot(x='Número de Pacientes', y='Ayuntamiento', data=cases_by_ayuntamiento, palette="viridis", ax=ax)
    
    # Adding labels to bars
    for index, value in enumerate(cases_by_ayuntamiento['Número de Pacientes']):
        ax.text(value, index, f'{value}', color='black', ha="left", va="center")
    
    ax.set_title(f'Número de Pacientes por ayuntamiento en {selected_year}', fontsize=16)
    ax.set_xlabel('Pacientes', fontsize=14)
    ax.set_ylabel('Ayuntamiento', fontsize=14)
    
    ax.set_xlim(left=0)
    ax.grid(True, which='both')
    
    plt.tight_layout()
    st.pyplot(fig)

@st.spinner("🧑‍💻Dibujando gráficas, por favor espera...")
def plot_average_metrics_by_ayuntamiento(df, selected_year):
    """
    Plot average metrics by municipality for a selected year.
    
    Args:
    df (pd.DataFrame): The data frame containing the data.
    selected_year (int): The year based on which the data will be filtered.
    """

    # Check if df_filtered is empty
    if df.empty:
        st.warning(f"No hay datos disponibles para el año {selected_year}.")
        return

    # Temporarily store the column 'ayuntamiento'
    ayuntamiento_column = df['ayuntamiento'].copy()

    # Exclude categorical columns
    df_filtered = df.select_dtypes(exclude=['object'])

    # Re-add the column 'ayuntamiento'
    df_filtered['ayuntamiento'] = ayuntamiento_column
    
    # Calculate metric averages by 'ayuntamiento'
    average_metrics_by_ayuntamiento = df_filtered.groupby('ayuntamiento').mean().reset_index()

    # Remove 'desconocido' from ayuntamiento for better visualization
    average_metrics_by_ayuntamiento = average_metrics_by_ayuntamiento[average_metrics_by_ayuntamiento['ayuntamiento'] != 'desconocido']

    # Sort data by each metric
    metrics = ['n_estancias', 'n_visitas', 'barthel', 'ps_ecog', 'gds_fast']
    sorted_data = {metric: average_metrics_by_ayuntamiento.sort_values(metric, ascending=False) for metric in metrics}

    # Create subgraphs with improved styling
    plt.style.use('bmh')
    fig, axes = plt.subplots(3, 2, figsize=(12, 18))
    fig.suptitle(f'Promedios de Métricas Clave por Ayuntamiento en {selected_year}', fontsize=20)

    # Metrics to add on labels
    titles = ['Promedio de Número de Estancias', 'Promedio de Número de Visitas',  'Promedio de Barthel', 'Promedio de PS ECOG', 'Promedio de GDS FAST']
    for ax, metric, title in zip(axes.flatten()[:5], metrics, titles):
        if sorted_data[metric].empty:
            # If the data is empty, display a warning message in the corresponding subgraph.
            ax.text(0.5, 0.5, f"No hay datos disponibles para {title.lower()} en {selected_year}", ha='center', va='center', fontsize=12, color='red')
            ax.axis('off')  # Deactivate the axes
        else:
            sns.barplot(x=metric, y='ayuntamiento', data=sorted_data[metric], ax=ax, palette="viridis")
            ax.set_title(title)
            # Adding labels to bars
            for p in ax.patches:
                width = p.get_width()
                ax.text(width + 0.1, p.get_y() + p.get_height() / 2, f'{width:.2f}', ha='left', va='center')

    # Remove unused additional shaft
    fig.delaxes(axes.flatten()[5])

    # Design adjustment
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    st.pyplot(fig)

@st.spinner("🧑‍💻Dibujando gráficas, por favor espera...")
def plot_top_ayuntamientos_for_category(df, selected_year, selected_ayuntamientos, category_column, selected_category_values, plot_type='bar'):
    """
    Plot top municipalities for a selected category.
    
    Args:
    df (pd.DataFrame): The data frame containing the data.
    selected_year (int): The year based on which the data will be filtered.
    selected_ayuntamientos (list): The list of selected municipalities.
    category_column (str): The category column based on which the data will be grouped.
    selected_category_values (list): The list of selected category values.
    plot_type (str, optional): The type of plot to be generated ('bar' or 'point'). Defaults to 'bar'.
    """
    plt.style.use('bmh')
    # Filter the DataFrame by the selected 'year' and the selected 'ayuntamiento'.
    df_filtered = df[(df['year'] == selected_year) & (df['ayuntamiento'].isin(selected_ayuntamientos))]
    
    # Check if df_filtered is empty
    if df_filtered.empty:
        st.warning(f"No hay datos disponibles para el año {selected_year} y los ayuntamientos seleccionados.")
        return
    
    # Filter the DataFrame by the selected values of the category column.
    df_filtered = df_filtered[df_filtered[category_column].isin(selected_category_values)]
    
    # Group by category and ayuntamiento column and count the number of cases.
    category_by_ayuntamiento = df_filtered.groupby([category_column, 'ayuntamiento']).size().reset_index(name='count')
    
    # Order and obtain the top 10 municipalities by number of cases for each category.
    top_category_by_ayuntamiento = category_by_ayuntamiento.sort_values(['count'], ascending=False).groupby(category_column).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot the selected graph
    if plot_type == 'Gráfico de barras':
        sns.barplot(x='ayuntamiento', y='count', hue=category_column, data=top_category_by_ayuntamiento, ax=ax)
    elif plot_type == 'Gráfico de puntos':
        sns.stripplot(x='ayuntamiento', y='count', hue=category_column, data=top_category_by_ayuntamiento, ax=ax, size=10, jitter=True)
    
    ax.set_title(f'Top Ayuntamientos por {category_column.capitalize()} en {selected_year}', fontsize=16)
    ax.set_xlabel('Número de Casos', fontsize=14)
    ax.set_ylabel('Ayuntamiento', fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)
    st.info("El número máximo de ayuntamientos a mostrar en la gráfica son 🔟")
