import requests
import logging
from datetime import datetime, timezone

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_historic_weather_data():
    try:
        start_time = datetime.strptime("2000-01-01", "%Y-%m-%d")
        now = datetime.now(timezone.utc)

        logger.info("Fetching historic weather data from Open-Meteo API...")

        params = {
            "latitude": 28.6519,
            "longitude": 77.2315,
            "start_date": start_time.strftime("%Y-%m-%d"),
            "end_date": now.strftime("%Y-%m-%d"),
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "rain",
                "weather_code",
                "cloud_cover",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "is_day",
            ],
            "timezone": "Asia/Kolkata",
        }

        response = requests.get(
            "https://archive-api.open-meteo.com/v1/archive", params=params
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        logger.info("Historic weather data fetched successfully.")
        return data
    except Exception as e:
        logger.error(f"Error fetching historic weather data: {e}")
        return {}


def fetch_current_weather_data():
    try:
        logger.info("Fetching current weather data from Open-Meteo API...")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 28.6519,
            "longitude": 77.2315,
            "daily": "weather_code",
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "rain",
                "weather_code",
                "cloud_cover",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "is_day",
            ],
            "timezone": "Asia/Kolkata",
            "forecast_days": 1,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        logger.info("Current weather data fetched successfully.")

        return {
            "hourly_data": data.get("hourly", {}),
            "daily_data": data.get("daily", {}),
            "metadata": {
                "coordinates": {
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude"),
                },
                "elevation": data.get("elevation"),
                "timezone": data.get("timezone"),
                "timezone_abbreviation": data.get("timezone_abbreviation"),
                "utc_offset_seconds": data.get("utc_offset_seconds"),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching current weather data: {e}")
        return {}
