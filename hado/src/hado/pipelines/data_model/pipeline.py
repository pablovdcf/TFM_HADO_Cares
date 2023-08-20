"""
This is a boilerplate pipeline 'data_model'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node
from .nodes import updated_create_and_save_model, plot_feature_importance, combine_models

def create_models_pipeline():
    return Pipeline([
        node(
            func=updated_create_and_save_model,
            inputs=["hado_model", "params:target_column"],
            outputs=["rf_model", "xgb_model"],
            name="train_model_node",
        ),
        node(
            func=combine_models,
            inputs=["rf_model", "xgb_model"],
            outputs="combined_models",
            name="combine_models_node"
        ),
        node(
            func=plot_feature_importance,
            inputs={
            "df": "hado_model",
            "target_column": "params:target_column",
            "models": "combined_models"
            },
            outputs=None,
            name="plot_importance_node",
        ),
    ])

