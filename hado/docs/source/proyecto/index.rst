.. HADO_CARES documentation master file, created by
   sphinx-quickstart on Sat Oct 7 15:34:38 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project Documentation
======================

.. toctree::
   :maxdepth: 2

   1.introduction
   2.raw_data_description 
   project_documentation



Data Problem Description and Analysis
-------------------------------------

Data Problem
~~~~~~~~~~~~

During the exploratory analysis and data preprocessing process, various challenges associated with data quality and consistency were identified. Among these, inconsistencies and lack of standardization were especially prevalent. The records, originating from multiple annual files and being manually managed, presented a series of inconsistencies and deficiencies that required detailed cleaning and preprocessing.

The challenge also lay in data quality. The need to carry out extensive cleaning and transformations indicated the existence of problems in the raw data, which could be attenuated in the future through a more standardized and automated data collection and management. Additionally, the presence of null values in various critical variables demanded a cautious management strategy to prevent the introduction of biases or errors in subsequent analyses.

Implemented Solutions and Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To address these issues, several strategies and solutions were implemented. Data standardization was a crucial step, where a unified and coherent dataset was created through the concatenation and standardization of various annual datasets. Additionally, text processing and data handling techniques were used to clean and transform the variables, thus improving the data quality for future analyses. In particular, a strategy was proposed to handle the NA values, grounded on the nature of each variable and the clinical context.

The use of Kedro facilitated a robust and reproducible data science workflow, ensuring that analyses and models could be easily replicated and audited.

Challenges and Future Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although measures have been taken to mitigate the identified data problems, there are challenges and considerations for the future. Automating the process, from data collection to the initial preprocessing phases, could improve efficiency and consistency in the future. It is also imperative to develop more sophisticated strategies or predictive models to handle missing data, especially in critical variables. Although this work focused on cleaning and preprocessing, subsequent analysis stages should explore the patterns and relationships in the data more deeply, leading to deeper analyses.

Raw Data Description
--------------------

Data Dictionary
~~~~~~~~~~~~~~~~

The columns for Raw Data:

.. list-table:: Data Dictionary raw Data
   :header-rows: 1

   * - Column Name
     - Data Type
     - Description
   * - Hospital
     - Object
     - Name or identifier of the hospital.
   * - Servicio
     - Object
     - Service type or department within the hospital.
   * - AP
     - Object
     - Possibly refers to a specific medical procedure or department.
   * - Otros
     - Object
     - A category for other miscellaneous entries.
   * - Diagnostico
     - Object
     - Diagnosis information.
   * - Motivo Ing
     - Object
     - Reason for admission or inquiry (e.g., symptom control).
   * - paliativo Onc
     - Object
     - Indicates if palliative care for oncology is provided.
   * - Paliativo No Onc
     - Object
     - Indicates if palliative care for non-oncology is provided.
   * - Fiebre
     - Object
     - Indicates presence of fever.
   * - Disnea
     - Object
     - Indicates presence of shortness of breath.
   * - Dolor
     - Object
     - Indicates presence of pain.
   * - Delirium
     - Object
     - Indicates presence of delirium.
   * - Astenia
     - Object
     - Indicates presence of asthenia (weakness).
   * - Anorexia
     - Object
     - Indicates presence of anorexia.
   * - Otros.1
     - Object
     - Another category for other miscellaneous entries.
   * - P terminal
     - Object
     - Possibly refers to terminal phase of a condition.
   * - Agonía
     - Object
     - Indicates presence of agony.
   * - PS/IK
     - Object
     - Possibly refers to performance status or a specific score/index.
   * - Barthel
     - Object
     - Possibly refers to the Barthel Index, a measure of disability.
   * - GDS-FAST
     - Object
     - Possibly refers to the Global Deterioration Scale or Functional Assessment Staging Test.
   * - EVA ing
     - Object
     - Possibly refers to a type of assessment or score at admission.
   * - Otros.2
     - Object
     - Another category for other miscellaneous entries.
   * - Complicaciones
     - Object
     - Indicates presence of complications.
   * - Nº estancias
     - Float64
     - Number of stays or admissions.
   * - Nº visitas
     - Float64/Object
     - Number of visits.
   * - SEDACIÓN
     - Object
     - Indicates presence of sedation.
   * - Mot. ALTA
     - Object
     - Reason for discharge or end of care.
   * - Médico
     - Object
     - Name or identifier of the medical professional.
   * - unnamed.1
     - Float64
     - Unspecified column with sparse data, likely an error or misplaced data.


