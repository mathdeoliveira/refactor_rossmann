from pandera import Check, Column


def df_schema() -> dict:

    schema = {
        'Store': Column(int),
        'DayOfWeek': Column(int),
        'Date': Column(str),
        'Sales': Column(int),
        'Customers': Column(int),
        'Open': Column(int, Check.isin(_available_open())),
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
    available_open = [0, 1]
    return available_open


def _available_stateholiday():
    available_stateholiday = ['a', 'b', 'c', '0']
    return available_stateholiday


def _available_schoolholiday():
    available_schoolholiday = [0, 1]
    return available_schoolholiday


def _available_storytype():
    available_storytype = ['a', 'b', 'c', 'd']
    return available_storytype


def _available_assortment():
    available_assortment = ['a', 'b', 'c']
    return available_assortment


def _available_promo2():
    available_promo2 = [0, 1]
    return available_promo2
