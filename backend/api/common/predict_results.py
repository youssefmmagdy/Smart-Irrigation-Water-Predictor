# from common.load_models import load_xgb_model, load_rf_model, load_dt_model, load_svm_model, load_sarimax_model, load_dnn_model
from api.services.actual_result import calculate_rain_contribution, calculate_crop_et
import numpy as np
from api.common.test_case import get_test_case

def get_water_predicted(model, test_case):
    
    test_case = get_test_case(test_case)
    if test_case is None:
        return None
    weather_feature_order = ['avgtemp_c', 'maxtemp_c', 'mintemp_c', 'avgwind_kph', 'avghumidity', 'totalprecip_mm', 'sunHour']

    # Extract the weather feature values in the correct order
    
    weather_features = [test_case[feature] for feature in weather_feature_order]
    
    # Convert the list of features into a NumPy array and ensure the data type is float64
    predicted_et_input = np.array([weather_features], dtype=np.float64)

    predicted_et = model.predict(predicted_et_input)

    water_predicted = (test_case['max_level'] - (test_case['initial_level'] + 
    calculate_rain_contribution(test_case['totalprecip_mm'], test_case['soil_type'])
    - calculate_crop_et(predicted_et[0], test_case['crop_type'], 'Late-season'))) * test_case['area']
    
    return water_predicted

def get_sarimax_water_predicted(model, test_case):
    test_case = get_test_case(test_case)
    if test_case is None:
        return None
    weather_feature_order = ['avgtemp_c', 'maxtemp_c', 'mintemp_c', 'avgwind_kph', 'avghumidity', 'totalprecip_mm', 'sunHour']

    # Extract the weather feature values in the correct order
    weather_features = [test_case[feature] for feature in weather_feature_order]

    # Convert the list of features into a NumPy array and ensure the data type is float64
    predicted_et_input = np.array([weather_features], dtype=np.float64)


    results = model.fit(disp=False)
    forecast = results.get_forecast(steps=1, exog=predicted_et_input)
    predicted_soil_moisture = forecast.predicted_mean

    

    water_predicted = (test_case['max_level'] - (test_case['initial_level'] + calculate_rain_contribution(test_case['totalprecip_mm'], test_case['soil_type'])
    - calculate_crop_et(predicted_soil_moisture.iloc[0], test_case['crop_type'], 'Late-season'))) * test_case['area']

    return water_predicted

