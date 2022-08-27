"""module responsible for data preparation"""
import numpy as np
import pandas as pd
import structlog
from feature_engine.wrappers import SklearnTransformerWrapper
from preprocessing import Preprocessing
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    MinMaxScaler,
    OneHotEncoder,
    OrdinalEncoder,
    RobustScaler,
)
from utils import load_model, save_model

logger = structlog.getLogger()


class DataPreparation:

    """Class preprocessing module"""

    def __init__(self) -> None:
        self.robustscaler = RobustScaler()
        self.minmaxscaler = MinMaxScaler()
        self.onehot = OneHotEncoder(sparse=False)
        self.ordinal = OrdinalEncoder()

    def train_preparation(
        self,
        rs_variables: list,
        mms_variables: list,
        onehot_variables: list,
        ordinal_variables: list,
    ) -> pd.DataFrame:
        """Preprocessing dataset

        Args:
            rs_variables: variables that will be transformed by RobustScaler
            mms_variables: variables that will be transformed by MinMaxSclaser
            onehot_variables: variables that will be transformed by OneHotEncoder
            ordinal_variables: variables that will be transformed by OrdinalEncoder

        Returns:
            pandas.DataFrame
        """
        logger.info(f"Data preparation starting...")
        rs = SklearnTransformerWrapper(
            transformer=self.robustscaler, variables=rs_variables
        )
        mms = SklearnTransformerWrapper(
            transformer=self.minmaxscaler, variables=mms_variables
        )
        onehot = SklearnTransformerWrapper(
            transformer=self.onehot, variables=onehot_variables
        )
        ordinal = SklearnTransformerWrapper(
            transformer=self.ordinal, variables=ordinal_variables
        )

        preparation_pipeline = Pipeline(
            [
                ('robust_scaler', rs),
                ('minmax_scaler', mms),
                ('onehot_encoder', onehot),
                ('ordinal_encoder', ordinal),
            ]
        )

        preprocess = Preprocessing()

        df = preprocess.preprocessing(train_data=True)
        df = df.sort_values('Date')
        df['Sales'] = np.log1p(df['Sales'])

        X_train = df[df['Date'] < '2015-06-19'].copy()
        y_train = X_train['Sales'].values
        X_train.drop('Sales', axis=1, inplace=True)

        X_valid = df[df['Date'] >= '2015-06-19'].copy()
        y_valid = X_valid['Sales'].values
        X_valid.drop('Sales', axis=1, inplace=True)

        X_train = preparation_pipeline.fit_transform(X_train, y_train)
        X_valid = preparation_pipeline.transform(X_valid)

        columns_to_drop = self._drop_columns()
        X_train.drop(columns_to_drop, axis=1, inplace=True)
        X_valid.drop(columns_to_drop, axis=1, inplace=True)

        logger.info(f"Saving pipeline in /models ...")
        save_model(model=preparation_pipeline, name_file='pipeline')

        return X_train, y_train, X_valid, y_valid

    def test_preparation(self) -> pd.DataFrame:
        """Preprocessing test dataset

        Returns:
            pandas.DataFrame
        """
        logger.info(f"Starting test dataset ...")

        preprocess = Preprocessing()

        df = preprocess.preprocessing(train_data=False)
        df = df.sort_values('Date')
        logger.info(f"Load pipeline from /models ...")

        pipeline = load_model(name_file='pipeline')

        columns_to_drop = self._drop_columns()
        X_test = pipeline.transform(df)
        X_test.drop(columns_to_drop, axis=1, inplace=True)
        return X_test

    def _drop_columns(self) -> list:
        """Drop columns
        Returns:
            list columns to drop
        """
        columns_to_drop = [
            'Date',
            'StateHoliday',
            'StoreType',
            'year_week',
            'competition_since',
            'promo_since',
        ]
        return columns_to_drop
