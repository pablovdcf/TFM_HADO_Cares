# data_cleaning.py

import pandas as pd
import string
import unidecode
import numpy as np


def remove_anomalous_values(
    df: pd.DataFrame, column: str, value: float
) -> pd.DataFrame:
    """
    Removes rows from a DataFrame based on a condition.
    :param df: Input DataFrame.
    :param column: Column to inspect for the condition.
    :param value: Value to exclude.
    :return: DataFrame after excluding rows.
    :raises: ValueError if `column` is not in `df`.
    """
    if column not in df.columns:
        raise ValueError(f"{column} does not exist in DataFrame.")
    return df[df[column] != value]


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strips whitespace, converts to lower case, removes punctuation and accents from text columns.
    :param df: Input DataFrame.
    :return: Cleaned DataFrame.
    """

    def data_strip(df):
        for column in df:
            if df[column].dtype == "object":
                df[column] = df[column].replace("\\s+", " ", regex=True).str.strip()
        return df

    def to_lowercase(df):
        for column in df:
            if df[column].dtype == "object":
                df[column] = df[column].str.lower()
        return df

    def remove_punctuation_and_accents(df):
        for column in df:
            if df[column].dtype == "object":
                df[column] = df[column].apply(
                    lambda x: unidecode.unidecode(x) if isinstance(x, str) else x
                )
                df[column] = df[column].str.translate(
                    str.maketrans("", "", string.punctuation)
                )
        return df

    return data_strip(to_lowercase(remove_punctuation_and_accents(df)))


def replace_na(df: pd.DataFrame, replacement_dict_na: dict) -> pd.DataFrame:
    """
    Replaces NA values in specified columns with given replacements.
    :param df: Input DataFrame.
    :param replacement_dict_na: Dictionary mapping replacements to columns.
    :return: DataFrame with NAs replaced.
    :raises: ValueError if a column specified in `replacement_dict_na` does not exist in `df`.
    """

    for value, columns in replacement_dict_na.items():
        for column in columns:
            if column not in df.columns:
                raise ValueError(f"{column} does not exist in DataFrame.")
            df[column] = df[column].fillna(value)
    return df


def convert_to_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Converts specified columns to numeric data type.
    :param df: Input DataFrame.
    :param columns: Columns to convert.
    :return: DataFrame with converted columns.
    :raises: ValueError if a column in `columns` does not exist in `df`.
    """
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"{column} does not exist in DataFrame.")
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def fill_na_with_mean(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Fills NA values in specified columns with the column mean.
    :param df: Input DataFrame.
    :param columns: Columns to fill.
    :return: DataFrame with filled columns.
    :raises: ValueError if a column in `columns` does not exist in `df`.
    """
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"{column} does not exist in DataFrame.")
        df[column] = df[column].fillna(df[column].mean())
    return df
