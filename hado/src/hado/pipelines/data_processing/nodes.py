"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""
from typing import Any, Dict
import pandas as pd
import unidecode
import string


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to clean text in a pandas DataFrame. The cleaning operations include:
    - Replacing multiple spaces with a single space
    - Stripping leading and trailing spaces
    - Converting text to lowercase
    - Removing punctuation
    - Removing accents

    Args:
        df (pd.DataFrame): Original DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """

    def clean_column(col: Any) -> Any:
        """
        Function to clean a pandas Series object. It will be applied only to object dtype.

        Args:
            col (Any): Original Series to clean.

        Returns:
            Any: Cleaned Series.
        """
        if pd.api.types.is_string_dtype(col):
            col = col.replace("\\s+", " ", regex=True).str.strip()
            col = col.str.lower()
            col = col.apply(
                lambda x: unidecode.unidecode(x) if isinstance(x, str) else x
            )
            col = col.str.translate(str.maketrans("", "", string.punctuation))
        return col

    df = df.copy()
    df = df.apply(clean_column)
    # print(df.head())
    return df


def replace_missing(df: pd.DataFrame, params: Dict) -> pd.DataFrame:
    """
    Replaces missing values in specified columns of the input DataFrame according to a provided dictionary of replacements.
    It also prints the percentage of missing values by column before and after the replacements.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame in which missing values are replaced.

    params : Dict
        Dictionary with the replacement values and the corresponding columns.
        Structure: {replacement_value1: [column1, column2, ...], replacement_value2: [column3, column4, ...]}

    Returns
    -------
    df : pd.DataFrame
        The DataFrame with replaced missing values.
    """
    df = df.copy()

    def print_missing_percentage(df):
        """Helper function to calculate and print missing values percentages"""
        missing_values = df.isnull().sum()
        missing_percentage = missing_values / len(df) * 100
        print("\nPercentage of missing values per column:")
        missing_percentage_sorted = missing_percentage.sort_values(ascending=False)
        for col, value in missing_percentage_sorted.items():
            print(f"{col}: {value}%")

    print_missing_percentage(df)

    for value, columns in params.items():
        df[columns] = df[columns].fillna(value)

    print_missing_percentage(df)

    return df


def replace_words(
    df: pd.DataFrame,
    replacement_dict_general: Dict,
    replacement_dict_diagnostico: Dict,
    replacement_dict_hospital_proc: Dict,
    replacement_dict_service_proc: Dict,
    replacement_dict_motivo_ing: Dict,
    replacement_dict_alta: Dict,
    replacement_dict_medic: Dict,
    replacement_dict_sedation: Dict,
    replacement_dict_city_council: Dict,
    replacement_dict_otros: Dict,
    replacement_dict_otros_1: Dict,
    replacement_dict_otros_complicaciones: Dict,
    replacement_dict_numeric: Dict,
) -> pd.DataFrame:
    """
    Replaces words in multiple columns of a DataFrame according to provided replacement dictionaries.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame in which words are replaced.

    replacement_dict_general : Dict
        Dictionary with the words to replace and the corresponding replacements in all columns except 'ayuntamiento'.

    replacement_dict_diagnostico : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'diagnostico' column.

    replacement_dict_hospital_proc : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'h_procedencia' column.

    replacement_dict_service_proc : Dict
        Dictionary with the words to replace and the corresponding replacements in the 's_procedencia' column.

    replacement_dict_motivo_ing : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'motivo_ing' column.

    replacement_dict_alta : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'motivo_alta' column.

    replacement_dict_medic : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'medico' column.

    replacement_dict_sedation : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'sedacion' column.

    replacement_dict_city_council : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'ayuntamiento' column.

    replacement_dict_otros : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'otros' column.

    replacement_dict_otros_1 : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'otros_1' column.

    replacement_dict_otros_complicaciones : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'otros_complicaciones' column.

    replacement_dict_numeric : Dict
        Dictionary  with the words to replace and the corresponding replacements in the 'gds_fast', 'barhel' and 'eva_ing' columns.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame with replaced words.
    """
    df = df.copy()

    # Function to replace words in a column and print unique values before and after
    def replace_and_print(
        df: pd.DataFrame, col: str, replacement_dict: Dict
    ) -> pd.DataFrame:
        # unique_values = df[col].astype(str).unique()
        # print(
        #     f"\nBefore replacement - '{col}' unique values:",
        #     len(unique_values),
        #     sorted(unique_values, reverse=False),
        # )

        for word, replacement in replacement_dict.items():
            df[col] = df[col].str.replace(
                r"\b{}\b".format(word), replacement, case=False, regex=True
            )

        unique_values = df[col].astype(str).unique()
        # print(
        #     f"\nAfter replacement - '{col}' unique values:",
        #     len(unique_values),
        #     sorted(unique_values, reverse=False),
        # )
        return df

    # Replace 'si' followed by a number with only the number
    df.replace(r"si\s*(\d+)", r"\1", regex=True, inplace=True)

    # Get a list of column names except 'ayuntamiento'
    general_columns = [col for col in df.columns if col != "ayuntamiento"]

    # Filter the columns which are of type object (i.e., string)
    string_columns = df[general_columns].select_dtypes(include="object").columns

    # Now apply the replacements only on these string columns
    for word, replacement in replacement_dict_general.items():
        if isinstance(replacement, str):  # check if 'replacement' is a string
            for col in string_columns:
                df[col] = df[col].str.replace(
                    r"\b{}\b".format(word), replacement, case=False, regex=True
                )
        else:
            print(
                f"Skipping replacement for word '{word}' because replacement value is not a string: {replacement}"
            )

    # List of columns and corresponding dictionaries
    cols_dicts = [
        ("diagnostico", replacement_dict_diagnostico),
        ("h_procedencia", replacement_dict_hospital_proc),
        ("s_procedencia", replacement_dict_service_proc),
        ("motivo_ing", replacement_dict_motivo_ing),
        ("motivo_alta", replacement_dict_alta),
        ("medico", replacement_dict_medic),
        ("sedacion", replacement_dict_sedation),
        ("ayuntamiento", replacement_dict_city_council),
        ("otros", replacement_dict_otros),
        ("otros_1", replacement_dict_otros_1),
        ("otros_complicaciones", replacement_dict_otros_complicaciones),
        ("gds_fast", replacement_dict_numeric),
        ("barthel", replacement_dict_numeric),
        ("eva_ing", replacement_dict_numeric),
        ("ps_ecog", replacement_dict_numeric),
    ]

    # Loop over columns and dictionaries and replace words
    for col, replacement_dict in cols_dicts:
        df = replace_and_print(df, col, replacement_dict)

    # Replace non digits for columns 'gds_fast', 'eva_ing', 'barthel'
    columns = ["gds_fast", "eva_ing", "barthel","ps_ecog"]
    for col in columns:
        df[col].replace(r"[^\d]+", "", regex=True, inplace=True)

    # Convert the values to numeric
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def process_fecha_alta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the 'fecha_alta' column of a DataFrame:
    - Remove 't'
    - Convert to datetime
    - Format as string in '%d/%m/%Y' format
    - Replace NaN values with ''

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a 'fecha_alta' column.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame with the processed 'fecha_alta' column.
    """
    df = df.copy()
    df["fecha_alta"] = df["fecha_alta"].str.replace("t", "")
    df["fecha_alta"] = pd.to_datetime(
        df["fecha_alta"], format="%Y%m%d%H%M%S", errors="coerce"
    )
    df["fecha_alta"] = df["fecha_alta"].dt.strftime("%d/%m/%Y")
    # df['fecha_alta'] = df['fecha_alta'].fillna('')
    df["fecha_alta"] = df["fecha_alta"].fillna("unknown")

    # Only include dates that are not empty strings
    # unique_values = df["fecha_alta"].unique()

    # print(f"Unique values ({len(unique_values)}): {unique_values}")

    return df

