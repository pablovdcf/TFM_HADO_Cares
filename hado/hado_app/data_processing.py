# Functions for data processing and data load
# Modules and libraries
import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import geopandas as gpd
import requests
from io import StringIO

# Load CSV file
def load_csv_home_expander(input_csv):
    """Load a CSV file and display its contents in a Streamlit app.

    This function reads a CSV file, displays the data along with some basic statistics,
    and explanations of data distribution and centrality measures.

    Parameters:
    input_csv (UploadedFile): The CSV file uploaded via Streamlit's file uploader.

    Returns:
    pd.DataFrame: The DataFrame created from the uploaded CSV file.
    """
    
    df = pd.read_csv(input_csv)
    with st.expander('Ver datos', expanded=True):
        st.write(f"{input_csv.name} tiene {df.shape[0]} filas y {df.shape[1]} columnas.")
        st.write(df)
        container = st.container()
        col1, col2 = container.columns([1, 1])
        with col1:
            
            st.write("Resumen de los datos numéricos:")
            st.write(df.describe(exclude='object').T, )
            st.divider()
            st.write("Resumen de los datos categóricos:")
            st.write(df.describe(include='object').T, )
        with col2:
            st.markdown("""
                        ## Distribución y centralidad de los datos

                        #### Para Datos Numéricos:
                        - **Count**: Número total de elementos no nulos.
                        - **Mean**: La media aritmética de los datos.
                        - **Std**: La desviación estándar, que mide la cantidad de variación o dispersión de un conjunto de valores.
                        - **Min**: El valor mínimo en el conjunto de datos.
                        - **25%**: El primer cuartil o percentil 25.
                        - **50%**: La mediana o percentil 50.
                        - **75%**: El tercer cuartil o percentil 75.
                        - **Max**: El valor máximo en el conjunto de datos.

                        #### Para Datos Categóricos:
                        - **Count**: Número total de elementos no nulos.
                        - **Unique**: Número de categorías únicas.
                        - **Top**: La categoría más común.
                        - **Freq**: La frecuencia de la categoría más común.

                        #### Intercuartiles Explicados:
                        - **25%** (Primer Cuartil): El valor por debajo del cual se encuentra el 25% de los datos.
                        - **50%** (Mediana): El valor medio que separa la mitad superior de la mitad inferior de los datos.
                        - **75%** (Tercer Cuartil): El valor por debajo del cual se encuentra el 75% de los datos.

                        Los cuartiles pueden ayudarnos a entender la dispersión de los datos entre diferentes puntos y a identificar posibles outliers o anomalías.

                        ---

                        Estas métricas se utilizan para obtener una visión general rápida de los datos y para entender mejor las tendencias y variaciones dentro del conjunto de datos.

                                                """)
    return df

# Function for sidebar and file upload
@st.cache_data(experimental_allow_widgets=True)
def sidebar_and_upload(csv_file):
    """Handle file upload and display a sidebar in a Streamlit app.

    This function checks if a CSV file has been uploaded, reads it into a pandas DataFrame,
    and displays a success message in a sidebar. The function leverages Streamlit's caching
    mechanism to avoid reloading the file upon every interaction.

    Parameters:
    csv_file (UploadedFile): The CSV file uploaded via Streamlit's file uploader.

    Returns:
    pd.DataFrame: The DataFrame created from the uploaded CSV file, or None if no file is uploaded.
    """

    # Check if a file has been uploaded
    if csv_file:
        container = st.container()
        col1, col2, col3 = container.columns([0.5, 2, 0.5])
        with col2:
        # Notify the user that the file has been uploaded
            st.info("Archivo subido con éxito 😊")
        # Read the uploaded file into a pandas DataFrame
        df_original = load_csv_home_expander(csv_file)
        df = df_original.copy()
    
    # Return the DataFrame
    return df

