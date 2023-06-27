# Create custom datasets

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
````
Finally, the `_describe` method is used to provide a description of the MongoDB connection details. This is mainly used for logging purposes.

This way, you can use **MongoDBDataSet** just like any other dataset in your Kedro project. When you run your pipeline, Kedro will take care of calling the `_load` and `_save` methods when necessary.
