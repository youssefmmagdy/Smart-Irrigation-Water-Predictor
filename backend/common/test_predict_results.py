import pytest
import numpy as np
from backend.common.predict_results import get_water_predicted, get_sarimax_water_predicted

@pytest.fixture
def dummy_model():
    class DummyModel:
        def predict(self, X: np.ndarray):
            # Always return a single value array
            return [3.14]  
    return DummyModel()

@pytest.fixture
def dummy_sarimax_model():
    # Mock object with a .fit() method returning itself, and .get_forecast() returning a forecast object
    class DummySARIMAXModel:
        def fit(self, disp=False):
            return self

        def get_forecast(self, steps=1, exog=None):
            class Forecast:
                # Mock predicted_mean
                @property
                def predicted_mean(self):
                    return [2.71]  
            return Forecast()
    return DummySARIMAXModel()

@pytest.fixture
def dummy_test_case():
    return {
        'avgtemp_c': 25.0,
        'maxtemp_c': 30.0,
        'mintemp_c': 20.0,
        'avgwind_kph': 10.0,
        'avghumidity': 60.0,
        'totalprecip_mm': 5.0,
        'sunHour': 8.0,
        'max_level': 100.0,
        'initial_level': 50.0,
        'soil_type': 'Loamy',
        'crop_type': 'Olive',
        'area': 200.0
    }

def test_get_water_predicted(dummy_model, dummy_test_case):
    amount = get_water_predicted(dummy_model, dummy_test_case)
    assert amount is not None
    assert amount >= 0  # Example assertion

def test_get_sarimax_water_predicted(dummy_sarimax_model, dummy_test_case):
    amount = get_sarimax_water_predicted(dummy_sarimax_model, dummy_test_case)
    assert amount is not None
    assert amount >= 0  # Example assertion