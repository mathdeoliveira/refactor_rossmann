"""module responsible for predict new data from trained model"""
import argparse

import numpy as np
import pandas as pd
import structlog
from data_preparation import DataPreparation
from firefly.client import Client
from utils import load_model

logger = structlog.getLogger()
parser = argparse.ArgumentParser(description='Receive store id for predict')
parser.add_argument(
    "--store", required=True, type=int, help='Store ID to be predict, only int'
)
store_id = parser.parse_args()


def predict(df: pd.DataFrame) -> np.ndarray:
    """Predict data

    Args:
        df: data for predict

    Returns:
        ndarray numpy: predicted value
    """
    model = load_model('CatBoostRegressor_model')

    y_pred = np.expm1(model.predict(df))

    return y_pred


def firefly(store: int = store_id.store) -> None:
    """Request firefly to predict data from model

    Returns:
         Predicted value of the chosen store
    """
    data_prep = DataPreparation()
    X_test = data_prep.test_preparation()
    client = Client("http://127.0.0.1:8000/")

    average_MAE_training = 853.95

    data = X_test.loc[X_test['Store'] == store][-1:].values.flatten().tolist()

    if not data:
        logger.error(f"Store Number {store} not founded, please try another one")
    else:
        logger.info(f"Starting request to predict.")
        pred = client.predict(df=data)
        logger.info(
            f"Store Number {store} will sell between:\
            \nthe worst scenario ${pred-average_MAE_training:.2f}\
            \nand the best scenario ${pred+average_MAE_training:.2f}\
            \nin the next 6 weeks."
        )
        logger.info(f"Predict was a success.")


if __name__ == '__main__':
    firefly()
