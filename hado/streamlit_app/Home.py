# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title('Uber pickups in NYC')

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache_data)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)

from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


project_path = r"C:/Users/Pablo Villar/Desktop/CURSOS/KSchool/Máster en Data Science/TFM/nuevo_entorno_kedro/hado"
bootstrap_project(project_path)

with KedroSession.create("hado", project_path) as session:
    context = session.load_context() 

# cargar los datos
df = context.catalog.load("hado_cleaned")

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Hospital Dashboard",
    page_icon="🏥",  # puedes usar cualquier emoji que prefieras
    layout="wide",
)

# Título de la página
st.title("Bienvenidos al Panel de Control del Hospital")

# Descripción de la página
st.write(
    """
    Este panel de control permite al personal del hospital obtener información en tiempo real sobre los pacientes y sus diagnósticos. 
    Aquí puedes visualizar los datos, filtrarlos y realizar análisis.
    """
)

st.subheader("Datos de los pacientes")
st.write(df)

# Aquí puedes añadir más visualizaciones, filtros y análisis según tus necesidades

