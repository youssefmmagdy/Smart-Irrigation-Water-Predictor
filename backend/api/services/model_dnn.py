from api.common.load_models import load_dnn_model
from api.common.predict_results import get_water_predicted
from api.common.load_models import load_dnn_model

class DNNModelService:
    def __init__(self):
        self.model = None

    def load(self):
        if self.model is None:
            self.model = load_dnn_model()        
        return self.model

    def predict(self, test_case):
        if self.model is None:
            self.model = load_dnn_model()
        return get_water_predicted(self.model, test_case)
        

        

        