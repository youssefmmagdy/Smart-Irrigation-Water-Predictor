# 🌿 Smart Irrigation System Simulator

A machine learning-powered web application that predicts **Evapotranspiration (ET)** using 15 years of historical and forecasted weather data. It offers intelligent irrigation recommendations tailored to location, crop, and soil type — supporting **sustainable agriculture** through data-driven decisions.

---

## 📷 Screenshots

![Frontend_Sample](https://github.com/user-attachments/assets/7336bc63-6416-4f74-85ea-7766da25415c)

---

## 🚀 Overview

The Smart Irrigation Simulator helps farmers and agricultural professionals optimize water usage by:

- Leveraging **weather data** and **soil/crop parameters**
- Predicting **daily ET** using trained ML models
- Calculating how much water is needed per day
- Minimizing waste and improving yield

---

## 📊 Key Features

- ✅ Predict **Evapotranspiration (ET)** using real-time & historical weather data  
- ✅ Calculate **ETc (crop evapotranspiration)** using standard crop coefficients  
- ✅ Estimate **required irrigation volume** by soil moisture, rainfall, and ETc  
- ✅ Compare performance of multiple ML models  
- ✅ Interactive frontend with charts and prediction results  
- ✅ Integrates with **WorldWeatherOnline** API for forecast data  

---

## 🛠️ Tech Stack

- **Frontend**: Angular  
- **Backend**: FastAPI (Python)  
- **Machine Learning**: Scikit-learn, TensorFlow, XGBoost, Prophet  
- **Database**: MongoDB  
- **Deployment**: Docker-ready (Render, Railway, Fly.io)  
- **Data Source**: [WorldWeatherOnline API](https://www.worldweatheronline.com)  

---

## 🧠 Machine Learning Models Used

| Model     | RMSE   | R² Score | Accuracy / Notes      |
|-----------|--------|----------|------------------------|
| **DNN**   | 0.0661 | 0.9942   | ✅ Best model overall   |
| XGBoost   | 0.0800 | 0.9950   | 84.25%                |
| RF        | 0.1113 | 0.9907   | 88.19%                |
| SVM       | 0.0801 | 0.9952   | 78.85%                |
| SARIMAX   | 0.364  | 0.8930   | Traditional model     |
| CNN       | 0.1401 | 0.9853   | 71.78%                |
| DT        | 0.1907 | 0.9727   | 79.65%                |
| ANN       | 0.1951 | 0.9715   | 37.36%                |
| LSTM      | 0.6940 | 0.6120   | 54.38%                |
| Prophet   | 0.9340 | 0.2980   | -317.09% (poor fit)   |

---

## 🔌 API Integration

### 🌤️ External Weather APIs

| API Endpoint                                                                 | Description                           |
|------------------------------------------------------------------------------|---------------------------------------|
| `http://api.worldweatheronline.com/premium/v1/past-weather.ashx`            | Historical weather data (15 years)    |
| `http://api.worldweatheronline.com/premium/v1/weather.ashx`                 | Future weather forecast (upcoming)    |

**Returned Features**:
- `avgtemp_c`
- `maxtemp_c`
- `mintemp_c`  
- `avgwind_kph`
- `avghumidity`
- `totalprecip_mm`
- `sunHour`  

---

## 🔗 Backend API Endpoints

| Endpoint                | Method | Description                                         |
|------------------------|--------|-----------------------------------------------------|
| `/getAllModels`        | GET   | Get accuracy metrics from all trained models        |
| `/loadModel/{model_id}`| POST   | Load a specific model (`dnn`, `xgboost`, etc.)      |
| `/predict/{model_id}`  | POST   | Predict ET using specified model and input features |

### 📥 Example Request Body

```json
{
  "date": "2025-05-01",
  "location": "Cairo",
  "crop_type": "Olive",
  "soil_type": "Loamy",
  "season": "Initial",
  "area": 1000,
  "initial_moisture": 20,
  "max_moisture": 35
}
```

---

## 🧪 How It Works

1. User provides: **Date**, **Location**, **Crop**, **Soil**, **Area**, **Moisture levels**  
2. System fetches future weather conditions from API  
3. Best ML model (DNN) predicts **ET**  
4. Calculates **ETc** (crop-adjusted ET)  
5. Computes irrigation volume with:

```
Irrigation = (max_level - (initial_level + rain_contribution - ETc)) × area
```

---

## 📦 Setup Instructions

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/youssefmmagdy/smart-irrigation-simulator.git
cd smart-irrigation-simulator
```

### 🧪 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

### 🌐 3. Frontend Setup (Angular)

```bash
cd frontend
npm install
ng serve
```

### 🔑 4. Environment Variables

Create a `.env` file beside your `backend/` and ``frontend/` directories:

```env
WEATHER_API_KEY=007f8f538a464794a8f115446250803
FUTURE_WEATHER_URL=http://api.worldweatheronline.com/premium/v1/weather.ashx
MONGODB_URI=mongodb+srv://youssefmmagdy55:zuIIE8LATtxn9u4u@cluster0.xq6ult7.mongodb.net/
```

---



## 🔮 Future Improvements

- 🌐 Multi-language support  
- 📱 Mobile app version  
- 🌾 Add more crops & dynamic Kc values  
- 📡 IoT sensor integration (real-time soil moisture)  
- 🗺️ GIS-based field mapping  

---

## 📄 License

This project is licensed under the **Megzz License**.

---

Made with 💧 and 💡 for a smarter, more sustainable agriculture.
