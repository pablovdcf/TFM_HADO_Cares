# TFM_HADO_Cares
Analysis of principal diagnoses, trends, treatments with NLP and make one aplication to enter the data and visualize for the hospital


# Información sobre los datos

En los datos de HADO 2022, 2021 y 2020 *(Pendiente de recibir datos anteriores)*

* **Fecha de alta:** Fecha en la que el paciente fue dado de alta del hospital (esta fecha solo existe para la mitad del 2022 y no está en el resto de los datos)
  
* **H. Procedencia:** Hospital o centro médico de donde proviene el paciente.
  
* **Servicio:** Servicio médico en el que fue atendido el paciente.
 
* **AP**: Atención Primaria. Indica si el paciente fue derivado desde Atención Primaria o no.
 
* **Motivo ING:** Motivo de ingreso del paciente en el hospital.
 
* **Diagnóstico Principal:** Diagnóstico principal que se realizó al paciente durante su estancia en el hospital.
 
* **Agudo Estable:** Indica si el paciente presentaba un estado agudo o estable.
 
* **Crónico Agud.:** Indica si el paciente presenta alguna enfermedad crónica con un empeoramiento agudo.
 
* **Paliativo ONC:** Indica si el paciente está recibiendo cuidados paliativos relacionados con una enfermedad oncológica.
 
* **Palt No ONC:** Indica si el paciente está recibiendo cuidados paliativos por una enfermedad no oncológica.
 
* **Trato antibiótico:** Indica si el paciente recibió tratamiento con antibióticos durante su estancia en el hospital.
 
* **Dolor:** Indica si el paciente presentaba dolor durante su estancia en el hospital.
 
* **Delirium:** Indica si el paciente presentaba delirium durante su estancia en el hospital.
 
* **Disnea:** Indica si el paciente presentaba dificultad para respirar durante su estancia en el hospital.
 
* **Ast-Anorx:** Indica si el paciente presenta un diagnóstico de astenia o anorexia. (cansado o tiene hambre)
 
* **Fiebre:** Indica si el paciente presentaba fiebre durante su estancia en el hospital.
 
* **Transfusion:** Indica si el paciente recibió una transfusión sanguínea durante su estancia en el hospital.
 
* **Paracentesis:** Indica si se realizó una paracentesis durante la estancia del paciente en el hospital.
 
* **Toracocentesis:** Indica si se realizó una toracocentesis durante la estancia del paciente en el hospital.
 
* **PS/ECOG:** Escala de evaluación de la calidad de vida y del desempeño de actividades diarias del paciente.
 
* **Barthel:** Indica el grado de dependencia del paciente para realizar actividades de la vida diaria.
 
* **GDS/FAST:** Escala de evaluación de la función cognitiva del paciente.
 
* **Otros/Complicaciones:** Indica cualquier otra complicación médica que haya surgido durante la estancia del paciente en el hospital.
 
* **Agonia:** Indica si el paciente estaba en una fase terminal de la enfermedad y cerca de fallecer.
 
* **Sedación:** Indica si el paciente recibió sedación para manejo de su dolor o ansiedad.
 
* **Motivo Alta:** Indica el motivo por el cual el paciente fue dado de alta del hospital.
 
* **N.º Visitas:** Número de veces que el paciente fue visitado por el personal médico durante su estancia en el hospital.
 
* **N.º estancias:** Número de días que el paciente permaneció en el hospital.
 
* **Ayuntamiento:** Ayuntamiento de residencia del paciente.
 
* **Médico:** Nombre del médico que atendió al paciente durante su estancia en el hospital.

# Pasos a realizar

1. Limpieza y preprocesamiento de datos: Antes de analizar los datos o construir modelos, es crucial asegurarse de que los datos estén limpios y en un formato adecuado. Realiza las siguientes tareas:

  * Comprobar si hay valores faltantes (NaN) y decidir cómo tratarlos (eliminar registros, imputar valores, etc.).
  * Convertir los datos categóricos a un formato numérico (por ejemplo, mediante codificación one-hot o ordinal).
  * Normalizar o estandarizar las variables numéricas si es necesario.
  * Verificar si hay errores en los datos y corregirlos.
  * Comprobar si hay duplicados y decidir cómo tratarlos.

