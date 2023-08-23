"""
This is a boilerplate pipeline 'data_model'
generated using Kedro 0.18.10
"""

from kedro.pipeline import Pipeline, node
from .nodes import preprocess_split_data, train_clf_model, evaluate_model

def create_models_pipeline():
     return Pipeline(
        [
            node(
                func=preprocess_split_data,
                inputs=["hado_final", "params:model_options_alta"],
                outputs=["X_alta_train_preprocessed", "X_alta_test_preprocessed", "y_alta_train", "y_alta_test"],
                name="preprocess_split_data_alta_node",
            ),
            node(
                func=preprocess_split_data,
                inputs=["hado_final", "params:model_options_diagnosis"],
                outputs=["X_diag_train_preprocessed", "X_diag_test_preprocessed", "y_diag_train", "y_diag_test"],
                name="preprocess_split_data_diagnosis_node",
            ),
            # Random Forest Models
            node(
                func=train_clf_model,
                inputs=["X_alta_train_preprocessed", "y_alta_train", "params:random_forest"],
                outputs="random_forest_model_alta",
                name="train_alta_model_rf",
            ),
            node(
                func=train_clf_model,
                inputs=["X_diag_train_preprocessed", "y_diag_train", 'params:random_forest'],
                outputs="random_forest_model_diag",
                name="train_diag_model_rf",
            ),
            # XgBoost Models
            node(
                func=train_clf_model,
                inputs=["X_alta_train_preprocessed", "y_alta_train", 'params:xgb'],
                outputs="xgboost_model_alta",
                name="train_alta_model_xgb",
            ),
            node(
                func=train_clf_model,
                inputs=["X_diag_train_preprocessed", "y_diag_train", 'params:xgb'],
                outputs="xgboost_model_diag",
                name="train_diag_model_xgb",
            ),
            # LightGBM Models
            node(
                func=train_clf_model,
                inputs=["X_alta_train_preprocessed", "y_alta_train", 'params:lgbm'],
                outputs="lightgbm_model_alta",
                name="train_alata_model_lgbm",
            ),
            node(
                func=train_clf_model,
                inputs=["X_diag_train_preprocessed", "y_diag_train", 'params:lgbm'],
                outputs="lightgbm_model_diag",
                name="train_diag_model_lgbm",
            ),
            # Evaluate Models
            node(
                func=evaluate_model,
                inputs=["random_forest_model_alta", "X_alta_test_preprocessed", "y_alta_test"],
                outputs='confusion_matrix_rf_alta_image',
                name="evaluate_rf_alta_node",
            ),
            node(
                func=evaluate_model,
                inputs=["random_forest_model_diag", "X_diag_test_preprocessed", "y_diag_test"],
                outputs='confusion_matrix_rf_diag_image',
                name="evaluate_rf_diag_node",
            ),
            node(
                func=evaluate_model,
                inputs=["xgboost_model_alta", "X_alta_test_preprocessed", "y_alta_test"],
                outputs='confusion_matrix_xgb_alta_image',
                name="evaluate_xgboost_alta_node",
            ),
            node(
                func=evaluate_model,
                inputs=["xgboost_model_diag", "X_diag_test_preprocessed", "y_diag_test"],
                outputs='confusion_matrix_xgb_diag_image',
                name="evaluate_xgboost_diag_node",
            ),
            node(
                func=evaluate_model,
                inputs=["lightgbm_model_alta", "X_alta_test_preprocessed", "y_alta_test"],
                outputs='confusion_matrix_lgb_alta_image',
                name="evaluate_lightgbm_alta_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["lightgbm_model_diag", "X_diag_test_preprocessed", "y_diag_test"],
                outputs='confusion_matrix_lgb_diag_image',
                name="evaluate_lightgbm_diag_model_node",
            ),
        ]
    )