# Function for Data Filters    
def apply_filters(df, reset=False):
    """
    Apply filters to a DataFrame based on user input in a Streamlit app.

    This function takes a DataFrame and a reset flag as input. It provides interactive filter
    options within a Streamlit app to filter the DataFrame based on various criteria such as
    year, council, patient status, visits, stays, and category. If the reset flag is set to True,
    it returns a copy of the original DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    reset (bool, optional): A flag to reset the filters and return the original DataFrame. Defaults to False.

    Returns:
    pd.DataFrame: The filtered DataFrame based on user-selected criteria.
    """
    if reset:
        return df.copy()
    
    filters = {}
    
    # Filters for categorical columns
    filtered_columns = [col for col in df.columns if 'category' in col or 'medico' in col]
    df_cat = df[filtered_columns]

    with st.expander("Año"):
        selected_year = st.multiselect("Seleccione año:", sorted(df['year'].unique()), default=None, placeholder="Selecciona uno o varios años")
        if selected_year:
            df = df[df['year'].isin(selected_year)]
            
    with st.expander("Ayuntamiento"):
        selected_council = st.multiselect("Seleccione Ayuntamiento:", sorted(df['ayuntamiento'].unique()), default=None, placeholder="Elige el ayuntamiento que quieras filtrar")
        if selected_council:
            df = df[df['ayuntamiento'].isin(selected_council)]
    
    with st.expander("Estado de pacientes"):
        filtered_columns_2 = [col for col in df.columns if 'classif' in col]
        df_cat_2 = df[filtered_columns_2]
        for col in df_cat_2.columns:
            unique_values = df[col].unique().tolist()
            filters[col] = st.multiselect(f"##### {col}", unique_values, default=None, placeholder="Selecciona los valores por los que filtrar")
            if filters[col]:
                df = df[df[col].isin(filters[col])]
                
    with st.expander("Visitas y Estancias"):
        # Filter for numeric columns
        df_num = df.select_dtypes(exclude='object')
        for col in df_num.columns[:2]:
            min_col, max_col = int(df[col].min()), int(df[col].max())
            if min_col != max_col:
                filters[col] = st.slider(f"##### Rango {col}", min_col, max_col, (min_col, max_col))
                df = df[(df[col] >= filters[col][0]) & (df[col] <= filters[col][1])]

    with st.expander("### Categoría"):
        for col in df_cat.columns:
            unique_values = df[col].unique().tolist()
            filters[col] = st.multiselect(f"##### {col}", unique_values, default=unique_values)
            if filters[col]:
                df = df[df[col].isin(filters[col])]
    return df


