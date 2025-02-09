"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline
from .pipelines.data_preprocessing.pipeline import create_pipeline_data_preprocessing
from .pipelines.data_processing.pipeline import create_pipeline_data_processing
from .pipelines.data_science.pipeline import create_models_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_preprocessing_pipeline = create_pipeline_data_preprocessing()
    data_processing_pipeline = (
        create_pipeline_data_processing()
    )  # Crea la pipeline de procesamiento de datos
    data_science = (
        create_models_pipeline()
    )
    pipelines = {
        "data_preprocessing": data_preprocessing_pipeline,
        "data_processing": data_processing_pipeline,  # Registra la pipeline de procesamiento de datos
        "data_science": data_science,
    }

    pipelines["__default__"] = sum(pipelines.values())

    return pipelines
