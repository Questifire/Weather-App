import requests
import json

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow Fall",
    73: "Moderate Snow Fall",
    75: "Heavy Snow Fall",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}

def get_weather(cityname):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {"name": cityname, "count": 1}


    try: 
        geo_response = requests.get(geo_url, params=geo_params)
        geo_data = geo_response.json()
        # return geo_data

        if not geo_data.get("results"):
            print(f"City not found: {cityname}")
            return None

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        full_name = f"{location.get('name')}, {location.get('admin1') or location.get('country')}"

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching geocoding data: {e}")
        return None

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m,apparent_temperature,weather_code,is_day,precipitation_probability,wind_direction_10m",
        "hourly": "temperature_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "timezone": "auto",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        }
    try:
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data.get("current", {})
        temp = current.get("temperature_2m")
        wind = current.get("wind_speed_10m")
        wind_direction = current.get("wind_direction_10m")
        humidity = current.get("relative_humidity_2m")
        feels_like = current.get("apparent_temperature")
        weather_code = current.get("weather_code")
        is_day = current.get("is_day")
        precipitation_chance = current.get("precipitation_probability")
        # air_quality = current.get("us_aqi")    
        temp = (temp * 9/5) + 32 
        feels_like = (feels_like * 9/5) + 32
        wind = (wind/1.609)
        if wind_direction in range(0, 89):
            wind_direction = "North"
        elif wind_direction in range(90, 179):
            wind_direction = "East"
        elif wind_direction in range(180, 269):
            wind_direction = "South"
        elif wind_direction in range(270, 359):
            wind_direction = "West"

        #return f"Weather for {full_name}:\nTemperature: {temp:.0f}°F\nWind Speed: {wind:.1f}mph\nWind Direction: {wind_direction}\nHumidity: {humidity:.0f}%\nFeels Like: {feels_like:.0f}°F\nWeather Code: {weather_code}\nIs It Day: {is_day}\nPrecipitation Chance: {precipitation_chance:.0f}%\nAir Quality: {air_quality}"
        weather_data["city_name"] = full_name
        with open("weather.json", "w") as f:
            json.dump(weather_data, f, indent=4)
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching weather data: {e}")
        return None
# inputcity = input("Enter a city name: ")   
print(get_weather("St. Louis"))
# weather_data = get_weather("St. Louis")
# print(WEATHER_CODES[weather_data["daily"]["weather_code"][0]])
