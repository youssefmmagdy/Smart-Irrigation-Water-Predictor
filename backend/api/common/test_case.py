import requests
import numpy as np
import requests

Weather_API_KEY = "007f8f538a464794a8f115446250803"
BASE_URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"

def get_future_data(city, date):

    history_url = f"{BASE_URL}?key={Weather_API_KEY}&q={city}&format=json&date={date}"
    history_data = []
    try:
        response = requests.get(history_url)

        if response.status_code == 200:
            data = response.json()

            if "data" in data and "weather" in data["data"]:
                for day in data["data"]["weather"]:
                  total_wind = 0
                  total_humidity = 0
                  total_precip = 0
                  count = 8

                  for i in range(count):
                      total_wind += float(day['hourly'][i]['windspeedKmph'])
                      total_humidity += float(day['hourly'][i]['humidity'])
                      total_precip += float(day['hourly'][i]['precipMM'])

                  day_data = {
                      'date': day['date'],
                      'avgtemp_c': float(day['avgtempC']),
                      'maxtemp_c': float(day['maxtempC']),
                      'mintemp_c': float(day['mintempC']),
                      'avgwind_kph': total_wind / count,
                      'avghumidity': total_humidity / count,
                      'totalprecip_mm': total_precip,
                      'sunHour': float(day['sunHour'])
                  }

                  history_data.append(day_data)

        else:
            print(f"Error fetching data for {date}: Status code {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return history_data

def get_test_case(data):
    future_data = get_future_data(data['location'], data['date'])
    if(future_data == []):
        return None
    test_case = np.array([future_data[0]['avgtemp_c'], future_data[0]['maxtemp_c'], future_data[0]['mintemp_c'], future_data[0]['avgwind_kph'], future_data[0]['avghumidity'], future_data[0]['totalprecip_mm'], future_data[0]['sunHour']]) # Example input features
    test_case = test_case.reshape(1, -1) # Reshape to match input shape
    test_case = np.append(test_case, [[data['initial_moisture'], data['crop_type'], data['soil_type'], data['area'], data['max_moisture']]], axis=1) # Append additional features
    test_case = test_case.astype(object) # Convert to object type to accommodate mixed data types

    # change to dictionary
    test_case = {
        'avgtemp_c': future_data[0]['avgtemp_c'],
        'maxtemp_c': future_data[0]['maxtemp_c'],
        'mintemp_c': future_data[0]['mintemp_c'],
        'avgwind_kph': future_data[0]['avgwind_kph'],
        'avghumidity': future_data[0]['avghumidity'],
        'totalprecip_mm': future_data[0]['totalprecip_mm'],
        'sunHour': future_data[0]['sunHour'],
        'initial_level': data['initial_moisture'],
        'crop_type': data['crop_type'],
        'soil_type': data['soil_type'],
        'area':    data['area'],
        'max_level': data['max_moisture'],
    }
    return test_case

