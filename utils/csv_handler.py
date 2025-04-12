"""
CSV Handler Module

This module provides functionality for storing weather data in CSV format.
It handles data formatting, validation, and file operations for weather measurements.
The module ensures consistent data structure and proper CSV file handling with
appropriate column headers and data types.
"""

import pandas as pd
import logging
from datetime import datetime
import os


logger = logging.getLogger(__name__)

# Define expected columns in order with their units
# These columns match the structure of the weather API response
# and include appropriate units for each measurement
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
    Format weather data according to the expected column structure.

    This function takes raw weather data from the API and formats it to match
    the predefined column structure. It handles missing data by providing
    default values to ensure data consistency.

    Args:
        weather_data (dict): Raw weather data from the API containing 'current_data'
                           with various weather measurements.

    Returns:
        dict: Formatted weather data with standardized keys and units.
              Contains all fields specified in COLUMNS with appropriate default values
              if data is missing.
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

    This function handles the process of:
    1. Formatting the raw weather data
    2. Creating a pandas DataFrame with proper column structure
    3. Appending the data to an existing CSV file or creating a new one
    4. Handling file existence and header writing logic

    Args:
        weather_data (dict): Raw weather data from the API containing current
                           weather measurements and metadata.
        csv_path (str): Path to the target CSV file. Defaults to
                       './dataset/delhi_weather.csv'.

    Returns:
        bool: True if the data was successfully appended to the CSV file,
              False if any error occurred during the process.

    Note:
        - Creates a new CSV file with headers if it doesn't exist
        - Appends to existing file without headers if it exists
        - Maintains consistent column ordering as defined in COLUMNS
    """
    try:
        formatted_data = format_weather_data(weather_data)
        df = pd.DataFrame([formatted_data], columns=COLUMNS)

        # Determine if we need to write headers based on file existence and size
        write_header = not (os.path.exists(csv_path) and os.path.getsize(csv_path) > 0)

        df.to_csv(csv_path, mode="a", header=write_header, index=False)
        logger.info(f"Weather data successfully appended to {csv_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to append weather data to CSV: {str(e)}")
        return False
