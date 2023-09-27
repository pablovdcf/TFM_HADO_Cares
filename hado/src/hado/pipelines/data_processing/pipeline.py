"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node

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

def create_pipeline_data_processing(**kwargs):
    """
This is a pipeline for data processing specifically designed for the HADO dataset. 

The pipeline is structured as follows:

1. **Text Cleaning**: 
    - Cleans the general text data to standardize the format.
    
2. **Missing Value Replacement**: 
    - Replaces missing values in the dataset based on a predefined dictionary.
    
3. **Barthel Score Cleaning and Classification**: 
    - Processes the 'barthel' column, replacing ambiguous values and classifying them based on defined thresholds.
    
4. **PS_ECOG Cleaning and Classification**: 
    - Processes the 'ps_ecog' column, rectifying ambiguous entries and classifying the data based on predefined rules.
    
5. **GDS_FAST Cleaning and Classification**: 
    - Processes the 'gds_fast' column, rectifying ambiguous entries and classifying the data based on predefined rules.

6. **Word Replacement**: 
    - Replaces specific words across multiple columns based on multiple dictionaries provided as parameters.

7. **Latitude, Longitude**
    - Assigns latitude and longitude (new columns) referred to "ayuntamientos" (locations) and do a name mapping
    
8. **Date Processing**: 
    - Processes the 'fecha_alta' column to format and possibly derive new features from the date.
    
9. **Sedation Information Assignment**: 
    - Assigns sedation information to the dataset.
    
10. **Medication Information Assignment**: 
    - Assigns specific medication information based on a predefined list.
    
11. **Categorization**: 
    - Uses predefined rules to categorize various columns in the dataset.
    
12. **Other Columns Grouping and Categorization**: 
    - Focuses on the 'otros' columns to group similar entries and categorize them.
    
13. **Variable Encoding**: 
    - Encodes specific variables to make them suitable for modeling.
    
The pipeline provides a seamless flow from raw HADO dataset to a cleaned, processed, and encoded version ready for data modeling and analysis.

To utilize this pipeline, ensure that the required dependencies are installed and the necessary parameters are set in the conf/base/parameters.yml file.

Returns:
- Pipeline: A Kedro pipeline object, which can be run using the Kedro run command.
"""

    return Pipeline(
        [
            # Clean text data
            node(
                func=clean_text,
                inputs="hado_concat",
                outputs="hado_clean",
                name="clean_text_node",
            ),
            # Replace missing values based on a dictionary
            node(
                func=replace_missing,
                inputs=["hado_clean", "params:replacement_dict_na"],
                outputs="hado_clean_na",
                name="replace_missing_node",
            ),
            node(
                func=clean_and_classify_barthel,
                inputs={
                    "df": "hado_clean_na",
                    "barthel_replacements": "params:barthel_cleaning.barthel_replacements",
                    "high_values": "params:barthel_cleaning.high_values",
                    "classification_rules": "params:barthel_cleaning.classification_rules"
                },
                outputs="hado_barthel_cleaned",
                name="clean_and_classify_barthel_node"
            ),
            node(
                func=clean_ps_ecog,
                inputs={
                    "df": "hado_barthel_cleaned",
                    "ambiguous_values": "params:ps_ecog_cleaning.ambiguous_values",
                    "value_replacements": "params:ps_ecog_cleaning.value_replacements",
                    "classification_rules": "params:ps_ecog_cleaning.classification_rules",
                    "ecog_classification": "params:ps_ecog_cleaning.ecog_classification"
                },
                outputs="hado_ps_ecog_cleaned",
                name="clean_and_classify_ps_ecog_node"
            ),
            node(
                func=clean_and_classify_gds_fast,
                inputs={
                    "df": "hado_ps_ecog_cleaned",
                    "ambiguous_values_to_zero": "params:gds_fast_cleaning.ambiguous_values_to_zero",
                    "barthel_to_gds_mappings": "params:gds_fast_cleaning.barthel_to_gds_mappings",
                    "gds_classification": "params:gds_fast_cleaning.gds_classification"
                },
                outputs="hado_gds_fast_cleaned",
                name="clean_and_classify_gds_fast_node"
            ),
            # Replace specific words based on multiple dictionaries
            node(
                func=replace_words,
                inputs=[
                    "hado_gds_fast_cleaned",
                    "params:word_replacement.replacement_dict_general",
                    "params:word_replacement.replacement_dict_diagnostico",
                    "params:word_replacement.replacement_dict_hospital_proc",
                    "params:word_replacement.replacement_dict_service_proc",
                    "params:word_replacement.replacement_dict_motivo_ing",
                    "params:word_replacement.replacement_dict_alta",
                    "params:word_replacement.replacement_dict_medic",
                    "params:word_replacement.replacement_dict_sedation",
                    "params:word_replacement.replacement_dict_city_council",
                    "params:word_replacement.replacement_dict_otros",
                    "params:word_replacement.replacement_dict_otros_1",
                    "params:word_replacement.replacement_dict_otros_complicaciones",
                    "params:word_replacement.replacement_dict_numeric",
                    "params:word_replacement.exclude_columns",
                ],
                outputs="hado_replaced_words",
                name="word_replacement_node",
            ),
            # Process the 'ayuntamiento' column and add latitude and longitude
            node(
                func=add_location_and_map_names,
                inputs=["hado_replaced_words","params:name_mapping", "params:locations"],
                outputs="hado_lat_lon",
                name="add_location_and_map_names_node",
            ),
            # Process the 'fecha_alta' column
            node(
                func=process_fecha_alta,
                inputs="hado_lat_lon",
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
                outputs="hado_encoded",
                name="dataframe_for_modeling_node"
            )
        ]
    )