2. Análisis exploratorio de datos (EDA): Una vez que los datos estén limpios, realizar un análisis exploratorio para obtener información sobre las distribuciones, las relaciones entre las variables y las posibles anomalías. Algunas técnicas son:

  * Estadísticas descriptivas (media, mediana, moda, etc.).
  * Gráficos de barras, histogramas, boxplots, etc.
  * Matrices de correlación y mapas de calor.
  * Gráficos de dispersión para analizar relaciones entre variables.

3. Definición de objetivos: Establecer los objetivos del proyecto, por ejemplo:

 * Predecir el tiempo de estancia en el hospital.
 * Identificar los factores que influyen en el motivo de alta.
 * Predecir si un paciente requerirá sedación.
 
4. Selección y entrenamiento de modelos: De acuerdo a los objetivos, seleccionar y entrenar uno o más modelos de aprendizaje automático o estadísticos, como regresión lineal, árboles de decisión, random forest, lightGBM, etc.

5. Evaluación y validación de modelos: Evaluar el rendimiento de los modelos utilizando métricas apropiadas, como precisión, recall, F1-score, error cuadrático medio (MSE), etc. Utilizar técnicas de validación cruzada para asegurar que los modelos sean generalizables.

6. Optimización de modelos: Ajustar los hiperparámetros de los modelos para mejorar su rendimiento. Puede utilizarse la búsqueda en cuadrícula (grid search) o búsqueda aleatoria (random search) para encontrar los mejores hiperparámetros.

7. Interpretación y comunicación de resultados: Interpretar los resultados de los modelos y comunicar los hallazgos a las partes interesadas del hospital.

8. Implementación y seguimiento: Implementar los modelos en la infraestructura del hospital y realizar un seguimiento de su rendimiento en el tiempo. Asegurarse de mantener y actualizar los modelos según sea necesario.

# Columnas

## Primero observo las columnas de los dataframes

1. Leo los datos
````python
from pandas_ods_reader import read_ods

df_22 = read_ods("data/HADO 22.ods",sheet= "Hoja1")
df_21 = read_ods("data/HADO21.ods")
df_20 = read_ods("data/HADO 20.ods")
df_19 = read_ods("data/HADO 19.ods")
df_18 = read_ods('data/Estadistica 2018.ods')
df_17 = read_ods("data/Estadística 2017.ods")
````
* Observamos espacios en los valores de las columnas pero antes hago unas transformaciones en los datos de 2019 ya que se repite la columna otros
  
````
#   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   Hospital        427 non-null    object 
 1   Servicio        427 non-null    object 
 2       AP          427 non-null    object 
 3    Otros          427 non-null    object 
 4   Diagnostico     427 non-null    object 
 5   Motivo Ing      421 non-null    object 
 6    pal Onc        427 non-null    object 
 7   Pal no Onc      427 non-null    object 
 8     Fiebre        426 non-null    object 
 9    Disnea         427 non-null    object 
 10    Dolor         427 non-null    object 
 11  Delirium        427 non-null    object 
 12  Astenia         427 non-null    object 
 13  Anorexia        427 non-null    object 
 14     Otros        427 non-null    object 
 15   P. terminal    426 non-null    object 
 16    Agonía        427 non-null    object 
 17    PS/IK         427 non-null    object 
 18  Barthel         427 non-null    object 
 19  GDS-FAST        427 non-null    object 
 20  EVA ing         426 non-null    object 
 21     Otros.1      427 non-null    object 
 22  Complicaciones  426 non-null    object 
 23  Nº estancias    427 non-null    float64
 24  Nº visitas      427 non-null    object 
 25  SEDACIÓN        427 non-null    object 
 26  Mot. ALTA       427 non-null    object 
 27  Médico          427 non-null    object
````
2. Soluciono el problema de la columna 'Otros' duplicada

````python
new_column_names = { ' Otros': 'otros', '   Otros': 'otros_1', '   Otros.1': 'otros_2'}

df_19 = df_19.rename(columns=new_column_names)
````
Entonces podemos hacer un strip pero esto separa también los espacios que forman los nombres de la columna

```python
def df_split_lower(df: pd.DataFrame) -> list:
    df.columns = df.columns.str.strip()         # Clean the spaces in columns names
    df.columns = df.columns.str.lower()         # To lowercase
    return df.columns
```
3. Aplico la función con un bucle for
   
````python
total = 0
for i, df in enumerate(dfs):
    i += 2017
    df_split_lower(df)
    total += len(df)
    print("df", i)
    print(df.columns)
    print(total)
