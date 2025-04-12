from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import threading
import time
import logging
import uvicorn
from datetime import datetime, timedelta
from weather_fetcher import (
    fetch_historic_weather_data,
    fetch_hourly_weather_data,
    fetch_current_weather_data,
)
from utils.csv_handler import append_weather_data_to_csv

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Default fetch frequency (in seconds)
fetch_interval = 3600  # 1 hour

# Shared variable to hold latest data
latest_weather_data = {}


# Function to run in background thread
def background_fetch():
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


# Start background thread
fetch_thread = threading.Thread(target=background_fetch, daemon=True)
fetch_thread.start()


# API endpoint to get current weather data
@app.get("/weather")
def get_current_weather():
    latest_weather_data = fetch_current_weather_data()
    return JSONResponse(content=latest_weather_data)


# API endpoint to get hourly weather data for a given date
@app.get("/weather/hourly")
def get_hourly_weather():
    hourly_data = fetch_hourly_weather_data()
    return JSONResponse(content=hourly_data)


# API endpoint to fetch historic weather data
@app.get("/weather/historic")
def get_historic_weather():
    historic_data = fetch_historic_weather_data()
    return JSONResponse(content=historic_data)


# API endpoint to change the fetch interval
@app.post("/update-frequency")
def update_frequency(seconds: int = Query(..., gt=0)):
    global fetch_interval
    fetch_interval = seconds
    logger.info(f"Fetch interval updated to {seconds} seconds.")
    return {"message": f"Data fetch frequency updated to every {seconds} seconds."}


# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
