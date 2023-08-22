"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    wrapped_rename_strip_lower_column,
    rename_columns,
    check_convert_and_concat,
)

def create_pipeline_data_preprocessing(**kwargs):
    """
    Create a data preprocessing pipeline.
    
    This pipeline performs the following tasks:
    1. Cleans and standardizes column names for each year.
    2. Renames columns based on provided mappings.
    3. Concatenates all yearly datasets into one.
    
    Returns:
    - Pipeline: A Kedro pipeline object.
    """
    return Pipeline(
        [
            # Cleaning and standardizing column names for the year 2017
            node(
                func=wrapped_rename_strip_lower_column("hado_17", 2017),
                inputs="hado_17",
                outputs="strip_lower_hado_17",
                name="cleaning_hado_17",
            ),
            node(
                func=wrapped_rename_strip_lower_column("hado_18", 2018),
                inputs="hado_18",
                outputs="strip_lower_hado_18",
                name="cleaning_hado_18",
            ),
            node(
                func=wrapped_rename_strip_lower_column("hado_19", 2019),
                inputs="hado_19",
                outputs="strip_lower_hado_19",
                name="cleaning_hado_19",
            ),
            node(
                func=wrapped_rename_strip_lower_column("hado_20", 2020),
                inputs="hado_20",
                outputs="strip_lower_hado_20",
                name="cleaning_hado_20",
            ),
            node(
                func=wrapped_rename_strip_lower_column("hado_21", 2021),
                inputs="hado_21",
                outputs="strip_lower_hado_21",
                name="cleaning_hado_21",
            ),
            node(
                func=wrapped_rename_strip_lower_column("hado_22", 2022),
                inputs="hado_22",
                outputs="strip_lower_hado_22",
                name="cleaning_hado_22",
            ),
            # Renaming columns for the year 2017 to 2022
            node(
                func=rename_columns,
                inputs=[
                    "strip_lower_hado_17",
                    "params:year_2017",
                    "params:rename_columns",
                ],
                outputs="rename_hado_17",
                name="rename_columns_hado_17",
            ),
            node(
                func=rename_columns,
                inputs=[
                    "strip_lower_hado_18",
                    "params:year_2018",
                    "params:rename_columns",
                ],
                outputs="rename_hado_18",
                name="rename_columns_hado_18",
            ),
            node(
                func=rename_columns,
                inputs=[
                    "strip_lower_hado_19",
                    "params:year_2019",
                    "params:rename_columns",
                ],
                outputs="rename_hado_19",
                name="rename_columns_hado_19",
            ),
            node(
                func=rename_columns,
                inputs=[
                    "strip_lower_hado_20",
                    "params:year_2020",
                    "params:rename_columns",
                ],
                outputs="rename_hado_20",
                name="rename_columns_hado_20",
            ),
            node(
                func=rename_columns,
                inputs=[
                    "strip_lower_hado_21",
                    "params:year_2021",
                    "params:rename_columns",
                ],
                outputs="rename_hado_21",
                name="rename_columns_hado_21",
            ),
            node(
                func=rename_columns,
                inputs=[
                    "strip_lower_hado_22",
                    "params:year_2022",
                    "params:rename_columns",
                ],
                outputs="rename_hado_22",
                name="rename_columns_hado_22",
            ),
            # Concatenate all yearly datasets into one
            node(
                func=check_convert_and_concat,
                inputs={
                    f"rename_hado_{year}": f"rename_hado_{year}"
                    for year in range(17, 23)
                },
                outputs="hado_concat",
                name="check_convert_and_concat",
            ),
        ]
    )