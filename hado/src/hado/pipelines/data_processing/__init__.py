"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""
from .nodes import (
    clean_text,
    replace_missing,
    clean_and_classify_barthel,
    clean_ps_ecog,
    clean_and_classify_gds_fast,
    replace_words,
    add_location_and_map_names,
    process_fecha_alta,
    assign_sedation,
    assign_medication,
    encoding_variables,
    apply_categorization,
    categorize_and_group_combined_otros,
)
from .pipeline import create_pipeline_data_processing

__all__ = ["create_pipeline_data_processing"]

__version__ = "0.1"