.. list-table:: Data Dictionary for the dataframe processed
   :header-rows: 1

   * - Column
     - Description
     - Data Type
   * - h_procedencia
     - Hospital or origin center of the patient (H. Procedencia)
     - Object
   * - hospital_category
     - (No description provided)
     - Object
   * - s_procedencia
     - Medical service that attended to the patient (Servicio)
     - Object
   * - procedencia_category
     - (No description provided)
     - Object
   * - diagnostico
     - Main diagnosis during the hospital stay (Diagnóstico Principal)
     - Object
   * - diagnosis_category
     - (No description provided)
     - Object
   * - motivo_ing
     - Reason for the patient's admission to the hospital (Motivo ING)
     - Object
   * - ingreso_category
     - (No description provided)
     - Object
   * - motivo_alta
     - Reason for the patient's discharge (Motivo Alta)
     - Object
   * - alta_category
     - (No description provided)
     - Object
   * - fecha_alta
     - Date the patient was discharged from the hospital (Fecha de alta)
     - Object
   * - ap
     - If the patient was referred from Primary Care (AP)
     - Object
   * - n_estancias
     - Number of days of stay in the hospital (N.º estancias)
     - Int64
   * - n_visitas
     - Number of medical visits during the hospital stay (N.º Visitas)
     - Int64
   * - paliativo_onc_noc
     - If the patient is in palliative care for oncological disease (Paliativo ONC)
     - Object
   * - paliativo_no_onc_noc
     - If the patient is in palliative care for non-oncological disease (Palt No ONC)
     - Object
   * - fiebre
     - If the patient had a fever (Fiebre)
     - Object
   * - disnea
     - If the patient experienced difficulty breathing (Disnea)
     - Object
   * - dolor
     - If the patient experienced pain (Dolor)
     - Object
   * - delirium
     - If the patient experienced delirium (Delirium)
     - Object
   * - sedacion
     - If sedation was administered to the patient (Sedación)
     - Object
   * - p_terminal
     - (No description provided)
     - Object
   * - agonia
     - If the patient was in a terminal phase of the disease (Agonia)
     - Object
   * - ast_anorx
     - If the patient was diagnosed with asthenia or anorexia (Ast-Anorx)
     - Object
   * - cronico_reag
     - If the patient has a chronic disease with acute exacerbation (Crónico Agud.)
     - Object
   * - trato_antibiotico
     - If the patient received antibiotic treatment (Trato antibiótico)
     - Object
   * - transfusion
     - If the patient received a blood transfusion (Transfusion)
     - Object
   * - paracentesis
     - If a paracentesis was performed on the patient (Paracentesis)
     - Object
   * - agudo_estable
     - If the patient was in an acute or stable state (Agudo Estable)
     - Object
   * - toracocentesis
     - If a thoracocentesis was performed on the patient (Toracocentesis)
     - Object
   * - fe_iv
     - (No description provided)
     - Object
   * - ps_ecog
     - Quality of life and daily activity assessment (PS/ECOG)
     - Int64
   * - ps_ecog_classification
     - (No description provided)
     - Object
   * - barthel
     - Degree of patient dependency for daily activities (Barthel)
     - Int64
   * - barthel_classification
     - (No description provided)
     - Object
   * - gds_fast
     - Cognitive function assessment (GDS/FAST)
     - Int64
   * - gds_fast_classification
     - (No description provided)
     - Object
   * - eva_ing
     - (No description provided)
     - Int64
   * - otros_complicaciones
     - Other medical complications during the hospital stay (Otros/Complicaciones)
     - Object
   * - otros
     - (No description provided)
     - Object
   * - otros_1
     - (No description provided)
     - Object
   * - otros_2
     - (No description provided)
     - Object
   * - otros_category
     - (No description provided)
     - Object
   * - categorized_combined_otros
     - (No description provided)
     - Object
   * - tiene_sedacion
     - (No description provided)
     - Int64
   * - morfina
     - (No description provided)
     - Int64
   * - midazolam
     - (No description provided)
     - Int64
   * - buscapina
     - (No description provided)
     - Int64
   * - haloperidol
     - (No description provided)
     - Int64
   * - levomepromazina
     - (No description provided)
     - Int64
   * - medico
     - Doctor who attended to the patient (Médico)
     - Object
   * - ayuntamiento
     - Place of residence of the patient (Ayuntamiento)
     - Object
   * - year
     - (No description provided)
     - Int64
   * - latitude
     - (No description provided)
     - Object
   * - longitude
     - (No description provided)
     - Object


