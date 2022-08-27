""" module responsible for testing preprocessing """
from refactor_rossmann.preprocessing import Preprocessing

pp = Preprocessing()


def test_preprocessing_columns():
    """
    Asserting preprocessing columns
    """
    # GIVEN
    data_train = pp.preprocessing(train_data=True).columns.tolist()
    data_test = pp.preprocessing(train_data=False).columns.tolist()

    # WHEN
    expected_columns = [
        'Store',
        'DayOfWeek',
        'Date',
        'Sales',
        'Promo',
        'StateHoliday',
        'SchoolHoliday',
        'StoreType',
        'Assortment',
        'CompetitionDistance',
        'CompetitionOpenSinceMonth',
        'CompetitionOpenSinceYear',
        'Promo2',
        'Promo2SinceWeek',
        'Promo2SinceYear',
        'year',
        'month',
        'day',
        'week_of_year',
        'year_week',
        'competition_since',
        'competition_time_month',
        'promo_since',
        'promo_time_week',
        'day_of_week_sin',
        'day_of_week_cos',
        'month_sin',
        'month_cos',
        'day_sin',
        'day_cos',
        'week_of_year_sin',
        'week_of_year_cos',
    ]

    # THEN
    assert data_train == expected_columns
    assert data_test == expected_columns
