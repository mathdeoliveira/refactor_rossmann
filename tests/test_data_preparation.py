"""module responsible for testing data preparation """
from refactor_rossmann.data_preparation import DataPreparation

dp = DataPreparation()


def test_drop_columns():
    """
    Asserting drop columns
    """
    # GIVEN
    columns_to_drop = dp._drop_columns()

    # WHEN
    expected_columns_to_drop = [
        'Date',
        'StateHoliday',
        'StoreType',
        'year_week',
        'competition_since',
        'promo_since',
    ]
    # THEN
    assert columns_to_drop == expected_columns_to_drop
