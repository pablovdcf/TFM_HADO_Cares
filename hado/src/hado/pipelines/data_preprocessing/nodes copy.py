"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.10
"""
from kedro.pipeline import node
from typing import Dict
import pandas as pd
import regex as re
import numpy as np
from .data_cleaning import remove_anomalous_values, clean_text, replace_na, convert_to_numeric, fill_na_with_mean, replacement_dict_na


# First step: change the name of the columns "otros" for df == 'hado_19'
def rename_columns(df, key):
    """
    Function to rename the columns in the DataFrame 'df' based on the year 'key'.
    If 'key' is 'hado_19', it renames the columns according to the dictionary 'new_column_names'.
    """
    try:
        new_column_names = { ' Otros': 'otros', '   Otros': 'otros_1', '   Otros.1': 'otros_2'}
        if key == 'hado_19':
            df = df.rename(columns=new_column_names)
    except Exception as e:
        print(f"Error renaming columns in {key}: {str(e)}")
    return df

def remove_unwanted_column(df, key):
    """
    Function to remove an unwanted column in the DataFrame 'df' based on the year 'key'.
    If 'key' is 'hado_17', it removes the column 'unnamed.1'.
    """
    try:
        if key == 'hado_17':
            if 'unnamed.1' in df.columns:
                df = df.drop(columns="unnamed.1")  # Remove the column 'unnamed.1' from the DataFrame 'hado_17'
    except Exception as e:
        print(f"Error removing unwanted column in {key}: {str(e)}")
    return df

def combine_columns(df, key):
    """
    Function to combine the columns 'astenia' and 'anorexia' in the DataFrame 'df' based on the year 'key'.
    If 'key' is in ['hado_17', 'hado_18', 'hado_19'], it creates a new column 'ast_anorx' from the columns 'astenia' and 'anorexia'.
    """
    try:
        if key in ['hado_17', 'hado_18', 'hado_19']:
            if set(['astenia', 'anorexia']).issubset(df.columns):
                df['ast_anorx'] = np.where(df['astenia']=='si', 'si', df['anorexia'])  # Combine the columns 'astenia' and 'anorexia'
                df = df.drop(['astenia', 'anorexia'], axis=1)
    except Exception as e:
        print(f"Error combining columns in {key}: {str(e)}")
    return df

# Second step: Clean the dataframes columns for concat later using strip, lower,
def clean_and_sort_column_names(dfs):
    """
    Main function to clean and sort the column names in each DataFrame in 'raw_data'.
    It uses the auxiliary functions 'rename_columns', 'remove_unwanted_column', and 'combine_columns'.
    """
    for key in dfs:
        try:
            if re.match(r'hado_\d+', key):  # check if the key matches the pattern 'hado_' followed by one or more digits
                df = dfs[key]
                df = rename_columns(df, key)
                df.columns = df.columns.str.strip()
                df.columns = df.columns.str.lower()
                             
                dfs[key] = df  # replace the original DataFrame in the dictionary with the cleaned DataFrame
        except Exception as e:
            print(f"Error cleaning and sorting column names in {key}: {str(e)}")
    return dfs


def rename_all_columns(dataframes: Dict[str, pd.DataFrame], column_mappings: Dict[str, Dict[str, str]]) -> Dict[str, pd.DataFrame]:
    """
    Function to rename the columns in each DataFrame in 'dataframes' based on 'column_mappings'.
    It renames the columns in-place in the original DataFrame.
    """
    for key, df in dataframes.items():
        try:
            if key in column_mappings:
                df.rename(columns=column_mappings[key], inplace=True)
        except Exception as e:
            print(f"Error renaming columns in {key} with provided column mappings: {str(e)}")
    return dataframes

def concatenate_dataframes(df_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Function to concatenate all the DataFrames in 'df_dict' into a single DataFrame.
    It ignores the index of the original DataFrames and creates a new one in the resulting DataFrame.
    """
    try:
        df = pd.concat(df_dict.values(), ignore_index=True)
        df = clean_text(df)
        df = replace_na(df, replacement_dict_na)
        df = convert_to_numeric(df, ['n_estancias', 'n_visitas'])
        df = fill_na_with_mean(df, ['n_estancias', 'n_visitas'])
        return df
    except Exception as e:
        print(f"Error concatenating DataFrames: {str(e)}")
        return pd.DataFrame()  # return an empty DataFrame in case of error