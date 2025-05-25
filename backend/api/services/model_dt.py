from common.load_models import load_dt_model
from common.predict_results import get_water_predicted
from common.load_models import load_dt_model

class DTModelService:
    def __init__(self):
        self.model = None

    def load(self):
        if self.model is None:
            self.model = load_dt_model()
        return self.model

    def predict(self, test_case):

        if self.model is None:
            self.model = load_dt_model()
        return get_water_predicted(self.model, test_case)

        

if __name__ == "__main__":
    dt_service = DTModelService()
    dt_service.load()
    test_case = {
        'avgtemp_c': 25.0,
        'maxtemp_c': 30.0,
        'mintemp_c': 20.0,
        'avgwind_kph': 10.0,
        'avghumidity': 60.0,
        'totalprecip_mm': 5.0,
        'sunHour': 8.0,
        'max_level': 100.0,
        'initial_level': 50.0,
        'soil_type': 'sandy',
        'crop_type': 'corn',
        'area': 1000.0
    }
    print(dt_service.predict(test_case))