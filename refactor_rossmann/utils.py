"""module responsible for functions utils"""
import os

import joblib
from pandera import Check, Column


def _model_dir():
    """Return the directory models

    Returns:
        model_dir: str, models directory
    """
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models')
    return model_dir


def save_model(model, name_file: str):
    """Save model in .joblib

    Args:
        model: model to save in joblib
        name_file: str, name for file to be save
    """
    mdir = _model_dir()
    joblib.dump(model, f'{mdir}/{name_file}.joblib')


def load_model(name_file: str):
    """Return model from model directory

    Args:
        name_file: str, name for file to be save

    Returns:
        model loaded from directory
    """
    mdir = _model_dir()
    model = joblib.load(f'{mdir}/{name_file}.joblib')
    return model


def df_schema(train_data: bool = True) -> dict:
    """Return schema for dataframe checks

    Args:
        train_data: if true, train dataset will be use else test data set

    Returns:
        Schema for training dataset or test dataset
    """
    if train_data is True:
        schema = {
            'Store': Column(int),
            'DayOfWeek': Column(int),
            'Date': Column(str),
            'Sales': Column(int),
            'Customers': Column(int),
            'Open': Column(
                int, Check.isin(_available_open()), nullable=True, coerce=True
            ),
            'Promo': Column(int),
            'StateHoliday': Column(str, Check.isin(_available_stateholiday())),
            'SchoolHoliday': Column(int, Check.isin(_available_schoolholiday())),
            'StoreType': Column(str, Check.isin(_available_storytype())),
            'Assortment': Column(str, Check.isin(_available_assortment())),
            'CompetitionDistance': Column(float, nullable=True),
            'CompetitionOpenSinceMonth': Column(float, nullable=True),
            'CompetitionOpenSinceYear': Column(float, nullable=True),
            'Promo2': Column(int, Check.isin(_available_promo2())),
            'Promo2SinceWeek': Column(float, nullable=True),
            'Promo2SinceYear': Column(float, nullable=True),
            'PromoInterval': Column(str, nullable=True),
        }
    else:
        schema = {
            'Id': Column(int),
            'Store': Column(int),
            'DayOfWeek': Column(int),
            'Date': Column(str),
            'Open': Column(
                int, Check.isin(_available_open()), nullable=True, coerce=True
            ),
            'Promo': Column(int),
            'StateHoliday': Column(str, Check.isin(_available_stateholiday())),
            'SchoolHoliday': Column(int, Check.isin(_available_schoolholiday())),
            'StoreType': Column(str, Check.isin(_available_storytype())),
            'Assortment': Column(str, Check.isin(_available_assortment())),
            'CompetitionDistance': Column(float, nullable=True),
            'CompetitionOpenSinceMonth': Column(float, nullable=True),
            'CompetitionOpenSinceYear': Column(float, nullable=True),
            'Promo2': Column(int, Check.isin(_available_promo2())),
            'Promo2SinceWeek': Column(float, nullable=True),
            'Promo2SinceYear': Column(float, nullable=True),
            'PromoInterval': Column(str, nullable=True),
        }
    return schema


def _available_open():
    """Return a list for variable avaliable open

    Returns:
        available_open: list
    """
    available_open = [0, 1]
    return available_open


def _available_stateholiday():
    """Return a list for variable available stateholiday

    Returns:
        available_stateholiday: list
    """
    available_stateholiday = ['a', 'b', 'c', '0']
    return available_stateholiday


def _available_schoolholiday():
    """Return a list for variable available schoolholiday

    Returns:
        available_schoolholiday: list
    """
    available_schoolholiday = [0, 1]
    return available_schoolholiday


def _available_storytype():
    """Return a list for variable available storytype

    Returns:
        available_storytype: list
    """
    available_storytype = ['a', 'b', 'c', 'd']
    return available_storytype


def _available_assortment():
    """Return a list for variable available assortment

    Returns:
        available_assortment: list
    """
    available_assortment = ['a', 'b', 'c']
    return available_assortment


def _available_promo2():
    """Return a list for variable available promo2

    Returns:
        _available_promo2: list
    """
    available_promo2 = [0, 1]
    return available_promo2
