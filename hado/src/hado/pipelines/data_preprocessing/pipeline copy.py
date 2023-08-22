"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    clean_and_sort_column_names,
    rename_columns,
    replace_na,
    concatenate_dataframes,
    replacement_dict_na,
)


def create_pipeline(**kwargs):
    return Pipeline(
        # [
        node(
            func=clean_and_sort_column_names,
            inputs=["hado_17", "hado_18", "hado_19", "hado_20", "hado_21", "hado_22"],
            outputs="preprocess_data",
            name="cleaning_data_columns",
        ),
        #     node(
        #         func=rename_columns,
        #         inputs=["cleaning_data_columns", "params:rename_columns"],
        #         outputs="renamed_data_columns",
        #         name="renaming_data_columns",
        #     ),
        #     node(
        #         func=replace_na,
        #         inputs=["data", "params:replacement_dict_na"],
        #         outputs="data_clean"
        #     ),
        #     node(
        #         func=concatenate_dataframes,
        #         inputs=[f"hado_renamed_{i}" for i in range(17, 23)],
        #         outputs="data",
        #         name="concatenating_dataframes",
        #     )
        #     # ...
        # ]
    )