# Function for CRUD Operations
@st.spinner("Cargando, por favor espera...")
def crud_operations(df, csv_file):
    """
    Perform CRUD (Create, Read, Update, Delete) operations on a DataFrame within a Streamlit app.

    This function provides an interactive interface within a Streamlit app for performing
    CRUD operations on an CSV file. Users can view, edit, delete, search for data,
    and save changes to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to perform CRUD operations on.
    csv_file (UploadedFile): The CSV file uploaded via Streamlit's file uploader.

    Returns:
    pd.DataFrame: The updated DataFrame after performing the desired CRUD operations.
    """
    # Inicializar session_state si no existe
    if 'df' not in st.session_state:
        st.session_state['df'] = df
    
    with st.expander("➕ Información CRUD", expanded=True):
        st.markdown(
    f"""
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
    - Los cambios se guardarán en un nuevo archivo CSV llamado {csv_file.name}.
    
    ## **Nota:** 📝
    - Este CRUD es un ejemplo para demostrar la posibilidad de modificar datos desde Streamlit.
    - Para una gestión de datos más dinámica y efectiva, se recomienda trabajar directamente en el archivo Excel o utilizar una base de datos como MongoDB.
    """
)

    # Read Data
    st.divider()
    st.subheader("Datos")
    st.write(st.session_state['df'])  # mostrar el DataFrame desde session_state
    
    col1, col2 = st.columns([1, 1])
    # Update Data
    with col1.expander("Editar Datos"):
        row_to_edit = st.number_input("#### Introduzca el índice de la fila que desea editar:",
                                      min_value=0, 
                                      max_value=st.session_state['df'].shape[0]-1, 
                                      value=0,
                                      step=1
                                      )
        
        if row_to_edit is not None:
            column_to_edit = st.selectbox("#### Seleccione la columna que desea editar:",  
                                          st.session_state['df'].columns.tolist()
                                          )
            if column_to_edit:
                new_value = st.text_input(f"#### Introduzca el nuevo valor para {column_to_edit} en índice {row_to_edit}:")
        
        if st.button("Actualizar", key="update"):
            if row_to_edit is not None and column_to_edit is not None and new_value is not None:
                original_value = st.session_state['df'].at[row_to_edit, column_to_edit]
                original_dtype = st.session_state['df'][column_to_edit].dtype
                
                try:
                    new_value_casted = original_dtype.type(new_value)
                    st.session_state['df'].at[row_to_edit, column_to_edit] = new_value_casted  # actualizar session_state['df']
                    st.success(f"Actualizado para la columna {column_to_edit} con el valor {original_value} modificado por {new_value_casted}")
                    
                    # Guarda los cambios en un archivo CSV
                    st.session_state['df'].to_csv(csv_file.name, index=False)
                    
                    # Muestra solo la fila actualizada
                    st.write("Fila actualizada:")
                    st.write(st.session_state['df'].loc[[row_to_edit]])
                except ValueError:
                    st.error(f"Entrada no válida. Tipo de datos esperado: {original_dtype}")

    
    # Search Data like Patient Records
    with col2.expander("Buscar datos"):
        search_column = st.selectbox("#### Selecciona la columna sobre la que deseas buscar:", df.columns.tolist(), index=None, placeholder="Escoge una única columna para iniciar la búsqueda")
        search_term = st.text_input("#### Introduzca un término de búsqueda:", placeholder="Escribe el valor que deseas buscar igual que se encuentra en los datos")
        if st.button("Buscar", key="search"):
            search_results = st.session_state['df'][st.session_state['df'][search_column].astype(str).str.contains(search_term, case=False)]
            st.write(f"Resultados de búsqueda para '{search_term}' en la columna '{search_column}':")
            st.write(search_results)
            
    # Delete Data
    with col2.expander("Borrar datos"):
        row_to_delete = st.number_input("#### Introduzca el índice de la fila que desea borrar:", min_value=0, max_value=df.shape[0]-1, value=0, step=1)
        if st.button("Eliminar", key="delete"):
            deleted_row = st.session_state['df'].iloc[[row_to_delete]]
            
            st.session_state['df'] = st.session_state['df'].drop(index=row_to_delete)  # actualizar session_state['df']
            st.session_state['df'].reset_index(drop=True, inplace=True)
            st.success(f"Fila borrada {row_to_delete}")
            st.write(deleted_row)
            
    # Botón para guardar cambios en un archivo CSV
    if st.button("Guardar cambios", key="save_changes"):
        st.session_state['df'].to_csv("uploaded_file.csv", index=False)  # guardar session_state['df'] a un archivo
        st.success("Changes saved to 'uploaded_file.csv'")
    
    st.info("Este solo es un ejemplo para ver que se pueden introducir datos y modificar datos desde la aplicación de streamlit, aunque sería mejor y más dinámico trabajar en el archivo Excel y subir para ver los insights o desde una BBDD como MongoDb")
    
    return st.session_state['df']


@st.cache_data(experimental_allow_widgets=True)
def generate_pandas_profiling(uploaded_file):
    """
    Generate a Pandas Profiling report from an uploaded file.

    This function reads a CSV file into a pandas DataFrame and generates
    a Pandas Profiling report with explorative analysis enabled.

    Parameters:
    uploaded_file (UploadedFile): The CSV file uploaded via Streamlit's file uploader.

    Returns:
    ProfileReport: The generated Pandas Profiling report for the given CSV file.
    """
    df_pr = pd.read_csv(uploaded_file)
    pr = ProfileReport(df_pr, explorative=True)
    
    return pr

@st.cache_data(experimental_allow_widgets=True)
def load_gdf():
    """Load and clean a GeoDataFrame from a remote geojson file.

    This function retrieves a geojson file from a specified URL, reads the file into a GeoDataFrame,
    and filters out rows where the geometry column is null.

    Returns:
    gpd.GeoDataFrame: The cleaned GeoDataFrame containing the geographic data from the specified geojson file.
    """
    # File path to file.geojson
    file_url = 'https://raw.githubusercontent.com/pablovdcf/TFM_HADO_Cares/main/hado/hado_app/data/ESP_adm4.geojson'
    
    # Download the file
    response = requests.get(file_url)
    response.raise_for_status() 
    # Load geojson data
    gdf = gpd.read_file(StringIO(response.text))
    
    # Clean the DataFrame Geo, filtering rows where the geometry it's null
    gdf_clean = gdf[gdf['geometry'].notnull()]
    
    return gdf_clean