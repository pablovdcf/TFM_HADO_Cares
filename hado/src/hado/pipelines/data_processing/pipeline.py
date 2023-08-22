"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    clean_text, 
    replace_missing, 
    replace_words, 
    process_fecha_alta, 
    assign_sedation, 
    assign_medication, 
    encoding_variables, 
    apply_categorization, 
    categorize_and_group_combined_otros,
)

def create_pipeline_data_processing(**kwargs):
    """
    Create a data processing pipeline.
    
    This pipeline performs the following tasks:
    1. Clean text data.
    2. Replace missing values.
    3. Replace specific words based on multiple dictionaries.
    4. Process 'fecha_alta' (discharge date).
    5. Assign sedation information.
    6. Assign medication information.
    7. Categorize the data.
    8. Categorize the 'otros' (other) data.
    9. Encode variables for modeling.
    
    Returns:
    - Pipeline: A Kedro pipeline object.
    """
    return Pipeline(
        [
            # Clean text data
            node(
                func=clean_text,
                inputs="hado_concat",
                outputs="hado_clean",
                name="clean_text",
            ),
            # Replace missing values based on a dictionary
            node(
                func=replace_missing,
                inputs=["hado_clean", "params:replacement_dict_na"],
                outputs="hado_clean_na",
                name="replace_missing",
            ),
            # Replace specific words based on multiple dictionaries
            node(
                func=replace_words,
                inputs=[
                    "hado_clean_na",
                    "params:replacement_dict_general",
                    "params:replacement_dict_diagnostico",
                    "params:replacement_dict_hospital_proc",
                    "params:replacement_dict_service_proc",
                    "params:replacement_dict_motivo_ing",
                    "params:replacement_dict_alta",
                    "params:replacement_dict_medic",
                    "params:replacement_dict_sedation",
                    "params:replacement_dict_city_council",
                    "params:replacement_dict_otros",
                    "params:replacement_dict_otros_1",
                    "params:replacement_dict_otros_complicaciones",
                    "params:replacement_dict_numeric",
                ],
                outputs="hado_replaced_words",
                name="word_replacement_node",
            ),
            # Process the 'fecha_alta' column
            node(
                func=process_fecha_alta,
                inputs="hado_replaced_words",
                outputs="hado_cleaned",
                name="process_fecha_alta_node",
            ),
            # Assign sedation information
            node(
                func=assign_sedation,
                inputs="hado_cleaned",
                outputs="hado_cleaned_sedation",
                name="assign_sedation_node",
            ),
            # Assign medication information
            node(
                func=assign_medication,
                inputs=["hado_cleaned_sedation", "params:medications"],
                outputs="hado_cleaned_medication",
                name="assign_medications_node",
            ),
            # Categorize data
            node(
                func=apply_categorization,
                inputs=["hado_cleaned_medication","parameters"],
                outputs="hado_categorized",
                name="categorized_data_node",
            ),
            # Group and categorize the 'otros' columns
            node(
                func=categorize_and_group_combined_otros,
                inputs=["hado_categorized","parameters"],
                outputs="hado_final",
                name="categorized_otros_data_node",
            ),
            # Encode variables for modeling
            node(
                func=encoding_variables,
                inputs=["hado_final","parameters"],
                outputs="hado_model",
                name="dataframe_for_modeling"
            )
        ]
    )
