"""module responsible preprocessing data with null input and feature engineering """
import datetime
import math

import numpy as np
import pandas as pd
import pandera as pa
import structlog
from data_ingest import DataIngest
from utils import df_schema

logger = structlog.getLogger()


class Preprocessing:
    """Class preprocessing module"""

    def __init__(self) -> None:
        pass

    def preprocessing(self, train_data: bool = True):
        """Preprocessing dataset

        Args:
            train_data: if true, train dataset will be use else test data set

        Returns:
            pandas.DataFrame
        """
        logger.info(f"Ingesting data...")
        data_ingest = DataIngest()
        df = data_ingest.create_data(train_data=train_data)
        logger.info(f"Ingested data was a success.")

        logger.info(f"Validating Schema...")
        schema = pa.DataFrameSchema(df_schema(train_data=train_data))
        schema.validate(df)
        logger.info(f"Validation was a success.")

        logger.info(f"Preprocessing features from data...")
        df['Date'] = self._date(df)
        df['CompetitionDistance'] = self._competition_distance(df)
        df['CompetitionOpenSinceMonth'] = self._competition_open_since_month(df)
        df['CompetitionOpenSinceYear'] = self._competition_open_since_year(df)
        df['Promo2SinceWeek'] = self._promo2_since_week(df)
        df['Promo2SinceYear'] = self._promo2_since_year(df)
        df['PromoInterval'] = self._promo_interval(df)
        logger.info(f"Preprocessing was a success.")

        logger.info(f"Feature engineering starting...")
        df = self._feature_engineering(df, train_data=train_data)
        logger.info(f"Feature engineering was as success...")
        return df

    def _date(self, df: pd.DataFrame):
        feature_preprocessed = pd.to_datetime(df['Date'])
        return feature_preprocessed

    def _competition_distance(self, df: pd.DataFrame) -> pd.Series:
        feature_preprocessed = df['CompetitionDistance'].apply(
            lambda x: 200000.0 if math.isnan(x) else x
        )
        return feature_preprocessed

    def _competition_open_since_month(self, df: pd.DataFrame) -> pd.Series:
        feature_preprocessed = df.apply(
            lambda x: x['Date'].month
            if math.isnan(x['CompetitionOpenSinceMonth'])
            else x['CompetitionOpenSinceMonth'],
            axis=1,
        ).astype(int)
        return feature_preprocessed

    def _competition_open_since_year(self, df: pd.DataFrame) -> pd.Series:
        feature_preprocessed = df.apply(
            lambda x: x['Date'].year
            if math.isnan(x['CompetitionOpenSinceYear'])
            else x['CompetitionOpenSinceYear'],
            axis=1,
        ).astype(int)
        return feature_preprocessed

    def _promo2_since_week(self, df: pd.DataFrame) -> pd.Series:
        feature_preprocessed = df.apply(
            lambda x: x['Date'].week
            if math.isnan(x['Promo2SinceWeek'])
            else x['Promo2SinceWeek'],
            axis=1,
        ).astype(int)
        return feature_preprocessed

    def _promo2_since_year(self, df: pd.DataFrame) -> pd.Series:
        feature_preprocessed = df.apply(
            lambda x: x['Date'].year
            if math.isnan(x['Promo2SinceYear'])
            else x['Promo2SinceYear'],
            axis=1,
        ).astype(int)
        return feature_preprocessed

    def _promo_interval(self, df) -> pd.Series:
        month_map = {
            1: 'Jan',
            2: 'Fev',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec',
        }

        df['PromoInterval'].fillna(0, inplace=True)

        df['month_map'] = df['Date'].dt.month.map(month_map)

        feature_preprocessed = df[['PromoInterval', 'month_map']].apply(
            lambda x: 0
            if x['PromoInterval'] == 0
            else 1
            if x['month_map'] in x['PromoInterval'].split(',')
            else 0,
            axis=1,
        )
        return feature_preprocessed

    def _feature_engineering(
        self, df: pd.DataFrame, train_data: bool = True
    ) -> pd.DataFrame:
        df_feature_engineering = df.copy()
        df_feature_engineering['year'] = df_feature_engineering['Date'].dt.year.astype(int)

        df_feature_engineering['month'] = df_feature_engineering['Date'].dt.month.astype(int)

        df_feature_engineering['day'] = df_feature_engineering['Date'].dt.day.astype(int)

        df_feature_engineering['week_of_year'] = (
            df_feature_engineering['Date'].dt.isocalendar().week
        ).astype(int)

        df_feature_engineering['year_week'] = df_feature_engineering[
            'Date'
        ].dt.strftime('%Y-%W')

        df_feature_engineering['competition_since'] = df_feature_engineering.apply(
            lambda x: datetime.datetime(
                year=x['CompetitionOpenSinceYear'],
                month=x['CompetitionOpenSinceMonth'],
                day=1,
            ),
            axis=1,
        )
        df_feature_engineering['competition_time_month'] = (
            (
                (
                    df_feature_engineering['Date']
                    - df_feature_engineering['competition_since']
                )
                / 30
            )
            .apply(lambda x: x.days)
            .astype(int)
        )

        df_feature_engineering['promo_since'] = (
            df_feature_engineering['Promo2SinceYear'].astype(str)
            + '-'
            + df_feature_engineering['Promo2SinceWeek'].astype(str)
        )
        df_feature_engineering['promo_since'] = df_feature_engineering[
            'promo_since'
        ].apply(
            lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w')
            - datetime.timedelta(days=7)
        )
        df_feature_engineering['promo_time_week'] = (
            (
                (df_feature_engineering['Date'] - df_feature_engineering['promo_since'])
                / 7
            )
            .apply(lambda x: x.days)
            .astype(int)
        )

        df_feature_engineering['Assortment'] = df_feature_engineering[
            'Assortment'
        ].apply(lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended')

        df_feature_engineering['StateHoliday'] = df_feature_engineering[
            'StateHoliday'
        ].apply(
            lambda x: 'public_holiday'
            if x == 'a'
            else 'easter_holiday'
            if x == 'b'
            else 'christmas'
            if x == 'c'
            else 'regular_day'
        )

        # day of week
        df_feature_engineering['day_of_week_sin'] = df_feature_engineering[
            'DayOfWeek'
        ].apply(lambda x: np.sin(x * (2.0 * np.pi / 7)))
        df_feature_engineering['day_of_week_cos'] = df_feature_engineering[
            'DayOfWeek'
        ].apply(lambda x: np.cos(x * (2.0 * np.pi / 7)))

        # month
        df_feature_engineering['month_sin'] = df_feature_engineering['month'].apply(
            lambda x: np.sin(x * (2.0 * np.pi / 12))
        )
        df_feature_engineering['month_cos'] = df_feature_engineering['month'].apply(
            lambda x: np.cos(x * (2.0 * np.pi / 12))
        )

        # day
        df_feature_engineering['day_sin'] = df_feature_engineering['day'].apply(
            lambda x: np.sin(x * (2.0 * np.pi / 30))
        )
        df_feature_engineering['day_cos'] = df_feature_engineering['day'].apply(
            lambda x: np.cos(x * (2.0 * np.pi / 30))
        )

        # week of year
        df_feature_engineering['week_of_year_sin'] = df_feature_engineering[
            'week_of_year'
        ].apply(lambda x: np.sin(x * (2.0 * np.pi / 52)))
        df_feature_engineering['week_of_year_cos'] = df_feature_engineering[
            'week_of_year'
        ].apply(lambda x: np.cos(x * (2.0 * np.pi / 52)))
        
        if train_data:
            df_feature_engineering = df_feature_engineering[
                (df_feature_engineering['Open'] != 0)
                & (df_feature_engineering['Sales'] > 0)
            ]
            cols_drop = ['Customers', 'Open', 'PromoInterval', 'month_map']
            df_feature_engineering = df_feature_engineering.drop(cols_drop, axis=1)
        else:
            df_feature_engineering = df_feature_engineering[
                (df_feature_engineering['Open'] != 0)
            ]
            cols_drop = ['Open', 'PromoInterval', 'month_map']
            df_feature_engineering = df_feature_engineering.drop(cols_drop, axis=1)

        return df_feature_engineering
