"""
This is a boilerplate pipeline 'data_model'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node
from .nodes import preprocess_data, train_model, evaluate_model

def create_models_pipeline():
     return Pipeline(
        [
            node(
                func=preprocess_data,
                inputs=["hado_final"],
                outputs=["X_train_preprocessed", "X_test_preprocessed", "y_train", "y_test"],
                name="preprocess_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train_preprocessed", "y_train", 'params:random_forest'],
                outputs="random_forest_model_alta",
                name="train_model_rf",
            ),
            node(
                func=train_model,
                inputs=["X_train_preprocessed", "y_train", 'params:xgb'],
                outputs="xgboost_model",
                name="train_model_xgb",
            ),
            node(
                func=train_model,
                inputs=["X_train_preprocessed", "y_train", 'params:lgbm'],
                outputs="lightgbm_model",
                name="train_model_lgbm",
            ),
            node(
                func=evaluate_model,
                inputs=["random_forest_model_alta", "X_test_preprocessed", "y_test"],
                outputs=None,
                name="evaluate_rf_alta_node",
            ),
            # node(
            #     func=evaluate_model,
            #     inputs=["xgboost_model", "X_test_preprocessed", "y_test"],
            #     outputs=None,
            #     name="evaluate_xgboost_model_node",
            # ),
            node(
                func=evaluate_model,
                inputs=["lightgbm_model", "X_test_preprocessed", "y_test"],
                outputs=None,
                name="evaluate_lightgbm_model_node",
            ),
        ]
    )