````
4. Despues de pasar todas las columnas a lower y quitar espacios hacemos el rename

````python
data_2017 = df_17.rename(columns={'hospital': 'h_procedencia',
                               'servicio': 's_procedencia',
                               'ap': 'ap',
                               'otros': 'otros',
                               'diagnostico': 'diagnostico',
                               'motivo ing': 'motivo_ing',
                               'paliativo onc': 'paliativo_onc/noc', 
                               'paliativo no onc': 'paliativo_no_onc/noc',
                               'fiebre': 'fiebre',
                               'disnea': 'disnea',
                               'dolor': 'dolor',
                               'delirium': 'delirium',
                               'astenia': 'astenia',
                               'anorexia': 'anorexia',                               
                               'otros.1': 'otros_1',
                               'agonía': 'agonia',
                               'p terminal': 'p_terminal',
                               'ps/ik': 'ps/ecog',
                               'barthel': 'barthel',
                               'gds-fast': 'gds/fast', 
                               'eva ing': 'eva_ing',
                               'otros.2': 'otros_2',
                               'complicaciones': 'otros/complicaciones',
                               'nº estancias': "n_estancias",
                               'nº visitas': "n_visitas",
                               'sedación': 'sedacion',
                               'mot. alta': 'motivo_alta', 
                               'médico': 'medico'})

data_2018 = df_18.rename(columns={'hospital': 'h_procedencia',
                               'servicio': 's_procedencia',
                               'ap': 'ap',
                               'otros': 'otros',
                               'diagnostico': 'diagnostico',
                               'motivo ing': 'motivo_ing',
                               'paliativo onc': 'paliativo_onc/noc', 
                               'paliativo no onc': 'paliativo_no_onc/noc',
                               'fiebre': 'fiebre',
                               'disnea': 'disnea',
                               'dolor': 'dolor',
                               'delirium': 'delirium',
                               'astenia': 'astenia',
                               'anorexia': 'anorexia',                               
                               'otros.1': 'otros_1',
                               'agonía': 'agonia',
                               'p terminal': 'p_terminal',
                               'ps/ik': 'ps/ecog',
                               'barthel': 'barthel',
                               'gds-fast': 'gds/fast', 
                               'eva ing': 'eva_ing',
                               'otros.2': 'otros_2',
                               'complicaciones': 'otros/complicaciones',
                               'nº estancias': "n_estancias",
                               'nº visitas': "n_visitas",
                               'sedación': 'sedacion',
                               'mot. alta': 'motivo_alta', 
                               'médico': 'medico'})
                               
data_2019 = df_19.rename(columns={'hospital': 'h_procedencia',
                               'servicio': 's_procedencia',
                               'ap': 'ap',
                               'otros': 'otros',
                               'diagnostico': 'diagnostico',
                               'motivo ing': 'motivo_ing',
                               'pal onc': 'paliativo_onc/noc', 
                               'pal no onc': 'paliativo_no_onc/noc',
                               'fiebre': 'fiebre',
                               'disnea': 'disnea',
                               'dolor': 'dolor',
                               'delirium': 'delirium',
                               'astenia': 'astenia',
                               'anorexia': 'anorexia',                               
                               'otros_1': 'otros_1', # Problema se repite otros en una colunmna ver si lo traga así
                               'agonía': 'agonia',
                               'p. terminal': 'p_terminal',
                               'ps/ik': 'ps/ecog',
                               'barthel': 'barthel',
                               'gds-fast': 'gds/fast', 
                               'eva ing': 'eva_ing',
                               'otros_2': 'otros_2',
                               'complicaciones': 'otros/complicaciones',
                               'nº estancias': "n_estancias",
                               'nº visitas': "n_visitas",
                               'sedación': 'sedacion',
                               'mot. alta': 'motivo_alta', 
                               'médico': 'medico'})
                               
