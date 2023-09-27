# Functions for generating interactive maps

# Modules and libraries
import streamlit as st
import streamlit.components.v1 as components
import folium
import folium.plugins

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
    
    # Filtrar los datos por año y agrupar por 'ayuntamiento' para obtener métricas
    data_year = data[data['year']==year].groupby('ayuntamiento')[column].agg(['count','mean', 'min', 'max', 'median']).reset_index()
    
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

