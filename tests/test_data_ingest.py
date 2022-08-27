"""module responsible for testing data ingest """
import os

from refactor_rossmann import data_ingest

di = data_ingest.DataIngest()


def test_created_data():
    """
    Asserting created_data
    """
    # GIVEN
    data_columns_train = di.create_data(train_data=True).columns.tolist()
    data_columns_test = di.create_data(train_data=False).columns.tolist()

    # WHEN
    expected_columns_train = [
        'Store',
        'DayOfWeek',
        'Date',
        'Sales',
        'Customers',
        'Open',
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
        'PromoInterval',
    ]
    expected_columns_test = [
        'Id',
        'Store',
        'DayOfWeek',
        'Date',
        'Open',
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
        'PromoInterval',
    ]

    # THEN
    assert data_columns_train == expected_columns_train
    assert data_columns_test == expected_columns_test


def test_path_train_test():
    """
    Asserting train and test path dir
    """
    # GIVEN
    path_train = os.path.join(di.data_raw_path, di.train_dataset)
    path_test = os.path.join(di.data_raw_path, di.test_dataset)

    # WHEN
    expected_path_train = di._path_train_test(train_data=True)
    expected_path_test = di._path_train_test(train_data=False)

    # THEN
    assert expected_path_train == path_train
    assert expected_path_test == path_test


def test_path_store():
    """
    Asserting train and test path dir
    """
    # GIVEN
    path_store = os.path.join(di.data_raw_path, di.store_dataset)

    # WHEN
    expected_path_store = di._path_store()

    # THEN
    assert expected_path_store == path_store
