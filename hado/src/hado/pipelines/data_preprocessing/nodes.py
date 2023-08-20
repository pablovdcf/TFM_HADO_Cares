"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.10
"""
from typing import Dict
from functools import partial, update_wrapper
import pandas as pd
import numpy as np


def rename_strip_lower_column(df, key, year):
    """
    Function to clean the DataFrame 'df' based on the year 'key'.
    If 'key' is 'hado_19', it renames the columns according to the dictionary 'new_column_names'.
    Then, it strips the spaces and converts all column names to lower case.
    If 'key' is 'hado_17', it drops the column "unnamed.1" with only 5 values for dataframe
    Finally, it prints the name of the DataFrame and its columns, separated by a line of '='*80.
    """
    if key == "hado_19":
        new_column_names = {
            " Otros": "otros",
            "   Otros": "otros_1",
            "   Otros.1": "otros_2",
        }
        df = df.rename(columns=new_column_names)

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df["year"] = year

    if key == "hado_17":
        df.drop(columns="unnamed.1", inplace=True)

    # Printing values for check
    # print(f"DataFrame: {key}\nColumns:")
    # print("\n".join(df.columns))
    # print("=" * 80)

    return df


def wrapped_rename_strip_lower_column(key, year):
    """
    This function creates a wrapped function of rename_strip_lower_column
    with the specified key and year as fixed arguments. This can be useful
    when you need to apply the rename_strip_lower_column function with
    different parameters as part of your pipeline.

    Parameters:
    key (str): The key used to retrieve data from the DataCatalog.
    year (int): The year associated with the data.

    Returns:
    function: A partially applied function of rename_strip_lower_column with the
    specified key and year as fixed arguments.
    """
    # Create a partial function with the given key
    partial_func = partial(rename_strip_lower_column, key=key, year=year)
    # Update the wrapper of partial_func to make it look like rename_strip_lower_column
    update_wrapper(partial_func, rename_strip_lower_column)
    return partial_func


def rename_columns(
    data: pd.DataFrame, year: int, rename_map: Dict[str, str]
) -> pd.DataFrame:
    """
    This function renames the columns of the provided DataFrame based on the
    provided map. It also combines 'astenia' and 'anorexia' columns into a single
    'ast_anorx' column for years 2017, 2018, and 2019. Lastly, it prints out the
    year associated with the DataFrame and the new columns.

    Parameters:
    data (pd.DataFrame): The DataFrame whose columns need to be renamed.
    year (int): The year associated with the data.
    rename_map (Dict[str, str]): A dictionary mapping old column names to new ones.

    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    data = data.rename(columns=rename_map[str(year)])
    if year in [2017, 2018, 2019]:
        data["ast_anorx"] = np.where(data["astenia"] == "si", "si", data["anorexia"])
        data.drop(["astenia", "anorexia"], axis=1, inplace=True)
    
    # Printing values for check
    # print(
    #     f"Year for the DataFrame: {year}"
    # )  # Asumiendo que el año es el nombre del DataFrame
    # print("New columns: ", sorted(data.columns.tolist(), reverse=False))
    
    return data


def check_convert_and_concat(**dataframes):
    """
    The function cleans and concats the input dataframes. Specifically, it converts the 'n_estancias' and 'n_visitas'
    columns to numeric, fills NaNs with the column meadian, removes a specific outlier in the 2022 dataframe, and
    concatenates all dataframes. The function also prints the unique sorted values of 'n_estancias' before and
    after cleaning.

    Parameters
    ----------
    dataframes : dict of {str: pd.DataFrame}
        Input dataframes to be cleaned and concatenated.

    Returns
    -------
    df_concat : pd.DataFrame
        The concatenated dataframe.
    """
    for year, data in dataframes.items():
        try:
            # Convert the values to numeric
            data["n_estancias"] = pd.to_numeric(data["n_estancias"], errors="coerce")
            data["n_visitas"] = pd.to_numeric(data["n_visitas"], errors="coerce")

            # Get unique sorted values of 'n_estancias' column in descending order, ignoring NaNs
            unique_sorted_values = np.sort(data["n_estancias"].dropna().unique())[::-1]

            print(f"Data_{year} unique sorted 'n_estancias':\n{unique_sorted_values}\n")
        except KeyError:
            print(f"Data_{year} does not have 'n_estancias' column\n")

        # Drop the outlier value in the 2022 DataFrame
        if year == "rename_hado_22":
            data = data[data["n_estancias"] != 2.793914e06]

        # Replace NaNs with the mean before converting to integer
        # data['n_estancias'].fillna(data['n_estancias'].mean(), inplace=True)
        # data['n_estancias'] = data['n_estancias'].astype(int)

        # data['n_visitas'].fillna(data['n_visitas'].mean(), inplace=True)
        # data['n_visitas'] = data['n_visitas'].astype(int)

        # Replace NaNs with the median before converting to integer
        data["n_estancias"].fillna(data["n_estancias"].median(), inplace=True)
        data["n_estancias"] = data["n_estancias"].astype(int)

        data["n_visitas"].fillna(data["n_visitas"].median(), inplace=True)
        data["n_visitas"] = data["n_visitas"].astype(int)

        unique_sorted_values = np.sort(data["n_estancias"].dropna().unique())[::-1]
        print(f"Data_{year} fixed and sorted 'n_estancias':\n{unique_sorted_values}\n")

        # This line ensures that pandas does not change type of columns
        dataframes[year] = data

    df_concat = pd.concat(dataframes.values(), ignore_index=True, axis=0)
    # Printing dataframe info for check
    # print(df_concat.info())
    return df_concat


def refactor_rename_strip_lower_column(df, year):
    """
    Function to clean the DataFrame column names.
    Strips the spaces and converts all column names to lower case.
    """
    df.columns = df.columns.str.strip().str.lower()
    df["year"] = year

    if year == 2017 and "unnamed.1" in df.columns:
        df.drop(columns="unnamed.1", inplace=True)

    return df


def refactor_rename_columns(data: pd.DataFrame, rename_map: Dict[str, str]) -> pd.DataFrame:
    """
    This function renames the columns of the provided DataFrame based on the provided map.
    """
    data = data.rename(columns=rename_map)
    return data

def combine_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Combines 'astenia' and 'anorexia' columns into a single 'ast_anorx' column.
    """
    if "astenia" in data.columns and "anorexia" in data.columns:
        data["ast_anorx"] = np.where(data["astenia"] == "si", "si", data["anorexia"])
        data.drop(["astenia", "anorexia"], axis=1, inplace=True)
    return data