"""module responsible for training model"""
import os

import hydra
import lightgbm as lgb
import mlflow
import pandas as pd
import structlog
import xgboost as xgb
from catboost import CatBoostRegressor
from data_preparation import DataPreparation
from omegaconf import DictConfig
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import cross_val_predict
from utils import save_model
import numpy as np
logger = structlog.getLogger()

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("rossmann-experiment")


@hydra.main(config_path="../config/process", config_name="process")
def train(config: DictConfig) -> None:
    """Start the training

    Args:
        hydra config.yaml

    Returns:
        None
    """
    rs = list(config.data_preparation.robust_scaler)
    mms = list(config.data_preparation.min_max_scaler)
    onehot = list(config.data_preparation.onehot)
    ordinal = list(config.data_preparation.ordinal)
    data_prep = DataPreparation()

    X_train, y_train, X_valid, y_valid = data_prep.train_preparation(
        rs_variables=rs,
        mms_variables=mms,
        onehot_variables=onehot,
        ordinal_variables=ordinal,
        train_data=True,
    )
    
    logger.info("Starting training...")
    
    with mlflow.start_run():

        models = {
            'XGBoostRegressor': xgb.XGBRegressor(),
            'GradientBoostingRegressor': GradientBoostingRegressor(),
            'LGBMRegressor': lgb.LGBMRegressor(),
            'CatBoostRegressor': CatBoostRegressor(verbose=False),
        }

        for model_name, model in models.items():
            logger.info(f"Starting training in model: {model_name}")

            y_pred_train = cross_val_predict(model, X_train, y_train, cv=10)
            mlflow.log_param("model_name", model_name)

            metrics_train = {
                f"train_{metric}": value
                for metric, value in _regression_metrics(y_train, y_pred_train).items()
            }

            mlmodel = model.fit(X_train, y_train)
            save_model(model=mlmodel, name_file=f'{model_name}_model')
            y_pred_valid = mlmodel.predict(X_valid)
            metrics_valid = {
                f"valid_{metric}": value
                for metric, value in _regression_metrics(y_valid, y_pred_valid).items()
            }

            metrics = {**metrics_valid, **metrics_train}
            
            mlflow.log_artifact(
                local_path=os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    f'../models/{model_name}_model.joblib',
                )
            )
            mlflow.log_artifact(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    f'../models/pipeline.joblib',
                )
            )
            mlflow.log_metrics(metrics)
            mlflow.end_run()
            logger.info(f"Logged in mlflow for model: {model_name}")


def _regression_metrics(actual: pd.Series, pred: pd.Series) -> dict:
    """Return a collection of regression metrics as a Series.

    Args:
        actual: series of actual/true values
        pred: series of predicted values

    Returns:
        Series with the following values in a labeled index:
        MAE, MSE and RMSE
    """
    
    actual = np.expm1(actual)
    pred = np.expm1(pred)
    
    return {
        "MAE": mean_absolute_error(actual, pred),
        "MSE": mean_squared_error(actual, pred),
        "RMSE": mean_squared_error(actual, pred, squared=False),
    }

if __name__ == '__main__':
    train()
