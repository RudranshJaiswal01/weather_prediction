"""
Weather Data API Service

This module implements a FastAPI-based web service that fetches and serves weather data.
It includes functionality for:
- Real-time weather data collection
- Historical weather data access
- Hourly weather updates
- Background data collection service

The service automatically syncs data collection with the start of each hour and
stores the collected data in a CSV file for persistence.
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import threading
import time
import logging
import uvicorn
from datetime import datetime, timedelta
from utils.weather_fetcher import (
    fetch_historic_weather_data,
    fetch_hourly_weather_data,
    fetch_current_weather_data,
)
from utils.csv_handler import append_weather_data_to_csv

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration constants
fetch_interval = 3600  # Default fetch frequency in seconds (1 hour)

# Global state variables
latest_weather_data = {}


def background_fetch():
    """
    Background service function that runs in a separate thread to periodically fetch weather data.

    This function:
    1. Synchronizes with the start of the next hour
    2. Fetches current weather data
    3. Appends the data to a CSV file
    4. Repeats the process every hour

    The function runs indefinitely until the application is stopped.
    """
    global latest_weather_data

    logger.info("Starting background weather data fetch service")

    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0)
    if now >= next_hour:
        next_hour = next_hour + timedelta(hours=1)
    initial_delay = (next_hour - now).total_seconds()

    logger.info(
        f"Waiting {initial_delay:.2f} seconds until next hour mark ({next_hour.strftime('%H:%M:%S')})"
    )

    time.sleep(initial_delay)

    logger.info("Starting hourly weather data fetch")

    while True:
        logger.info("Fetching current weather data")
        latest_weather_data = fetch_current_weather_data()

        # Append to CSV file
        if append_weather_data_to_csv(latest_weather_data):
            logger.info("Weather data updated successfully. Waiting for next hour.")
        else:
            logger.warning("Failed to append weather data to CSV. Waiting for next hour.")

        time.sleep(3600)  # Sleep for exactly one hour


# Initialize background data collection service
fetch_thread = threading.Thread(target=background_fetch, daemon=True)
fetch_thread.start()


@app.get("/weather")
def get_current_weather():
    """
    API endpoint to retrieve the current weather data.

    Returns:
        JSONResponse: Current weather conditions including temperature, humidity, etc.
    """
    latest_weather_data = fetch_current_weather_data()
    return JSONResponse(content=latest_weather_data)


@app.get("/weather/hourly")
def get_hourly_weather():
    """
    API endpoint to retrieve hourly weather data.

    Returns:
        JSONResponse: Hourly weather data including temperature, humidity, etc.
                     for each hour of the current day.
    """
    hourly_data = fetch_hourly_weather_data()
    return JSONResponse(content=hourly_data)


@app.get("/weather/historic")
def get_historic_weather():
    """
    API endpoint to retrieve historical weather data.

    Returns:
        JSONResponse: Historical weather data including temperature, humidity, etc.
                     for previous days.
    """
    historic_data = fetch_historic_weather_data()
    return JSONResponse(content=historic_data)


@app.post("/update-frequency")
def update_frequency(seconds: int = Query(..., gt=0)):
    """
    API endpoint to update the frequency of weather data collection.

    Args:
        seconds (int): New interval in seconds between data collections.
                      Must be greater than 0.

    Returns:
        dict: Confirmation message with the updated frequency.
    """
    global fetch_interval
    fetch_interval = seconds
    logger.info(f"Fetch interval updated to {seconds} seconds.")
    return {"message": f"Data fetch frequency updated to every {seconds} seconds."}


# Application entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
