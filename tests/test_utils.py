""" module responsible for testing utils """
from refactor_rossmann import utils


def test_available_open():
    """
    Asserting available_open
    """

    # GIVEN
    expected_available_open = [0, 1]

    # WHEN
    available_open = utils._available_open()

    # THEN
    assert expected_available_open == available_open


def test_available_stateholiday():
    """
    Asserting available_stateholiday
    """

    # GIVEN
    expected_available_stateholiday = ['a', 'b', 'c', '0']

    # WHEN
    available_stateholiday = utils._available_stateholiday()

    # THEN
    assert expected_available_stateholiday == available_stateholiday


def test_available_schoolholiday():
    """
    Asserting available_schoolholiday
    """

    # GIVEN
    expected_available_schoolholiday = [0, 1]

    # WHEN
    available_schoolholiday = utils._available_schoolholiday()

    # THEN
    assert expected_available_schoolholiday == available_schoolholiday


def test_available_storytype():
    """
    Asserting available_storytype
    """

    # GIVEN
    expected_available_storytype = ['a', 'b', 'c', 'd']

    # WHEN
    available_storytype = utils._available_storytype()

    # THEN
    assert expected_available_storytype == available_storytype


def test_available_assortment():
    """
    Asserting available_assortment
    """

    # GIVEN
    expected_available_assortment = ['a', 'b', 'c']

    # WHEN
    available_assortment = utils._available_assortment()

    # THEN
    assert expected_available_assortment == available_assortment


def test_available_promo2():
    """
    Asserting available_promo2
    """

    # GIVEN
    expected_available_promo2 = [0, 1]

    # WHEN
    available_promo2 = utils._available_open()

    # THEN
    assert expected_available_promo2 == available_promo2


def test_schema_dict_keys():
    """
    Asserting schema_dict
    """

    # GIVEN
    expected_schema_dict_keys = [
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

    # WHEN
    schema_dict_keys = list(utils.df_schema().keys())

    # THEN
    assert expected_schema_dict_keys == schema_dict_keys
