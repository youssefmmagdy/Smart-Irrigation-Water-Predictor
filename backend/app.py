from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.predict_schema import PredictionInput
from services.model_dnn import DNNModelService
from services.model_dt import DTModelService
from services.model_rf import RFModelService
from services.model_xgboost import XGBoostModelService
from services.model_sarimax import SARIMAXModelService
from services.model_svm import SVMModelService
from services.actual_result import ActualResultService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

dnn_service = DNNModelService()
dt_service = DTModelService()
rf_service = RFModelService()
xgboost_service = XGBoostModelService()
sarimax_service = SARIMAXModelService()
svm_service = SVMModelService()

@app.get("/getAllModels")
def get_all_models():
    return {
        "models": [
            "dnn",
            "dt",
            "rf",
            "xgboost",
            "sarimax",
            "svm"
        ]
    }

@app.post("/load/{model_id}")
def load_model(model_id: str):
    model_id = model_id.lower()
    if model_id == "dnn":
        dnn_service.load()
        return {"model": "DNN model loaded"}
    elif model_id == "dt":
        dt_service.load()
        return {"model": "DT model loaded"}
    elif model_id == "rf":
        rf_service.load()
        return {"model": "RF model loaded"}
    elif model_id == "xgboost":
        xgboost_service.load()
        return {"model": "XGBoost model loaded"}
    elif model_id == "sarimax":
        sarimax_service.load()
        return {"model": "SARIMAX model loaded"}
    elif model_id == "svm":
        svm_service.load()
        return {"model": "SVM model loaded"}
    else:
        return {"error": f"Model '{model_id}' is not supported"}


@app.post("/predict/{model_id}")
def predict(model_id: str, data: PredictionInput):
    model_id = model_id.lower()

    if model_id == "dnn":
        x = dnn_service.predict(data)
        if(x is None):
            return {"amount": None}
        return {"amount": float(x)}
    elif model_id == "dt":
        x = dt_service.predict(data)
        print("hey")
        print(x)
        return {"amount": float(x)}
    elif model_id == "rf":
        x = rf_service.predict(data)
        
        return {"amount": float(x)}
    elif model_id == "sarimax":
        
        x = sarimax_service.predict(data)
        return {"amount": float(x)}
    elif model_id == "svm":
        return {"amount": svm_service.predict(data)}
    elif model_id == "xgboost":
        x = xgboost_service.predict(data)
        if(x is None):    
            return {"amount": None}
        return {"amount": float(x)}
    elif model_id == "actual":        
        return {"amount": float(ActualResultService().compute(data))}
