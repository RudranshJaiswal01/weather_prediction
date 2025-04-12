import pandas as pd
import logging
from datetime import datetime
import os


logger = logging.getLogger(__name__)

# Define expected columns in order
COLUMNS = [
    "time",
    "temperature_2m (°C)",
    "relative_humidity_2m (%)",
    "precipitation (mm)",
    "rain (mm)",
    "weather_code (wmo code)",
    "cloud_cover (%)",
    "surface_pressure (hPa)",
    "wind_speed_10m (km/h)",
    "wind_direction_10m (°)",
    "is_day ()",
]


def format_weather_data(weather_data):
    """
    Format weather data according to expected structure.
    """
    current_data = weather_data.get("current_data", {})
    formatted_data = {
        "time": current_data.get("time", datetime.now().strftime("%Y-%m-%dT%H:%M")),
        "temperature_2m (°C)": current_data.get("temperature_2m", 0),
        "relative_humidity_2m (%)": current_data.get("relative_humidity_2m", 0),
        "precipitation (mm)": current_data.get("precipitation", 0.00),
        "rain (mm)": current_data.get("rain", 0.00),
        "weather_code (wmo code)": current_data.get("weather_code", 0),
        "cloud_cover (%)": current_data.get("cloud_cover", 0),
        "surface_pressure (hPa)": current_data.get("surface_pressure", 0),
        "wind_speed_10m (km/h)": current_data.get("wind_speed_10m", 0),
        "wind_direction_10m (°)": current_data.get("wind_direction_10m", 0),
        "is_day ()": current_data.get("is_day", 0),
    }
    return formatted_data


def append_weather_data_to_csv(weather_data, csv_path="./dataset/delhi_weather.csv"):
    """
    Append weather data to the specified CSV file.

    Args:
        weather_data (dict): Weather data to append
        csv_path (str): Path to the CSV file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        formatted_data = format_weather_data(weather_data)
        df = pd.DataFrame([formatted_data], columns=COLUMNS)

        # Check if file exists to determine if we need headers
        write_header = not (os.path.exists(csv_path) and os.path.getsize(csv_path) > 0)

        df.to_csv(csv_path, mode="a", header=write_header, index=False)
        logger.info(f"Weather data successfully appended to {csv_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to append weather data to CSV: {str(e)}")
        return False