data_2020 = df_20.rename(columns={'h proced': 'h_procedencia', 
                               's proced': 's_procedencia',
                               'ap': 'ap',
                               'otros': 'otros',
                               'diag principal': 'diagnostico',
                               'motivo ing': 'motivo_ing',
                               'agudo estable': 'agudo_estable',    # Posible otros
                               'crónico reag': 'cronico_reag',      # Posible otros
                               'paliativo onc': 'paliativo_onc/noc', 
                               'pal no onc': 'paliativo_no_onc/noc',
                               'trato antibiótico': "trato_antibiotico",
                               'dolor': 'dolor',
                               'delirium': 'delirium',
                               'disnea': 'disnea',
                               'ast-anorx': 'ast/anorx',     # Agrupan astenia y anorexia (en 17,18 y 19 la separaban)
                               'fiebre': 'fiebre',
                               'transfusion': 'transfusion',        # Posible otros
                               'paracentesis': 'paracentesis',      # Posible otros
                               'toracentesis': 'toracentesis',
                               'ps/ik': 'ps/ecog',
                               'barthel': 'barthel',
                               'gds-fast': 'gds/fast',
                               'otros/complicaciones': 'otros/complicaciones',
                               'agonía': 'agonia',
                               'sedación': 'sedacion',
                               'motivo alta': 'motivo_alta',
                               'n.º estancias': "n_estancias",
                               'n.º visitas': "n_visitas",
                               'ayuntamiento': 'ayuntamiento',          # Se empieza a incluir en el 2020
                               'médico': 'medico'})

data_2021 = df_21.rename(columns={'h proced': 'h_procedencia', 
                               's proced': 's_procedencia',
                               'ap': 'ap',
                               'otros': 'otros',
                               'diag principal': 'diagnostico',
                               'motivo ing': 'motivo_ing',
                               'agudo estable': 'agudo_estable',    # Posible otros
                               'crónico reag': 'cronico_reag',      # Posible otros
                               'paliativo onc': 'paliativo_onc/noc', 
                               'pal no onc': 'paliativo_no_onc/noc',
                               'trato antibiótico': "trato_antibiotico",
                               'dolor': 'dolor',
                               'delirium': 'delirium',
                               'disnea': 'disnea',
                               'ast-anorx': 'ast/anorx',     # Agrupan astenia y anorexia (en 17,18 y 19 la separaban)
                               'fiebre': 'fiebre',
                               'transfusion': 'transfusion',        # Posible otros
                               'paracentesis': 'paracentesis',      # Posible otros
                               'toracentesis': 'toracentesis',
                               'ps/ik': 'ps/ecog',
                               'barthel': 'barthel',
                               'gds-fast': 'gds/fast',
                               'otros/complicaciones': 'otros/complicaciones',
                               'agonia': 'agonia',
                               'sedación': 'sedacion',
                               'motivo alta': 'motivo_alta',
                               'n.º estancias': "n_estancias",
                               'n.º visitas': "n_visitas",
                               'ayuntamiento': 'ayuntamiento',          # Se empieza a incluir en el 2020
                               'médico': 'medico'})
                               
data_2022 = df_22.rename(columns={'fecha de alta': 'fecha_alta', 
                               'h.procedencia': 'h_procedencia',
                               'servicio': 's_procedencia',
                               'ap': 'ap',
                               'motivo ing': 'motivo_ing',
                               'diagnóstico principal': 'diagnostico',
                               'agudo estable': 'agudo_estable',    # Posible otros
                               'crónico agud.': 'cronico_reag',      # Posible otros
                               'paliativo onc': 'paliativo_onc/noc', 
                               'palt no onc': 'paliativo_no_onc/noc',
                               'antibiotico iv': "trato_antibiotico",
                               'dolor': 'dolor',
                               'disnea': 'disnea',
                               's febril': 'fiebre',
                               'delirium': 'delirium',
                               'astenia/anorexia': 'ast/anorx', # Agrupan astenia y anorexia (en 17,18 y 19 la separaban)
                               'fe iv': '¿?',          # Se añade en 2022 (Puede ser fiebre)                                                      
                               'transf': 'transfusion',        # Posible otros
                               'paracen': 'paracentesis',      # Posible otros
                               'toracen': 'toracentesis',
                               'ps/ecog': 'ps/ecog',
                               'barthel': 'barthel',
                               'gds/fast': 'gds/fast',
                               'sedación': 'sedacion',
                               'motivo alta': 'motivo_alta',
                               'n.º estancias': "n_estancias",
                               'n.º visitas': "n_visitas",
                               'ayuntamiento': 'ayuntamiento',          # Se empieza a incluir en el 2020
                               'médico': 'medico'})
