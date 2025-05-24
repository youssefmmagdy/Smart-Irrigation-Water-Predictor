from api.common.load_models import load_sarimax_model
from api.common.load_models import load_sarimax_model
from api.common.predict_results import get_sarimax_water_predicted
class SARIMAXModelService:
    def __init__(self):
        self.model = None

    def load(self):
        if self.model is None:
            self.model = load_sarimax_model()
        return self.model

    def predict(self, test_case):
        if self.model is None:
            self.model = load_sarimax_model()
            print("hey SARIMAX model loaded")
            print(type(self.model))
            
        return get_sarimax_water_predicted(self.model, test_case)

        

        