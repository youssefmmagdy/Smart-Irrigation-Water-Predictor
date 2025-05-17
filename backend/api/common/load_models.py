import tempfile
import tensorflow as tf
from tensorflow.keras.models import load_model
import io
import joblib
from pymongo import MongoClient
import gridfs
import os
import requests

# Connect to MongoDB
client = MongoClient("mongodb+srv://youssefmmagdy55:zuIIE8LATtxn9u4u@cluster0.xq6ult7.mongodb.net/<dbname>?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true",
    tls=True,
    tlsAllowInvalidCertificates=True)
print(client.list_database_names())
db = client['Bachelor']

# GridFS for storing large files (models)
fs = gridfs.GridFS(db)

print("Available files in GridFS:")
for f in fs.find():
    print(f.filename)
print("Finished listing files in GridFS.")

def load_model_from_mongodb(model_name):
    # Find the file by filename
    file = fs.find_one({'filename': model_name})
    if file is None:
        raise FileNotFoundError(f"No file named '{model_name}' found in MongoDB.")

    # Read file data
    file_data = file.read()
    return file_data


def load_keras_model(model_name):
    print(f"hey Loading '{model_name}'...")
    file_data = load_model_from_mongodb(model_name)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.h5') as tmp_file:
        tmp_file.write(file_data)
        tmp_filename = tmp_file.name

    # Now load model from the temp file
    model = load_model(tmp_filename)

    # Optionally delete the temp file after loading
    os.remove(tmp_filename)
    print(f"hey'{model_name}' loaded successfully.")
    return model

def load_sklearn_model_from_mongodb(model_name):
    print(f"hey Loading '{model_name}'...")
    file = fs.find_one({'filename': model_name})
    if not file:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found in MongoDB.")
    model_data = file.read()
    model = joblib.load(io.BytesIO(model_data))
    print(f"hey '{model_name}' loaded successfully.")
    return model

def load_xgb_model():
    return load_sklearn_model_from_mongodb('XGBoost')

def load_rf_model():
    return load_sklearn_model_from_mongodb('RF')    


def load_dt_model():
    return load_sklearn_model_from_mongodb('DT')

def load_svm_model():
    return load_sklearn_model_from_mongodb('SVM')

# def load_sarimax_model():
#     return joblib.load('../../Models/sarimax_model.pkl')

def load_sarimax_model():
    return load_sklearn_model_from_mongodb('SARIMAX')

def load_dnn_model():
    return load_keras_model('DNN')


# model = load_keras_model('DNN')
# model = load_sarimax_model()
# print(type(model))

