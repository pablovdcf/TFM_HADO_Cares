"""
This is a boilerplate pipeline 'data_model'
generated using Kedro 0.18.10
"""
from typing import Dict, Tuple, Any, Optional
import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV

from imblearn.over_sampling import SMOTE

from io import BytesIO
from PIL import Image
import seaborn as sns
import importlib
import logging

# Preprocesado

def preprocess_split_data(data: pd.DataFrame, parameters) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
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
    # Load parameters
    target = parameters['target']
    test_size = parameters['test_size']
    random_state = parameters['random_state']
    
    # Definir características y etiquetas
    X = data.drop(target, axis=1)
    y = data[target]

    # Identificar columnas numéricas y categóricas
    numeric_features = data.select_dtypes(exclude=['object']).columns.to_list()
    numeric_features.remove('year')

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_features = data.select_dtypes(include=['object']).columns.tolist()
    # valid_columns_2_15 = data[categorical_features].nunique().between(2, 15)
    # selected_categorical_features_2_15 = valid_columns_2_15[valid_columns_2_15].index.tolist()
    
    if target in categorical_features:
        categorical_features.remove(target)
    else:
        pass

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Crear preprocesador
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

    # Aplicar el preprocesador a los datos
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)
    
        # Apply SMOTE only to the training set SMOTE is for class rebalancing..
    if target != 'alta_category':
        smote = SMOTE(random_state=random_state)
        X_train_preprocessed, y_train = smote.fit_resample(X_train_preprocessed, y_train)
    else:
        pass
    # print(f"y_train\n{y_train.unique()}\n{'='*50}\ny_test\n{y_test.unique()}")
    return X_train_preprocessed, X_test_preprocessed, y_train, y_test, preprocessor

# Entrenar los modelos
def train_clf_model(
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
    logger = logging.getLogger(__name__)

    # Parse parameters
    model_module = model_options.get("module")
    model_type = model_options.get("class")
    model_arguments = model_options.get("kwargs")
    
    # Parse parameters for GridSearchCV
    param_grid = model_options.get("param_grid", {})
    
    # Import and instantiate the classifier object
    classifier_class = getattr(importlib.import_module(model_module), model_type)
    
    label_encoder = None
    # If the model is XGBoost, encode the labels
    if model_type == "XGBClassifier":
        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train)

    classifier_instance = classifier_class(**model_arguments)
    
    # Descomentar para usar los mejores parámetros del Grid Search cambiandolos en data_science.yml

    logger.info(f"Fitting classifier of type {type(classifier_instance)}")

    # Fit model
    classifier_instance.fit(X_train, y_train)
    flat_model_params = {**{"model_type": model_type}, **model_arguments}
    
    return classifier_instance, flat_model_params, label_encoder
    
    # Descomentar para usar Grid Search (param_grid) y comentar desde logger hasta return classifier
    # # Use stratified cross-validation to maintain the class distribution
    # cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # # GridSearchCV
    # grid_search = GridSearchCV(classifier_instance, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
    # grid_search.fit(X_train, y_train)
    
    # best_model = grid_search.best_estimator_
    # best_params = grid_search.best_params_
    
    # return best_model, best_params, label_encoder


# Evaluation for the model

def evaluate_model(model_and_params: Tuple[BaseEstimator, Dict[str, Any], Optional[LabelEncoder]], 
                   X_test: pd.DataFrame, 
                   y_test: pd.Series
                   ) -> Image:
    
    model, _, label_encoder = model_and_params  # Desempaquetamos la tupla
    
    # Si hay un label_encoder, codificar y_test antes de predecir
    if label_encoder is not None:
        y_test_encoded = label_encoder.transform(y_test)
        y_pred_encoded = model.predict(X_test)
        y_pred = label_encoder.inverse_transform(y_pred_encoded)  # Decodificar las predicciones
        
    else:
        y_pred = model.predict(X_test)
        
    classification_results = classification_report(y_test, y_pred)
    confusion_mat = confusion_matrix(y_test, y_pred)
    
    # Reporte de clasificación
    print("Classification Report:")
    print(classification_results)
    
    # Matriz de confusión
    print("Confusion Matrix:")
    print(confusion_mat)
    
    class_labels = y_test.unique().tolist()
    
    # Visualización de la matriz de confusión
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(confusion_mat, annot=True, fmt="d", cmap="Blues", xticklabels=class_labels, yticklabels=class_labels)
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')
    ax.set_title('Confusion Matrix')

    # Convertir la figura en una imagen PIL para que Kedro pueda manejarla
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image = Image.open(buf)
    
    return image

# GridSearch
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

def retrain_and_evaluate_best_model(data: pd.DataFrame, preprocessor: ColumnTransformer, parameters: dict) -> Tuple[str]:
    """
    Retrain the best model using the full dataset.
    
    Args:
    - data: Complete dataset.
    - preprocessor: Fitted preprocessor instance.
    - parameters: Parameters dictionary with model details and target column.
    
    Returns:
    - BaseEstimator: Retrained model.
    """
    print(parameters)

    target = parameters["target"]
    X = data.drop(target, axis=1)
    y = data[target]
    
    # Transform using the fitted preprocessor
    X_preprocessed = preprocessor.transform(X)
    
    # Import and instantiate the classifier object
    model_module = parameters["module"]
    model_class = parameters["class"]
    model_kwargs = parameters["kwargs"]
    
    classifier_class = getattr(importlib.import_module(model_module), model_class)
    best_model = classifier_class(**model_kwargs)
    
    # If the model is XGBClassifier, encode y
    if model_class == "XGBClassifier":
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
    else:
        y_encoded = y
        
    best_model.fit(X_preprocessed, y_encoded)
    
    # Predict using the model
    y_pred_encoded = best_model.predict(X_preprocessed)
    
    # If the model is XGBClassifier, decode y_pred and y back to original labels
    if model_class == "XGBClassifier":
        y_pred = label_encoder.inverse_transform(y_pred_encoded)
        y = label_encoder.inverse_transform(y_encoded)
    else:
        y_pred = y_pred_encoded
    
    # Evaluate the model
    report = classification_report(y, y_pred)
    confusion_mat = confusion_matrix(y, y_pred)
    print(report, confusion_mat)
    return (report,)