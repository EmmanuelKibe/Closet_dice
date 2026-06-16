import requests
from datetime import date

def fetch_weekly_forecast(location_string, api_key):
    """
    Hits the Visual Crossing API to get a 5-day weather breakdown.
    Returns a structured list of days containing forecast data.
    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location_string}/next7days?unitGroup=metric&elements=datetime,tempmax,tempmin,conditions&key={api_key}&contentType=json"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('days', [])
    except requests.RequestException:
        pass
    
    return []

def determine_weather_suitability(max_temp):
    """
    Algorithmic classification engine that translates raw Celcius max temperatures
    into standard ClosetDice clothing categories.
    """
    if max_temp < 15:
        return "COLD"
    elif 15 <= max_temp <= 25:
        return "ALL"  # Mild/Temperate weather
    else:
        return "HOT"