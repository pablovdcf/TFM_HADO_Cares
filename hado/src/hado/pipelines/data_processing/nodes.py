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
            col = col.replace('\\s+', ' ', regex=True).str.strip()
            col = col.str.lower()
            col = col.apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
            col = col.str.translate(str.maketrans("", "", string.punctuation))
        return col

    df = df.copy()
    df = df.apply(clean_column)
    print(df.head())
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
        missing_percentage_sorted = round(missing_percentage.sort_values(ascending=False), 2)
        for col, value in missing_percentage_sorted.items():
            print(f"{col}: {value}%")

    print_missing_percentage(df)

    for value, columns in params.items():
        df[columns] = df[columns].fillna(value)
        
    print_missing_percentage(df)

    return df

def replace_words(df: pd.DataFrame,\
    replacement_dict_general: Dict,\
    replacement_dict_diagnostico: Dict,\
    replacement_dict_hospital_proc: Dict,\
    replacement_dict_service_proc: Dict,\
    replacement_dict_motivo_ing: Dict,\
    replacement_dict_alta: Dict,\
    replacement_dict_medic: Dict,\
    replacement_dict_sedation: Dict,\
    replacement_dict_city_council: Dict,\
    replacement_dict_otros: Dict,\
    replacement_dict_otros_1: Dict,\
    replacement_dict_otros_complicaciones: Dict
    ) -> pd.DataFrame:
    """
    Replaces words in the 'diagnostico', 'h_procedencia' and 's_procedencia' columns of a DataFrame 
    according to provided replacement dictionaries. 

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame in which words are replaced.

    replacement_dict : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'diagnostico' column.
        
    replacement_dict_general : Dict
        Dictionary with the words to replace and the corresponding replacements in all columns.
        
    replacement_dict_procedencia : Dict
        Dictionary with the words to replace and the corresponding replacements in the 'h_procedencia' column.
        
    replacement_dict_service_origin : Dict
        Dictionary with the words to replace and the corresponding replacements in the 's_procedencia' column.

    Returns
    -------
    df : pd.DataFrame
        The DataFrame with replaced words.
    """
    df = df.copy()

    # Function to replace words in a column and print unique values before and after
    def replace_and_print(df: pd.DataFrame, col: str, replacement_dict: Dict) -> pd.DataFrame:
        unique_values = df[col].astype(str).unique()
        print(f"\nBefore replacement - '{col}' unique values:", len(unique_values), sorted(unique_values, reverse=False))
        
        for word, replacement in replacement_dict.items():
            df[col] = df[col].str.replace(r'\b{}\b'.format(word), replacement, case=False, regex=True)

        unique_values = df[col].astype(str).unique()
        print(f"\nAfter replacement - '{col}' unique values:", len(unique_values), sorted(unique_values, reverse=False))
        return df

    # Replace 'si' followed by a number with only the number
    df.replace(r'si\s*(\d+)', r'\1' ,regex=True, inplace=True)
    
    # Replace words in all columns
    for word, replacement in replacement_dict_general.items():
        df.replace(r'\b{}\b'.format(word), replacement, regex=True, inplace=True)
    
    # List of columns and corresponding dictionaries
    cols_dicts = [
        ('diagnostico', replacement_dict_diagnostico),
        ('h_procedencia', replacement_dict_hospital_proc),
        ('s_procedencia', replacement_dict_service_proc),
        ('motivo_ing', replacement_dict_motivo_ing),
        ('motivo_alta', replacement_dict_alta),
        ('medico', replacement_dict_medic),
        ('sedacion', replacement_dict_sedation),
        ('ayuntamiento', replacement_dict_city_council),
        ('otros', replacement_dict_otros),
        ('otros_1', replacement_dict_otros_1),
        ('otros_complicaciones', replacement_dict_otros_complicaciones)
    ]
    
    # Loop over columns and dictionaries and replace words
    for col, replacement_dict in cols_dicts:
        df = replace_and_print(df, col, replacement_dict)

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
    df['fecha_alta'] = df['fecha_alta'].str.replace('t', '')
    df['fecha_alta'] = pd.to_datetime(df['fecha_alta'], format='%Y%m%d%H%M%S', errors='coerce')
    df['fecha_alta'] = df['fecha_alta'].dt.strftime('%d/%m/%Y')
    df['fecha_alta'] = df['fecha_alta'].fillna('')

    # Only include dates that are not empty strings
    unique_values = [date for date in df['fecha_alta'].unique() if date != '']
    
    print(f"Unique values ({len(unique_values)}): {', '.join(unique_values)}")
    
    return df