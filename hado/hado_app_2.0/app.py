# Principal file for the Streamlit Aplication
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import base64
import matplotlib
matplotlib.rc('font', family='DejaVu Sans')


from data_processing import sidebar_and_upload,\
                            apply_filters, \
                            crud_operations,\
                            generate_pandas_profiling,\
                            load_gdf
                            
from visualization import plot_classification_heatmap,\
                            plot_selected_category, \
                            plot_heatmap, \
                            plot_time_trends, \
                            plot_total_patients,\
                            plot_time_trends_line
                            
from interactive_maps import folium_static,\
                            generate_interactive_maps,\
                            plot_patients_by_ayuntamiento,\
                            plot_average_metrics_by_ayuntamiento,\
                            plot_top_ayuntamientos_for_category
                            
from utils import machine_learning, ui_info, ui_spacer
import seaborn
import pandas
import streamlit_pandas_profiling
import ydata_profiling
import geopandas
import folium


st.set_page_config(page_title="HADO",
                   layout='wide', 
                   initial_sidebar_state = 'auto',
                    page_icon="🏥")

ss = st.session_state

if 'show_filters' not in ss:
    ss.show_filters = True
    
# Main Function
def main():
    # Set the title and information message in the sidebar
    st.write("# HADO CARES")
    
    with st.sidebar:
        ui_info()
        ui_spacer(2)
    
    # Initialize with None df
    df=None
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Home 🏠", "Filtros 🔍", "Visualizaciones 📊", "Mapa 🗺️", "CRUD Operations ✍️", "Pandas Profiling 📃"
    ])
    with tab1:
        md_expander = st.expander("📃Información", expanded=True)
        with md_expander:
            st.markdown("""
                        # Bienvenido a HADO CARES 🚀

HADO CARES es una aplicación interactiva diseñada para facilitar el análisis y la exploración de datos de atención médica. Esta plataforma ofrece una variedad de herramientas para visualizar, filtrar, y comprender los datos, proporcionando insights valiosos para la toma de decisiones.

## 🏠 Home

En esta sección, puedes cargar tu archivo CSV para empezar a explorar los datos. Una vez cargados los datos, las diversas pestañas en la parte superior te permitirán navegar a través de las diferentes funcionalidades de la aplicación:

- **Filtros 🔍**: Aplica filtros avanzados a los datos para focalizar tus análisis en subconjuntos específicos.
- **Visualizaciones 📊**: Explora visualizaciones detalladas generadas a partir de los datos.
- **Mapa 🗺️**: Investiga distribuciones geográficas y patrones a través de mapas interactivos.
- **CRUD Operations ✍️**: Realiza operaciones de Crear, Leer, Actualizar y Eliminar en los datos.
- **ML 🖥️**: Explora y aplica algoritmos de machine learning a los datos.
- **Pandas Profiling 📃**: Genera informes detallados del análisis exploratorio de los datos.

### ¿Cómo Utilizar HADO CARES?

1. **Cargar Datos**: Utiliza la sección de carga de datos para subir tu archivo CSV. (Justo aquí abajo 👇)
2. **Navegar**: Utiliza las pestañas para explorar las diferentes secciones y funcionalidades de la aplicación.
3. **Interactuar**: Aprovecha los filtros y opciones disponibles en cada sección para personalizar tus análisis y visualizaciones.
4. **Analizar**: Utiliza las visualizaciones y herramientas proporcionadas para obtener insights sobre los datos.

### ¡Empecemos!
Por favor, carga tu archivo CSV para comenzar a explorar y analizar los datos. Si tienes dudas o necesitas ayuda, no dudes en consultar la sección de información en la barra lateral.

_Disfruta explorando e interactuando con los datos en HADO CARES!_
                    
                            """)
        try:
            container = st.container()
            col1, col2, col3 = container.columns([0.5, 2, 0.5])
            with col2:
                # Create a file uploader widget in the sidebar
                uploaded_file = st.file_uploader("Sube tu archivo Excel en formato CSV", type=["csv"], key="csv_file")
            df = sidebar_and_upload(csv_file=uploaded_file)
            
        except Exception as e:
            st.info("Por favor suba el archivo CSV para inicialzar la aplicación")
            # st.sidebar.write(f"Ocurrió un error: {e}")
            
    if df is not None:
        
        # Apply Filters
        with tab2:
            st.header("Filtrado y Descarga de Datos")
            # Uso de columnas para organizar el contenido
            col1, col2, col3 = st.columns([1, 0.05, 1])
            with col1.expander("Instrucciones para el uso de filtros 🛠️", expanded=True):
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
                if ss.show_filters:
                    df_filtered = apply_filters(df)

                if st.button("Reset Filters"):
                    
                    # Hides filters and shows the original DataFrame
                    ss.show_filters = False
                    df_filtered = df.copy()

                # Show filters again (this will reset them)
                ss.show_filters = True
            
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
            df_tab3 = df.copy()
            with st.expander("Información para el uso de Visualizaciones", expanded=True):
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
                    selected_year = st.selectbox("Seleccione un año:", sorted(df_tab3['year'].unique()), index=None, placeholder="Selecciona un año para visualizar los datos")
                    if selected_year != None:
                        df_tab3 = df_tab3[df_tab3['year'] == selected_year]  # Filter the DataFrame by the selected year
            
            # Filter columns by number of unique values in columns    
            filtered_columns = df_tab3.columns[(df_tab3.nunique() >= 2) & (df_tab3.nunique() <= 15)].tolist()
            with col2:
                selected_column = st.selectbox("Seleccione una columna para visualizar:", filtered_columns, index=None, placeholder="Puedes ver los diferentes datos de cada categoría")
            
            col1, col2 = st.columns(2)
            with col1:
                if year_option != "Año específico":
                    plot_total_patients(df_tab3)
                    st.divider()
                    if selected_column:
                        plot_selected_category(df_tab3, selected_column)
                else:
                    if selected_column:
                        plot_selected_category(df_tab3, selected_column)
                
            with col2:
                if year_option != "Año específico":
                    if selected_column:
                        plot_time_trends_line(df_tab3, selected_column)
                        st.divider()
                        plot_time_trends(df_tab3, selected_column)
            st.divider()
            
            with st.expander('Relación con Otra Variable', expanded=True):
                st.info("Seleccione dos columnas distintas para explorar la relación entre ellas.")
                col1, col2 = st.columns([1,1])
                with col1:
                    selected_column1 = st.selectbox("#### Seleccione una columna (eje y):", filtered_columns, index=None, placeholder="Escoge una única opción")
                    selected_column2 = st.selectbox("#### Seleccione una columna (eje x):", filtered_columns, index=None, placeholder="Escoge una única opción")

                if selected_column1 == selected_column2:
                    st.warning("🧐 No pueden ser las mismas columnas. Por favor, escoja otra columna.")
                if selected_column1 != None and selected_column2 !=None and selected_column1 != selected_column2:
                    st.write("### Heatmap de Relación")

                    # Obtén los valores únicos de las columnas seleccionadas
                    unique_values_col1 = df_tab3[selected_column1].unique()
                    unique_values_col2 = df_tab3[selected_column2].unique()
                    
                    with col2:
                        # SelectBoxes para seleccionar valores únicos
                        selected_value_col1 = st.multiselect(
                            f"#### Seleccione un valor único para {selected_column1}:",
                            unique_values_col1,
                            default=unique_values_col1,
                            key=f"unique_select_{selected_column1}"
                            )

                        selected_value_col2 = st.multiselect(
                            f"#### Seleccione un valor único para {selected_column2}:",
                            unique_values_col2,
                            default=unique_values_col2,
                            key=f"second_unique_select_{selected_column2}"
                            )


                    # Filtra el DataFrame basado en los valores seleccionados
                    filtered_df_tab3 = df_tab3[(df_tab3[selected_column1].isin(selected_value_col1)) & (df_tab3[selected_column2].isin(selected_value_col2))]
                    
                    # Verifica si el DataFrame filtrado está vacío
                    if filtered_df_tab3.empty:
                        st.warning("Por favor, seleccione al menos un valor de cada columna para visualizar el heatmap.")

                    col1, col2, col3 = st.columns([0.5,2,0.5])
                    with col2:
                        plot_heatmap(filtered_df_tab3, selected_column1, selected_column2)
            
            # Create or retrieve status variables for each chart
            if 'show_barthel' not in ss:
                ss.show_barthel = False
            if 'show_ps_ecog' not in ss:
                ss.show_ps_ecog = False
            if 'show_gds_fast' not in ss:
                ss.show_gds_fast = False

            container = st.container()
            col1, col2, col3 = container.columns([0.5, 2, 0.5])
            with col2:
                # Barthel
                barthel_expander = st.expander("### Barthel", expanded=True)
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
                    # if st.button("Mostrar/Ocultar Gráfico Barthel"):
                    #     ss.show_barthel = not ss.show_barthel
                    # if ss.show_barthel:
                    plot_classification_heatmap(df_tab3, 'barthel_classification', 'barthel')
                
                # PS_ECOG
                ps_ecog_expander = st.expander("### PS_ECOG", expanded=True)
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
                    # if st.button("Mostrar/Ocultar Gráfico PS_ECOG"):
                    #     ss.show_ps_ecog = not ss.show_ps_ecog
                    # if ss.show_ps_ecog:
                    plot_classification_heatmap(df_tab3, 'ps_ecog_classification', 'ps_ecog')
                
                # GDS_FAST
                gds_fast_expander = st.expander("### GDS_FAST", expanded=True)
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
                    # if st.button("Mostrar/Ocultar Gráfico GDS_FAST"):
                    #     ss.show_gds_fast = not ss.show_gds_fast
                    # if ss.show_gds_fast:
                    plot_classification_heatmap(df_tab3, 'gds_fast_classification', 'gds_fast')

        # Mapa
        with tab4:
            df_tab4 = df.copy()
            md_expander = st.expander("➕ Información", expanded=True)
            with md_expander:
                st.markdown("""
                           ### Guía de Uso de las Visualizaciones 🌟

¡Bienvenido a la sección de visualizaciones! Aquí podrás explorar diferentes aspectos de los datos a través de gráficos interactivos y mapas. A continuación, te presentamos una guía detallada para ayudarte a navegar y aprovechar al máximo esta sección.

#### 1. Mapa Interactivo 🗺️

En esta sección, encontrarás un mapa interactivo que muestra información geográfica relevante. Para personalizar tu experiencia y visualizar los datos que te interesan, puedes utilizar los siguientes filtros:

- **Seleccione un Año:** Este filtro te permite visualizar los datos correspondientes a un año específico. La selección de un año afectará todas las visualizaciones de la página.
- **Seleccione la Columna para Visualizar:** Aquí, puedes elegir la métrica que deseas visualizar en el mapa. Las opciones disponibles son: 'barthel', 'gds_fast', 'ps_ecog', 'n_visitas', y 'n_estancias'.

**Visualizaciones Adicionales:**
Además del mapa, encontrarás las siguientes visualizaciones que proporcionan insights adicionales:
- **Número de Pacientes por Ayuntamiento:** Este gráfico de barras te muestra la cantidad de pacientes por cada ayuntamiento para el año seleccionado.
- **Promedios de Métricas Clave por Ayuntamiento:** Aquí podrás ver varios gráficos de barras que representan los promedios de diferentes métricas clave por ayuntamiento.

---
#### 2. Top de Ayuntamientos por Columnas 📊

En la parte inferior de la página, podrás explorar los ayuntamientos que destacan en diferentes categorías. Utiliza los filtros disponibles para personalizar la visualización:

- **Seleccione una Categoría:** Permite elegir una categoría (columna) del conjunto de datos para analizar.
- **Seleccione Valores de Categoría:** Después de seleccionar una categoría, podrás filtrar por valores específicos dentro de ella.
- **Seleccione Ayuntamientos:** Este filtro te da la opción de seleccionar uno o varios ayuntamientos para incluir en la visualización.
- **Seleccione un Tipo de Gráfico:** Aquí, puedes decidir el formato en el que deseas visualizar los datos, pudiendo elegir entre 'Gráfico de barras' y 'Gráfico de puntos'.

💡 **Consejo:** Solo podrás seleccionar categorías que tengan 15 o menos valores únicos.
                            """)
            gdf = None
            gdf = load_gdf()
            
            container = st.container()
            col1, col2, col3 = container.columns([0.5, 2, 0.5])
            if gdf is not None:
                with col1:
                    st.write("### Filtros 🔍")
                    st.info("La selección del año afecta a todas las visualizaciones de esta página")
                        
                    selected_year = st.selectbox("Seleccione un año:", sorted(df_tab4['year'].unique()),index=None, placeholder="Pulsa para ver los años y seleccionar")
                        
                    column = st.selectbox("Seleccione la columna para visualizar:", ['barthel', 'gds_fast', 'ps_ecog', 'n_visitas', 'n_estancias'], index=None, placeholder="Escoge la columna que deseas visualizar en el mapa")
                
                with col2:
                    if column == None:
                        map_object = None
                        st.info("Selecciona una columna para visualizar el mapa con los ayuntamientos", icon="🚨")
                    else:
                        map_object = generate_interactive_maps(df_tab4, column, gdf, selected_year)

                        if isinstance(map_object, str):
                            st.error(map_object)
                        else:
                            folium_static(map_object)
            
                ui_spacer(1)
                
                with col2:
                    if selected_year != None:    
                        df_filtered_tab4 = df_tab4[df_tab4['year'] == selected_year]
                        plot_patients_by_ayuntamiento(df_filtered_tab4, selected_year)

                        st.divider()
                        plot_average_metrics_by_ayuntamiento(df_tab4, selected_year)
                        st.info("No se tienen en cuenta ayuntamientos desconocidos para el calculo de los promedios")

                        st.divider()
                        
                        
                        st.markdown("""
                                    ## Top de Ayuntamientos por columnas
                                    """)
                        selected_plot_type = st.selectbox("Seleccione un tipo de gráfico:", ['Gráfico de barras', 'Gráfico de puntos'], index=None, placeholder="Elige entre gráfico de barras o de puntos")
                        container = st.container()
                        col1, col2 = container.columns([1, 1])
                        # Columna 1
                        with col1:
                            # Lista de columnas categóricas con 15 o menos valores únicos
                            categorical_columns = [col for col in df_tab4.select_dtypes(include='object').columns if df_tab4[col].nunique() <= 15]
                            
                            # Crear un selector para estas columnas
                            selected_category = st.selectbox("Seleccione una categoría:", categorical_columns, key="category_tab4", index=None, placeholder="¿Qué columna quieres visualizar?")
                            
                            # Obtener los valores únicos de la columna de categoría seleccionada y crear un selector para estos valores
                            if selected_category != None and selected_plot_type != None:
                                unique_category_values = sorted(df_tab4[selected_category].unique().tolist())
                                selected_category_values = st.multiselect(f"Seleccione valores de {selected_category}:", unique_category_values, default=unique_category_values, key="category_values_tab4")
                            else:
                                st.warning("Una vez escojas gráfico y categoría se mostrará la visualización")

                        # Columna 2
                        if selected_category != None and selected_plot_type != None:
                            with col2:
                                # Obtener la lista de ayuntamientos únicos y crear un selector para estos ayuntamientos
                                unique_ayuntamientos = sorted(df_tab4['ayuntamiento'].unique().tolist())
                                selected_ayuntamientos = st.multiselect("Seleccione ayuntamientos:", unique_ayuntamientos, default=unique_ayuntamientos, key="council_tab4")
                                

                            plot_top_ayuntamientos_for_category(df_tab4, selected_year,selected_ayuntamientos, selected_category, selected_category_values, selected_plot_type)
                
            else:
                st.warning("No se pudo cargar el archivo GeoJson o el archivo no existe.")
                
                
                
        # CRUD Operations
        with tab5:
            crud_operations(df,csv_file=uploaded_file)
        
            # Machine Learning
            # with tab7:
    # La parte de Machine learning no está funcionando correctamente, devuelve el resultado en el log para la app en deploy
    # Funciona de manera local por si interesa utilizarse solo habría que descomentar las filas "with tab7" y la función "machine_learning(df)"
    # También crear un nuevo tab7 arriba seguido de "Pandas Profiling 📃" con "ML" por ejemplo y definirlo
            #     machine_learning(df)
        
    # Pandas Profiling
    with tab6:
        st.header("**Pandas Profiling Report**")
        pandas_pr_expander = st.expander("### ➕ Información", expanded=True)
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
        with col2:
            uploaded_file = st.file_uploader("Sube tu archivo Excel en formato CSV", type=["csv"], key="pr_csv_file")
        with col1:
            ui_spacer(2)
            st.info("Sube un archivo en formato CSV que quieras explorar, dale al botón 👇 y espera a que se haga la magia 🪄")
            if st.button('Generar Pandas Profiling Report'):
                report = generate_pandas_profiling(uploaded_file)
                with col2:
                    st_profile_report(report)

if __name__ == "__main__":
    main()