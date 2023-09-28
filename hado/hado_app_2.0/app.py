# Principal file for the Streamlit Aplication

import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import base64
import pandas as pd

import ydata_profiling
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport


from data_processing import sidebar_and_upload,\
                            apply_filters, \
                            crud_operations,\
                            generate_pandas_profiling,\
                            load_gdf
from visualization import plot_classification_heatmap,\
                            plot_selected_category, \
                            plot_heatmap, \
                            plot_time_trends, \
                            plot_total_patients
from interactive_maps import folium_static,\
                            generate_interactive_maps,\
                            plot_patients_by_ayuntamiento,\
                            plot_average_metrics_by_ayuntamiento,\
                            plot_top_ayuntamientos_for_category
                            
from utils import machine_learning



st.set_page_config(page_title="HADO",
                   layout='wide', 
                   initial_sidebar_state = 'auto',
                    page_icon="🏥")

if 'show_filters' not in st.session_state:
    st.session_state.show_filters = True
    

# Main Function
def main():
    
    st.write("# HADO CARES")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Home 🏠", "Filtros 🔍", "Visualizaciones 📊", "Mapa 🗺️", "CRUD Operations ✍️", "ML 🖥️", "Pandas Profiling 📃"
    ])
    try:
        df = None
        df = sidebar_and_upload()
        
    except Exception as e:
        st.sidebar.info("Por favor suba el archivo CSV para inicialzar la aplicación")
        # st.sidebar.write(f"Ocurrió un error: {e}")
        
    if df is not None:
        with tab1:
            st.write("## Datos de muestra")
            st.write(df.head(10))
            st.write(f"El dataset tiene {df.shape[0]} filas y {df.shape[1]} columnas.")
        
        # Apply Filters
        with tab2:
            st.header("Filtrado y Descarga de Datos")
            # Uso de columnas para organizar el contenido
            col1, col2, col3 = st.columns([1, 0.05, 1])
            with col1.expander("Instrucciones para el uso de filtros 🛠️"):
                st.markdown(
    """
    ### **Instrucciones para el uso de filtros:** 🛠️
    
    **1. Filtros por Categoría:** 🏷️
       - **Selecciona** las categorías que deseas incluir en cada filtro desplegable.
       - Puedes seleccionar **múltiples categorías** a la vez. Por ejemplo:
         Puedes filtrar por las categorías de **diagnóstico** y **médico** entre muchos otros.
    
    **2. Año:** 📅
       - **Selecciona** el o los años para los cuales deseas visualizar los datos.
       - Esto te permitirá visualizar datos específicos para cada año seleccionado.
    
    **3. Estado de Pacientes:** 🩺
       - **Filtra** los datos según el estado de los pacientes.
       - Útil para analizar datos según diferentes estados de salud.
    
    **4. Filtros de Visitas y Estancias:** 🏥
       - **Ajusta los rangos** para el número de visitas y estancias que desees filtrar.
       - Esto te permitirá enfocarte en datos que cumplen con ciertos criterios.
    
    **5. Ayuntamiento:** 🏛️
       - **Selecciona** el o los ayuntamientos que deseas filtrar.
       - Puedes seleccionar uno o varios ayuntamientos para analizar.
    
    **6. Reset Filters:** ♻️
       - Si deseas revertir los filtros aplicados, haz clic en este botón.
       - Esto te llevará de nuevo al conjunto de datos original.
    
    **7. Descarga:** 💾
       - Una vez aplicados los filtros, haz clic en 'Descargar CSV' para obtener tus datos.
       - Recibirás un archivo CSV con los datos filtrados.
    """
    )       
            # Filtros y acciones en la segunda columna
            with col3:
                st.write("### Filtros ⬇️")     
                if st.session_state.show_filters:
                    df_filtered = apply_filters(df)

                if st.button("Reset Filters"):
                    
                    # Hides filters and shows the original DataFrame
                    st.session_state.show_filters = False
                    df_filtered = df.copy()

                # Show filters again (this will reset them)
                st.session_state.show_filters = True
            
            with col1:
                st.write("## Datos filtrados")
                
                st.write(f"El dataset tiene {df_filtered.shape[0]} filas y {df_filtered.shape[1]} columnas.")
                
                st.write(df_filtered)
            
            st.write("## Download DataFrame")
            download_button = st.button("Download CSV")
            if download_button:
                csv = df_filtered.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="modified_dataframe.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)
                
        
        # Data Visualizations
        with tab3:
            with st.expander("Información para el uso de Visualizaciones"):
                st.markdown(
    """
    # **Visualizaciones de Datos** 📊
    
    En esta sección, puedes explorar diversas visualizaciones que te ayudarán a entender mejor tus datos.
    
    ## **1. Selección de Año:** 📅
    - **Opción para Todos los Años:** Visualiza los datos acumulativos de todos los años disponibles.
    - **Opción de Año Específico:** Filtra y visualiza los datos para un año seleccionado.
    
    ## **2. Selección de Columna:** 🎛️
    - **Selecciona una Columna:** Escoge una columna del conjunto de datos para la visualización.
    - Las columnas disponibles incluyen categorías, médico y clasificaciones.
    
    ## **3. Relación con Otra Variable:** 🔗
    - **Explora Relaciones:** Selecciona las columnas para explorar su relación y sus valores únicos.
    - Se muestra un heatmap para visualizar la relación entre las dos variables seleccionadas.
    
    ## **4. Visualizaciones Detalladas:** 🔍
    - **Barthel, PS ECOG, GDS FAST:** Explora visualizaciones detalladas para cada uno de estos índices.
    - **Mostrar/Ocultar Gráficos:** Utiliza los botones para visualizar u ocultar gráficos detallados.
    - Cada índice tiene una descripción detallada y características principales para poder interpretar los resultados.
    
    ## **5. Información Adicional:** ℹ️
    - Las visualizaciones se generan dinámicamente en base a tus selecciones.
    - Utiliza los desplegables y botones para personalizar las visualizaciones según tus necesidades.
    - Explora las diferentes opciones y visualizaciones para obtener insights valiosos de tus datos.
    """
)           
            st.divider()
            # Option to select to display by year or by all years
            col1, col2 = st.columns([1,1])
            with col1:
                year_option = st.selectbox("### ¿Quieres visualizar por un año específico o por todos los años?", ["Todos los años", "Año específico"])
            
                # If the user selects "Specific year", we display an additional selector for the user to choose the year
                if year_option == "Año específico":
                    selected_year = st.selectbox("### Seleccione un año:", sorted(df['year'].unique()))
                    df = df[df['year'] == selected_year]  # Filter the DataFrame by the selected year
                
            filtered_columns = [col for col in df.columns if 'category' in col or 'medico' in col or 'classification' in col]
            with col2:
                selected_column = st.selectbox("### Seleccione una columna para visualizar:", filtered_columns)
            
            col1, col2 = st.columns(2)
            with col1:
                if year_option != "Año específico":
                    plot_total_patients(df)
                    st.divider()
                    if selected_column:
                        plot_selected_category(df, selected_column)
                else:
                    if selected_column:
                        plot_selected_category(df, selected_column)
                
            with col2:
                if year_option != "Año específico":
                    if selected_column:
                        plot_time_trends(df, selected_column)
                        st.divider()
            st.divider()
            
            with st.expander('### Relación con Otra Variable'):
                st.info("Seleccione otra columna para explorar la relación con la columna previamente seleccionada.")
                col1, col2 = st.columns([1,1])
                with col1:
                    selected_column1 = st.selectbox("#### Seleccione una columna:", filtered_columns)
                    selected_column2 = st.selectbox("#### Seleccione Otra Columna para observar la relación entre ambas:", filtered_columns)

                if selected_column1 == selected_column2:
                    st.warning("🧐 No pueden ser las mismas columnas. Por favor, escoja otra columna.")
                else:
                    st.write("### Heatmap de Relación")

                    # Obtén los valores únicos de las columnas seleccionadas
                    unique_values_col1 = df[selected_column1].unique()
                    unique_values_col2 = df[selected_column2].unique()
                    
                    with col2:
                        # SelectBoxes para seleccionar valores únicos
                        selected_value_col1 = st.multiselect(f"#### Seleccione un valor único para {selected_column1}:", unique_values_col1)
                        selected_value_col2 = st.multiselect(f"#### Seleccione un valor único para {selected_column2}:", unique_values_col2)

                    # Filtra el DataFrame basado en los valores seleccionados
                    filtered_df = df[(df[selected_column1].isin(selected_value_col1)) & (df[selected_column2].isin(selected_value_col2))]
                    
                    # Verifica si el DataFrame filtrado está vacío
                    if filtered_df.empty:
                        st.warning("Por favor, seleccione al menos un valor de cada columna para visualizar el heatmap.")

                    col1, col2, col3 = st.columns([0.5,2,0.5])
                    with col2:
                        plot_heatmap(filtered_df, selected_column1, selected_column2)
            
            # Create or retrieve status variables for each chart
            if 'show_barthel' not in st.session_state:
                st.session_state.show_barthel = False
            if 'show_ps_ecog' not in st.session_state:
                st.session_state.show_ps_ecog = False
            if 'show_gds_fast' not in st.session_state:
                st.session_state.show_gds_fast = False

            container = st.container()
            col1, col2, col3 = container.columns([0.5, 2, 0.5])
            with col2:
                # Barthel
                barthel_expander = st.expander("### Barthel")
                with barthel_expander:
                    st.markdown("""
                                ### Índice de Barthel

El índice de Barthel evalúa la independencia de una persona para realizar actividades básicas de la vida diaria, asignando un puntaje entre 0 (dependencia total) y 100 (independencia total). Según el puntaje, se clasifica la dependencia como:

- **< 20 puntos:** Total
- **20 - 40 puntos:** Severa
- **40 - 60 puntos:** Moderada
- **60 - 90 puntos:** Leve o mínima
- **90 - 100 puntos:** Independencia

Esta herramienta es útil para valorar la funcionalidad, evolución, pronóstico del paciente y planificar su atención, permitiendo comparar el estado funcional entre pacientes.

""")
                    if st.button("Mostrar/Ocultar Gráfico Barthel"):
                        st.session_state.show_barthel = not st.session_state.show_barthel
                    if st.session_state.show_barthel:
                        plot_classification_heatmap(df, 'barthel_classification', 'barthel')
                
                # PS_ECOG
                ps_ecog_expander = st.expander("### PS_ECOG")
                with ps_ecog_expander:
                    st.markdown("""
                                ### Escala PS ECOG

La escala PS ECOG mide la calidad de vida y capacidad de un paciente oncológico para realizar actividades diarias, clasificándolo en:

- **ECOG 0:** Asintomático, capaz de realizar trabajo y actividades normales.
- **ECOG 1:** Síntomas leves, limitado para trabajos arduos.
- **ECOG 2:** Incapaz de trabajar, en cama menos del 50% del día.
- **ECOG 3:** En cama más de la mitad del día, necesita ayuda para muchas actividades.
- **ECOG 4:** Encamado el 100% del día, necesita ayuda para todas las actividades.
- **ECOG 5:** Fallecido.

Diseñada por el Eastern Cooperative Oncology Group (ECOG) y validada por la OMS, esta escala objetiva la calidad de vida del paciente, influenciando el protocolo terapéutico y el pronóstico de la enfermedad. Es fundamental para valorar la evolución y autonomía del paciente oncológico.


""")
                    if st.button("Mostrar/Ocultar Gráfico PS_ECOG"):
                        st.session_state.show_ps_ecog = not st.session_state.show_ps_ecog
                    if st.session_state.show_ps_ecog:
                        plot_classification_heatmap(df, 'ps_ecog_classification', 'ps_ecog')
                
                # GDS_FAST
                gds_fast_expander = st.expander("### GDS_FAST")
                with gds_fast_expander:
                    st.markdown("""
                                ### Escala GDS-FAST
                                
La escala GDS-FAST mide el grado de deterioro cognitivo y funcional en personas con demencia, especialmente Alzheimer, clasificándolos en 7 estadios (GDS 1-7) que van desde la normalidad hasta el deterioro severo. Cada estadio tiene características y subfases específicas, evaluadas por la Escala de Evaluación Funcional (FAST). La tabla abajo resume los estadios y características principales:

| Estadio | Descripción | Características Principales |
| ------- | ----------- | --------------------------- |
| GDS 1   | Normal | Sin déficit cognitivo o funcional |
| GDS 2   | Déficit Cognitivo Muy Leve | Olvidos menores, sin impacto en actividades diarias |
| GDS 3   | Déficit Cognitivo Leve | Primeros defectos claros, afecta tareas complejas |
| GDS 4   | Déficit Cognitivo Moderado | Afecta tareas económicas y de planificación |
| GDS 5   | Déficit Cognitivo Moderadamente Grave | Necesita asistencia en elección de ropa, desorientación temporal |
| GDS 6   | Déficit Cognitivo Grave | Necesita asistencia total, incontinencia |
| GDS 7   | Déficit Cognitivo Muy Grave | Pérdida de habilidades básicas, incapacidad para hablar o caminar |

Esta escala es fundamental para evaluar la evolución, pronóstico y decidir el tratamiento y cuidados adecuados para pacientes con demencia.

""")
                    if st.button("Mostrar/Ocultar Gráfico GDS_FAST"):
                        st.session_state.show_gds_fast = not st.session_state.show_gds_fast
                    if st.session_state.show_gds_fast:
                        plot_classification_heatmap(df, 'gds_fast_classification', 'gds_fast')

        # Mapa
        with tab4:
            try:
                gdf = None
                gdf = load_gdf()
                
            except Exception as e:
                st.info("Por favor suba el archivo GeoJson para observar el mapa con los municipios")
                # st.error(f"Ocurrió un error: {e}")
            md_expander = st.expander("➕ Información")
            with md_expander:
                st.markdown("""
                           ### Guía de Uso de las Visualizaciones 🌟

¡Bienvenido a la sección de visualizaciones! Aquí podrás explorar diferentes aspectos de los datos a través de gráficos interactivos y mapas. A continuación, te presentamos una guía detallada para ayudarte a navegar y aprovechar al máximo esta sección.

#### 1. Subida del Archivo GeoJson 📤

Antes de empezar a explorar el mapa interactivo, es necesario subir el archivo GeoJson que contiene la información geográfica de los municipios. Encontrarás una opción para cargar este archivo en la parte superior de la sección. Una vez cargado correctamente, podrás visualizar el mapa y explorar los datos geográficos.

💡 **Consejo:** Si no se carga el archivo GeoJson o si ocurre algún error durante la carga, se mostrará una advertencia, y no podrás visualizar el mapa.

---
#### 2. Mapa Interactivo 🗺️

En esta sección, encontrarás un mapa interactivo que muestra información geográfica relevante. Para personalizar tu experiencia y visualizar los datos que te interesan, puedes utilizar los siguientes filtros:

- **Seleccione un Año:** Este filtro te permite visualizar los datos correspondientes a un año específico. La selección de un año afectará todas las visualizaciones de la página.
- **Seleccione la Columna para Visualizar:** Aquí, puedes elegir la métrica que deseas visualizar en el mapa. Las opciones disponibles son: 'barthel', 'gds_fast', 'ps_ecog', 'n_visitas', y 'n_estancias'.

**Visualizaciones Adicionales:**
Además del mapa, encontrarás las siguientes visualizaciones que proporcionan insights adicionales:
- **Número de Pacientes por Ayuntamiento:** Este gráfico de barras te muestra la cantidad de pacientes por cada ayuntamiento para el año seleccionado.
- **Promedios de Métricas Clave por Ayuntamiento:** Aquí podrás ver varios gráficos de barras que representan los promedios de diferentes métricas clave por ayuntamiento.

---
#### 3. Top de Ayuntamientos por Columnas 📊

En la parte inferior de la página, podrás explorar los ayuntamientos que destacan en diferentes categorías. Utiliza los filtros disponibles para personalizar la visualización:

- **Seleccione una Categoría:** Permite elegir una categoría (columna) del conjunto de datos para analizar.
- **Seleccione Valores de Categoría:** Después de seleccionar una categoría, podrás filtrar por valores específicos dentro de ella.
- **Seleccione Ayuntamientos:** Este filtro te da la opción de seleccionar uno o varios ayuntamientos para incluir en la visualización.
- **Seleccione un Tipo de Gráfico:** Aquí, puedes decidir el formato en el que deseas visualizar los datos, pudiendo elegir entre 'Gráfico de barras' y 'Gráfico de puntos'.

💡 **Consejo:** Solo podrás seleccionar categorías que tengan 15 o menos valores únicos.
                            """)
            container = st.container()
            col1, col2, col3 = container.columns([0.5, 2, 0.5])
            if gdf is not None:
                with col1:
                    st.write("### Filtros para el mapa")
                    st.info("La selección del año afecta a todas las visualizaciones de esta página")
                        
                    selected_year = st.selectbox("Seleccione un año:", sorted(df['year'].unique()))
                        
                    column = st.selectbox("Seleccione la columna para visualizar:", ['barthel', 'gds_fast', 'ps_ecog', 'n_visitas', 'n_estancias'])
                
                with col2: 
                    map_object = generate_interactive_maps(df, column, gdf, selected_year)

                    if isinstance(map_object, str):
                        st.error(map_object)
                    else:
                        folium_static(map_object)
                        
            else:
                st.warning("No se pudo cargar el archivo GeoJson o el archivo no existe.")
            
            st.write("")
            with col2: 
                df_filtered = df[df['year'] == selected_year]
                plot_patients_by_ayuntamiento(df_filtered, selected_year)

                st.divider()
                plot_average_metrics_by_ayuntamiento(df, selected_year)
                st.info("No se tienen en cuenta ayuntamientos desconocidos para el calculo de los promedios")

                st.divider()
                
                
                st.markdown("""
                            ## Top de Ayuntamientos por columnas
                            """)
                selected_plot_type = st.selectbox("Seleccione un tipo de gráfico:", ['Gráfico de barras', 'Gráfico de puntos'])
                container = st.container()
                col1, col2 = container.columns([1, 1])
                # Columna 1
                with col1:
                    # Lista de columnas categóricas con 15 o menos valores únicos
                    categorical_columns = [col for col in df.select_dtypes(include='object').columns if df[col].nunique() <= 15]
                    
                    # Crear un selector para estas columnas
                    selected_category = st.selectbox("Seleccione una categoría:", categorical_columns)
                    
                    # Obtener los valores únicos de la columna de categoría seleccionada y crear un selector para estos valores
                    unique_category_values = sorted(df[selected_category].unique().tolist())
                    selected_category_values = st.multiselect(f"Seleccione valores de {selected_category}:", unique_category_values, default=unique_category_values)

                # Columna 2
                with col2:
                    # Obtener la lista de ayuntamientos únicos y crear un selector para estos ayuntamientos
                    unique_ayuntamientos = sorted(df['ayuntamiento'].unique().tolist())
                    selected_ayuntamientos = st.multiselect("Seleccione ayuntamientos:", unique_ayuntamientos, default=unique_ayuntamientos)
                    

                plot_top_ayuntamientos_for_category(df, selected_year,selected_ayuntamientos, selected_category, selected_category_values, selected_plot_type)
                
                
                
        # CRUD Operations
        with tab5:
            crud_operations(df)
        
        # Machine Learning
        with tab6:
            
            machine_learning(df)
        
        # Pandas Profiling
        with tab7:
            st.header("**Pandas Profiling Report**")
            pandas_pr_expander = st.expander("### ➕ Información")
            with pandas_pr_expander:
                st.markdown("""
                        ### 📘 Acerca de la Aplicación

Esta aplicación te permite explorar y analizar conjuntos de datos. Utiliza Pandas Profiling para generar informes detallados que te proporcionan una visión general de la distribución, limpieza y estructura de tus datos.

### 🚀 Cómo Utilizar

1. **Cargar Datos:** Utiliza la opción de carga de archivos para subir tu conjunto de datos en formato CSV.
2. **Generar Informe:** Haz clic en el botón 'Generar Pandas Profiling Report' para crear un informe detallado de tu conjunto de datos.
3. **Explorar Informe:** Navega a través del informe generado para obtener insights valiosos y estadísticas detalladas sobre cada columna de tu conjunto de datos.

---
### 🔍 Sobre Pandas Profiling

Pandas Profiling es una herramienta de exploración de datos que genera informes de perfiles a partir de un DataFrame pandas. El informe resultante actúa como una descripción general de alta calidad del conjunto de datos y ofrece lo siguiente:

- **Descripción General:** Resumen de las filas, columnas, valores perdidos, tipos de datos y memoria usada.
- **Estadísticas de Variables:** Distribución de valores, estadísticas descriptivas, correlaciones, y valores distintos.
- **Valores Faltantes:** Análisis de los valores nulos o faltantes en el conjunto de datos.
- **Correlaciones:** Matrices de correlación entre variables numéricas.
- **Valores Extremos:** Identificación de posibles outliers en el conjunto de datos.

Esta herramienta es útil tanto para la exploración inicial de datos como para la limpieza y preprocesamiento de datos antes de la modelización.

---
### 💡 Tips

- Utiliza Pandas Profiling para identificar problemas en tu conjunto de datos rápidamente.
- Explora las correlaciones entre variables para obtener insights sobre relaciones.
- Revisa los valores faltantes y considera estrategias de imputación.

---
    """)        
            container = st.container()
            col1, col2, col3 = container.columns([0.5, 2, 0.5])
            with col1:
                st.info("Sube un archivo al sidebar que quieras explorar, dale al botón 👇 y espera a que se haga la magia 🪄")
                if st.button('Generar Pandas Profiling Report'):
                    report = generate_pandas_profiling(df)
                    with col2:
                        st_profile_report(report)

if __name__ == "__main__":
    main()