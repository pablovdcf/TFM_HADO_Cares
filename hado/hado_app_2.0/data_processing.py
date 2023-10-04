# Functions for data processing and data load

# Modules and libraries
import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import geopandas as gpd


# Load CSV file
def load_csv(input_csv):
    df = pd.read_csv(input_csv)
    with st.expander('Ver datos'):
        st.write(f"{input_csv.name} tiene {df.shape[0]} filas y {df.shape[1]} columnas.")
        st.write(df)
        st.write("Resumen de los datos:")
        st.write(df.describe(include='all').T, )
        
    return df

# Function for sidebar and file upload
@st.cache_data(experimental_allow_widgets=True)
def sidebar_and_upload(csv_file):
    """
    The function reads the uploaded file into a pandas DataFrame.
    If no file is uploaded, a message is displayed on the Streamlit app.

    The function leverages Streamlit's caching mechanism to avoid reloading 
    the file upon every interaction, which is controlled by the 
    `@st.cache_data(experimental_allow_widgets=True)` decorator.

    Returns:
        pd.DataFrame: The DataFrame created from the uploaded CSV file. 
                      If no file is uploaded, the function will return None.
    """
    
    # Check if a file has been uploaded
    if csv_file:
        container = st.container()
        col1, col2, col3 = container.columns([0.5, 2, 0.5])
        with col2:
        # Notify the user that the file has been uploaded
            st.info("Archivo subido con éxito 😊")
        # Read the uploaded file into a pandas DataFrame
        df_original = load_csv(csv_file)
        df = df_original.copy()
    
    # Return the DataFrame
    return df

# Function for Data Filters    
def apply_filters(df, reset=False):
    
    if reset:
        return df.copy()
    
    filters = {}
    
    # Filters for categorical columns
    filtered_columns = [col for col in df.columns if 'category' in col or 'medico' in col]
    df_cat = df[filtered_columns]

    # col1, col2, col3 = st.columns([5,0.5,5])
    
    
# with col1:
    with st.expander("### Año"):
        selected_year = st.multiselect("Seleccione un año:", sorted(df['year'].unique()))
        if selected_year:
            df = df[df['year'].isin(selected_year)]
            
    with st.expander("### Ayuntamiento"):
        selected_council = st.multiselect("Seleccione Ayuntamiento:", sorted(df['ayuntamiento'].unique()))
        if selected_council:
            df = df[df['ayuntamiento'].isin(selected_council)]
    
    with st.expander("### Estado de pacientes"):
        filtered_columns_2 = [col for col in df.columns if 'classif' in col]
        df_cat_2 = df[filtered_columns_2]
        for col in df_cat_2.columns:
            unique_values = df[col].unique().tolist()
            filters[col] = st.multiselect(f"##### {col}", unique_values, default=unique_values)
            if filters[col]:
                df = df[df[col].isin(filters[col])]
                
    with st.expander("### Visitas y Estancias"):
        # Filter for numeric columns
        df_num = df.select_dtypes(exclude='object')
        for col in df_num.columns[:2]:
            min_col, max_col = int(df[col].min()), int(df[col].max())
            if min_col != max_col:
                filters[col] = st.slider(f"##### Rango {col}", min_col, max_col, (min_col, max_col))
                df = df[(df[col] >= filters[col][0]) & (df[col] <= filters[col][1])]

# with col3:
    with st.expander("### Categoría"):
        for col in df_cat.columns:
            unique_values = df[col].unique().tolist()
            filters[col] = st.multiselect(f"##### {col}", unique_values, default=unique_values)
            if filters[col]:
                df = df[df[col].isin(filters[col])]
    return df


# Function for CRUD Operations
@st.cache_data(experimental_allow_widgets=True)
def crud_operations(df, csv_file):
    # CRUD Page
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
    st.write(df)
    
    col1, col2 = st.columns([1, 1])
    # Update Data
    with col1.expander("Editar Datos"):
        row_to_edit = st.number_input("#### Introduzca el índice de la fila que desea editar:", min_value=0, max_value=df.shape[0]-1, value=0, step=1)
        
        if row_to_edit is not None:
            column_to_edit = st.selectbox("#### Seleccione la columna que desea editar:", df.columns.tolist())
            if column_to_edit:
                new_value = st.text_input(f"#### Introduzca el nuevo valor para {column_to_edit} en índice {row_to_edit}:")
        
        if st.button("Actualizar"):
            if row_to_edit is not None and column_to_edit is not None and new_value is not None:
                original_value = df.at[row_to_edit, column_to_edit]
                original_dtype = df[column_to_edit].dtype
                
                try:
                    new_value_casted = original_dtype.type(new_value)
                    df.at[row_to_edit, column_to_edit] = new_value_casted
                    st.success(f"Actualizado para la columna {column_to_edit} con el valor {original_value} modificado por {new_value_casted}")
                    
                    # Guarda los cambios en un archivo CSV
                    df.to_csv(csv_file.name, index=False)
                    
                    # Muestra solo la fila actualizada
                    st.write("Fila actualizada:")
                    st.write(df.loc[[row_to_edit]])
                except ValueError:
                    st.error(f"Entrada no válida. Tipo de datos esperado: {original_dtype}")

    
    # Search Data like Patient Records
    with col2.expander("Search Data"):
        search_column = st.selectbox("Choose the column to search in:", df.columns.tolist())
        search_term = st.text_input("Enter a search term:")
        if st.button("Search"):
            search_results = df[df[search_column].astype(str).str.contains(search_term, case=False)]
            st.write(f"Search results for '{search_term}' in column '{search_column}':")
            st.write(search_results)
            
    # Delete Data
    with col2.expander("Delete Data"):
        row_to_delete = st.number_input("Enter the index of the row you want to delete:", min_value=0, max_value=df.shape[0]-1, value=0, step=1)
        if st.button("Delete"):
            df = df.drop(index=row_to_delete)
            df.reset_index(drop=True, inplace=True)
            st.success(f"Deleted row {row_to_delete}")
            
    # Botón para guardar cambios en un archivo CSV
    if st.button("Save Changes"):
        df.to_csv("uploaded_file.csv", index=False)
        st.success("Changes saved to 'uploaded_file.csv'")
    
    st.info("Este solo es un ejemplo para ver que se pueden introducir datos y modificar datos desde la aplicación de streamlit, aunque sería mejor y más dinámico trabajar en el archivo Excel y subir para ver los insights o desde una BBDD como MongoDb")
    
    return df


@st.cache_data(experimental_allow_widgets=True)
def generate_pandas_profiling(df):
    pr = ProfileReport(df, explorative=True)
    
    return pr

@st.cache_data(experimental_allow_widgets=True)
def load_gdf():
    # Definir la ruta del archivo .geojson
    file_path = "hado_app_2.0/data/ESP_adm4.geojson"
    
    # Cargar los datos geojson
    gdf = gpd.read_file(file_path)
    
    # Limpiar el DataFrame Geo, eliminando las filas donde la geometría es nula
    gdf_clean = gdf[gdf['geometry'].notnull()]
    
    return gdf_clean
