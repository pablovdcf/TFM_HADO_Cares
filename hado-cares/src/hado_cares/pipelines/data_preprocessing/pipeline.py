"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import clean_and_preprocess_data

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clean_and_preprocess_data,
                "hospital_data",
                "cleaned_hospital_data",
            ),
        ]
    )

