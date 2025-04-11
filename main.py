from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import threading
import time
import logging
import uvicorn
from weather_fetcher import fetch_historic_weather_data, fetch_current_weather_data

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
# def background_fetch():
#     global latest_weather_data
#     while True:
#         latest_weather_data = fetch_current_weather_data()
#         time.sleep(fetch_interval)

# # Start background thread
# fetch_thread = threading.Thread(target=background_fetch, daemon=True)
# fetch_thread.start()


# API endpoint to get latest weather data
@app.get("/weather")
def get_weather():
    latest_weather_data = fetch_current_weather_data()
    return JSONResponse(content=latest_weather_data)


# API endpoint to fetch historic weather data
@app.get("/weather/historic")
def get_historic_weather():
    data = fetch_historic_weather_data()
    return JSONResponse(content=data)


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
