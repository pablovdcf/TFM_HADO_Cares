# Functions and utility classes

import streamlit as st
# from pycaret.classification import setup, compare_models, pull, save_model

# # Function for Machine Learning
# def machine_learning(df):
#     st.header("Build your own Machine Learning Model with Pycaret!")
#     target = st.selectbox("Select Your Target", df.columns)
#     trained = st.button("Train Model")
#     if trained:
#         with st.spinner("Wait we are training your model"):
#             setup(df, target=target)
#             setup_df = pull()
#             best_model = compare_models()
#             st.info("This is the ML Experiment settings")
#             st.dataframe(setup_df)
#             compare_df = pull()
#             st.info("This is the ML Model")
#             st.dataframe(compare_df)
#             best_model
#             save_model(best_model, 'best_model')
#             with open("best_model.pkl", 'rb') as f:
#                 st.download_button("Download the Model", f, "trained_model.pkl")
#         pass
    
 
def show_sidebar_info(selected_tab):
    # Define los markdowns para cada tab
    
    markdown_home = """
    ### Información del Tab 1
    Aquí va la información y las instrucciones para el primer tab.
    """

    markdown_filtros = """
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

    markdown_visualizaciones = """
    # **Visualizaciones de Datos** 📊
    
    En esta sección, puedes explorar diversas visualizaciones que te ayudarán a entender mejor tus datos.
    
    ## **1. Selección de Año:** 📅
    - **Opción para Todos los Años:** Visualiza los datos acumulativos de todos los años disponibles.
    - **Opción de Año Específico:** Filtra y visualiza los datos para un año seleccionado.
    
    ## **2. Selección de Columna:** 🎛️
    - **Selecciona una Columna:** Escoge una columna del conjunto de datos para la visualización.
    - Las columnas disponibles incluyen categorías, métrico médico y clasificaciones.
    
    ## **3. Relación con Otra Variable:** 🔗
    - **Explora Relaciones:** Selecciona otra columna para explorar su relación con la columna previamente seleccionada.
    - Se muestra un heatmap para visualizar la relación entre las dos variables seleccionadas.
    
    ## **4. Visualizaciones Detalladas:** 🔍
    - **Barthel, PS ECOG, GDS FAST:** Explora visualizaciones detalladas para cada uno de estos índices.
    - **Mostrar/Ocultar Gráficos:** Utiliza los botones para visualizar u ocultar gráficos detallados.
    - Cada índice tiene una descripción detallada y características principales para ayudarte a interpretar los resultados.
    
    ## **5. Información Adicional:** ℹ️
    - Las visualizaciones se generan dinámicamente en base a tus selecciones.
    - Utiliza los desplegables y botones para personalizar las visualizaciones según tus necesidades.
    - Explora las diferentes opciones y visualizaciones para obtener insights valiosos de tus datos.
    """
    markdown_mapas = """
    ### Información del Tab 4
    Aquí va la información y las instrucciones para el primer tab.
    """
    markdown_crud = """
    # **Operaciones CRUD para Archivos Excel** 🛠️
    
    En esta sección, puedes realizar operaciones de Crear, Leer, Actualizar y Eliminar (CRUD) en tu archivo Excel.
    
    ## **1. Ver Datos** 👁️
    - Visualiza las primeras filas de tu conjunto de datos.
    - Te permite obtener una vista rápida de los datos cargados.
    
    ## **2. Editar Datos** ✏️
    - **Indica el índice** de la fila que deseas editar.
    - **Selecciona la columna** que deseas modificar.
    - **Introduce el nuevo valor** y haz clic en 'Actualizar'.
    - **Guardar Cambios:** No olvides guardar los cambios realizados.
    
    ## **3. Eliminar Datos** 🗑️
    - Indica el índice de la fila que deseas eliminar.
    - Haz clic en 'Eliminar' para remover la fila seleccionada.
    - Los cambios se reflejarán inmediatamente en los datos.
    
    ## **4. Buscar Datos** 🔍
    - Introduce un término de búsqueda.
    - Selecciona la columna en la que deseas buscar.
    - Haz clic en 'Buscar' para ver los resultados que coincidan.
    
    ## **5. Guardar Cambios** 💾
    - Una vez realizadas las operaciones, haz clic en 'Guardar Cambios'.
    - Los cambios se guardarán en un nuevo archivo CSV llamado 'uploaded_file.csv'.
    
    ## **Nota:** 📝
    - Este CRUD es un ejemplo para demostrar la posibilidad de modificar datos desde Streamlit.
    - Para una gestión de datos más dinámica y efectiva, se recomienda trabajar directamente en el archivo Excel o utilizar una base de datos como MongoDB.
    """
    markdown_ml = """
    ### Información del Tab 6
    Aquí va la información y las instrucciones para el primer tab.
    """
    markdown_pr = """
                        ### 📘 Acerca de la Aplicación

