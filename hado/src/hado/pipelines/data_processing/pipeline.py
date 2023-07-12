"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node

from .nodes import clean_text, replace_missing, replace_words, process_fecha_alta

def create_pipeline_data_processing(**kwargs):
    return Pipeline(
        [
            node(
                func=clean_text,
                inputs="hado_concat",
                outputs="hado_clean",
                name="clean_text",
            ),
            node(
                func=replace_missing,
                inputs=["hado_clean", "params:replacement_dict_na"],
                outputs="hado_clean_na",
                name="replace_missing",
            ),
            node(
            func=replace_words,
            inputs=["hado_clean_na",\
                "params:replacement_dict_general",\
                "params:replacement_dict_diagnostico",\
                "params:replacement_dict_hospital_proc",\
                "params:replacement_dict_service_proc",\
                "params:replacement_dict_motivo_ing",\
                "params:replacement_dict_alta",\
                "params:replacement_dict_medic",\
                "params:replacement_dict_sedation",\
                "params:replacement_dict_city_council",\
                "params:replacement_dict_otros",\
                "params:replacement_dict_otros_1",\
                "params:replacement_dict_otros_complicaciones"
                ],
            outputs="hado_replaced_words",
            name="word_replacement_node",
            ),
             node(
            func=process_fecha_alta,
            inputs="hado_replaced_words",
            outputs="hado_cleaned",
            name="process_fecha_alta_node",
            ),
        ]
    )