"""module responsible for testing data ingest """
import numpy as np

from refactor_rossmann import utils


def test_predict():
    """
    Asserting predict
    """
    # GIVEN
    model = utils.load_model('CatBoostRegressor_model')
    predict_return = np.expm1(
        model.predict(
            [
                1111.0,
                4.0,
                1.0,
                0.0,
                0.0,
                -0.0693548387096774,
                6.0,
                2014.0,
                1.0,
                31.0,
                2013.0,
                1.0,
                9.0,
                17.0,
                38.0,
                -0.0136986301369863,
                0.5473441108545034,
                -0.433883739117558,
                -0.9009688679024191,
                -1.0,
                -1.8369701987210294e-16,
                -0.4067366430757998,
                -0.9135454576426012,
                -0.992708874098054,
                -0.1205366802553235,
                0.0,
                0.0,
                0.0,
                1.0,
                1.0,
                0.0,
                0.0,
                0.0,
            ]
        )
    )

    # WHEN
    expected_predict_value = 5256.05205344216

    # GHEN
    assert expected_predict_value == predict_return
