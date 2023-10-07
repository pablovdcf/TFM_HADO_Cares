import pandas as pd
import numpy as np

def generate_data(n):
    # Generando datos aleatorios para cada una de las columnas numéricas
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
    numero_estancias = np.random.choice([21, 24, 14, 1, 2, 13, 22, 5, 9, 3, 103, 6, 69, 33, 18, 4, 8, 10, 23, 15, 11, 20, 92, 49, 30, 35, 7, 16, 98, 45, 41, 96, 100, 36, 47, 40, 26, 32, 28, 27, 34, 46, 12, 19, 25, 50, 87, 42, 17, 31, 67, 68, 141, 48, 29, 51, 39, 55, 37, 56, 0, 71, 58, 74, 38, 72, 43, 73, 99, 63, 64, 304, 54, 75, 180, 53, 78, 84, 135, 57, 76, 106, 86, 60, 79, 44, 104, 70, 52, 111, 65, 77, 61, 66, 90, 140, 130, 119, 126, 161, 62, 93, 89, 204, 91, 95, 102, 97, 131, 150, 88, 134, 142, 109, 123, 138, 107, 80, 166, 133, 59, 154, 188, 125, 101, 117, 118, 171], n)

    numero_visitas = np.random.choice([10, 8, 6, 1, 2, 5, 3, 21, 31, 15, 7, 4, 40, 14, 12, 18, 35, 9, 11, 20, 37, 34, 16, 17, 23, 24, 22, 45, 48, 0, 13, 33, 28, 25, 60, 27, 26, 19, 30, 50, 36, 43, 29, 56, 51, 41, 42, 32, 54, 71, 76, 49, 68, 38, 39, 99, 80, 44], n)


    eva_ing = np.random.choice([0, 70, 80, 60, 30, 90, 100, 50, 40, 78, 20, 23], n)
    
    ayuntamiento = np.random.choice([ 'Santiago de Compostela', 'Brión', 'Lalín', 'Ames', 'Negreira',
                                    'Teo', 'Padrón', 'Rois', 'A Baña', 'Oroso', 'Ordes', 'Trazo', 'A Estrada',
                                    'O Pino', 'Touro', 'Boqueixón', 'Vedra', 'Tordoia', 'Val do Dubra', 'Dodro',
                                    'Valga', 'Santa Comba', 'Pontecesures', 'Silleda', 'Sionlla', 'Lousame',
                                    'Frades', 'Pontevea', 'Rianxo', 'Noia', 'Sigüeiro', 'Vila de Cruces', 'Ortoño'], n)
    year = np.random.choice([2017, 2018, 2019, 2020, 2021, 2022], n)
    
    
    # Definiendo las clasificaciones correspondientes
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
    
    # Creando el DataFrame
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