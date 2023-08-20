"""
This is a boilerplate pipeline 'data_model'
generated using Kedro 0.18.10
"""

import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import pandas as pd
import pickle
import os

def updated_create_and_save_model(df, target_column):
    # Separar características y objetivo
    X = df.drop(columns=target_column)
    y = df[target_column]
    
    # Determinar si la tarea es de regresión o clasificación
    is_regression_task = y.dtype == 'float'
    
    # Entrenar RandomForest
    rf_model = RandomForestRegressor() if is_regression_task else RandomForestClassifier()
    rf_model.fit(X, y)
    
    # Entrenar XGBoost
    xgb_model = xgb.XGBRegressor() if is_regression_task else xgb.XGBClassifier()
    xgb_model.fit(X, y)
    
    # Devolver los modelos entrenados en lugar de los nombres de archivo
    return rf_model, xgb_model

def combine_models(rf_model, xgb_model):
    return [rf_model, xgb_model]

def plot_feature_importance(df, target_column, models):
    X = df.drop(columns=target_column)
    
    for model in models:
        # Determinar el tipo de modelo basado en su tipo
        model_type = type(model).__name__
        
        # Si el modelo es RandomForest, obtenemos las importancias directamente
        if "RandomForest" in model_type:
            importances = model.feature_importances_
            feature_importances_df = pd.DataFrame(
                {"feature": list(X.columns), "importance": importances}
            ).sort_values("importance", ascending=False)
        # Si es XGBoost, usamos la función get_booster
        elif "XGB" in model_type:
            importances = model.get_booster().get_score(importance_type='weight')
            feature_importances_df = pd.DataFrame(
                list(importances.items()), columns=["feature", "importance"]
            ).sort_values("importance", ascending=False)

        # Aquí puedes agregar cualquier visualización adicional o guardar la visualización.
        # Por ahora, simplemente vamos a imprimir las importancias.
        print(feature_importances_df)