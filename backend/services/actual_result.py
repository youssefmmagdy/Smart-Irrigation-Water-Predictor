import math

class ActualResultService:
    def __init__(self):
        pass

    def compute(self, test_case):
        """
        Calculate the actual water required for a crop based on weather data and soil type.

        Parameters:
        - test_case (dict): Dictionary containing weather data and crop/soil information.

        Returns:
        - float: Total water required for the crop in liters.
        """
        return get_actual_water(test_case)

def calculate_et(temp, humidity, solar_radiation, wind_speed, pressure=101.3, altitude=0):
    """
    Calculate reference evapotranspiration (ET) using the Penman-Monteith equation.

    Parameters:
    - temp (float): Air temperature in Celsius
    - humidity (float): Relative humidity in %
    - solar_radiation (float): Solar radiation in MJ/m²/day
    - wind_speed (float): Wind speed in m/s
    - pressure (float): Atmospheric pressure in kPa (default: 101.3 kPa at sea level)
    - altitude (float): Altitude above sea level in meters (affects pressure)

    Returns:
    - float: Evapotranspiration (ET) in mm/day
    """

    # Constants
    L = 2.45  # Latent heat of vaporization (MJ/kg)
    cp = 1.013 * 10 ** -3  # Specific heat of air (MJ/kg°C)
    epsilon = 0.622  # Ratio molecular weight of water vapor/dry air

    # Adjust atmospheric pressure by altitude (kPa)
    pressure = 101.3 * ((293 - 0.0065 * altitude) / 293) ** 5.26

    # Saturation vapor pressure (es) using temperature (kPa)
    es = 0.6108 * math.exp((17.27 * temp) / (temp + 237.3))

    # Actual vapor pressure (ea) using relative humidity (kPa)
    ea = es * (humidity / 100)

    # Slope of the saturation vapor pressure curve (delta, kPa/°C)
    delta = (4098 * es) / ((temp + 237.3) ** 2)

    # Psychrometric constant (gamma, kPa/°C)
    gamma = (cp * pressure) / (epsilon * L)

    # Net radiation (Rn) approximation (MJ/m²/day)
    Rn = solar_radiation * 0.77

    # Wind speed adjustment (2m reference height)
    u2 = wind_speed * (4.87 / math.log(67.8 * 2 - 5.42))

    # Penman-Monteith Equation (mm/day)
    ET = (0.408 * delta * Rn + gamma * (900 / (temp + 273)) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))

    return round(ET, 2)

def calculate_crop_et(ET0, crop_type, season):
    """
    Calculate the crop evapotranspiration (ETc).

    Parameters:
    - ET0 (float): Reference evapotranspiration in mm/day
    - crop_type (str): Type of crop (e.g., 'Rice', 'Olives', 'Date Palms', 'Oranges')
    - season (str): Season ('Initial', 'Mid-season', 'Late-season')

    Returns:
    - float: Crop evapotranspiration (ETc) in mm/day
    """
    kc_values = {
        'Rice': {'Initial': 1.05, 'Mid-season': 1.20, 'Late-season': 0.90},
        'Olive': {'Initial': 0.30, 'Mid-season': 0.60, 'Late-season': 0.55},
        'Date': {'Initial': 0.90, 'Mid-season': 0.95, 'Late-season': 0.85},
        'Orange': {'Initial': 0.65, 'Mid-season': 0.85, 'Late-season': 0.70}
    }

    kc = kc_values[crop_type][season]
    ETc = kc * ET0
    return ETc

def calculate_solar_radiation(sunHour, maxtemp, mintemp):
  tmax = maxtemp
  tmin = mintemp
  tmax_k = tmax + 273.15
  tmin_k = tmin + 273.15
  albedo = 0.23  # Albedo of grass reference crop
  altitude = 0
  ea = 2.5
  # Stefan-Boltzmann constant (MJ/K^4/m²/day)
  sigma = 4.903e-9

  # Clear sky solar radiation (Rso) approximation
  total_solar = sunHour * 0.2 * 4.92
  rso = (0.75 + 2e-5 * altitude) * total_solar

  # Longwave radiation (Rl)
  rl = (sigma * ((tmax_k**4 + tmin_k**4) / 2) * (0.34 - 0.14 * math.sqrt(ea))
      * (1.35 * (total_solar / rso) - 0.35))

  # Net radiation (Rn)
  rn = (1 - albedo) * total_solar - rl

  return rn

