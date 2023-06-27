import pandas as pd

from pathlib import Path, PurePosixPath
from pandas_ods_reader import read_ods
#pandas_ods_reader: La biblioteca pandas_ods_reader proporciona una manera fácil de leer archivos OpenDocument Spreadsheet (ODS) y convertirlos en DataFrames de pandas. 
# La función read_ods se utiliza para leer un archivo ODS y devolver un DataFrame de pandas.

import fsspec
# fsspec: La biblioteca fsspec (File System Spec) es una interfaz de sistema de archivos virtual 
# que permite trabajar con diferentes sistemas de archivos como local, S3, HDFS, entre otros. 
# En este caso, se utiliza para crear un sistema de archivos que se ajuste al protocolo correspondiente (por ejemplo, local o S3) y abrir el archivo ODS.

from kedro.io import AbstractDataSet
# kedro.io: Kedro es un marco de trabajo de flujo de datos de Python que ayuda a organizar proyectos de ciencia de datos y aprendizaje automático. 
# En este caso, se utiliza para extender la funcionalidad de Kedro y crear un nuevo conjunto de datos personalizado que pueda leer archivos ODS.

# AbstractDataSet: Es una clase base abstracta de Kedro que representa un conjunto de datos genérico. 
# Al extender esta clase, podemos crear un nuevo conjunto de datos personalizado que se ajuste a nuestras necesidades específicas (en este caso, leer archivos ODS).

from kedro.io.core import get_filepath_str, get_protocol_and_path
# get_filepath_str, get_protocol_and_path: Estas funciones de utilidad de Kedro se utilizan para obtener el protocolo, la ruta y la ruta del archivo
# como cadena a partir de una ruta de archivo dada.

from io import BytesIO
from pymongo import MongoClient

class ODSDataSet(AbstractDataSet):
    def __init__(self, filepath: str, sheet: str):
        # Extraer el protocolo y la ruta del archivo de la ruta proporcionada.
        protocol, path = get_protocol_and_path(filepath)
        self.protocol = protocol
        self.filepath = PurePosixPath(filepath)
        # Crear un sistema de archivos para el protocolo correspondiente.
        self._fs = fsspec.filesystem(self.protocol)
        # Indicar la hoja del archivo ODS que se cargará (por defecto, la primera hoja).
        self.sheet = sheet

    def _load(self) -> pd.DataFrame:
        # Obtener la ruta del archivo en formato de cadena.
        return read_ods(self.filepath, self.sheet)

    def _save(self, data: pd.DataFrame) -> None:
        # No se implementa la función de guardado, ya que la clase solo está diseñada para leer archivos ODS.
        raise NotImplementedError("Saving ODS files is not supported.")
    
    def _exists(self) -> bool:
        # Verificar si el archivo existe en el sistema de archivos.
        path = self._get_load_path()
        return Path(path).exists()

    def _describe(self) -> dict:
        # Devolver una descripción del conjunto de datos en forma de diccionario.
        return dict(filepath=self.filepath, sheet=self.sheet)


class MongoDBDataSet(AbstractDataSet):
    def __init__(self, uri: str, database: str, collection: str, load_args: dict = None, save_args: dict = None):
        self._uri = uri
        self._database = database
        self._collection = collection
        self._load_args = load_args if load_args is not None else dict()
        self._save_args = save_args if save_args is not None else dict()

    def _load(self) -> pd.DataFrame:
        client = MongoClient(self._uri)
        db = client[self._database]
        collection = db[self._collection]
        # Modificar esta parte según cómo desees utilizar load_args
        return pd.DataFrame(list(collection.find(projection=self._load_args)))

    def _save(self, data: pd.DataFrame) -> None:
        client = MongoClient(self._uri)
        db = client[self._database]
        collection = db[self._collection]
        # Modificar esta parte según cómo desees utilizar save_args
        collection.insert_many(data.to_dict('records'), **self._save_args)

    def _describe(self) -> dict:
        return dict(uri=self._uri, database=self._database, collection=self._collection, load_args=self._load_args, save_args=self._save_args)