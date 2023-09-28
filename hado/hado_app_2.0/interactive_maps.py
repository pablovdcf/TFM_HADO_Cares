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
    
    
# Function for Data Visualizations
def generate_interactive_maps(data, column, gdf, year):
    """
    Genera mapas interactivos con visualización temporal y datos agregados.
    
    Parámetros:
    - df (DataFrame): DataFrame que contiene los datos a visualizar.
    - column (str): Nombre de la columna en el DataFrame para visualizar en el mapa.
    - gdf (GeoDataFrame): GeoDataFrame que contiene los datos geográficos de Galicia.
    
    Retorna:
    - folium.Map: Objeto del mapa generado.
    """
    # Crear el mapa interactivo con zoom mínimo y máximo
    m = folium.Map(location=[42.7550000, -8.5000000], zoom_start=9, tiles="cartodb positron", min_zoom=8, max_zoom=11)
    
    # Añadir más estilos de mapas
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    
    # Filtrar los datos por año
    data_year = data[data['year'] == year]
    
    # Verificar si todos los valores de 'ayuntamiento' son 'desconocido' en data_year
    if (data_year['ayuntamiento'] == 'desconocido').all():
        # Retornar un mensaje de error si todos los ayuntamientos son "desconocido"
        return f"No existen datos para ayuntamientos conocidos en el año {year}"
    
    # Agrupar por 'ayuntamiento' para obtener métricas
    data_year = data_year.groupby('ayuntamiento')[column].agg(['count','mean', 'min', 'max', 'median']).reset_index()
    
    # Verificar si data_year está vacío
    if data_year.empty:
        # Retornar un mensaje de error si no hay datos
        return f"No existen datos para este año {year} y esta categoría {column}"
        
    # Fusionar con el GeoDataFrame de Galicia
    merged_gdf = gdf.merge(data_year, left_on='NAME_4', right_on='ayuntamiento', how='left')
    
    # Choropleth map
    choropleth = folium.Choropleth(
        geo_data=merged_gdf,
        name=f'choropleth_{year}',
        data=merged_gdf,
        columns=['NAME_4', 'mean'],
        key_on='feature.properties.NAME_4',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Distribución de {column} en {year}'
    ).add_to(m)
    
    # Función para agregar popups
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['NAME_4', 'count', 'mean', 'min', 'max', 'median'], 
                                        aliases=['Municipio:', 'Total de pacientes:', f'Media de {column}:', f'Mínimo de {column}:', f'Máximo de {column}:', f'Mediana de {column}:'], 
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


