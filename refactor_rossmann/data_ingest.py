"""module responsible for reading training and testing files and returning the processed file """
import os

import pandas as pd
import structlog

logger = structlog.getLogger()


class DataIngest:
    """Class Data Ingest"""

    def __init__(self) -> None:
        self.train_dataset = "train.csv"
        self.test_dataset = "test.csv"
        self.store_dataset = "store.csv"
        self.data_raw_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '../data/raw'
        )

    def create_data(self, train_data: bool = True) -> pd.DataFrame:
        """Function to create data into pandas dataframe

        params:
        train_data, bool: which dataset will be created

        return:
        pandas dataframe
        """
        logger.info(f"Starting data ingesting...")
        df_train = pd.read_csv(self._path_train_test(train_data=True), engine="python")
        df_test = pd.read_csv(self._path_train_test(train_data=False), engine="python")
        df_store = pd.read_csv(self._path_store(), engine="python")

        if train_data == True:
            logger.info(f"Loading {self.train_dataset} data from {self.data_raw_path}")
            return df_train.merge(df_store, on="Store")         
        else:
            logger.info(f"Loading {self.test_dataset} data from {self.data_raw_path}")
            return df_test.merge(df_store, on="Store").dropna()

    def _path_train_test(self, train_data: bool = True) -> str:

        if train_data == True:
            return os.path.join(self.data_raw_path, self.train_dataset)
            
        else:
            return os.path.join(self.data_raw_path, self.test_dataset)

    def _path_store(self) -> str:
        path_store = os.path.join(self.data_raw_path, self.store_dataset)
        return path_store
