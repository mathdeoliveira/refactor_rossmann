"""module responsible for reading training and testing files and returning the processed file """
import os

import pandas as pd
import structlog

logger = structlog.getLogger()
logger.info(f"Starting data ingesting...")


class DataIngest:
    """Class Data Ingest"""

    def __init__(self) -> None:
        self.train_dataset = "train.csv"
        self.test_dataset = "test.csv"
        self.store_dataset = "store.csv"
        self.data_raw_path = os.path.abspath(os.path.join(os.getcwd(), "data/raw"))

    def create_data(self, train_data: bool = True) -> pd.DataFrame:
        """Function to create data into pandas dataframe

        params:
        train_data, bool: which dataset will be created

        return:
        pandas dataframe
        """

        df_train = pd.read_csv(self._path_train_test(), engine="python")
        df_test = pd.read_csv(self._path_train_test(train=False), engine="python")
        df_store = pd.read_csv(self._path_store(), engine="python")

        if train_data:
            df_final = df_train.merge(df_store, on="Store")
            logger.info(f"Loaded {self.train_dataset} data from {self.data_raw_path}")
        else:
            df_final = df_test.merge(df_store, on="Store")
            logger.info(f"Loaded {self.test_dataset} data from {self.data_raw_path}")
        return df_final

    def _path_train_test(self, train=True) -> str:

        if train:
            path_data = os.path.join(self.data_raw_path, self.train_dataset)
        else:
            path_data = os.path.join(self.data_raw_path, self.test_dataset)
        return path_data

    def _path_store(self) -> str:
        path_store = os.path.join(self.data_raw_path, self.store_dataset)
        return path_store