def calculate_rain_contribution(P, soil_type):
    """
    Calculate the rain contribution to soil moisture based on soil type.

    Parameters:
    - P (float): Precipitation (rainfall) in mm/day
    - soil_type (str): Type of soil ('Sandy', 'Loamy', 'Clay')

    Returns:
    - float: Rain contribution to soil moisture in mm/day
    """
    infiltration_efficiency = {
        'Sandy': 0.85,
        'Loamy': 0.60,
        'Clay': 0.50
    }

    if soil_type not in infiltration_efficiency:
        raise ValueError("Invalid soil type. Choose from 'Sandy', 'Loamy', or 'Clay'.")

    rain_contribution = P * infiltration_efficiency[soil_type]
    return rain_contribution

def calculate_soil_moisture_delta_from_df_row(row, altitude=0):
    """
    Calculate daily soil moisture change (mm/day) from weather data.

    Parameters:
    - row (Series): Pandas row with columns:
        avgtemp_c, maxtemp_c, mintemp_c, avgwind_kph, avghumidity, totalprecip_mm, sunHour
    - altitude (float): Altitude in meters (default: 0)

    Returns:
    - float: Net change in soil moisture (mm/day)
    """
    # Extract weather inputs
    temp = row['avgtemp_c']
    tmax = row['maxtemp_c']
    tmin = row['mintemp_c']
    wind_speed_mps = row['avgwind_kph'] / 3.6  # Convert kph to m/s
    humidity = row['avghumidity']
    rain_mm = row['totalprecip_mm']
    sun_hours = row['sunHour']

    # Calculate solar radiation (MJ/m²/day)
    solar_radiation = calculate_solar_radiation(sun_hours, tmax, tmin)

    # Calculate evapotranspiration (mm/day)
    et = calculate_et(temp, humidity, solar_radiation, wind_speed_mps, altitude=altitude)

    # Net soil moisture change (mm)
    delta_soil_moisture = et

    return round(delta_soil_moisture, 2)

def get_actual_water(test_case):
    from common.test_case import get_test_case
    
    test_case = get_test_case(test_case)
    if test_case is None:
        return None
    # Initialize empty lists to store the calculated values
    result = 0

    # Loop through each row of the DataFrame

    row = [

    test_case['avgtemp_c'],            # avgtemp_c
    test_case['maxtemp_c'],            # maxtemp_c
    test_case['mintemp_c'],            # mintemp_c
    test_case['avgwind_kph'],            # maxwind_kph (becomes avgwind_kph)
    test_case['avghumidity'],            # avghumidity
    test_case['totalprecip_mm'],           # totalprecip_mm
    test_case['sunHour'],             # sunHour
    test_case['initial_level'],            # initial_level / soil_moisture
    test_case['crop_type'],       # crop_type
    test_case['soil_type'],        # soil_type
    test_case['area'],           # area
    test_case['max_level']             # max_moisture
    ]



    avgtemp_c = float(row[0])  # Convert to float for temperature
    maxtemp_c = float(row[1])  # Convert to float for temperature
    mintemp_c = float(row[2])  # Convert to float for temperature
    maxwind_kph = float(row[3])  # Convert to float for wind speed
    avghumidity = float(row[4])  # Convert to float for humidity
    totalprecip_mm = float(row[5])  # Convert to float for precipitation
    sunHours = float(row[6])  # Convert to float for sun hours
    initial_level = float(row[7])  # Convert to float for initial soil moisture level
    soil_level = float(initial_level)  # Use the same conversion for soil moisture
    crop_type = row[8]  # Crop type stays as a string
    soil_type = row[9]  # Soil type stays as a string
    area = float(row[10])  # Convert to float for area in m²
    max_level = float(row[11])  # Convert to float for maximum soil moisture level

    calculated_solar_radition = calculate_solar_radiation(sunHours, maxtemp_c, mintemp_c)

    et = calculate_et(
        temp=avgtemp_c,
        humidity=avghumidity,
        solar_radiation=calculated_solar_radition,
        wind_speed=maxwind_kph / 3.6
    )
    rain_contribution = calculate_rain_contribution(totalprecip_mm, soil_type)

    crop_et = calculate_crop_et(et, crop_type, 'Late-season')

    soil_level += rain_contribution
    soil_level -= crop_et

    if soil_level > max_level:
        soil_level = max_level

    water_required = max_level - soil_level
    if water_required < 0:
        water_required = 0

    total_water_required_for_crop = water_required * area

    result = total_water_required_for_crop

    return result