"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""
from typing import Any, Dict, List
import pandas as pd
import unidecode
import string

# Functions by order in Pipeline

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

    # print_missing_percentage(df)

    for value, columns in params.items():
        df[columns] = df[columns].fillna(value)

    print_missing_percentage(df)

    return df

def clean_and_classify_barthel(df: pd.DataFrame,
                               barthel_replacements: Dict[str, str], 
                               high_values: List[int],
                               classification_rules: Dict[str, str]
                               ) -> pd.DataFrame:
    """
    Cleans and classifies the values in the 'barthel' column of the DataFrame.
    
    Args:
    - df (pd.DataFrame): The original DataFrame containing the 'barthel' column.
    - barthel_replacements (Dict[str, str]): Dictionary of ambiguous values to replace in 'barthel' column.
    - high_values (List[int]): List of high values in 'barthel' that need correction.
    - classification_rules (Dict[str, str]): Rules for classifying the 'barthel' scores.
    
    Returns:
    - pd.DataFrame: DataFrame with cleaned 'barthel' column and a new 'barthel_classification' column.
    """
    
    # Reemplazar valores '1000' por '100' en la columna 'barthel'
    df['barthel'] = df['barthel'].replace("1000", "100")

    # Reemplazar valores ambiguos según los parámetros
    df['barthel'].replace(barthel_replacements, inplace=True)

    # Correcciones para valores superiores a 100
    def correct_barthel_values(value):
        if int(value) in high_values:
            return str(int(value) // 10)
        return value

    df['barthel'] = df['barthel'].apply(correct_barthel_values)

    # Clasificación basada en reglas
    def classify_barthel(score: int) -> str:
        if score <= classification_rules['Dependencia total']:
            return "Dependencia total"
        elif score <= classification_rules['Dependencia severa']:
            return "Dependencia severa"
        elif score <= classification_rules['Dependencia moderada']:
            return "Dependencia moderada"
        elif score <= classification_rules['Dependencia leve o minima']:
            return "Dependencia leve o minima"
        else:
            return "Independencia"

    # Convertir la columna 'barthel' a tipo entero
    df['barthel'] = df['barthel'].astype(int)

    # Aplicar la función classify_barthel
    df['barthel_classification'] = df['barthel'].apply(classify_barthel)
    print(df['barthel_classification'].value_counts())
    return df


def clean_ps_ecog(df: pd.DataFrame, 
                  ambiguous_values: List[str],
                  value_replacements: Dict[str, str],
                  classification_rules: Dict[str, str],
                  ecog_classification: Dict[str, str],
                  barthel_col: str = 'barthel_classification') -> pd.DataFrame:
    """
    Cleans and classifies the values in the 'ps_ecog' column of the DataFrame.
    
    Args:
    - df (pd.DataFrame): The original DataFrame containing the 'ps_ecog' column.
    - ambiguous_values (List[str]): List of ambiguous values in 'ps_ecog' column.
    - value_replacements (Dict[str, str]): Dictionary of values to replace in 'ps_ecog' column.
    - classification_rules (Dict[str, str]): Rules for inferring 'ps_ecog' values from 'barthel_classification'.
    - ecog_classification (Dict[str, str]): Classification rules for 'ps_ecog' based on its value.
    - barthel_col (str, optional): Name of the column containing the barthel classification. Default is 'barthel_classification'.
    
    Returns:
    - pd.DataFrame: DataFrame with cleaned 'ps_ecog' column and a new 'ps_ecog_classification' column.
    """
    # Función auxiliar para corregir valores basados en dígitos
    def correct_values(value: str) -> str:
        if value.isdigit():
            return str(max([int(digit) for digit in value]))
        return value
    
   

    # Función auxiliar para inferir el valor ps_ecog basado en la clasificación de barthel
    def infer_values(row) -> str:
        if row['ps_ecog'] in ambiguous_values:
            return classification_rules.get(row[barthel_col], row['ps_ecog'])
        return row['ps_ecog']

    # Corregir valores en ps_ecog basados en dígitos y reemplazar valores obvios
    df['ps_ecog'] = df['ps_ecog'].apply(correct_values)
    df['ps_ecog'].replace(value_replacements, inplace=True)
    
    # Convertir la columna 'ps_ecog' a string antes de inferir valores
    df['ps_ecog'] = df['ps_ecog'].astype(str)
    print(f"\n{df['ps_ecog'].value_counts()}")
    # Inferir valores de ps_ecog basados en barthel_classification
    df['ps_ecog'] = df.apply(infer_values, axis=1)
    
    # Clasificación textual basada en el valor ECOG
    df['ps_ecog_classification'] = df['ps_ecog'].map(ecog_classification)
    return df

def clean_and_classify_gds_fast(df: pd.DataFrame, 
                                ambiguous_values_to_zero: List[str],
                                barthel_to_gds_mappings: Dict[str, str],
                                gds_classification: Dict[int, str],
                                barthel_col: str = 'barthel_classification') -> pd.DataFrame:
    """
    Cleans and classifies the values in the 'gds_fast' column of the DataFrame.
    
    Args:
    - df (pd.DataFrame): The original DataFrame containing the 'gds_fast' column.
    - ambiguous_values_to_zero (List[str]): List of ambiguous values to replace with "0" in 'gds_fast'.
    - barthel_to_gds_mappings (Dict[str, str]): Mappings from barthel classification to gds_fast values.
    - gds_classification (Dict[int, str]): Classification rules for 'gds_fast' based on its value.
    - barthel_col (str, optional): Name of the column containing the barthel classification. Default is 'barthel_classification'.
    
    Returns:
    - pd.DataFrame: DataFrame with cleaned 'gds_fast' column and a new 'gds_fast_classification' column.
    """
    
    # Replace ambiguous values with 0
    df['gds_fast'].replace(ambiguous_values_to_zero, "0", inplace=True)
    
    # Infer values of gds_fast based on barthel_classification
    for classification, value in barthel_to_gds_mappings.items():
        df.loc[(df['gds_fast'] == 'si') & (df[barthel_col] == classification), 'gds_fast'] = value
    
    # Extract numbers from values indicating a stage or sub-stage
    df['gds_fast'] = df['gds_fast'].str.extract(r'(\d+)')[0]

    # Extract the highest digit from the values
    df['gds_fast'] = df['gds_fast'].astype(str).apply(lambda value: str(max([int(digit) for digit in value])) if value.isdigit() else value)
    df['gds_fast'] = df['gds_fast'].astype(int)

    # Apply the classification
    df['gds_fast_classification'] = df['gds_fast'].map(gds_classification)
    
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
    exclude_columns: List[str]
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
    
    exclude_columns: List
        List with columns that we don't need to replace the words from the dictionarys

    Returns
    -------
    df : pd.DataFrame
        The DataFrame with replaced words.
    """

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

        # unique_values = df[col].astype(str).unique()
        # print(
        #     f"\nAfter replacement - '{col}' unique values:",
        #     len(unique_values),
        #     sorted(unique_values, reverse=False),
        # )
        return df

    # Replace 'si' followed by a number with only the number
    df.replace(r"si\s*(\d+)", r"\1", regex=True, inplace=True)

    # Filter the columns which are of type object (i.e., string) but are not in the exclude_columns list
    string_columns = [col for col in df.select_dtypes(include="object").columns 
                      if col not in exclude_columns]

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
        ("eva_ing", replacement_dict_numeric),
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

def add_location_and_map_names(
    df: pd.DataFrame,
    name_mapping: Dict[str, str],
    locations: Dict[str, Dict[str, float]]
) -> pd.DataFrame:
    """
    Adds latitude and longitude columns to the DataFrame and maps municipality names.

    Parameters:
    df (pd.DataFrame): DataFrame containing the 'ayuntamiento' column.
    name_mapping (Dict[str, str]): Dictionary to map the names of the municipalities.
    locations (Dict[str, Dict[str, float]]): Dictionary with the locations (latitude and longitude) of the municipalities.

    Returns:
    pd.DataFrame: DataFrame with added latitude and longitude columns and mapped municipality names.
    """
    
    # Add latitude and longitude columns
    df['latitude'] = df['ayuntamiento'].map(lambda x: locations.get(x, {}).get('lat', "desconocido"))
    df['longitude'] = df['ayuntamiento'].map(lambda x: locations.get(x, {}).get('lon', "desconocido"))
    
    # Print statements to check the added columns
    # print("Added Latitude and Longitude:")
    # print(df['ayuntamiento'].unique())
    # print(df['latitude'].unique())
    # print(df['longitude'].unique())
    
    # Normalize and map municipality names
    df['ayuntamiento'] = df['ayuntamiento'].map(name_mapping).fillna(df['ayuntamiento'])
    
    # Check for NA values in the DataFrame
    if df.isna().any().any():
        print("Warning: The DataFrame contains NA values.")
        
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


def assign_sedation(df: pd.DataFrame) -> pd.DataFrame:
    df['tiene_sedacion'] = df['sedacion'].apply(lambda x: 0 if x == 'no' else 1)
    return df

def assign_medication(df: pd.DataFrame, medications) -> pd.DataFrame:
    for medication in medications:
        df[medication] = df['sedacion'].apply(lambda x: 1 if medication in x else 0)
    return df

# Funciones para la categorización de columnas
def apply_categorization(df: pd.DataFrame, parameters) -> pd.DataFrame:
    def classify(value, categories):
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in value.lower():
                    return category
        return "Otros"

    df['hospital_category'] = df['h_procedencia'].apply(lambda x: classify(x, parameters['hospital_categories']))
    df['diagnosis_category'] = df['diagnostico'].apply(lambda x: classify(x, parameters['diagnosis_categories']))
    df['ingreso_category'] = df['motivo_ing'].apply(lambda x: classify(x, parameters['ingreso_categories']))
    df['alta_category'] = df['motivo_alta'].apply(lambda x: classify(x, parameters['alta_categories']))
    df['procedencia_category'] = df['s_procedencia'].apply(lambda x: classify(x, parameters['procedencia_categories']))
    df['otros_category'] = df['otros'].apply(lambda x: classify(x, parameters['otros_categories']))

    return df



# Funciones para la combinación y categorización de las columnas 'otros'

def categorize_and_group_combined_otros(df: pd.DataFrame, parameters) -> pd.DataFrame:
    """
    Combine specified columns, categorize their values based on predefined categories, 
    and group non-primary categories into the "Otros" category.
    
    Args:
    - data (pd.DataFrame): The input dataframe containing the columns to be combined and categorized.
    - parameters (dict): Parameters from the `data_processing.yml` file.
    
    Returns:
    - pd.DataFrame: The dataframe with the combined and categorized column.
    """
    
    # Function to combine columns
    def combine_columns(row):
        values = [row[column] for column in parameters["combined_otros_columns"]]
        combined_values = [val for val in values if val not in ['no', 'desconocido']]
        return '|'.join(combined_values) if combined_values else 'no'
    
    # Define keywords for 'combined_otros' categories
    categories = parameters["combined_otros_categories"]

    # Function to classify values into categories
    def classify_combined_otros(value):
        categories_result = []
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in value.lower():
                    categories_result.append(category)
                    break  # Break the inner loop if a match is found
        return '|'.join(categories_result) if categories_result else "Otros"

    # Combine the columns
    df['combined_otros'] = df.apply(combine_columns, axis=1)
    
    # Apply the function to classify values
    df['categorized_combined_otros'] = df['combined_otros'].apply(classify_combined_otros)
    
    # List of primary categories
    main_categories = list(categories.keys())

    # Replace any value not in main_categories with "Otros"
    df['categorized_combined_otros'] = df['categorized_combined_otros'].apply(lambda x: x if x in main_categories else "Otros")
    
    # Order df columns
    columns_order = parameters["columns_order"]
    df = df[columns_order]
    
    return df

def encoding_variables(df: pd.DataFrame, parameters) -> pd.DataFrame:
    """
    Encode and transform a given dataframe.

    Parameters:
    - df (pd.DataFrame): Dataframe to encode and transform.

    Returns:
    - pd.DataFrame: Transformed dataframe with specific columns and their data types converted.
    """
    def map_values(val):
        """Map specific values to binary values."""
        no_values = parameters["no_values"]
        yes_values = parameters["yes_values"]
        
        return 1 if val in yes_values else 0
    
    def apply_frequency_encoding(column_name):
        """Apply frequency encoding to a specific column."""
        frequencies = df[column_name].value_counts(normalize=True)
        df[column_name] = df[column_name].map(frequencies).fillna(0)  # Handling potential missing values
    
    columns_to_map = parameters['columns_to_map']
    for col in columns_to_map:
        df[col] = df[col].apply(map_values)
    
    columns_for_freq_encoding = parameters['columns_for_freq_encoding']
    if columns_for_freq_encoding:
        for col in columns_for_freq_encoding:
            apply_frequency_encoding(col)
    else:
        pass
    
    # Maps for the categories
    hospital_category_map = parameters['hospital_category_map'] # Values {Santiago, no, Otros}
    diagnosis_category_map = parameters['diagnosis_category_map']
    ingreso_category_map = parameters['ingreso_category_map']
    alta_category_map = parameters['alta_category_map']
    procedencia_category_map = parameters['procedencia_category_map']
    otros_category_map = parameters['otros_category_map']
    categorized_combined_otros_map = parameters['categorized_combined_otros_map']

    # Aplicar los mapeos a las columnas correspondientes
    df['hospital_category'] = df['hospital_category'].map(hospital_category_map)
    df['diagnosis_category'] = df['diagnosis_category'].map(diagnosis_category_map)
    df['ingreso_category'] = df['ingreso_category'].map(ingreso_category_map)
    df['alta_category'] = df['alta_category'].map(alta_category_map)
    df['procedencia_category'] = df['procedencia_category'].map(procedencia_category_map)
    df['otros_category'] = df['otros_category'].map(otros_category_map)
    df['categorized_combined_otros'] = df['categorized_combined_otros'].map(categorized_combined_otros_map)
        
    return df