General Data Description
~~~~~~~~~~~~~~~~~~~~~~~~

The data subject to this analysis comprises **4,013 records** of patients attended in the HADO area of Santiago de Compostela hospital over a span of 6 years. Each record, equivalent to a hospitalization episode, encapsulates a rich variety of demographic, clinical, and administrative data of the patient, detailed in the Data Dictionary.

**Data Quality**:
- **Missing Data**: The variable "Discharge Date" presents a notable issue as it is available only until mid-2022, limiting temporal analyses involving this variable. Managing missing data in this and other variables will be vital to ensure the validity of subsequent analyses.
- **Data Consistency**: The evaluation of data consistency will be carried out by analyzing outliers and unexpected values, adjusting detected inconsistencies to ensure the reliability of the results.
- **Variable Cardinality**: Variables with high cardinality such as "Main Diagnosis" and "ING Reason" may pose a challenge and require strategies like grouping or category transformation to simplify analyses.

**Variable Distribution**:
A detailed exploratory data analysis (EDA) will be carried out in subsequent stages to gain more precise insights on the distribution and inherent trends in clinical and demographic variables, such as age, diagnoses, and length of stay.

**Preprocessing Strategy**:
Data preprocessing techniques will be implemented to manage missing data, inconsistencies, and transformation of high cardinality variables. Additionally, new variables (feature engineering) will be generated to provide additional value to subsequent analyses, utilizing, for example, NLP techniques to extract and categorize information from free text variables like "Main Diagnosis".

Data Features
~~~~~~~~~~~~~

The datasets from the HADO area of the Santiago de Compostela hospital vary year by year not only in terms of the number of entries but also in their structure and quality. Below are the main features of the annual datasets from 2017 to 2022:

- **Inconsistencies in Column Names**: The datasets present variability in the column names, reflecting a lack of standardization in data capture and storage.
- **Presence of Null Values**: Certain columns, such as "Discharge Date" in 2022 and "Complications" in other years, have a significant number of null values, requiring a considered strategy for missing data management.
- **Variability in Columns**: Some years have additional columns or fewer columns compared to other years, highlighting the need to align and reconcile these differences during preprocessing.

Preliminary Data Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

An initial exploration of the data reveals the following key features:

- **Categorical Data**: Most variables are of object type, indicating that they are categorical or text. This may require encoding or grouping techniques to facilitate further analysis and modeling.
- **Numerical Data**: A limited number of columns are of numeric type (float64), such as "No. of Visits," "No. of Stays," and potentially some other variables that may require conversion or imputation.
- **Missing Data**: The presence of null values in various columns indicates that it will be crucial to establish strategies for managing these missing data, whether through imputation, deletion, or some other suitable method.

Proposed Strategies for Data Cleaning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given this preliminary analysis, some initial strategies for data cleaning may include:

