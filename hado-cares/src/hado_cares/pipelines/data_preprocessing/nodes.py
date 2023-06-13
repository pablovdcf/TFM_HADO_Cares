"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.7
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler

def clean_and_preprocess_data(hospital_data: pd.DataFrame) -> pd.DataFrame:
    # Tratar los valores faltantes
    # (Aquí puedes usar el mismo código que te mostré antes)
    
    # Convertir los datos categóricos a un formato numérico
    # (Aquí puedes usar el mismo código que te mostré antes)

    # Normalizar o estandarizar las variables numéricas
    # (Aquí puedes usar el mismo código que te mostré antes)

    # Verificar si hay errores en los datos y corregirlos
    # (Realizarás esto en el paso de EDA)

    # Comprobar si hay duplicados y decidir cómo tratarlos
    hospital_data.drop_duplicates(inplace=True)
    
    return hospital_data