def asignar_sedacion(df):
    df['tiene_sedacion'] = df['sedacion'].apply(lambda x: 0 if x == 'no' else 1)
    return df

def asignar_medicamentos(df):
    medicamentos = ['morfina', 'midazolam', 'buscapina', 'haloperidol', 'levomepromazina']
    for medicamento in medicamentos:
        df[medicamento] = df['sedacion'].apply(lambda x: 1 if medicamento in x else 0)
    return df

def encoding_variables(df):
    """
    Encode and transform a given dataframe.

    Parameters:
    - df (pd.DataFrame): Dataframe to encode and transform.

    Returns:
    - pd.DataFrame: Transformed dataframe with specific columns and their data types converted.
    """
    
    # Constants for clarity
    SANTIAGO = 1
    NO = 0
    OTHERS = 2
    
    def map_hospital_categorie(hospital_name):
        """Map hospital name to a specific category."""
        mapping = {
            'gil casares': 'Santiago',
            'clinico': 'Santiago',
            'provincial': 'Santiago',
            'conxo': 'Santiago',
            'rosaleda': 'Santiago',
            'residencia': 'Santiago',
            'no': 'no'
        }
        return mapping.get(hospital_name, 'otros')

    def map_values(val):
        """Map specific values to binary values."""
        no_values = ['no', 'vacio', 'b', 'm']
        yes_values = ['si', '2 concentrados']
        
        return 1 if val in yes_values else 0
    
    def apply_frequency_encoding(column_name):
        """Apply frequency encoding to a specific column."""
        frequencies = df[column_name].value_counts(normalize=True)
        df[column_name] = df[column_name].map(frequencies).fillna(0)  # Handling potential missing values
    
    df['hospital_categorie'] = df['h_procedencia'].apply(map_hospital_categorie)
    df['hospital_categorie'].replace({'Santiago': SANTIAGO, 'no': NO, 'otros': OTHERS}, inplace=True)
    
    columns_to_map = [
        'ap', 'paliativo_onc_noc', 'paliativo_no_onc_noc', 'fiebre', 'disnea',
        'dolor', 'delirium', 'p_terminal', 'agonia', 'ast_anorx', 'agudo_estable',
        'cronico_reag', 'trato_antibiotico', 'transfusion', 'paracentesis',
        'toracocentesis', 'fe_iv'
    ]
    for col in columns_to_map:
        df[col] = df[col].apply(map_values)
    
    columns_for_freq_encoding = [
        'diagnostico', 'motivo_ing', 'motivo_alta', 's_procedencia',
        'otros', 'otros_1', 'otros_2', 'otros_complicaciones'
    ]
    for col in columns_for_freq_encoding:
        apply_frequency_encoding(col)
    
    # Columns order
    columns_order = ['h_procedencia','hospital_categorie', 's_procedencia', 'procedencia_category', 'diagnostico', 'diagnosis_category', 'motivo_ing', 'ingreso_category', 'motivo_alta', 'alta_category', 'fecha_alta',
         'ap', 'n_estancias', 'n_visitas', 'paliativo_onc_noc', 'paliativo_no_onc_noc', 'fiebre', 'disnea',
         'dolor', 'delirium', 'sedacion', 'p_terminal', 'agonia', 'ast_anorx', 'cronico_reag', 'trato_antibiotico', 'transfusion', 'paracentesis', 'agudo_estable', 'toracocentesis', 'fe_iv',
         'ps_ecog',  'barthel', 'gds_fast', 'eva_ing',
         'otros_complicaciones', 'otros', 'otros_1',  'otros_2',
         'tiene_sedacion', 'morfina', 'midazolam', 'buscapina', 'haloperidol', 'levomepromazina',
         'medico', 'ayuntamiento',
         'year']
        
    df = df[columns_order]
    
    # Columns to keep
    return df.select_dtypes(exclude=['object'])

