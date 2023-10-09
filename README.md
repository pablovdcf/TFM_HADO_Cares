# TFM_HADO_Cares: Healthcare Data Analysis with Kedro

## Overview

`TFM_HADO_Cares` embarks on a meticulous journey through healthcare data, utilizing the Kedro framework to orchestrate a coherent, insightful, and reproducible data science workflow. From initial data scrutiny to implementing sophisticated machine learning models, this project threads through various stages of data analysis, offering a structured, transparent, and replicable methodology encapsulated in a series of Python scripts and Jupyter notebooks.

#### Context and Problem

The HADO area of the Santiago de Compostela hospital manages patient records, among other ways, manually using Excel spreadsheets. This methodology, although functional, leads to a lack of standardization in data formats and limited utilization of the collected information, further hampered by the absence of an efficient system to process and analyze the data in a comprehensive and cohesive manner.


### Objectives

The main objective of this project is to enhance the current patient monitoring process in HADO by:
- Conducting exploratory data analysis (EDA) with a special focus on primary diagnostics.
- Identifying trends and classifying high-cardinality variables.
- Applying Natural Language Processing (NLP) and modeling techniques to group and classify variables.
- Creating an application for visualizing the transformed and analyzed data, thus assisting in the decision-making process of HADO professionals.

## Getting Started

### Prerequisites

- Python 3.10
- Kedro 0.18.13

### Installation & Usage

1. Clone, navigate, and install dependencies:
   ```sh
   git clone https://github.com/pablovdcf/TFM_HADO_Cares.git
   cd TFM_HADO_Cares/hado
   pip install -r src/requirements.txt
   ```
2. Run the Kedro pipeline:
   ```sh
   kedro run
   ```
3. Explore notebooks in `hado/notebooks` for detailed data analysis and visualizations.


## Structure

### 1. [hado/src](https://github.com/pablovdcf/TFM_HADO_Cares/tree/main/hado/src)
   - **data_preprocessing**: Contains nodes for data preprocessing tasks.
   - **data_processing**: Includes nodes for processing the data.
   - **data_science**: Contains nodes that handle data science-related tasks.

### 2. [hado/hado_app](https://github.com/pablovdcf/TFM_HADO_Cares/tree/main/hado/hado_app)
   - **app.py**: A Python script that may serve as the main application or API.
   - **data_processing.py**: Handles data processing within the application.
   - **visualization.py**: Manages data visualization aspects of the application.

### 3. [hado/notebooks](https://github.com/pablovdcf/TFM_HADO_Cares/tree/main/hado/notebooks)
   - **1.1.Data cleaning and preprocessing.ipynb**: A notebook for data cleaning and preprocessing.
   - **2.1.Diagnostics_analysis.ipynb**: Focuses on the analysis of diagnostics.
   - **6.Clasification_Models.ipynb**: Deals with classification models.
   - **8.Models.ipynb**: Contains various models for data analysis.
   - **9.Temporal_Analysis.ipynb**: Focuses on temporal data analysis.

#### NLP Notebooks
   - **1.Analisis_NLP_HADO.ipynb**: Analyzes data using NLP.
   - **2.Validacion_Interna_Clustering.ipynb**: Handles internal validation of clustering.
   - **3.Validacion_Externa_Clustering.ipynb**: Manages external validation of clustering.
   - **4.Stability_Validation_Clustering.ipynb**: Focuses on stability validation of clustering.
   - **5.PCA_and_Clustering_Visualization.ipynb**: Visualizes PCA and clustering.
   - **6.Cross_Method_Comparison_Clustering.ipynb**: Compares clustering across different methods.

## Kedro Project Overview

### Data Preprocessing Pipeline
The data preprocessing pipeline is defined in [data_preprocessing/pipeline.py](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/src/hado/pipelines/data_preprocessing/pipeline.py) and involves several nodes, such as `split_data(...)`, which are defined in [data_preprocessing/nodes.py](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/src/hado/pipelines/data_preprocessing/nodes.py). Parameters like `test_size` and `random_state` are configured in [data_preprocessing.yml](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/conf/base/parameters/data_preprocessing.yml).


### Data Processing Pipeline
The data processing pipeline, defined in [data_processing/pipeline.py](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/src/hado/pipelines/data_processing/pipeline.py), includes nodes like `create_master_table(...)` and `create_model_input_table(...)`, which are defined in [data_processing/nodes.py](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/src/hado/pipelines/data_processing/nodes.py). Parameters such as `rating_weight` and `price_weight` are set in [data_processing.yml](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/conf/base/parameters/data_processing.yml).


### Data Science Pipeline
The data science pipeline, defined in [data_science/pipeline.py](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/src/hado/pipelines/data_science/pipeline.py), encompasses nodes like `split_data(...)`, `train_model(...)`, and more, which are defined in [data_science/nodes.py](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/src/hado/pipelines/data_science/nodes.py). Parameters such as `test_size` and `random_state` are configured in [data_science.yml](https://github.com/pablovdcf/TFM_HADO_Cares/blob/main/hado/conf/base/parameters/data_science.yml).

 
#### General Data Description
   - **Volume of Data**: 4,013 patient records over six years.
   - **Data Characteristics**: Inconsistencies in column names, variability in columns, categorical and numerical data, and presence of null values.
   - **Data Quality**: Issues with missing data, data consistency, and variable cardinality.
   
#### Implemented Solutions and Strategies
   - **Data Standardization**: Creating a unified dataset by concatenating and standardizing annual datasets.
   - **Text Processing and Data Handling**: Employing text processing and data handling techniques to clean and transform variables.
   - **Handling NA Values**: A strategy for handling NA values was proposed, based on the nature of each variable and clinical context.
   - **Use of Kedro**: Facilitated a robust and reproducible data science workflow.

#### Future Challenges and Considerations
   - Emphasis on automation, developing sophisticated predictive strategies for handling missing data, and deeper data analysis in subsequent stages.
   
#### Methodology
   - **Techniques and Methodologies**: Implementation of machine learning techniques and statistical methodologies.
   - **Proposed Data Cleaning Strategies**: Including standardization of column names, handling null values, data type conversion, and text normalization.
   - **Data Science Workflow**: Detailed steps for data preprocessing, exploratory data analysis (EDA), data transformation, statistical analysis, modeling, and result communication.  


<!-- ## Contributing

Kindly refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributions, and feel free to open issues or pull requests. -->

## Contact

- **Contact**: Your Name - [Email](mailto:pablovdcf@gmail.com)