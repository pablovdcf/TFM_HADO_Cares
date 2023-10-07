# Function for generate data test

# Modules
import pandas as pd
import numpy as np

def generate_data(n):
    """
    Generates synthetic data with various attributes, aimed at simulating a dataset within a healthcare domain.

    Parameters:
    n (int): Number of entries to be generated.

    Returns:
    pd.DataFrame: A DataFrame containing the generated synthetic data.
    
    Description:
    The generate_data function generates random data for a specified number of entries (n). The generated data mimics a realistic healthcare dataset, with multiple attributes concerning patient, hospital, and treatment information. NumPy's random choice functionality is utilized to generate random values for each attribute. The function also defines classifications for certain attributes based on their generated numerical values, and encapsulates all the generated data into a pandas DataFrame which is then returned.
    """
    # Generating random data for each of the numerical columns
    gds_fast = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7], n)
    barthel = np.random.choice([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], n)
    ps_ecog = np.random.choice([0, 1, 2, 3, 4], n)
    
    hospital = np.random.choice(['Santiago', 'Coruña', 'Vigo', 'Ponetvedra', 'Ourense', 'Lugo', 'Barbanza'], n)
    servicio_procedencia = np.random.choice(['Unidad Paliativos', 'Oncologia', 'MIR', 'Digestivo', 'Urgencias', 'Otros', 
                                             'Hematologia', 'Neumologia', 'Cardiologia', 'Neurologia'], n)
    diagnostico_categoría = np.random.choice(['Canceres y neoplasias', 'Neurologicas', 'Hepaticas y pancreaticas',
                                                'Hematologicas', 'Pulmonares y respiratorias', 'Otros',
                                                'Renales y urinarias', 'Infecciones', 'Musculoesqueléticas y de piel',
                                                'Cardiacas'
                                                ], n)
    motivo_ing = np.random.choice(['control sintomas', 'mal control dolor', 'control evolutivo',
                                    'administracion octreotido', 'transfusion', 'infosteosintesis', 'dolor',
                                    'valoracion', 'dolor abdominal', 'infeccion respiratoria', 'neumonia',
                                    'celulitis', 'tratamiento', 'broncoaspiracion', 'inyeccion octreotrido',
                                    'control dolor', 'tratamiento antibiotico IV', 'recambio peg', 'curas',
                                    'postoperatorio', 'angustia', 'diarrea', 'valoracion ulcera',
                                    'valoracion ulceras', 'paracentesis', 'infeccion respirat', 'itu',
                                    'continuacion cuidados', 'fiebre y dolor costal', 'antibioterapia',
                                    'ulcera tumoral', 'tratamiento IV', 'dolo abdominal',
                                    'curas herida quirurgica', 'ascitis', 'deterioor del estado general',
                                    'infeccion urinaria', 'bronquiectasias infectadas', 'seguimiento', 'fiebre',
                                    'hierro IV', 'administracion seguril IV', 'control analgesico',
                                    'seguimineto evolutivo ajuste de tratamiento',
                                    'tratamiento IV y control evolutivo',
                                    'tratamiento antibiotico y control evolutivo',
                                    'tratamiento analgesico y control evolutivo',
                                    'control analgesico y recambio peg', 'cuidados paliativos',
                                    'dolor precordial', 'control analgesico y valoracion hematuria',
                                    'curas y control evolutivo', 'sindrome anemicotransfusion'
                                    ], n)
    ingreso_categoría = np.random.choice(['Sintomas', 'Evaluaciones', 'Otros', 'Tratamientos'], n)
    motivo_alta = np.random.choice(['reingreso', 'exitus', 'fin cuidados', 'reingreso por urgencias a hado',
                                'traslado otro centro', 'traslado a upal', 'traslado a urgencias',
                                'ingreso en digestivo clinico', 'ingreso para trasplante', 'reingreso orl',
                                'traslado a cpl', 'traslado a oncologia', 'reingreso upal', 'trasladoa upal',
                                'traslado a acv', 'ingreso nml clinico',
                                'peticion de la familia de posponer tratamiento', 'traslado a pasliativos',
                                'ingreso en oncologia', 'ingreso en nrc'  'paso a urgencias',
                                'unidad de algias musculoesqueleticas', 'reingreso en oncologia',
                                'traslado a urgencias del clinico',
                                'sin condiciones para seguimiento hado', 'solicitud familiar',
                                'reingreso en neumologia',
                                'cambio de domicilio fuera de area asistencial de hado',
                                'traslado a urgencias por el 061', 'ingreso en orl',
                                'traslado a urgencias para ingreso mir', 'ingreso medicina interna',
                                'ingreso en utr', 'alta paso por urgencias', 'ingreso en medicina interna',
                                'reingreso hospital privado', 'ingreso cirugia vascular',
                                'ingreso oncologia'
                                ], n)
    alta_categoría = np.random.choice(['Complicaciones', 'Exitus', 'Otros', 'Recuperacion'], n)
    atencion_primaria = np.random.choice(['no', 'si'], n)
    numero_estancias = np.random.randint(0, 305, n)
    numero_visitas = np.random.randint(0, 100, n)


    eva_ing = np.random.randint(0, 100, n)
    
    ayuntamiento = np.random.choice([ 'Santiago de Compostela', 'Brión', 'Lalín', 'Ames', 'Negreira',
                                    'Teo', 'Padrón', 'Rois', 'A Baña', 'Oroso', 'Ordes', 'Trazo', 'A Estrada',
                                    'O Pino', 'Touro', 'Boqueixón', 'Vedra', 'Tordoia', 'Val do Dubra', 'Dodro',
                                    'Valga', 'Santa Comba', 'Pontecesures', 'Silleda', 'Sionlla', 'Lousame',
                                    'Frades', 'Pontevea', 'Rianxo', 'Noia', 'Sigüeiro', 'Vila de Cruces', 'Ortoño'], n)
    year = np.random.randint(2013,2023, n)
    
    
    # Defining the corresponding classifications
    gds_fast_classification = [
        ['No realizado o desconocido', 'Deficit cognitivo muy leve', 'Deficit cognitivo leve',
         'Deficit cognitivo moderado', 'Deficit cognitivo moderadamente grave', 'Deficit cognitivo grave',
         'Deficit cognitivo muy grave', 'Ausencia de deficit cognitivo'][i] for i in gds_fast]
    
    barthel_classification = [
        ['Dependencia total', 'Dependencia severa', 'Dependencia moderada', 'Dependencia leve o minima', 'Independencia'][
            0 if i < 20 else 1 if i < 40 else 2 if i < 60 else 3 if i < 90 else 4] for i in barthel]
    
    ps_ecog_classification = [
        ['Totalmente asintomatico', 'Sintomas leves', 'Sintomas moderados', 
         'Necesita ayuda para la mayoria de actividades', 'Encamado el 100%'][i] for i in ps_ecog]
    
    # Creating the DataFrame
    data = pd.DataFrame({
        "hospital": hospital,
        "servicio_procedencia": servicio_procedencia,
        "diagnostico_categoría": diagnostico_categoría,
        "motivo_ing": motivo_ing,
        "ingreso_categoría":ingreso_categoría,
        'motivo_alta': motivo_alta,
        'alta_categoría': alta_categoría,
        'atencion_primaria': atencion_primaria,
        'n_estancias': numero_estancias.astype('int64'),
        'n_visitas': numero_visitas.astype('int64'),
        'eva_ing': eva_ing.astype('int64'),
        'ayuntamiento': ayuntamiento,
        'year': year,
        'gds_fast': gds_fast.astype('int64'),
        'gds_fast_classification': gds_fast_classification,
        'barthel': barthel.astype('int64'),
        'barthel_classification': barthel_classification,
        'ps_ecog': ps_ecog.astype('int64'),
        'ps_ecog_classification': ps_ecog_classification,
    })
    
    return data