from flask import Flask, request, jsonify
from flask_cors import CORS
from api.services.model_dnn import DNNModelService
from api.services.model_dt import DTModelService
from api.services.model_rf import RFModelService
from api.services.model_xgboost import XGBoostModelService
from api.services.model_sarimax import SARIMAXModelService
from api.services.model_svm import SVMModelService
from api.services.actual_result import ActualResultService

app = Flask(__name__)
CORS(app)

dnn_service = DNNModelService()
dt_service = DTModelService()
rf_service = RFModelService()
xgboost_service = XGBoostModelService()
sarimax_service = SARIMAXModelService()
svm_service = SVMModelService()

@app.route("/getAllModels", methods=["GET"])
def get_all_models():
    return jsonify({
        "models": [
            "dnn",
            "dt",
            "rf",
            "xgboost",
            "sarimax",
            "svm"
        ]
    })

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"Hello": "World"})

@app.route("/load/<model_id>", methods=["POST"])
def load_model(model_id):
    model_id = model_id.lower()
    if model_id == "dnn":
        dnn_service.load()
        return jsonify({"model": "DNN model loaded"})
    elif model_id == "dt":
        dt_service.load()
        return jsonify({"model": "DT model loaded"})
    elif model_id == "rf":
        rf_service.load()
        return jsonify({"model": "RF model loaded"})
    elif model_id == "xgboost":
        xgboost_service.load()
        return jsonify({"model": "XGBoost model loaded"})
    elif model_id == "sarimax":
        sarimax_service.load()
        return jsonify({"model": "SARIMAX model loaded"})
    elif model_id == "svm":
        svm_service.load()
        return jsonify({"model": "SVM model loaded"})
    else:
        return jsonify({"error": f"Model '{model_id}' is not supported"}), 400

@app.route("/predict/<model_id>", methods=["POST"])
def predict(model_id):
    model_id = model_id.lower()
    data = request.get_json()
    
    if model_id == "dnn":
        x = dnn_service.predict(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    elif model_id == "dt":
        x = dt_service.predict(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    elif model_id == "rf":
        x = rf_service.predict(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    elif model_id == "sarimax":
        x = sarimax_service.predict(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    elif model_id == "svm":
        x = svm_service.predict(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    elif model_id == "xgboost":
        x = xgboost_service.predict(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    elif model_id == "actual":
        x = ActualResultService().get_actual_result(data)
        if x is None:
            return jsonify({"amount": None})
        return jsonify({"amount": float(x)})
    else:
        return jsonify({"error": f"Model '{model_id}' is not supported"}), 400
    