# Funciones para la categorización de columnas

def classify_diagnosis(diagnosis):
    categories = {
        "Infecciones": ["infeccion", "ITU", "sepsis", "bacteriemia", "neumonia", "infectiva", "absceso"],
        "Enfermedades Cardiacas": ["cardiaca", "coronaria", "corazon", "miocardio", "arritmia"],
        "Canceres": ["cancer", "tumor", "neoplasia", "leucemia", "linfoma", "melanoma", "carcinoma"],
    }
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in diagnosis.lower():
                return category
    return "Otros"

def classify_ingreso(motivo):
    categories = {
        "Sintomas": ["sintoma", "dolor", "disnea", "nauseas", "fiebre", "malestar"],
        "Tratamientos": ["tratamiento", "antibiotico", "quimioterapia", "radioterapia", "terapia", "medicacion"],
        "Evaluaciones": ["evaluacion", "valoracion", "control", "revision", "seguimiento"],
    }
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in motivo.lower():
                return category
    return "Otros"

def classify_alta(motivo):
    categories = {
        "Recuperación": ["mejoria", "recuperado", "alta voluntaria", "traslado"],
        "Tratamiento completado": ["tratamiento finalizado", "medicación completada"],
        "Complicaciones": ["complicaciones", "reingreso"],
        "Exitus": ["exitus", "fallecido", "muerte"]
    }
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in motivo.lower():
                return category
    return "Otros"

