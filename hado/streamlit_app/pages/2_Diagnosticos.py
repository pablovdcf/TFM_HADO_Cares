from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
import streamlit as st
import plotly.express as px


project_path = r"C:/Users/Pablo Villar/Desktop/CURSOS/KSchool/Máster en Data Science/TFM/nuevo_entorno_kedro/hado"
bootstrap_project(project_path)

with KedroSession.create("hado", project_path) as session:
    context = session.load_context() 

# cargar los datos
df = context.catalog.load("hado_cleaned")

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Hospital Dashboard",
    page_icon="🏥",
    layout="wide",
)

# Título de la página
st.title("Análisis de diagnósticos")

# Descripción de la página
st.write(
    """
    Este panel de control permite al personal del hospital obtener información en tiempo real sobre los pacientes y sus diagnósticos. 
    Aquí puedes visualizar los datos, filtrarlos y realizar análisis.
    """
)

# Mostrar los datos en un dataframe
diagnostic_counts = df['diagnostico'].value_counts()
st.write(diagnostic_counts)


# Descripción de la página
st.write("""
    Seleccione un diagnóstico y una columna para visualizar.
""")

# Cargando los datos (aquí deberías cargar tus datos)
df = context.catalog.load("hado_cleaned")

# Creando los selectores de diagnóstico y columna
selected_diagnosis = st.selectbox("Seleccione un diagnóstico", options=df['diagnostico'].unique())
selected_column = st.selectbox("Seleccione una columna", options=df.columns)

# Filtrando el dataframe por diagnóstico
filtered_df = df[df.diagnostico == selected_diagnosis]

# Ordenando los valores del histograma y tomando solo los 10 más comunes
filtered_df = filtered_df[selected_column].value_counts().sort_values(ascending=False).reset_index()

# Creando la figura
fig = px.histogram(filtered_df, x='index', y=selected_column,
                   title=f"Frecuencia de {selected_column} para {selected_diagnosis}")

# Mostrando la figura
st.plotly_chart(fig)