def plot_patients_by_ayuntamiento(df_filtered, selected_year):
    # Estilo del gráfico
    plt.style.use('bmh')
    
    # Contar el número de pacientes por ayuntamiento
    cases_by_ayuntamiento = df_filtered['ayuntamiento'].value_counts().reset_index()
    cases_by_ayuntamiento.columns = ['Ayuntamiento', 'Número de Pacientes']
    
    # Permitir a los usuarios seleccionar ayuntamientos
    ayuntamientos_options = sorted(cases_by_ayuntamiento['Ayuntamiento'].tolist())
    selected_ayuntamientos = st.multiselect("Seleccione Ayuntamientos:", ayuntamientos_options, default=ayuntamientos_options)
    
    # Filtrar los datos por los ayuntamientos seleccionados
    cases_by_ayuntamiento = cases_by_ayuntamiento[cases_by_ayuntamiento['Ayuntamiento'].isin(selected_ayuntamientos)]
    
    # Verificar si todos los valores de 'ayuntamiento' son 'desconocido' en data_year
    if (df_filtered['ayuntamiento'] == 'desconocido').all():
        # Retornar un mensaje de error si todos los ayuntamientos son "desconocido"
        return f"No existen datos para ayuntamientos conocidos en el año {selected_year}"
    
    # Crear la figura y los ejes
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    
    # Datos a ser graficados
    sns.barplot(x='Número de Pacientes', y='Ayuntamiento', data=cases_by_ayuntamiento, palette="viridis", ax=ax)
    
    # Añadir etiquetas a las barras
    for index, value in enumerate(cases_by_ayuntamiento['Número de Pacientes']):
        ax.text(value, index, f'{value}', color='black', ha="left", va="center")
    
    # Configurar títulos y etiquetas
    ax.set_title(f'Número de Pacientes por ayuntamiento en {selected_year}', fontsize=16)
    ax.set_xlabel('Pacientes', fontsize=14)
    ax.set_ylabel('Ayuntamiento', fontsize=14)
    
    # Límites de los ejes
    ax.set_xlim(left=0)
    
    # Cuadrícula
    ax.grid(True, which='both')
    
    # Ajuste del diseño
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    
def plot_average_metrics_by_ayuntamiento(df, selected_year):
    # Filtrar el DataFrame por el año seleccionado
    df_filtered = df[df['year'] == selected_year]

    # Verificar si df_filtered está vacío
    if df_filtered.empty:
        st.warning(f"No hay datos disponibles para el año {selected_year}.")
        return

    # Calcular los promedios de métricas por ayuntamiento
    average_metrics_by_ayuntamiento = df_filtered.groupby('ayuntamiento').mean().reset_index()

    # Eliminar 'desconocido' de los ayuntamientos para una mejor visualización
    average_metrics_by_ayuntamiento = average_metrics_by_ayuntamiento[average_metrics_by_ayuntamiento['ayuntamiento'] != 'desconocido']

    # Ordenar los datos por cada métrica
    metrics = ['n_estancias', 'n_visitas', 'barthel', 'ps_ecog', 'gds_fast']
    sorted_data = {metric: average_metrics_by_ayuntamiento.sort_values(metric, ascending=False) for metric in metrics}

    # Crear subgráficos con un estilo mejorado
    plt.style.use('bmh')
    fig, axes = plt.subplots(3, 2, figsize=(12, 18))
    fig.suptitle(f'Promedios de Métricas Clave por Ayuntamiento en {selected_year}', fontsize=20)

    # Dibujar cada métrica y agregar etiquetas a las barras
    titles = ['Promedio de Número de Estancias', 'Promedio de Número de Visitas',  'Promedio de Barthel', 'Promedio de PS ECOG', 'Promedio de GDS FAST']
    for ax, metric, title in zip(axes.flatten()[:5], metrics, titles):
        if sorted_data[metric].empty:
            # Si los datos están vacíos, mostrar un mensaje de advertencia en el subgráfico correspondiente
            ax.text(0.5, 0.5, f"No hay datos disponibles para {title.lower()} en {selected_year}", ha='center', va='center', fontsize=12, color='red')
            ax.axis('off')  # Desactivar los ejes
        else:
            sns.barplot(x=metric, y='ayuntamiento', data=sorted_data[metric], ax=ax, palette="viridis")
            ax.set_title(title)
            # Añadir etiquetas a las barras
            for p in ax.patches:
                width = p.get_width()
                ax.text(width + 0.1, p.get_y() + p.get_height() / 2, f'{width:.2f}', ha='left', va='center')

    # Eliminar el eje adicional que no se utiliza
    fig.delaxes(axes.flatten()[5])

    # Ajuste del diseño
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


def plot_top_ayuntamientos_for_category(df, selected_year, selected_ayuntamientos, category_column, selected_category_values, plot_type='bar'):
    # Filtrar el DataFrame por el año seleccionado y los ayuntamientos seleccionados
    df_filtered = df[(df['year'] == selected_year) & (df['ayuntamiento'].isin(selected_ayuntamientos))]
    
    # Verificar si df_filtered está vacío
    if df_filtered.empty:
        st.warning(f"No hay datos disponibles para el año {selected_year} y los ayuntamientos seleccionados.")
        return
    
    # Filtrar el DataFrame por los valores seleccionados de la columna de categoría
    df_filtered = df_filtered[df_filtered[category_column].isin(selected_category_values)]
    
    # Agrupar por la columna de categoría y ayuntamiento y contar el número de casos
    category_by_ayuntamiento = df_filtered.groupby([category_column, 'ayuntamiento']).size().reset_index(name='count')
    
    # Ordenar y obtener los top 10 ayuntamientos por número de casos para cada categoría
    top_category_by_ayuntamiento = category_by_ayuntamiento.sort_values(['count'], ascending=False).groupby(category_column).head(10)
    
    # Establecer el estilo de la gráfica
    plt.style.use('bmh')
    
    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Dibujar la gráfica seleccionada
    if plot_type == 'Gráfico de barras':
        sns.barplot(x='ayuntamiento', y='count', hue=category_column, data=top_category_by_ayuntamiento, ax=ax)
    elif plot_type == 'Gráfico de puntos':
        sns.stripplot(x='ayuntamiento', y='count', hue=category_column, data=top_category_by_ayuntamiento, ax=ax, size=10, jitter=True)
    
    # Configurar títulos y etiquetas
    ax.set_title(f'Top Ayuntamientos por {category_column.capitalize()} en {selected_year}', fontsize=16)
    ax.set_xlabel('Número de Casos', fontsize=14)
    ax.set_ylabel('Ayuntamiento', fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    # Ajuste del diseño
    plt.tight_layout()
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    st.info("El número máximo de ayuntamientos a mostrar en la gráfica son 🔟")