def classify_procedencia(value):
    categories = {
        "Oncología": ["oncologia"],
        "Urgencias": ["urgencias"],
        "MIR": ["mir"],
    }
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in value.lower():
                return category
    return "Otros"

def classify_otros(value):
    categories = {
        "Especialidades Médicas": ["nefrologia", "oncologia", "cardiologia", "neumologia", "urologia", "digestivo", "vascular"],
        "No especificado": ["no", "ncr"]
    }
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in value.lower():
                return category
    return "Otros"

def apply_categorization(df: pd.DataFrame) -> pd.DataFrame:
    df['diagnosis_category'] = df['diagnostico'].apply(classify_diagnosis)
    df['ingreso_category'] = df['motivo_ing'].apply(classify_ingreso)
    df['alta_category'] = df['motivo_alta'].apply(classify_alta)
    df['procedencia_category'] = df['s_procedencia'].apply(classify_procedencia)
    df['otros_category'] = df['otros'].apply(classify_otros)
    return df

# Funciones para la combinación y categorización de las columnas 'otros'

def combine_columns(row):
    values = [row['otros'], row['otros_1'], row['otros_2'], row['otros_complicaciones']]
    combined_values = [val for val in values if val not in ['no', 'desconocido']]
    return '|'.join(combined_values) if combined_values else 'no'

def classify_combined_otros(value):
    categories = {
        "Sintomas generales": ["nauseas", "vomitos", "agitacion", "insomnio", "diarrea", "ansiedad", "dolor", "fiebre"],
        "Complicaciones": ["infeccion respiratoria", "insuficiencia respiratoria", "retencion urinaria", "hematuria", "broncoaspiracion", "sepsis", "acv"],
        "Condiciones relacionadas con la familia o el entorno": ["claudicacion familiar", "residencia"],
        "Desconocido/No especificado": ["no", "ncr", "desconocido"]
    }
    categories_result = []
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in value.lower():
                categories_result.append(category)
                break
    return '|'.join(categories_result) if categories_result else "Otros"

def apply_combined_otros_categorization(data: pd.DataFrame) -> pd.DataFrame:
    data['combined_otros'] = data.apply(combine_columns, axis=1)
    data['categorized_combined_otros'] = data['combined_otros'].apply(classify_combined_otros)
    return data