- **Standardization of Column Names**: Aligning the column names across all datasets to ensure consistency and facilitate data concatenation.
- **Handling Null Values**: Establishing and applying strategies for managing null values in the dataset, potentially using different techniques for different types of variables.
- **Data Type Conversion**: Ensuring that variables are stored in the most suitable data type and performing conversions when necessary.
- **Text Normalization**: For text variables, applying text normalization and cleaning techniques to facilitate text analysis and natural language processing in later stages.

General Observations:
~~~~~~~~~~~~~~~~~~~~~

1. **Categorical Variables**:
   - Many categorical variables seem to be binary (yes/no) or have a few unique categories, such as 'Hospital,' 'Service,' 'AP,' etc.
   - Several categories have a significant number of the 'no' category, which may suggest that many patients did not experience certain symptoms or treatments.
   - Some categorical variables, such as 'Diagnosis' and 'Ing Reason,' have many unique categories that could represent a wide range of conditions or reasons for admission.

2. **Numerical Variables**:
   - 'No. of Visits' and 'No. of Stays' are numerical variables and seem to have some outliers that could distort the mean.
   - It's interesting to note that 'No. of Stays' has extremely high values in some datasets, but not in others. This might be worth investigating further to understand whether these values are legitimate or data errors.

Suggested Steps for Analysis:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Data Cleaning**: Identify and handle missing values, verify and correct possible outliers, and review and correct inconsistencies in categories.
2. **Exploratory Data Analysis (EDA)**: Includes visualizing distributions, investigating relationships between variables, and examining trends and patterns.
3. **Variable Transformation**: May include converting categorical variables into dummy variables and normalizing numerical variables.
4. **Statistical Analysis and Modeling**: Choose a suitable model, validate the model, and interpret the results.
5. **Communication of Results**: Create clear visualizations and document the steps and results.

Methodology
-----------

Techniques and Methodologies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project will implement a variety of **machine learning techniques** and **statistical methodologies** tailored to the character and challenges present in the data. Given the nature of the available variables and the project's objectives, **clustering and classification techniques** for high cardinality variables and **predictive models** to identify trends and correlations in the data are anticipated.

Justification of Chosen Techniques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The choice of these techniques is based on the nature of the data and the project objectives. The use of **classification and clustering techniques** is justified by the need to simplify and categorize high cardinality variables, while **predictive models** will be used to explore and understand the correlations and trends present in the data, providing valuable insights that could be utilized to improve patient management.

Data Science Workflow
~~~~~~~~~~~~~~~~~~~~~

The data science workflow for this project will be as follows:

1. **Data Preprocessing**: Will include data cleaning, missing value management, and variable transformation.
   
2. **Exploratory Data Analysis (EDA)**: Variables will be explored to understand their distribution and relationship with other variables.

3. **Feature Engineering**: New variables useful for machine learning models will be generated.
   
4. **Modeling**: Machine learning models will be built and evaluated to explore relationships in the data and possibly predict variables of interest.
   
5. **Data Visualization**: Various visualization tools will be used to explore and present the results of the EDA and modeling in a clear and comprehensible manner.
   
6. **Interpretation and Communication of Results**: Results will be communicated through visualizations and explanatory texts, ensuring they are accessible and understandable to all stakeholders.

Summary of Main Results
-----------------------

Summary
~~~~~~~

[Note: A summary of the most important results will be added once the corresponding analyses and modelings are conducted.]

Reference to Jupyter Notebooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For more detailed analysis and results, reference can be made to the Jupyter Notebooks available in the repository: TFM_HADO_Cares.

Conclusions
-----------

Recapitulation of Findings
~~~~~~~~~~~~~~~~~~~~~~~~~~

[Note: Conclusions and findings will be added once the analyses and modelings are conducted.]

Implications and Recommendations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[Note: Implications of the findings and recommendations for clinical practice and data management in the future will be added.]

Considerations for Future Works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[Note: Suggestions and areas for future research and analysis based on the project's findings will be included.]

---

**Note**: Sections requiring results, conclusions, and findings will be completed more specifically and detailed once the analyses and modelings have been conducted and their results are available for discussion and interpretation.



.. Indices and Tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
