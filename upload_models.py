from pymongo import MongoClient
import gridfs
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['Bachelor']

# GridFS for storing large files (models)
fs = gridfs.GridFS(db)

# Upload a model
def upload_model_to_mongodb(filepath, model_name):
    with open(filepath, 'rb') as file_data:
        fs.put(file_data, filename=model_name)

#Example usage
# upload_model_to_mongodb('Models/xgb_model.pkl', 'XGBoost')
# upload_model_to_mongodb('Models/dnn_model.h5', 'DNN')
upload_model_to_mongodb('Models/rf_model.pkl', 'RF')
# upload_model_to_mongodb('Models/dt_model.pkl', 'DT')
# upload_model_to_mongodb('Models/sarimax_model.pkl', 'SARIMAX')
upload_model_to_mongodb('Models/svm_model.pkl', 'SVM')