`````

* Antes de hacer el concat o el merge vamos a crear una columna nueva de año para cada dataframe y así identificar a que año pertenecen esos datos.
  
5. Añadimos columna year para identificar el año de los datos.

````python
data_2017["year"] = 2017
data_2018["year"] = 2018
data_2019["year"] = 2019
data_2020["year"] = 2020
data_2021["year"] = 2021
data_2022["year"] = 2022
```` 
6. Seleccionamos y eliminamos las columnas no deseadas

   * Eliminamos la columna `unnamed.1` No conocemos que representan los 5 valores unnamed de los datos de 2017.
   * La columna de `trato_anibiotico` solo está a partir del 2020 se mantiene pero solo para esos años
   * La columna de astenia y anorexia viene a partir del 2020 agrupada
     * Agrupar los datos de astenia y anorexia del 17 al 19 antes del `concat` y renombrar la columna por `ast/anorx` 
   * La columna fe_iv no sé a que pertenece pero solo está en 2022 con el nombre cambiado a `¿?`
   * ¿Qué hacer con las columnas `otros_1` y `otros_2`?

````python
# Quitamos columnas innecesarias 

data_2017.drop(columns="unnamed.1", inplace=True)  # Unnamed no tiene valores importantes sólo 5 valores numéricos que no sé que son
````
````python
# Función para eliminar la columna de trato_antibiotico de los datos de 2020 en adelante
def del_trato_antibiotico(dataframes):
    for df in dataframes:
        df = df.drop(['trato_antibiotico'], axis=1, inplace=True)

# Función para agrupar las columnas de astenia y anorexia porque se agrupan en los datos de 2020 en adelante

def col_astenia_anorexia(dataframes):
    for df in dataframes:
        df['ast/anorx'] = np.where(df['astenia']=='si', 'si', df['anorexia'])
        df = df.drop(['astenia', 'anorexia'],axis=1, inplace=True)
````
7. Agrupamos astenia y anorexia y eliminamos la columna trato antibiotico
````python
astenia_anorexia = [data_2017, data_2018, data_2019]      # Lista con los df que tienen astenia y anorexia separados

col_astenia_anorexia(astenia_anorexia)

datos_trato_antibiotico = [data_2020, data_2021, data_2022]

del_trato_antibiotico(datos_trato_antibiotico)
````

8. Seguidamente creo una lista con todos los dataframes renombrados:

````python
all_data_rename = [data_2017, data_2018, data_2019 ,data_2020, data_2021, data_2022]
````

9. Muestro los datos con la función para ver la forma e información de los dataframes
````python
def df_split_lower_list(dataframes) -> list:
    for df in dataframes:
        df.columns = df.columns.str.strip()         # Clean the spaces in columns names
        df.columns = df.columns.str.lower()         # To lowercase
        print(df.columns)

for i, data in enumerate(all_data_rename):
    i += 2017
    print("Datos del año",i)
    print(data.shape)
    print(data.info())
    print("="*80)
````
10. Hago el concat de todos los dataframes
````python
df_concatenado = pd.concat(all_data_rename, ignore_index=True, axis=0)
````
* Para ver si hay index duplicado:
````python
print(data_2017.index.duplicated().sum())
print(data_2018.index.duplicated().sum())
print(data_2019.index.duplicated().sum())
print(data_2020.index.duplicated().sum())
print(data_2021.index.duplicated().sum())
print(data_2022.index.duplicated().sum())
````
11. Función para ver los valores unicos del dataframe concatenado
````python
def unicos(df):
    columns = df.columns.tolist()
    for i, column in enumerate(columns):
        v_column = df[column].unique()
        print(df.columns.values[i])
        print(len(v_column), v_column)
        print("="*66)
````

# NEXT STEPS:

1. Limpieza de los datos.
2. Pasar los datos que correspondan a enteros.
3. Normalizar los datos.
4. **Fuzzy String Matching**

# TO DOS:

 1. Municipios, datos faltantes
 2. Normalizar y pasar el tipo de datos
 3. Preguntar columnas `otros` y con interrogantes (fe iv)
 4. ~~Group de astenia y anorexia para las otras fechas que van por separado~~
 5. ~~Columna otros duplicada en 2019. Solucionar~~
 6. Hacer dataframe con listas de los valores correctos para remplazar con 'fuzzywuzzy'
    1. H.procedencia, servicio, ap, ast/anorx, etc
    > Fuzzywuzzy ahora es `thefuzz` https://github.com/seatgeek/thefuzz