Esta aplicación te permite explorar y analizar conjuntos de datos. Utiliza Pandas Profiling para generar informes detallados que te proporcionan una visión general de la distribución, limpieza y estructura de tus datos.

### 🚀 Cómo Utilizar

1. **Cargar Datos:** Utiliza la opción de carga de archivos para subir tu conjunto de datos en formato CSV.
2. **Generar Informe:** Haz clic en el botón 'Generar Pandas Profiling Report' para crear un informe detallado de tu conjunto de datos.
3. **Explorar Informe:** Navega a través del informe generado para obtener insights valiosos y estadísticas detalladas sobre cada columna de tu conjunto de datos.

### 🔍 Sobre Pandas Profiling

Pandas Profiling es una herramienta de exploración de datos que genera informes de perfiles a partir de un DataFrame pandas. El informe resultante actúa como una descripción general de alta calidad del conjunto de datos y ofrece lo siguiente:

- **Descripción General:** Resumen de las filas, columnas, valores perdidos, tipos de datos y memoria usada.
- **Estadísticas de Variables:** Distribución de valores, estadísticas descriptivas, correlaciones, y valores distintos.
- **Valores Faltantes:** Análisis de los valores nulos o faltantes en el conjunto de datos.
- **Correlaciones:** Matrices de correlación entre variables numéricas.
- **Valores Extremos:** Identificación de posibles outliers en el conjunto de datos.

Esta herramienta es útil tanto para la exploración inicial de datos como para la limpieza y preprocesamiento de datos antes de la modelización.

### 💡 Tips

- Utiliza Pandas Profiling para identificar problemas en tu conjunto de datos rápidamente.
- Explora las correlaciones entre variables para obtener insights sobre relaciones.
- Revisa los valores faltantes y considera estrategias de imputación.
"""

    # Mostrar el markdown correspondiente en el sidebar
    if selected_tab == "Home":
        st.sidebar.markdown(markdown_home)
    elif selected_tab == "Filtros":
        st.sidebar.markdown(markdown_filtros)
    elif selected_tab == "Visualizaciones":
        st.sidebar.markdown(markdown_visualizaciones)
    elif selected_tab == "Mapa":
        st.sidebar.markdown(markdown_mapas)
    elif selected_tab == "CRUD Operations":
        st.sidebar.markdown(markdown_crud)
    elif selected_tab == "ML":
        st.sidebar.markdown(markdown_ml)
    elif selected_tab == "Pandas Profiling":
        st.sidebar.markdown(markdown_pr)
        
        
def ui_spacer(n=2, line=False, next_n=0):
	for _ in range(n):
		st.write('')
	if line:
		st.tabs([' '])
	for _ in range(next_n):
		st.write('')

def ui_info():
	st.markdown(f"""
	# HADO CARES
	""")
	ui_spacer(1)
	st.write("Made by [Pablo Villar del Castillo](https://www.linkedin.com/in/pablovillardelcastillo/).", unsafe_allow_html=True)
	ui_spacer(1)
	st.markdown("""
		Gracias por su interés en mi aplicación.
		Tenga en cuenta que esto es sólo una aplicación de prueba
		y puede contener errores o características sin terminar.
		""")
	ui_spacer(1)
	st.markdown('El código fuente está disponible [aquí](https://github.com/pablovdcf/TFM_HADO_Cares).')