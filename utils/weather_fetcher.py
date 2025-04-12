"""
Weather Data Fetcher Module

This module provides functions to fetch weather data from the Open-Meteo API.
It supports retrieving:
- Historical weather data from 2000 onwards
- Hourly weather forecasts
- Current weather conditions

The module uses the Open-Meteo free weather API and focuses on Delhi's coordinates
(latitude: 28.6519, longitude: 77.2315).
"""

import requests
import logging
from datetime import datetime, timezone

# Constants for Delhi coordinates
LATITUDE = 28.6519
LONGITUDE = 77.2315

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_historic_weather_data():
    """
    Fetch historical weather data from Open-Meteo Archive API starting from 2000.

    The function retrieves various weather parameters including:
    - Temperature at 2m above ground
    - Relative humidity
    - Precipitation and rain
    - Weather code and cloud cover
    - Surface pressure
    - Wind speed and direction
    - Day/night indicator

    Returns:
        dict: Historical weather data in JSON format containing hourly measurements.
              Returns empty dict on error.
    """
    try:
        start_time = datetime.strptime("2000-01-01", "%Y-%m-%d")
        now = datetime.now(timezone.utc)

        logger.info("Fetching historic weather data from Open-Meteo API...")

        url = "https://archive-api.open-meteo.com/v1/archive"

        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
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

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        logger.info("Historic weather data fetched successfully.")
        return data
    except Exception as e:
        logger.error(f"Error fetching historic weather data: {e}")
        return {}


def fetch_hourly_weather_data():
    """
    Fetch hourly weather forecast data from Open-Meteo API for the next 24 hours.

    The function retrieves various weather parameters including:
    - Temperature at 2m above ground
    - Relative humidity
    - Precipitation and rain
    - Weather code and cloud cover
    - Surface pressure
    - Wind speed and direction
    - Day/night indicator

    Returns:
        dict: Dictionary containing:
            - hourly_data: Hourly weather measurements
            - daily_data: Daily aggregated data
            - metadata: Location and timezone information
              Returns empty dict on error.
    """
    try:
        logger.info("Fetching hourly weather data from Open-Meteo API...")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
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

        logger.info("Hourly weather data fetched successfully.")

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


def fetch_current_weather_data():
    """
    Fetch current weather conditions from Open-Meteo API.

    The function retrieves various current weather parameters including:
    - Temperature at 2m above ground
    - Relative humidity
    - Precipitation and rain
    - Weather code and cloud cover
    - Surface pressure
    - Wind speed and direction
    - Day/night indicator

    Returns:
        dict: Dictionary containing:
            - current_data: Current weather measurements
            - current_data_units: Units for each measurement
            - metadata: Location and timezone information
              Returns empty dict on error.
    """
    try:
        logger.info("Fetching current weather data from Open-Meteo API...")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "is_day",
                "precipitation",
                "rain",
                "weather_code",
                "cloud_cover",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
            ],
            "forecast_days": 1,
            "timezone": "Asia/Kolkata",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        logger.info("Current weather data fetched successfully.")

        return {
            "current_data": data.get("current", {}),
            "current_data_units": data.get("current_units", {}),
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
