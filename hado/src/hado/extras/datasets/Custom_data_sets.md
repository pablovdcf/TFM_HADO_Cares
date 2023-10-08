# Create custom datasets

- [1 Guide to Create and Use a Custom ODSDataSet in Kedro](#1guide-to-create-and-use-a-custom-odsdataset-in-kedro)
- [2 Guide to Create and Use a Custom MongoDBDataSet in Kedro](#2guide-to-create-and-use-a-custom-mongodbdataset-in-kedro)
- [3 Guide to Load Raw Data to MongoDB and Configure Kedro](#3guide-to-load-raw-data-to-mongodb-and-configure-kedro)

## 1.Guide to Create and Use a Custom ODSDataSet in Kedro

### Introduction

This guide provides step-by-step instructions on how to create a custom dataset in Kedro for reading ODS files and use it in your project's `catalog.yml`.

### Step 1: Create the ODSDataSet Class

Start by defining a new class called `ODSDataSet` that will inherit from `AbstractDataSet`.

```python
from kedro.io import AbstractDataSet
from pandas_ods_reader import read_ods
from pathlib import PurePosixPath
import fsspec

class ODSDataSet(AbstractDataSet):
```

### Step 2: Initialize the Class

The `__init__` method initializes the class with the file path and the sheet name of the ODS file.

```python
    def __init__(self, filepath: str, sheet: str):
        protocol, path = get_protocol_and_path(filepath)
        self.protocol = protocol
        self.filepath = PurePosixPath(filepath)
        self._fs = fsspec.filesystem(self.protocol)
        self.sheet = sheet
```

### Step 3: Load the Data

The `_load` method reads the specified sheet from the ODS file into a pandas DataFrame.

```python
    def _load(self) -> pd.DataFrame:
        return read_ods(self.filepath, self.sheet)
```

### Step 4: Handle Saving Data (Not Supported)

The `_save` method raises an error as this class is designed only to read ODS files, not to save them.

```python
    def _save(self, data: pd.DataFrame) -> None:
        raise NotImplementedError("Saving ODS files is not supported.")
```

### Step 5: Check If the File Exists

The `_exists` method checks if the ODS file exists in the file system.

```python
    def _exists(self) -> bool:
        path = self._get_load_path()
        return Path(path).exists()
```

### Step 6: Describe the DataSet

The `_describe` method provides a description of the ODS file details, mainly for logging purposes.

```python
    def _describe(self) -> dict:
        return dict(filepath=self.filepath, sheet=self.sheet)
```

### Step 7: Configure the DataSet in `catalog.yml`

After defining the `ODSDataSet`, you can use it in your `catalog.yml` to specify which ODS files and sheets should be loaded.

```yaml
# Example configuration in catalog.yml

hado_22:
  type: hado.extras.datasets.custom_data_set.ODSDataSet
  filepath: "data/01_raw/HADO 22.ods"
  sheet: "Hoja1"
  layer: raw

```

By following these steps, you can seamlessly integrate ODS file reading capabilities into your Kedro project using the custom `ODSDataSet`. This allows you to utilize Kedro's powerful data engineering capabilities while working with ODS files.

### Note

Make sure the necessary libraries (`pandas_ods_reader` and `fsspec`) are installed in your environment before using this custom dataset.

## 2.Guide to Create and Use a Custom MongoDBDataSet in Kedro

## MongoDB

In this case, we are defining a custom dataset to work with MongoDB.
```python

from kedro.io import AbstractDataSet
from pymongo import MongoClient
import pandas as pd

class MongoDBDataSet(AbstractDataSet):
```

We are defining a new class called **MongoDBDataSet** that inherits from AbstractDataSet, the base class provided by Kedro for all datasets.

```python
    def __init__(self, uri: str, database: str, collection: str):
        self._uri = uri
        self._database = database
        self._collection = collection
```

The `__init__ `method is used to initialize the class with the MongoDB URI, the database name and the collection name.

```python
    def _load(self) -> pd.DataFrame:
        client = MongoClient(self._uri)
        db = client[self._database]
        collection = db[self._collection]
        return pd.DataFrame(list(collection.find()))
```
The `_load` method is used to load data from the MongoDB database. It connects to MongoDB using the URI, selects the database and collection, and then loads all documents from the collection into a pandas DataFrame.

```python
    def _save(self, data: pd.DataFrame) -> None:
        client = MongoClient(self._uri)
        db = client[self._database]
        collection = db[self._collection]
        collection.insert_many(data.to_dict('records'))
```
The `_save` method is used to save the data in the MongoDB database. It converts the pandas DataFrame into a list of dictionaries and then inserts them into the MongoDB collection.

```python

    def _exists(self) -> bool:
        client = MongoClient(self._uri)
        db = client[self._database]
        return self._collection in db.list_collection_names()
````

The `_exists method` is used to check if the MongoDB collection exists.

```python
    def _describe(self) -> dict:
        return dict(uri=self._uri, database=self._database, collection=self._collection)
```
Finally, the `_describe` method is used to provide a description of the MongoDB connection details. This is mainly used for logging purposes.

This way, you can use **MongoDBDataSet** just like any other dataset in your Kedro project. When you run your pipeline, Kedro will take care of calling the `_load` and `_save` methods when necessary.


## 3.Guide to Load Raw Data to MongoDB and Configure Kedro

This guide demonstrates how to load raw data from ODS files into MongoDB and how to set up Kedro to read that data through the `catalog.yml`.

### Prerequisites:

- MongoDB Server: Ensure MongoDB is installed and running on your system.
- MongoDB Compass: This is the official GUI for MongoDB, which helps in visual data exploration. While not mandatory, it's highly recommended for visually inspecting the data, building queries, and managing the database. You can download it from the [official website](https://www.mongodb.com/try/download/compass).

### Step 1: Set Up the Environment

Before starting, ensure you have the required packages installed:

```
pip install pymongo pandas_ods_reader
```

### Step 2: Establish Connection to MongoDB

To connect to MongoDB, create an instance of `MongoClient`:

```python
from pymongo import MongoClient

# Establish connection to MongoDB
client = MongoClient('localhost', 27017)
```

### Step 3: Create or Select a Database

Select or create a database in MongoDB:

```python
db = client['HADO_raw']
```

### Step 4: Define Function to Load Raw Data to MongoDB

Define a function that reads an ODS file and loads it into a MongoDB collection:

```python
from pandas_ods_reader import read_ods

def load_raw_data_to_mongodb(file_path, collection_name):
    # Create or select a collection in the database
    collection = db[collection_name]

    # Read the ODS file using pandas
    df = read_ods(file_path, 1)

    # Convert the pandas DataFrame into a dictionary and load it into MongoDB
    collection.insert_many(df.to_dict('records'))
```

### Step 5: Load Data

Use the function created above to load your ODS files into MongoDB:

```python
file_paths = [
    # List of paths to your ODS files
]

collection_names = [
    # List of collection names corresponding to the ODS files
]

# Load each raw file into MongoDB
for file_path, collection_name in zip(file_paths, collection_names):
    load_raw_data_to_mongodb(file_path, collection_name)
```

### Step 6: Configure Kedro

To read data from MongoDB using Kedro, you need to set up `catalog.yml` to use a custom dataset that connects to MongoDB. Here's an example based on the attached MD file.

```
collection_name:
  type: path.to.MongoDataSet  # Ensure you have the correct path to the custom MongoDB DataSet
  database: "HADO_raw"
  collection: "collection_name"
  ...
```

Follow the detailed steps in [Custom_data_sets.md](./Custom_data_sets.md) to set up and use your custom `MongoDataSet` in Kedro.

---

With these steps, you should be able to load your raw data into MongoDB and set up Kedro to read that data from MongoDB.
```

This guide covers the basic steps to load data into MongoDB and configure Kedro. Adapt it according to your specific needs and project structure.