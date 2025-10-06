import openmeteo_requests
import pandas as pd
import requests_cache
import aiohttp
from retry_requests import retry

class WeatherAPI:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def query(self):
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": "temperature_2m",
        }
        responses = self.openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        print("\nHourly data\n", hourly_dataframe)

    async def get_location(self):
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={str(self.latitude)}&longitude={str(self.longitude)}&localityLanguage=en"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "city": data.get("city"),
                        "countryCode": data.get("countryCode"),
                    }
                else: return None