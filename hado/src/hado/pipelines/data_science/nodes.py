"""
This is a boilerplate pipeline 'data_model'
generated using Kedro 0.18.10
"""
from typing import Dict, Tuple, Any
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator
import importlib
import logging

# Preprocesado

def preprocess_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Preprocess the input data.
    
    Steps:
    - Extract features and labels.
    - Identify numeric and categorical features.
    - Create preprocessing pipeline for numeric and categorical features.
    - Split data into training and test sets.
    - Apply preprocessing to the data.
    
    Args:
    - data: Input DataFrame.
    
    Returns:
    - Tuple containing preprocessed training features, test features, training labels, and test labels.
    """
    # Definir características y etiquetas
    X = data.drop('alta_category', axis=1)
    y = data['alta_category']

    # Identificar columnas numéricas y categóricas
    numeric_features = data.select_dtypes(exclude=['object']).columns.to_list()
    numeric_features.remove('year')

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_features = data.select_dtypes(include=['object']).columns.tolist()
    valid_columns_2_6 = data[categorical_features].nunique().between(2, 6)
    selected_categorical_features_2_6 = valid_columns_2_6[valid_columns_2_6].index.tolist()
    selected_categorical_features_2_6.remove('alta_category')

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Crear preprocesador
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, selected_categorical_features_2_6)])

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Aplicar el preprocesador a los datos
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)

    return X_train_preprocessed, X_test_preprocessed, y_train, y_test


def split_data_diagnosis(data: pd.DataFrame, parameters: Dict) -> Tuple:
    """
    Split data into training and test sets for diagnosis.
    
    Args:
    - data: Input DataFrame.
    - parameters: Dictionary containing model options for diagnosis.
    
    Returns:
    - Tuple containing training features, test features, training labels, and test labels.
    """
    X = data[parameters["model_options_diagnosis"]["features"]]
    y = data["diagnosis_category"]
    return train_test_split(
        X, y, 
        test_size=parameters["model_options_diagnosis"]["test_size"], 
        random_state=parameters["model_options_diagnosis"]["random_state"]
    )


# Entrenar los modelos

def train_rf_alta(X_train_alta, y_train_alta):
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train_alta, y_train_alta)
    return rf

def train_xgboost_alta(X_train_alta, y_train_alta):
    xgb_model = XGBClassifier(objective="multi:softprob", random_state=42)
    xgb_model.fit(X_train_alta, y_train_alta)
    return xgb_model

def train_lightgbm_alta(X_train_alta, y_train_alta):
    lgb_model = LGBMClassifier(objective='multiclass', random_state=42)
    lgb_model.fit(X_train_alta, y_train_alta)
    return lgb_model

def train_random_forest_diagnosis(X_train_diagnosis, y_train_diagnosis):
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train_diagnosis, y_train_diagnosis)
    return rf

def train_xgboost_diagnosis(X_train_diagnosis, y_train_diagnosis):
    xgb_model = XGBClassifier(objective="multi:softprob", random_state=42)
    xgb_model.fit(X_train_diagnosis, y_train_diagnosis)
    return xgb_model

def train_lightgbm_diagnosis(X_train_diagnosis, y_train_diagnosis):
    lgb_model = LGBMClassifier(objective='multiclass', random_state=42)
    lgb_model.fit(X_train_diagnosis, y_train_diagnosis)
    return lgb_model

# Evaluacion

def evaluate_model(model_and_params: Tuple[RandomForestClassifier, Dict], X_test: pd.DataFrame, y_test: pd.Series):
    model, _ = model_and_params  # Desempaquetamos la tupla
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))


def evaluate_rf_diagnosis(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def evaluate_xgboost_alta(model: XGBClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def evaluate_xgboost_diagnosis(model: XGBClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def evaluate_lightgbm_alta(model: LGBMClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def evaluate_lightgbm_diagnosis(model: LGBMClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

# GridSearch

from sklearn.model_selection import GridSearchCV

def grid_search_rf_alta(X_train: pd.DataFrame, y_train: pd.Series, parameters: Dict) -> RandomForestClassifier:
    """
    Conduct a grid search over hyperparameters for a Random Forest Classifier.
    
    Args:
    - X_train: Training data of independent features.
    - y_train: Training data labels.
    - parameters: Dictionary containing grid search parameters.
    
    Returns:
    - RandomForestClassifier: Best model found in the grid search.
    """
    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        model, 
        parameters["grid_search_rf"], 
        cv=parameters["cross_validation"]["cv"]
    )
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model

def train_model(
    X_train: pd.DataFrame, y_train: pd.Series, model_options: Dict[str, Any]
) -> Tuple[BaseEstimator, Dict[str, Any]]:
    """
    Trains a model based on provided options.
    
    Args:
    - X_train: Training data of independent features.
    - y_train: Training data labels.
    - model_options: Dictionary containing options like model type, its module, and arguments.
    
    Returns:
    - Tuple containing the trained model and its parameters.
    """

    # Parse parameters
    model_module = model_options.get("module")
    model_type = model_options.get("class")
    model_arguments = model_options.get("kwargs")

    # Import and instantiate the classifier object
    classifier_class = getattr(importlib.import_module(model_module), model_type)
    
    # If the model is XGBoost, encode the labels
    if model_type == "XGBClassifier":
        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train)

    classifier_instance = classifier_class(**model_arguments)

    logger = logging.getLogger(__name__)
    logger.info(f"Fitting classifier of type {type(classifier_instance)}")

    # Fit model
    classifier_instance.fit(X_train, y_train)
    flat_model_params = {**{"model_type": model_type}, **model_arguments}
    
    return classifier_instance, flat_model_params


