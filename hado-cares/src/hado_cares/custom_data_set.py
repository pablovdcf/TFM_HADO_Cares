import pandas as pd
from pandas_ods_reader import read_ods
from kedro.io import AbstractDataSet

class ODSDataSet(AbstractDataSet):
    def __init__(self, filepath: str, sheet: str = 1):
        self.filepath = filepath
        self.sheet = sheet

    def _load(self) -> pd.DataFrame:
        return read_ods(self.filepath, self.sheet)

    def _save(self, data: pd.DataFrame) -> None:
        raise NotImplementedError("Saving ODS files is not supported.")

    def _describe(self) -> dict:
        return dict(filepath=self.filepath, sheet=self.sheet)